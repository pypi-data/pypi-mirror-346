import abc 
import typing
import inspect
import json 
from truffle.common import get_logger

class BaseRuntime(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build(self, class_instance: typing.Any) -> None:
        pass


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False


def get_members(obj : typing.Any, pred: typing.Callable) -> typing.Dict[str, typing.Any]:
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and pred(value):
            pr[name] = value
    return pr

def get_non_function_members(obj):
    return get_members(obj, lambda o: not inspect.ismethod(o))

def get_function_members(obj):
    return get_members(obj, inspect.ismethod)
    

def args_from_func(func : typing.Callable) -> typing.Dict[str, typing.Any]:
    type_hints = typing.get_type_hints(func)
    assert callable(func), f"Expected a function, got type: {type(func)} {func}."
    assert type_hints, f"Function {func.__name__} must have type hints."
    
    assert "return" in type_hints, f"Function {func.__name__} must have a return value and type hint."

    args_dict = {}
    for param_name, param in type_hints.items():
        param_type = type_hints.get(param_name, type(None))
        assert param_type.__name__ != "NoneType", (
            f"Function {func.__name__}: Parameter '{param_name}' has no type hint. Make sure to include a type hint."
        )
        args_dict[param_name] = param_type

    assert "return" in args_dict, f"Args dict missing return value for function {func.__name__}."
    return args_dict


def get_truffle_tool_fns(obj):
    tools = {}
    for name, func in get_function_members(obj).items():
        if hasattr(func, "__truffle_tool__"):
            if hasattr(func, "__self__"):
                tools[name] = func.__func__
            else:
                tools[name] = func
                get_logger().warning(f"Function {func.__name__} missing self parameter. Trying to make it work.")
    assert len(tools) > 0, f"Object {obj.__name__} has no truffle tools defined."
    return tools


def verify_func(func : typing.Callable) -> bool:
    assert len(args_from_func(func)), f"Function {func.__name__} invalid"
    return True

def verify_arg_descriptions(fn_name :str, kwargs : typing.Dict[str, typing.Any]) -> bool:
    assert len(kwargs) > 0, f"{fn_name} - truffle.args() requires at least one [name, description] pair, got none"
    for key, value in kwargs.items():
        assert isinstance(key, str),   f"{fn_name}.args({key}='{value}') - Expected string, got type {type(key)} {key}."
        assert isinstance(value, str), f"{fn_name}.args({key}='{value}') - Expected string, got type {type(value)} {value}."
    return True


def verify_predicate(func : typing.Callable) -> bool:
    assert callable(func), f"Predicate for {func.__name__} must be callable"
    assert inspect.isfunction(func), f"Predicate for {func.__name__} must be a function"
    # assert no args
    assert len(inspect.signature(func).parameters) == 0, f"Predicate for {func.__name__} must have no arguments"
    # should assert returns bool, but we don't want to call it, so we will just wrap it in something that deals with that

    return True


def check_groups(obj : typing.Any) -> bool:
    groups = {}
    for name, func in get_function_members(obj).items():
        if getattr(func, "__truffle_group__", None) is not None:
            is_leader = getattr(func, "__truffle_group_leader__", False)
            group_name = str(func.__truffle_group__)
            if group_name not in groups:
                groups[group_name] = {"leaders": [], "members": []}
            if is_leader:
                groups[group_name]["leaders"].append(func)
            else:
                groups[group_name]["members"].append(func)

    for group_name, group in groups.items():
        assert len(group["leaders"]) > 0, f"Group {group_name} has no leaders, so all tools in the group will be ignored."
        if len(group["members"]) == 0:
            get_logger().warning(f"Group {group_name} has no members, so all tools in the group will be available")

    return True
           