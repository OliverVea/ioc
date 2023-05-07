"""
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
"""