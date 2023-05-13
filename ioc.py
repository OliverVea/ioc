from typing import Any, Type

from ioc.errors import *

class IOC:
    def __init__(self):
        self._anonymous_instances: dict[int, list[object]] = {}
        self._named_instances: dict[int, list[object]] = {}

    def _anonymous_instance_key(self, instance_type: Type) -> int:
        return (instance_type)

    def _named_instance_key(self, instance_type: Type, instance_id: str) -> int:
        return (instance_type, instance_id)
        
    def add_instance(self, instance: Any, instance_type: Type | None = None, instance_id: str | None = None, clear_previous: bool = False) -> None:
        actual_type = type(instance)

        if instance_type:
            invalid_type = actual_type != instance_type and instance_type not in actual_type.__bases__
            if invalid_type:
                raise InstanceIncorrectTypeError(f'object of type {type(instance)} is not instance of type {instance_type}')

        else:
            instance_type = actual_type

        if instance_id:
            service_key = self._named_instance_key(instance_type, instance_id)
            collection = self._named_instances
        
        else:
            service_key = self._anonymous_instance_key(instance_type)
            collection = self._anonymous_instances

        if clear_previous and service_key in collection:
            del collection[service_key]

        services = collection.setdefault(service_key, [])
        
        if instance not in services:
            services.append(instance)

    def get_instance(self, instance_type: Type, instance_id: str | None = None, required: bool = False) -> Any:
        service = None

        if instance_id: 
            instance_key = self._named_instance_key(instance_type, instance_id)
            if instance_key in self._named_instances:
                service = self._named_instances[instance_key][-1]

        else:
            instance_key = self._anonymous_instance_key(instance_type)
            if instance_key in self._anonymous_instances:
                service = self._anonymous_instances[instance_key][-1]
        
        if required and service is None:
            message = f'Could not find object with type \'{instance_type}\'' + (f' and instance id \'{instance_id}\'' if instance_id else '') + '.'
            raise InstanceNotFoundError(message)

        return service
    
    def get_instances(self, instance_type: Type) -> list[Any]:
        instance_key = self._anonymous_instance_key(instance_type)

        if not instance_key in self._anonymous_instances:
            return []
        
        return self._anonymous_instances[instance_key]
