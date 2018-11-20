from importlib import import_module

from .base_protocol import BaseProtocol

import inspect


def grab(protocol_name, *args, **kwargs):

    try:
        module_name = protocol_name
        if not module_name.endswith("_protocol"):
            module_name = module_name + "_protocol"

        module = import_module('.' + module_name, package='protocols')
        classes = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name != "BaseProtocol":
                classes.append((name, obj))
        if len(classes) != 1:
            raise Exception("File for protocol {} contains {} classes. Requires 1".format(protocol_name, len(classes)))
        class_name  = classes[0][0]


        protocol_class = getattr(module, class_name)

        instance = protocol_class()

    except (AttributeError, AssertionError, ModuleNotFoundError) as e:
        raise ImportError('{} is not a supported protocol because {}.'.format(protocol_name, e))
    else:
        if not issubclass(protocol_class, BaseProtocol):
            raise ImportError("{} is importable but is not a Protocol".format(protocol_class))

    return instance
