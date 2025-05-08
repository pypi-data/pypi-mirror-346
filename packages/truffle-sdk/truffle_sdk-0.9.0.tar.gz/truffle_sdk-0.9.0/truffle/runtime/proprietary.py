

import typing
import types
import os 
import inspect
import functools
import re
import copy 
import json 
import base64

from concurrent import futures
from datetime import datetime
from dataclasses import dataclass
from collections import OrderedDict

import warnings
warnings.filterwarnings("ignore")
from google.protobuf import any_pb2, timestamp_pb2, text_format
from google.protobuf.descriptor import MethodDescriptor,  Descriptor, ServiceDescriptor, FieldDescriptor
from google.protobuf.service_reflection import GeneratedServiceType
from google.protobuf import descriptor_pool, descriptor_pb2
# from google.protobuf import service
from google.protobuf.service import Service
from google.protobuf.service_reflection import GeneratedServiceType
from google.protobuf.json_format import MessageToDict
from google import protobuf as pb

import grpc
from grpc_reflection.v1alpha import reflection

from google.protobuf import descriptor

from truffle.common import get_logger
from truffle.platform import APP_SOCK, SDK_SOCK
from .base import *



logger = get_logger()


# ALL THE PROTOBUF AND GRPC CODE. TRUFFLE RUNTIME AT EOF 

def to_upper_camel(snake_str: str) -> str:
    if not snake_str:
        return snake_str
    return (
        snake_str[0].upper()
        + re.sub("_([a-zA-Z])", lambda pat: pat.group(1).upper(), snake_str)[1:]
    )
def add_fd_to_pool(fd_pb: descriptor_pb2.FileDescriptorProto, pool: descriptor_pool.DescriptorPool) -> None:
    try:
        existing_fd = pool.FindFileByName(fd_pb.name)
        existing_pb = descriptor_pb2.FileDescriptorProto()
        existing_fd.CopyToProto(existing_pb)
        if (
            existing_pb.dependency != fd_pb.dependency and
            existing_pb.message_type.keys() != fd_pb.message_type.keys() and
            existing_pb.service.keys() != fd_pb.service.keys()
        ):
            raise TypeError(f"File {fd_pb.name} already exists in pool and is different") 
    except KeyError:
        try:
            pool.Add(fd_pb)
        except TypeError:
            logger.error(f"Error adding {fd_pb.name} to pool")
            raise
def desc_to_message_class(desc: Descriptor) -> typing.Type:
    try:
        message_class = desc._concrete_class
    except (TypeError, SystemError, AttributeError):
        # protobuf version compatibility
        if hasattr(pb.reflection.message_factory, "GetMessageClass"):
            message_class = pb.reflection.message_factory.GetMessageClass(desc)
        else:
            message_class = pb.reflection.message_factory.MessageFactory().GetPrototype(desc)
            
    for nested_message_descriptor in desc.nested_types:
        nested_message_class = desc_to_message_class(
            nested_message_descriptor
        )
        setattr(message_class, nested_message_descriptor.name, nested_message_class)

    return message_class
def is_numeric_field(field: FieldDescriptor):
    numeric_types = [
        FieldDescriptor.TYPE_DOUBLE,
        FieldDescriptor.TYPE_FLOAT,
        FieldDescriptor.TYPE_INT32,
        FieldDescriptor.TYPE_INT64,
        FieldDescriptor.TYPE_UINT32,
        FieldDescriptor.TYPE_UINT64,
        FieldDescriptor.TYPE_SINT32,
        FieldDescriptor.TYPE_SINT64,
        FieldDescriptor.TYPE_FIXED32,
        FieldDescriptor.TYPE_FIXED64,
        FieldDescriptor.TYPE_SFIXED32,
        FieldDescriptor.TYPE_SFIXED64,
    ]
    return field.type in numeric_types


def is_float_field(field: FieldDescriptor):
    return field.type in [FieldDescriptor.TYPE_DOUBLE, FieldDescriptor.TYPE_FLOAT]

class FuncToProto:
    def __init__(self, func: typing.Callable, package: str):
        self.func = func
        self.package = package
      
        self.imports = set()    

        self.pool : descriptor_pool.DescriptorPool = descriptor_pool.Default()
        self.name : str = to_upper_camel(func.__name__) #protobufs are picky! 
        
        self.type_mapping  = {
       #     typing.Any: any_pb2.Any, #the people do not deserve this 
            bool: descriptor.FieldDescriptor.TYPE_BOOL,
            str: descriptor.FieldDescriptor.TYPE_STRING,
            bytes: descriptor.FieldDescriptor.TYPE_BYTES,
            datetime: timestamp_pb2.Timestamp,
            float: descriptor.FieldDescriptor.TYPE_DOUBLE,
            int: descriptor.FieldDescriptor.TYPE_INT64,
        }


        self.args_dict = args_from_func(func)

        self.field_num_dict = OrderedDict(
            (name, i) for i, name in enumerate(self.args_dict.keys())
        )

        self.input_type, self.output_type = self.make_fake_types(self.name, self.args_dict)

        self.input_desc = self.convert(self.input_type)
        # clear imports? - nahhhhh

        self.output_desc = self.convert(self.output_type)

    def descriptors(self) -> typing.Tuple[Descriptor, Descriptor]:
        return self.input_desc, self.output_desc
    def message_classes(self) -> typing.Tuple[typing.Type, typing.Type]:
        return desc_to_message_class(self.input_desc), desc_to_message_class(self.output_desc)
    

    
    def make_fake_types(self, name : str, args_dict: typing.Dict[str, typing.Any] ) -> typing.Tuple[typing.Type, typing.Type]:
        ret_args ={ 'return_value': args_dict['return']}
        output_type = type(name + "Return", (object,), ret_args)
        args_dict.pop('return')
        input_type = type(name + "Args", (object,), args_dict)
        return input_type, output_type
    
   
    
    def convert(self, type_ : typing.Any) -> Descriptor:
        typename : str = type_.__name__
        
        desc_pb = self._conv(typename, type_)
        fd_pb = descriptor_pb2.FileDescriptorProto(
            name=f"{self.package}.{typename.lower()}.proto",
            package=self.package,
            syntax="proto3",
            dependency=sorted(list(self.imports)),
            message_type=[desc_pb]
        )
        add_fd_to_pool(fd_pb, self.pool)
        full_name = f"{self.package}.{typename}"
        logger.debug(f"Converted: {full_name}")
        return self.pool.FindMessageTypeByName(full_name)

    def _conv(self, name : str, entry : typing.Any) -> descriptor_pb2.DescriptorProto:

        #concrete types
        concrete_type = self.get_concrete_type(entry)
        if concrete_type:
            return self._convert_concrete_type(concrete_type)

        # dicts 
        map_info = self.get_map_key_val_types(entry)
        if map_info:
            return self._convert_map(name, *map_info)

        # returns the final descriptor_pb2.DescriptorProto
        message_fields = self.get_message_fields(entry)
        if message_fields is not None:
            return self._convert_message(name, entry, message_fields)

        raise ValueError(f"Got unsupported entry type({type(entry)}) {entry} for {name}")

    def get_concrete_type(self, entry_type: typing.Any) -> typing.Optional[typing.Type]:
        if entry_type in self.type_mapping or isinstance( entry_type, Descriptor):
           return entry_type
        descriptor_attr = getattr(entry_type, "DESCRIPTOR", None)
        if descriptor_attr is not None:
            return descriptor_attr
        return None
    
    def get_map_key_val_types(self, entry: typing.Any) -> typing.Optional[typing.Tuple[typing.Type, typing.Type]]:
        if typing.get_origin(entry) is dict:
            key_type, val_type = typing.get_args(entry)
            print(key_type, val_type)
            return (
                self._conv("key", key_type),
                self._conv("value", val_type),
            )
        return None
    def get_message_fields(self, entry: typing.Any) -> typing.Optional[typing.Dict[str, descriptor_pb2.FieldDescriptorProto]]:
        obj = entry
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith("__") and not inspect.ismethod(value):
                pr[name] = value
        pr = [(name, value) for name, value in pr.items()]
        return pr
    
    def _convert_concrete_type(self, concrete_type: typing.Type) -> Descriptor:
        entry_type = self.type_mapping.get(concrete_type, concrete_type)
        pb_type_desc = None
        desc_ref = self._get_descriptor(entry_type)
        if desc_ref is not None:
            pb_type_desc = desc_ref
        else:
            if concrete_type not in self.type_mapping:
                raise ValueError(f"Unsupported type {concrete_type}")
            pb_type_value = self.type_mapping[concrete_type]
            pb_type_desc = getattr(pb_type_value, "DESCRIPTOR", None)
            if pb_type_desc is None:
                if not isinstance(pb_type_value, int):
                    raise ValueError(f"Unsupported type {concrete_type}")
                pb_type_desc = pb_type_value
        if isinstance(pb_type_desc,Descriptor):
            self._add_import(pb_type_desc)
            logger.debug("Added descriptor to imports {pb_type_desc.name}")
        return pb_type_desc



    def _convert_map(self, name: str, key_type: int, val_type: Descriptor) -> descriptor_pb2.DescriptorProto:
        nested_name = f"{to_upper_camel(name)}Entry"
        key_field = descriptor_pb2.FieldDescriptorProto(
            name="key",
            type=key_type,
            number=1
        )
        val_field_kwargs = {}
        msg_descriptor_kwargs = {}
        if isinstance(val_type, int):
            val_field_kwargs = {"type": val_type}
        elif isinstance(val_type, descriptor.EnumDescriptor):
            val_field_kwargs = {
                "type": descriptor.FieldDescriptor.TYPE_ENUM,
                "type_name": val_type.name,
            }
        elif isinstance(val_type, descriptor.Descriptor):
            val_field_kwargs = {
                "type": descriptor.FieldDescriptor.TYPE_MESSAGE,
                "type_name": val_type.name,
            }
        elif isinstance(val_type, descriptor_pb2.EnumDescriptorProto):
            val_field_kwargs = {
                "type": descriptor.FieldDescriptor.TYPE_ENUM,
                "type_name": val_type.name,
            }
            msg_descriptor_kwargs["enum_type"] = [val_type]
        elif isinstance(val_type, descriptor_pb2.DescriptorProto):
            val_field_kwargs = {
                "type": descriptor.FieldDescriptor.TYPE_MESSAGE,
                "type_name": val_type.name,
            }
            msg_descriptor_kwargs["nested_type"] = [val_type]
        else:
            raise ValueError(f"Unsupported map value type: {val_type} {val_type.name}")

        val_field = descriptor_pb2.FieldDescriptorProto(
            name="value",
            number=2,
            **val_field_kwargs,
        )
        nested = descriptor_pb2.DescriptorProto(
            name=nested_name,
            field=[key_field, val_field],
            options=descriptor_pb2.MessageOptions(map_entry=True),
            **msg_descriptor_kwargs,
        )
        return nested
    

    def _convert_message(self, name: str, entry: typing.Any, message_fields: typing.Dict[str, descriptor_pb2.FieldDescriptorProto]) -> descriptor_pb2.DescriptorProto:
        #this mostly hasnt changed from IBM lib i stole it from
        field_descriptors = []
        nested_messages = []
        message_name = to_upper_camel(name)

        for field_name, field_def in message_fields:
            field_number = self.get_field_number(
                len(field_descriptors), field_def, field_name=field_name
            )
            field_kwargs = {
                "name": field_name,
                "number": field_number,
                "label": descriptor.FieldDescriptor.LABEL_OPTIONAL,
            }

            if self.is_repeated_field(field_def):
                field_kwargs["label"] = descriptor.FieldDescriptor.LABEL_REPEATED
            
            field_type = self.get_field_type(field_def)
            nested_name = self.get_field_type_name(field_type, field_name)
            nested_result = self._conv(entry=field_type, name=nested_name)
            nested_results = [(nested_result, {})]


            for nested, extra_kwargs in nested_results:
                nested_field_kwargs = copy.copy(field_kwargs)
                nested_field_kwargs.update(extra_kwargs)

                # int = pb type already 
                if isinstance(nested, int):
                    nested_field_kwargs["type"] = nested

                elif isinstance(nested, descriptor.Descriptor):
                    nested_field_kwargs["type"] = (
                        descriptor.FieldDescriptor.TYPE_MESSAGE
                    )
                    nested_field_kwargs["type_name"] = nested.full_name

                elif isinstance(nested, descriptor_pb2.DescriptorProto):
                    nested_field_kwargs["type"] = (
                        descriptor.FieldDescriptor.TYPE_MESSAGE
                    )
                    nested_field_kwargs["type_name"] = nested.name
                    nested_messages.append(nested)

                    if nested.options.map_entry:
                        nested_field_kwargs["label"] = (
                            descriptor.FieldDescriptor.LABEL_REPEATED
                        )

                        while nested.nested_type:
                            nested_type = nested.nested_type.pop()
                            plain_name = nested_type.name
                            nested_name = to_upper_camel(
                                "_".join([field_name, plain_name])
                            )
                            nested_type.MergeFrom(
                                descriptor_pb2.DescriptorProto(name=nested_name)
                            )
                            for field in nested.field:
                                if field.type_name == plain_name:
                                    field.MergeFrom(
                                        descriptor_pb2.FieldDescriptorProto(
                                            type_name=nested_name
                                        )
                                    )
                            nested_messages.append(nested_type)
                field_descriptors.append(
                    descriptor_pb2.FieldDescriptorProto(**nested_field_kwargs)
                )

        descriptor_proto = descriptor_pb2.DescriptorProto(
            name=message_name,
            field=field_descriptors,
            nested_type=nested_messages,
        )
        return descriptor_proto

    
    def _add_import(self, desc: Descriptor) -> None:
        import_file = desc.file.name
        if desc.file.pool != self.pool:
            fd_pb = descriptor_pb2.FileDescriptorProto()
            desc.file.CopyToProto(fd_pb)
            add_fd_to_pool(fd_pb, self.pool)
        self.imports.add(import_file)
    def _get_descriptor(self, entry: typing.Any) -> Descriptor:
        if isinstance(entry, Descriptor):
            return entry
        descriptor_attr = getattr(entry, "DESCRIPTOR", None)
        if descriptor_attr and isinstance(descriptor_attr, Descriptor):
            return descriptor_attr
        return None
    def get_field_type(self, field_def: typing.Any) -> typing.Any:
        if typing.get_origin(field_def) is list:
            args = typing.get_args(field_def)
            if len(args) == 1:
                return args[0]
        return field_def
    def get_field_type_name(self, field_def: typing.Any, field_name: str) -> str:
        if isinstance(field_def, type):
            return field_def.__name__
        return field_name
    def is_repeated_field(self, field_def: typing.Any) -> bool:
        return typing.get_origin(field_def) is list
    def get_field_number(self, num_fields: int, field_def: type, field_name: str) -> int:
        if self.field_num_dict and field_name in self.field_num_dict:
            return self.field_num_dict[field_name] + 1
        elif field_name == "return_value":
            return num_fields + 1
        else:
            logger.warning(f"Field {field_name} not found in field num dict")
        return num_fields + 1


@dataclass
class GRPCService:
    descriptor: ServiceDescriptor
    registration_function: typing.Callable[[Service, grpc.Server], None]
    client_stub_class: typing.Type
    service_class: typing.Type[Service]


@dataclass
class ToolMethod:
    func: typing.Callable
    method_desc: MethodDescriptor = None
    input_desc: Descriptor = None
    output_desc: Descriptor = None
    input_msg: typing.Type = None #actual python proto Message inst
    output_msg: typing.Type = None # ^
    wrapper_fn: typing.Callable = None
    predicate_fn: typing.Callable = None #for conditional masking
    group_name: str = None #for tool group availability


def methods_to_service( methods : typing.Dict[str, ToolMethod], package: str) -> GRPCService:
    pool = descriptor_pool.Default()
    service_fd_proto = _methods_to_service_file_descriptor_proto(
        methods=methods, package=package, pool=pool
    )
    assert len(service_fd_proto.service) == 1, (
        f"File Descriptor {service_fd_proto.name} should only have one service"
    )
    service_descriptor_proto = service_fd_proto.service[0]

    add_fd_to_pool(service_fd_proto, pool)
    service_fullname = (
        service_fd_proto.package + "." + service_fd_proto.package
    )  # name if not package else ".".join([package, name])

    service_descriptor = pool.FindServiceByName(service_fullname)

    client_stub = _service_descriptor_to_client_stub(
        service_descriptor, service_descriptor_proto
    )
    registration_function = _service_descriptor_to_server_registration_function(
        service_descriptor, service_descriptor_proto
    )
    service_class = _service_descriptor_to_service(service_descriptor)
    return GRPCService(
        descriptor=service_descriptor,
        service_class=service_class,
        client_stub_class=client_stub,
        registration_function=registration_function,
    )


def _methods_to_service_file_descriptor_proto(methods : typing.Dict[str, ToolMethod], package: str, pool: descriptor_pool.DescriptorPool) -> descriptor_pb2.FileDescriptorProto:
  
    method_descriptor_protos: typing.List[descriptor_pb2.MethodDescriptorProto] = []
    imports: typing.List[str] = []

    for name, func in methods.items():
        input_descriptor = func.input_desc
        output_descriptor = func.output_desc
        method_descriptor_protos.append(
            descriptor_pb2.MethodDescriptorProto(
                name=name,
                input_type=input_descriptor.full_name,  # this might be the bug lol
                output_type=output_descriptor.full_name,
                client_streaming=False,
                server_streaming=False,
            )
        )
        imports.append(input_descriptor.file.name)
        imports.append(output_descriptor.file.name)

    imports = sorted(list(set(imports)))

    service_descriptor_proto = descriptor_pb2.ServiceDescriptorProto(
        name=package, method=method_descriptor_protos
    )

    fd_proto = descriptor_pb2.FileDescriptorProto(
        name=f"{package.lower()}.proto",
        package=package,
        syntax="proto3",
        dependency=imports,
        # **proto_kwargs,
        service=[service_descriptor_proto],
    )

    return fd_proto


def _service_descriptor_to_service( service_descriptor: ServiceDescriptor) -> typing.Type[Service]:
    return types.new_class(
        service_descriptor.name,
        (Service,),
        {"metaclass": GeneratedServiceType},
        lambda ns: ns.update({"DESCRIPTOR": service_descriptor}),
    )



def _service_descriptor_to_client_stub(
    service_descriptor: ServiceDescriptor,
    service_descriptor_proto: descriptor_pb2.ServiceDescriptorProto,
) -> typing.Type:
    """Generates a new client stub class from the service descriptor

    Args:
        service_descriptor:  google.protobuf.descriptor.ServiceDescriptor
            The ServiceDescriptor to generate a service interface for
        service_descriptor_proto:  google.protobuf.descriptor_pb2.ServiceDescriptorProto
            The descriptor proto for that service. This holds the I/O streaming information
            for each method
    """
    _assert_method_lists_same(service_descriptor, service_descriptor_proto)

    def _get_channel_func(
        channel: grpc.Channel, method: descriptor_pb2.MethodDescriptorProto
    ) -> typing.Callable:
        if method.client_streaming and method.server_streaming:
            return channel.stream_stream
        if not method.client_streaming and method.server_streaming:
            return channel.unary_stream
        if method.client_streaming and not method.server_streaming:
            return channel.stream_unary
        return channel.unary_unary

  
    def initializer(self, channel: grpc.Channel):
        for method, method_proto in zip(
            service_descriptor.methods, service_descriptor_proto.method
        ):
            setattr(self,method.name,
                _get_channel_func(channel, method_proto)(
                    _get_method_fullname(method),
                    request_serializer=desc_to_message_class(
                        method.input_type
                    ).SerializeToString,
                    response_deserializer=desc_to_message_class(
                        method.output_type
                    ).FromString,
                ),
            )
    return type(
        f"{service_descriptor.name}Stub",
        (object,),
        {
            "__init__": initializer,
        },
    )


def _service_descriptor_to_server_registration_function(
    service_descriptor: ServiceDescriptor,
    service_descriptor_proto: descriptor_pb2.ServiceDescriptorProto,
) -> typing.Callable[[Service, grpc.Server], None]:

    _assert_method_lists_same(service_descriptor, service_descriptor_proto)

    def _get_handler(method: descriptor_pb2.MethodDescriptorProto):
        if method.client_streaming and method.server_streaming:
            return grpc.stream_stream_rpc_method_handler
        if not method.client_streaming and method.server_streaming:
            return grpc.unary_stream_rpc_method_handler
        if method.client_streaming and not method.server_streaming:
            return grpc.stream_unary_rpc_method_handler
        return grpc.unary_unary_rpc_method_handler

    def registration_function(servicer: Service, server: grpc.Server):
        rpc_method_handlers = {
            method.name: _get_handler(method_proto)(
                getattr(servicer, method.name),
                request_deserializer=desc_to_message_class(
                    method.input_type
                ).FromString,
                response_serializer=desc_to_message_class(
                    method.output_type
                ).SerializeToString,
            )
            for method, method_proto in zip(
                service_descriptor.methods, service_descriptor_proto.method
            )
        }
        generic_handler = grpc.method_handlers_generic_handler(
            service_descriptor.full_name, rpc_method_handlers
        )
        server.add_generic_rpc_handlers((generic_handler,))

    return registration_function


def _get_method_fullname(method: MethodDescriptor):
    method_name_parts = method.full_name.split(".")
    return f"/{'.'.join(method_name_parts[:-1])}/{method_name_parts[-1]}"


def _assert_method_lists_same(
    service_descriptor: ServiceDescriptor,
    service_descriptor_proto: descriptor_pb2.ServiceDescriptorProto,
):
    assert len(service_descriptor.methods) == len(service_descriptor_proto.method), (
        f"Method count mismatch: {service_descriptor.full_name} has"
        f" {len(service_descriptor.methods)} methods but proto descriptor"
        f" {service_descriptor_proto.name} has {len(service_descriptor_proto.method)} methods"
    )

    for m1, m2 in zip(service_descriptor.methods, service_descriptor_proto.method):
        assert m1.name == m2.name, f"Method mismatch: {m1.name}, {m2.name}"


# THE MAGIC STARTS HERE 

class TruffleRuntime(BaseRuntime):
    def __init__(self):
        self.cls = None
        self.tool_methods = {}
    def build(self, class_instance):
        self.cls = class_instance

        

        def attach_func_to_class(func, cls):
            func.__truffle_tool__ = True
            func.__truffle_description__ = func.__name__
            func.__truffle_icon__ = None
            func.__truffle_args__ = None
            func.__truffle_group__ = None
            func.__truffle_internal__ = True
            func.__truffle_flags__ = None

            
            setattr(cls, func.__name__, types.MethodType(func, cls))
            return func

        def attach_GetToolMask(inst : TruffleRuntime):
            def TruffleGetToolMask(self, check_all: bool) -> typing.Dict[str, bool]:
                mask = {}
                for name, tool_method in inst.tool_methods.items():
                    if tool_method.predicate_fn is not None:
                        try:
                            can_call = tool_method.predicate_fn()
                            if not isinstance(can_call, bool):
                                raise ValueError(f"Predicate for {name} must return a boolean, got {type(can_call)}")
                            mask[name] = can_call
                        except Exception as e:
                            mask[name] = True
                            logger.error(f"Error calling predicate for {name}: {e}")
                    else:
                        mask[name] = True
                return mask
            attach_func_to_class(TruffleGetToolMask, inst.cls)
        
        def attach_LoadState(inst : TruffleRuntime):
            def TruffleLoadState(self, state: bytes) -> bool:
                try: 
                    state_dict = json.loads(state)
                    logger.debug(f"Loading state: {state_dict}")
                    for name, value in state_dict.items():
                        setattr(self, name, value)
                    return True
                except Exception as e:
                    logger.error(f"Error loading state: {e}")
                    return False
                
            attach_func_to_class(TruffleLoadState, inst.cls)
        def attach_SaveState(inst : TruffleRuntime):
            def TruffleSaveState(self, flags : int) -> bytes:
                vars = get_non_function_members(self)
                print(vars)
                state = {}
                for name, value in vars.items():
                    if is_jsonable(value):
                        state[name] = value
                try:
                    serialized = json.dumps(state).encode()
                    logger.debug(f"Saving state: {state}")
                    return serialized
                except Exception as e:
                    logger.error(f"Error serializing state: {e}")
                    return b""
            attach_func_to_class(TruffleSaveState, inst.cls)


        TO_ATTACH = [
            attach_GetToolMask,
            attach_LoadState,
            attach_SaveState
        ]
        for fn in TO_ATTACH:
            fn(self)
            logger.debug(f"Attached {fn.__name__} to {self.cls.__class__.__name__}")

        tool_fns = get_truffle_tool_fns(self.cls)
        print(tool_fns)

        for name, func in tool_fns.items():
            if to_upper_camel(name) != name:
                name = to_upper_camel(name)

            ftp = FuncToProto(func, self.cls.__class__.__name__)
            input_desc, output_desc =  ftp.descriptors()
            input_msg, output_msg = ftp.message_classes()

            #todo: fix function names! 

            tool_method = ToolMethod(
                func=func,
                input_desc=input_desc,
                output_desc=output_desc,
                input_msg=input_msg,
                output_msg=output_msg,
                wrapper_fn=None,
                predicate_fn= getattr(func, "__truffle_predicate__", None),
                group_name=getattr(func, "__truffle_group__", None)
            )
            self.tool_methods[name] = tool_method
            logger.debug(f"Built tool method {name}")
        self._service = methods_to_service(self.tool_methods, self.cls.__class__.__name__)
        logger.debug(f"Built service {self._service.descriptor.name}")


        def handle_request(method : ToolMethod, cls, request, context : grpc.ServicerContext):
            for metadatum in context.invocation_metadata(): # how we add additional info from decs 
                if metadatum.key == "get_desc":
                    metadata = (
                        ("truffle_tool_desc", method.func.__truffle_description__),
                        ("truffle_tool_name", method.func.__name__),
                    )
                    if hasattr(method.func, "__truffle_icon__") and method.func.__truffle_icon__ is not None:
                        metadata += (("truffle_tool_icon", method.func.__truffle_icon__),)
                    if hasattr(method.func, "__truffle_args__") and method.func.__truffle_args__ is not None:
                        for var_name, var_desc in method.func.__truffle_args__.items():
                            metadata += ((var_name, var_desc),)
                    if hasattr(method.func, "__truffle_group__") and method.func.__truffle_group__ is not None:
                        metadata += (("truffle_tool_group", method.func.__truffle_group__),)

                    if hasattr(method.func, "__truffle_internal__") and method.func.__truffle_internal__:
                        metadata += (("truffle_tool_internal", "true"),)
                    if hasattr(method.func, "__truffle_flags__") and method.func.__truffle_flags__ is not None:
                        metadata += (("truffle_tool_flags", method.func.__truffle_flags__),)
                    context.set_trailing_metadata(metadata)
                    logger.debug(f"Sent metadata for {method.func.__name__}")
                    return method.output_msg()
            args_dict = MessageToDict( # we hate this fn 
                request,
                always_print_fields_with_no_presence=True, # we <3 this flag
                preserving_proto_field_name=True,
                descriptor_pool=descriptor_pool.Default()
            )
            #do stupid string conversion.. honestly dont ask
            for field  in method.input_msg.DESCRIPTOR.fields:
                if field.name in args_dict:
                    if is_numeric_field(field):
                        args_dict[field.name] = float(args_dict[field.name]) if is_float_field(field) else int(args_dict[field.name])
                    if field.type == FieldDescriptor.TYPE_BYTES:
                        if isinstance(args_dict[field.name], str):
                            if hasattr(request, field.name):
                                args_dict[field.name] = getattr(request, field.name)
                            else:
                                #message to dict probably base64'd bytes to a string 
                                try:
                                    args_dict[field.name] = bytes(base64.b64decode(args_dict[field.name]))
                                except Exception as e:
                                    args_dict[field.name] = bytes(args_dict[field.name].encode()) 

                            if type(args_dict[field.name]) != bytes:
                                logger.error(f"Expected bytes for field {field.name}, got {type(args_dict[field.name])}")
                                
            args = list(args_dict.values())

            logger.debug(f"Received request for {method.func.__name__} with args <{args}>")
            #logger.debug(text_format.MessageToString(request, print_unknown_fields=True, use_field_number=True, ))

            try:
                ret = method.func(cls, *args)
                ret_pb = method.output_msg()
                for field in ret_pb.DESCRIPTOR.fields:
                    if field.name != "return_value":
                        continue
                    if field.message_type and field.message_type.has_options and field.message_type.GetOptions().map_entry:
                        if isinstance(ret, dict):
                            map_field = getattr(ret_pb, field.name)
                            map_field.update(ret)
                            logger.debug(f"Updated map field {field.name} with {ret}")
                        else:
                            logger.error(f"Expected dict for map field {field.name}, got {type(ret)}")
                    elif field.label == FieldDescriptor.LABEL_REPEATED:
                        if isinstance(ret, (list, tuple)):
                            getattr(ret_pb, field.name).extend(ret)
                        else:
                            getattr(ret_pb, field.name).append(ret)
                    else:
                        if field.type == FieldDescriptor.TYPE_MESSAGE:
                            logger.debug(f"Message field {field.name} is {field.message_type}")
                            if isinstance(ret, dict):
                                getattr(ret_pb, field.name).ParseFromDict(ret)
                            else:
                                nested = getattr(ret_pb, field.name)
                                logger.debug("nested message: ", type(nested))
                                nested = ret # questionable
                        else:
                            logger.debug(f"setting field {field.name} to {ret}")
                            setattr(ret_pb, field.name, ret)
                context.set_code(grpc.StatusCode.OK)
                context.set_details(f"Success calling {method.func.__name__}")
                return ret_pb
            except Exception as e:
                logger.error(f"Error calling {method.func.__name__}: {e}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Error calling {method.func.__name__}: {e}")
                return method.output_msg()
        for name, method in self.tool_methods.items():
            method.wrapper_fn = functools.partial(handle_request, method, self.cls)
        
        class AppService(self._service.service_class):
            def __init__(self, tool_methods, desc):
                super().__init__()
                self.tool_methods = tool_methods
                self.desc = desc
            def __getattribute__(self, name: str) -> typing.Any:
                if name != "tool_methods":
                    if name in self.tool_methods:
                        return self.tool_methods[name].wrapper_fn
                return super().__getattribute__(name)
        if os.path.exists(APP_SOCK):
            os.unlink(APP_SOCK)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=4)) # only us hitting this from outside of container
        self._service.registration_function(AppService(self.tool_methods, self._service.descriptor), server) #i honestly dont remember what i was doing with this
        reflection.enable_server_reflection(
            [self._service.descriptor.full_name, reflection.SERVICE_NAME], server
        )
        server.add_insecure_port(APP_SOCK)
        logger.info(f"Starting server on {APP_SOCK}")
     
        server.start()
        logger.debug("Server is up")
        server.wait_for_termination()
        logger.info("Server terminated")

        

#cmd to test:
#grpcurl -plaintext -unix -use-reflection unix:///tmp/truffle_app.sock describe   



#damn derek even broke this 
# i am bitter but this basically fuzzes every fn. well it did. before someone copypasta'ed my shit into worse shit
def test_client(socket_path: str):

    def _assign_test_value_to_oneof_arg(field):
        if field.type == FieldDescriptor.TYPE_BOOL:
            setattr(args, field.name, False)
        elif (
            field.type == FieldDescriptor.TYPE_INT32
            or field.type == FieldDescriptor.TYPE_INT64
            or field.type == FieldDescriptor.TYPE_UINT32
            or field.type == FieldDescriptor.TYPE_UINT64
        ):
            setattr(args, field.name, 1)
        elif (
            field.type == FieldDescriptor.TYPE_FLOAT
            or field.type == FieldDescriptor.TYPE_DOUBLE
        ):
            setattr(args, field.name, 6.9)
        elif field.type == FieldDescriptor.TYPE_STRING:
            setattr(
                args,
                field.name,
                "https://en.wikipedia.org",
            )
        elif field.type == FieldDescriptor.TYPE_MESSAGE:
            is_map = (
                field.message_type
                and field.message_type.has_options
                and field.message_type.GetOptions().map_entry
            )
            if is_map:
                map_field = getattr(args, field.name)
                map_field.update({"testkey": "testvalue"})
            else:
                logger.debug(f"field {field.name} is message")
                logger.debug(f"field message type: {field.message_type}")
                logger.debug(f"field message type name: {field.message_type.name}")
    from grpc_reflection.v1alpha.proto_reflection_descriptor_database import ProtoReflectionDescriptorDatabase
    from google.protobuf.descriptor_pool import DescriptorPool
    
    logger.info("trying to connect to TruffleApp gRPC server")
    channel = grpc.insecure_channel(socket_path)
    reflection_db = ProtoReflectionDescriptorDatabase(channel)
    server_pool = DescriptorPool(reflection_db)
    service_names = reflection_db.get_services()
    for name in service_names:
        if name == "grpc.reflection.v1alpha.ServerReflection":
            continue
        logger.debug(f"found service: {name}")
        service_desc = server_pool.FindServiceByName(name)
        logger.debug(f"service desc: {service_desc.full_name}")
        for method in service_desc.methods:
            logger.debug(f"method: {method.name}")
            # if method.name != "EnviromentInfo":
            #     continue
            logger.debug(f"input: {method.input_type.name}")
            logger.debug(f"output: {method.output_type.name}")
            logger.debug(f"in type desc: {repr(method.input_type)}")
            logger.debug(
                f"input desc: {server_pool.FindMessageTypeByName(method.input_type.full_name)}",
            )
            args_type = desc_to_message_class(method.input_type)
            logger.debug(args_type)
            ret_type = desc_to_message_class(method.output_type)
            args = args_type()
            for field_descriptor in args.DESCRIPTOR.fields:
                # handle repeated fields as lists, since assignment is not allowed!!
                if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
                    repeated_field = getattr(args, field_descriptor.name)
                    repeated_field.extend(["http://example.com", "http://example.com"])
                else:
                    _assign_test_value_to_oneof_arg(field_descriptor)

            logger.debug(f"args: {args}")
            ret = ret_type()
            logger.debug(f"ret: {ret}")
            logger.debug("calling method with get_desc")
            response, call = channel.unary_unary(
                f"/{service_desc.full_name}/{method.name}",
                request_serializer=args.SerializeToString,
                response_deserializer=ret.FromString,
            ).with_call(args, metadata=(("get_desc", "true"),))
            logger.debug(f"response: {response}")
            logger.debug(f"call: {call.trailing_metadata()}")
            logger.debug("calling method without get_desc")
            response = channel.unary_unary(
                f"/{service_desc.full_name}/{method.name}",
                request_serializer=args.SerializeToString,
                response_deserializer=ret.FromString,
            )(args)
            logger.debug(f"response: {response}")
