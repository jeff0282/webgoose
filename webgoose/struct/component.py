
import  re
import  os

from    typing      import      Any
from    typing      import      Optional
from    typing      import      Type

from    webgoose.exceptions     import      _BaseWebgooseException
from    webgoose.struct         import      FileGroup



class ComponentExistsError(_BaseWebgooseException):
    pass


class MalformedComponentNameError(_BaseWebgooseException):
    pass


class Component:

    _name: str
    _slug: Optional[str]
    _parent: Optional[Type['Component']]
    _children: list[Type['Component']]
    pages: Type[PageGroup]
    files: Type[FileGroup]
    context: dict[str, Any]

    def __init__(self, name: str) -> None:
        
        # validate component name
        self._validate_component_name(name)

        self._name = name
        self._slug = None
        self._parent = None
        self._children = []
        self.context = dict()
        self.pages = PageGroup()
        self.files = FileGroup()


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    

    def __getattr__(self, key: str) -> Optional[Type['Component']]:
        return self.get_child(key)


    def __getitem__(self, key: str) -> Any:
        self.context.get(key)


    def __setitem__(self, key: str, value: Any) -> None:
        self.context.update(key, value)


    def __delitem__(self, key: str) -> None:
        self.context.pop(key)


    @property
    def name(self) -> str:
        return self._name
    

    @property
    def slug(self) -> Optional[str]:
         return self._slug
    

    @property
    def parent(self) -> Type['Component']:
        return self._parent


    @property
    def children(self) -> tuple[Type['Component']]:
        return tuple(self._children)
    

    @staticmethod
    def _validate_component_name(self, name: str) -> None:
        """
        Validate a string name for use as a component name
        
        Raises MalformedComponentNameError on error
        """

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$"):
            raise MalformedComponentNameError("""Invalid Component Name. Must only contain letters, 
                                                numbers & underscores, and be a valid Python attribute name""")


    def add(self, page: Type['Renderable']) -> None:
        self.pages.add(page)


    def add_static(self, filename: str | os.PathLike) -> None:
        self.files.add(filename)
            

    def get_component(self, name: str, default: Optional[Any] = None) -> Optional[Type['Component']]:
        """
        Get a child component by it's name

        Takes an optional default value, otherwise returns None on no match
        """

        for child in self._children:
            if child.name == name:
                return child
            
        return default


    def attach_component(self, component: Type['Component'], attach_point: Optional[str] = None) -> None:
        """
        Attach a component as a child of this one


        Raises:
            - ComponentExistsError() if a child component with a duplicate name exists
            - ValidationError() if the attach_point is not a valid string path
        """

        # check for duplicate name
        if self.get_component(component.name, default=None):
            raise ComponentExistsError(f"Component '{self}' already has a child component with name '{component.name}'")
        

        # set up relationship
        component._parent = self
        component._slug = attach_point
        self._children.append(component)


        



                    
        
    



    
    


