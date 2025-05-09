from truffle.common import get_logger
from .base import *
from dataclasses import is_dataclass


logger = get_logger()

class TruffleClientRuntime(BaseRuntime):
    def __init__(self):
        self.cls = None

    def build(self, class_instance):
        self.cls = class_instance

        check_groups(self.cls)

        tool_fns = get_truffle_tool_fns(self.cls)
        assert tool_fns and len(tool_fns), "No tools found in your app, don't forget to add @truffle.tool to your functions."

        for name, func in tool_fns.items():

            # must have args and types for args
            args = args_from_func(func)
            assert args != None, f"Function {func.__name__} invalid"
            
            verify_arg_descriptions("ex", func.__truffle_args__)
            verify_arg_types("ex", args)
        
        # maybeeee fuzz every tool ??

        logger.success("Validated all tools, building Truffle app...")
        return self.cls
    

