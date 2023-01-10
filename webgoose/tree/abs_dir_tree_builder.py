
import  logging
import  yaml

from    pathlib     import      Path
from    typing      import      Any
from    typing      import      List
from    typing      import      Tuple
from    typing      import      Union

from    tree.factory    import      FileFactory
from    tree.struct     import      File



# Initialise Logger for this Module
logger = logging.getLogger(__name__)



class AbsDirTreeBuilder:

    """
    Abstract Directory Tree builder:
    ---

    Recursively grabs all (non-hidden) files from a directory, and constructs an abstract
    directory tree representing the completed structure, with all special files evaluated
    and file and directory information retrieved.

    This Builder grabs all information, and creates an mutable structure, will is then converted 
    to an Immutable Structure by way of the Directory class and subclasses.


    NOTE:

    Methods here are NOT fully private, as doing so would prevent inheritance.
    """



    class _MutableDirectory:

        """
        Mutable Directory
        ---

        A Throwaway Class to act as a mutable node in a directory tree

        Nested inside Abstract Directory Tree Builder as this is the only context where it is used

        I could use a Dict but this is slightly more robust/easier to read
        """

        def __init__(self, parent: Union[str, None], name: str) -> None:

            self.parent = parent
            self.dirname = name
            self.meta = {}
            self.subdirectories = []
            self.files = []



    def __init__(self, path: str) -> None:

        """
        Initialise Mutable Directory Structure with Root Directory

        This Mutable Structure will be Filled In with Directory Info (recursive), 
        and Converted to an Immutable Form
        """

        self.__path = Path(path)
        self.__root = AbsDirTreeBuilder._MutableDirectory(None, "/")



    def build_tree(self) -> 'Directory':

        """
        Public method responsible for calling every method required to gather information
        about a directory recursively, construct the mutable tree, and create the immutable tree from it

        Returns the root directory node of the resulting immutable tree.
        """

        # Returns A List of Path Objects
        file_paths = self._get_files()

        print(file_paths)

        # Handle Every File Found
        for file in file_paths:

            # Ensure A Path Exists To The Destination Dir Node In The Tree
            # And Get A Pointer To It
            current_dir = self._make_path(file)

            # Pass Every Path Object to the File Handler
            # This Handler Will Return Either A File Node or None
            file_node = self._handle_file(current_dir, file)


            # If Handler Returns None, The File Will Not Be Added To The Tree
            if file_node != None:
                print(f"adding file {file.name} to {current_dir.dirname}")
                current_dir.files.append(file_node)
            else:
                print(f"skipping file {file.name}")

        # Return the root node, which should now represent the root of the completed tree
        return self.__root



    def _get_files(self) -> List[Path]:

        """
        Semi-Private method responsible for getting all files from the search directory specified

        Returns a list of Path objects for every non-hidden file found.
        """

        # Lambda 'is_hidden' -> bool
        # Checks if a file path is hidden
        # True if any part of the path after the search directory starts with a dot
        # otherwise False
        is_hidden = lambda path: any(part for part in path.relative_to(self.__path).parts if part.startswith("."))

        # Recursively glob the search directory, add only files to the list provided they are not hidden
        return [file for file in self.__path.rglob("**/*") if file.is_file() and not is_hidden(file)]



    def _make_path(self, file_path: Path) -> '_MutableDirectory':

        """
        Semi-Private method for ensuring a path exists to a file location in the mutable directory tree

        Creates directory nodes for the path if it doesn't already exist

        Returns the last directory in the chain; the directory that the file should be placed in
        """

        def helper(current_dir: '_MutableDirectory', path_parts: Tuple[str]) -> '_MutableDirectory':

            # Base Case
            # There are no more parts in the path to create/match a directory for
            if len(path_parts) <= 0:
                return current_dir


            # Recursive Case
            # We first see if there is a directory with a matching name to the current path part
            find_matching_dir = (dir for dir in current_dir.subdirectories if dir.dirname == path_parts[0])

            # We attempt to yield the next value, which should cause an exception if no match is found
            try:

                # If This Succeeds, The Directory Exists, So We Just Use It!
                next_dir = next(find_matching_dir)

            except StopIteration:
                
                # The Directory Doesn't Exist, So We Make It
                next_dir = AbsDirTreeBuilder._MutableDirectory(current_dir, path_parts[0])

                # And add it to the current dirs subdirectory list
                current_dir.subdirectories.append(next_dir)

            
            # We Make A Recursive Call To Complete The Creation Of Directory Nodes
            # We Pass The Next_Directory, And The Path_Elements Minus First Elements As It Has Just Been Checked
            return helper(next_dir, path_parts[1:])

        
        # The Abstract Directory Tree Only Cares For What Is Inside The Directory Specified
        # (otherwise you'll potentially have a bunch of meaningless dir nodes at the root of the tree :/)
        # Path Objects May Have The Search Directory As A Prefix, Which We Must Remove
        tree_path = file_path.relative_to(self.__path)

        # Divide The Parent Directory Of The File Into It's Parts To Get A Tuple Of The Directories That Need To Exist
        path_parts = tree_path.parent.parts

        # Call The Helper Func Which Will Create The Nodes Recursively From The Root Node
        return helper(self.__root, path_parts)



    def _handle_file(self, current_dir: '_MutableDirectory', file_path: Path) -> Union[None, File]:

        """
        Semi-Private method responsible for handling files, seperating my filename/extension, etc

        This function dictates a tree Builder's 'personality'

        If this method returns None, nothing will be added to the tree

        ---
        IMPLEMENTATION NOTE:

        This being the base class for abstract directory trees, every file here is treated equally
        (with the exception of directory.info files)
        """

        if file_path.name == "dir.info":
            # Add Metadata To Directory (returns None)
            return self._add_dir_info(current_dir, file_path)

        # In Any Other Case, Assume It's A File
        file_fac = FileFactory(file_path)
        return file_fac.build()



    def _add_dir_info(self, dir: '_MutableDirectory', file_path: Path) -> None:

        """
        ### REQUIRES LOGGING OF SOME KIND FOR YAML ERRORS ###
        """

        # Open File For Reading
        raw_dir_info = file_path.open('r', encoding='utf-8')

        try:

            dir_info = yaml.safe_load(raw_dir_info)
            dir.meta.update(dir_info)

        except yaml.YAMLError as e:

            # !!!! REPLACE WITH PROPER LOGGING !!!!
            logger.error(f"ERROR: COULD NOT PARSE YAML DIR INFO FOR '{file_path.as_posix()}'...Skipping...")
        


    def _create_immutable_tree(self) -> 'Directory':

        """
        Private method responsible for creating the Immutable Directory Tree using the Mutable Version.

        Returns the root node of the resulting tree.


        NOTE:

        The implementation of the Immutable Directory Tree is inside 'directory.py' module in webgoose.structs.tree
        (all nodes wield the same amount of power, so no special tree class)

        This method may be overridden by subclasses to enable special types of directory nodes (see 'abs_data_dir_Builder.py')
        """

        pass