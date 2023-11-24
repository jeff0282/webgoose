"""
Context
"""

from    typing      import      Any
from    typing      import      Type


class Context:
    """
    A simple class that restricts addition of key/value pairs based
    on what already exists in it's 'fixed' dictionary

    
    """

    _fixed: dict[str, Any]
    _overwritable: dict[str, Any]

    def __init__(self) -> None:
        """
        Create a new Context instance
        """
        self._fixed = dict()
        self._overwritable = dict()


    def __repr__(self) -> str:
        return str(self.to_dict())


    def __contains__(self, cmp: Any):
        cmp in self.to_dict()


    def __getitem__(self, key: str) -> Any:
        """
        Get a value by key from this instance
        """
        val = self.to_dict().get(key, None)
        if val:
            return val

        raise KeyError(f"No such key '{key}' found")


    def __setitem__(self, key: str, value: Any) -> None:
        """
        Add a key/value pair to this instance's overwritable mapping
        """
        self.add(key=value)


    def __delitem__(self, key: str):
        """
        Delete a key/value pair from this instance by key
        """
        if key in self._fixed:
            return self._fixed.pop(key)
        elif key in self._overwritable:
            return self._overwritable.pop(key)
        
        raise KeyError(f"No such key '{key}' found")
        

    def to_dict(self) -> dict[str, Any]:
        """
        Convert this Context Instance to a Dict
        """

        # ensure that even if something went wrong
        # fixed key/vals still override overwritable key/vals
        ctx = dict(self._overwritable)
        ctx.update(self._fixed)
        return ctx


    def add(self, **new_mappings) -> None:
        """
        Add an overwritable mapping

        Throws a KeyError if a Key already exists as a fixed mapping
        """
        self.validate_keys(new_mappings)
        
        # if all good, add to overwritable
        self._overwritable.update(new_mappings)


    def add_fixed(self, **new_mappings) -> None:
        """
        Add a fixed mapping

        Throws a KeyError if a Key already exists as a fixed mapping
        """
        self.validate_keys(new_mappings)
        
        # if all good, add to overwritable
        self._fixed.update(new_mappings)

    
    def validate_keys(self, new_mappings: dict[str, Any]) -> None:
        """
        Validate a dict containing new mappings

        Throws a KeyError if a Key already exists as a fixed mapping
        """
        if any(k for k in new_mappings.keys() if k in self._fixed):
            raise KeyError("Cannot add mapping: Key '{k}' already exists as a fixed mapping")


    @classmethod
    def from_context(cls, instance: Type['Context']) -> Type['Context']:
        """
        Create a new Context instance using an existing instance 
        """
        new_ctx = cls()
        new_ctx._fixed = instance._fixed
        new_ctx._overwritable = instance._overwritable
