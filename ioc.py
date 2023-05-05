from typing import Any, Type

class InstanceNotFoundError(ValueError):
    pass

class InstanceIncorrectTypeError(TypeError):
    pass

class IOC:
    def __init__(self):
        self._anonymous_instances: dict[int, list[object]] = {}
        self._services: dict[int, list[object]] = {}

    def _anonymous_instance_key(self, instance_type: Type) -> int:
        return (instance_type)

    def _named_instance_key(self, instance_type: Type, instance_id: str) -> int:
        return (instance_type, instance_id)
        
    def add_instance(self, instance: Any, instance_type: Type | None = None, instance_id: str | None = None) -> None:
        actual_type = type(instance)

        if instance_type:
            invalid_type = actual_type != instance_type and instance_type not in actual_type.__bases__
            if invalid_type:
                raise InstanceIncorrectTypeError(f'object of type {type(instance)} is not instance of type {instance_type}')

        else:
            instance_type = actual_type

        if instance_id:
            service_key = self._named_instance_key(instance_type, instance_id)
            services = self._services.setdefault(service_key, [])
            
            if instance not in services:
                services.append(instance)

        else:
            service_key = self._anonymous_instance_key(instance_type)
            services = self._anonymous_instances.setdefault(service_key, [])
            
            if instance not in services:
                services.append(instance)

    def get_instance(self, instance_type: Type, instance_id: str | None = None, required: bool = False) -> Any:
        service = None

        if instance_id: 
            instance_key = self._named_instance_key(instance_type, instance_id)
            if instance_key in self._services:
                service = self._services[instance_key][-1]

        else:
            instance_key = self._anonymous_instance_key(instance_type)
            if instance_key in self._anonymous_instances:
                service = self._anonymous_instances[instance_key][-1]
        
        if required and service is None:
            message = f'Could not find object with type \'{instance_type}\'' + f' and instance id \'{instance_id}\'' if instance_id else '' + '.'
            raise InstanceNotFoundError(message)

        return service
    
    def get_instances(self, instance_type: Type) -> list[Any]:
        instance_key = self._anonymous_instance_key(instance_type)

        if not instance_key in self._anonymous_instances:
            return []
        
        return self._anonymous_instances[instance_key]

ioc = IOC()

if __name__ == '__main__':
    a = 10

    ioc.add_instance(a)
    ioc.add_instance(a, int)

    error = None
    try: ioc.add_instance(a, float)
    except InstanceIncorrectTypeError as e: error = e
    assert error != None

    assert ioc.get_instance(int) is a

    b = 5
    ioc.add_instance(b)
    
    assert ioc.get_instance(int) is not a
    assert ioc.get_instance(int) is b

    ioc.add_instance(a, instance_id = 'a')
    ioc.add_instance(b, instance_id = 'b')

    assert ioc.get_instance(int, 'a') is a
    assert ioc.get_instance(int, 'b') is b

    assert ioc.get_instance(float) is None
    assert ioc.get_instance(int, 'c') is None

    error = None
    try: ioc.get_instance(float, required=True)
    except InstanceNotFoundError as e: error = e
    assert error != None

    error = None
    try: ioc.get_instance(int, 'c', required=True)
    except InstanceNotFoundError as e: error = e
    assert error != None

    ints = ioc.get_instances(int)

    assert len(ints) == 2
    assert a in ints and b in ints

    floats = ioc.get_instances(float)

    assert len(floats) == 0

    c = 0.5

    ioc.add_instance(c)

    floats = ioc.get_instances(float)

    assert len(floats) == 1
    assert c in floats


    class Parent:
        pass

    class Child(Parent):
        pass

    parent = Parent()
    child = Child()

    ioc.add_instance(parent)
    ioc.add_instance(child)

    assert ioc.get_instance(Parent) is parent
    assert ioc.get_instance(Child) is child

    ioc.add_instance(child, Parent)

    parents = ioc.get_instances(Parent)

    assert parent in parents and child in parents
