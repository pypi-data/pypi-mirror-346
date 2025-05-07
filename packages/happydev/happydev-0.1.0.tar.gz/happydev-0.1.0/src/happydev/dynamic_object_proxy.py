from wrapt.wrappers import ObjectProxy


# if you try to do 'class DynamicObjectProxy(wrapt.ObjectProxy):' it fails with 'TypeError: can't apply this __setattr__ to DynamicObjectProxy object'
# I have absolutely no idea why
# @todo mutable object proxy eh um nome melhor?
class DynamicObjectProxy(ObjectProxy):
    __slots__ = ('_self_wrapped_getter',)

    def __init__(self, wrapped_getter):
        """
        Creates an proxy to an object, which is resolved each time it's accessed. wrapped_getter is a function returning the wrapped object.
        This is useful when using libraries that don't pick up changes to global state. Example use:

        import mymodule
        proxied_var = DynamicObjectProxy(lambda: mymodule.var)
        function(mymodule.var)  # if mymodule.var is updated, function won't see it
        function(proxied_var)  # using DynamicObjectProxy proxy, mymodule.var will be resolved on each access
        """
        self._self_wrapped_getter = wrapped_getter

    @property
    def __wrapped__(self):
        value = self._self_wrapped_getter()
        # as it stands, I dont think it's possible to reuse the code in ObjectProxy.__setattr__ without unreasonable hoops
        try:
            object.__delattr__(self, '__qualname__')
        except AttributeError:
            pass
        try:
            object.__setattr__(self, '__qualname__', value.__qualname__)
        except AttributeError:
            pass
        try:
            object.__delattr__(self, '__annotations__')
        except AttributeError:
            pass
        try:
            object.__setattr__(self, '__annotations__', value.__annotations__)
        except AttributeError:
            pass
        return value
