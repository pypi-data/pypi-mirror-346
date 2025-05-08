from truffle.common import get_logger
from .base import *
from dataclasses import is_dataclass
from truffle.types import TruffleFile


logger = get_logger()

class TruffleClientRuntime(BaseRuntime):
    def __init__(self):
        self.cls = None

    def build(self, class_instance):
        self.cls = class_instance
        
        check_groups(self.cls)
        
        # check that we have truffle_tools
        tool_fns = get_truffle_tool_fns(self.cls)
        assert tool_fns and len(tool_fns), "No tools found in your app, don't forget to add @truffle.tool to your functions."


        # check every tool has type annotations
        for name, func in tool_fns.items():
            #make sure reserved names are not used
            if name.startswith("Truffle"):
                raise Exception(f"Function {name} is using a reserved name. Please don't use names starting with 'Truffle'.")

            args = args_from_func(func)
            assert args and len(args), f"Function {name} has no type annotations or arguments."

            # check that all argument types are allowed
            # these rules are based on trial and error on what runs in the proprietary runtime
            for arg_name, arg_type in args.items():
                assert not is_dataclass(arg_type), f"Function {name} has a dataclass type: {arg_type}"
                
                allowed_arg_types = [str, int, float, bool, list, dict]
                allowed_return_types = [str, int, float, bool, list, dict, TruffleFile] # TruffleImage?
                
                if arg_name == 'return':
                    if not any(arg_type is t for t in allowed_return_types) and not hasattr(arg_type, "__origin__"):
                        raise TypeError(f"Function {name} return type has invalid type: {arg_type}. Must be one of: {', '.join(t.__name__ for t in allowed_return_types)}")
                else:
                    if not any(arg_type is t for t in allowed_arg_types) and not hasattr(arg_type, "__origin__"):
                        raise TypeError(f"Function {name} argument {arg_name} has invalid type: {arg_type}. Must be one of: {', '.join(t.__name__ for t in allowed_arg_types)}")
                
                if hasattr(arg_type, "__origin__"):
                    origin = arg_type.__origin__
                    assert origin in (list, dict), f"Function {name} argument {arg_name} uses unsupported generic type: {origin}"
                    
                    for inner_type in arg_type.__args__:
                        assert inner_type in allowed_arg_types and not (hasattr(inner_type, "__origin__") and inner_type.__origin__ is typing.Union), \
                        f"Function {name} argument {arg_name} has invalid inner type: {inner_type}. Optional types are not supported."

        # maybeeee fuzz every tool ??

        logger.success("Validated all tools, building Truffle app...")
        return self.cls
    

