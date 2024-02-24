import os
import shutil

from promptulate.tools.base import Tool

class WriteFileTool(Tool):
    name: str = "write-file"
    description: str = (
        "Write to a file"
        "Useful when you need to edit/create edit a file."
        "It can edit the specified file in the specified directory/local directory"
        "If the file does not exist, edit it after it is created."
        "The output parameters must be: file_name(file name), text(related information)."
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str, text: str) -> str:
        """Write to a file

        Args:
            query: file_name and text.
            file_name(Optional(str)): The name of the file you want to edit.
            text(Optional(str)): The content you want to edit.
        
        Returns:
            str: Write file successfully
        """
        with open(f"{self.root_dir}/{file_name}", "w") as file:
            file.write(text)
        return "Write file successfully"

class AppendFileTool(Tool):
    name: str = "append-file"
    description: str = (
        "Append to a file"
        "Useful when you need to edit/create edit a file."
        "It can edit the specified file in the specified directory/local directory,"
        "Append the content to the end of the file."
        "If the file does not exist, edit it after it is created."
        "The output parameters must be: file_name(file name), text(related information)."
    )
    
    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str, text: str) -> str:
        """Append to a file

        Args:
            query: file_name and text.
            file_name(Optional(str)): The name of the file you want to edit.
            text(Optional(str)): The content you want to edit.
        
        Returns:
            str: Append file successfully
        """
        with open(f"{self.root_dir}/{file_name}", "a") as file:
            file.write(text)
        return "Append file successfully"

class ReadFileTool(Tool):
    name: str = "read-file"
    description: str = (
        "Read a file"
        "Useful when you need to read a file."
        "It can read the specified file in the specified directory/local directory."
        "The output parameters must be: file_name(file name)."
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str) -> str:
        """Read a file
        
        Args:
            query: file_name.
            file_name(Optional(str)): The name of the file you want to read.
        
        Returns:
            str: The contents of the file.
        """
        with open(f"{self.root_dir}/{file_name}", "r") as file:
            return file.read()

class DeleteFileTool(Tool):
    name: str = "delete-file"
    description: str = (
        "Delete a file"
        "Useful when you need to delete a file."
        "It can delete the specified file in the specified directory/local directory."
        "The output parameters must be: file_name(file name)."
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str) -> str:
        """Delete a file
        
        Args:
            query: file_name.
            file_name(Optional(str)): The name of the file you want to delete.

        Returns:
            str: Delete file successfully
        """
        os.remove(f"{self.root_dir}/{file_name}")
        return "Delete file successfully"
    
class ListDirectoryTool(Tool):
    name: str = "list-directory"
    description: str = (
        "List directory"
        "Useful when you need to list all files in the directory."
        "It can list all files in the specified directory/local directory."
        "The output parameters is None."
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self) -> str:
        """List directory
        
        Args:
            query: None.
        
        Returns:
            str: All files in the current path(Separated by newlines)
        """
        entries = os.listdir(self.root_dir)
        return "\n".join(entries)

class CopyFileTool(Tool):
    name: str = "copy-file"
    description: str = (
        "Copy a file"
        "Useful when you need to copy a file."
        "It can copy the specified file in the specified directory/local directory."
        "The output parameters must be: file_name(file name),destination_path(destination path)."
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str,destination_path:str) -> str:
        """Copy a file

        Args:
            query: file_name.
            file_name(Optional(str)): The name of the file you want to copy.
            destination_path(Optional(str)): The path you want to copy the file to.
            
        Returns:
            str: Copy file successfully
        """
        shutil.copy(f"{self.root_dir}/{file_name}", f"{destination_path}/{file_name}.copy")
        return "Copy file successfully"

class MoveFileTool(Tool):
    name: str = "move-file"
    description: str = (
        "Move a file"
        "Useful when you need to move a file."
        "It can move or rename the specified file in the specified directory/local directory."
        "The output parameters must be: file_name(file name),destination_path(destination path)"
    )

    def __init__(self, root_dir: str) -> None:
        self.root_dir = root_dir
    def _run(self, file_name: str,destination_path:str) -> str:
        """Move a file
        
        Args:
            query: file_name and destination_path.
            file_name(Optional(str)): The name of the file you want to move.
            destination_path(Optional(str)): The path you want to move the file to.
        
        Returns:
            str: Move file successfully
        """
        shutil.move(f"{self.root_dir}/{file_name}", f"{destination_path}/{file_name}")
        return "Move file successfully"
