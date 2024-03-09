import os
import shutil
from typing import Optional

from promptulate.pydantic_v1 import BaseModel, Field
from promptulate.tools.base import Tool


class RToolParameters(BaseModel):
    file_name: str = Field(
        description="The name of the file you want to edit.",
    )


class ToolParameters(RToolParameters):
    text: Optional[str] = Field(
        default=None,
        description="The content you want to edit.",
    )


class CMToolParameters(RToolParameters):
    destination_path: str = Field(
        description="The directory you want to reach.",
    )


class WriteFileTool(Tool):
    name: str = "write-file"
    description: str = (
        "Write to a file"
        "Useful when you need to edit/create and edit a file."
        "It can edit the specified file in the specified directory/local directory"
        "If the file does not exist, edit it after it is created."
    )
    parameters = ToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str, text: Optional[str] = None) -> str:
        """Write to a file

        Args:
            file_name(Optional(str)): The name of the file you want to edit.
            text(Optional(str)): The content you want to edit.

        Returns:
            str: Write file successfully
        """
        try:
            with open(f"{self.root_dir}/{file_name}", "w") as file:
                file.write(text)
        except IOError:
            return "An error occurred while trying to write to the file."
        except PermissionError:
            return "Permission denied: You don't have permission to write to this file."
        return "Write file successfully"


class AppendFileTool(Tool):
    name: str = "append-file"
    description: str = (
        "Append to a file"
        "Useful when you need to edit/create edit a file."
        "It can edit the specified file in the specified directory/local directory,"
        "Append the content to the end of the file."
        "If the file does not exist, edit it after it is created"
    )
    parameters = ToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str, text: Optional[str] = None) -> str:
        """Append to a file

        Args:
            file_name(Optional(str)): The name of the file you want to edit.
            text(Optional(str)): The content you want to edit.

        Returns:
            str: Append file successfully
        """
        try:
            with open(f"{self.root_dir}/{file_name}", "a") as file:
                file.write(text)
        except IOError:
            return "An error occurred while trying to write to the file."
        except PermissionError:
            return "Permission denied: You don't have permission to write to this file."
        return "Append file successfully"


class ReadFileTool(Tool):
    name: str = "read-file"
    description: str = (
        "Read a file"
        "Useful when you need to read a file."
        "It can read the specified file in the specified directory/local directory."
    )
    parameters = RToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str) -> str:
        """Read a file

        Args:
            file_name(Optional(str)): The name of the file you want to read.

        Returns:
            str: The contents of the file.
        """
        try:
            with open(f"{self.root_dir}/{file_name}", "r") as file:
                return file.read()
        except FileNotFoundError:
            return "File not found: The file you are trying to read does not exist."
        except PermissionError:
            return "Permission denied: You don't have permission to read this file."
        except UnicodeDecodeError:
            return (
                "Unicode decode error:"
                "The file could not be decoded with utf-8 encoding."
            )
        except IOError:
            return "An error occurred while trying to read the file."


class DeleteFileTool(Tool):
    name: str = "delete-file"
    description: str = (
        "Delete a file"
        "Useful when you need to delete a file."
        "It can delete the specified file in the specified directory/local directory."
    )
    parameters = RToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str) -> str:
        """Delete a file

        Args:
            file_name(Optional(str)): The name of the file you want to delete.

        Returns:
            str: Delete file successfully
        """
        try:
            os.remove(f"{self.root_dir}/{file_name}")
        except FileNotFoundError:
            return "File not found: The file you are trying to read does not exist."
        except PermissionError:
            return "Permission denied: You don't have permission to read this file."
        except IOError:
            return "An error occurred while trying to delete the file."
        return "Delete file successfully"


class ListDirectoryTool(Tool):
    name: str = "list-directory"
    description: str = (
        "List directory"
        "Useful when you need to list all files in the directory."
        "It can list all files in the specified directory/local directory."
    )
    parameters = None

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self) -> str:
        """List directory

        Args:
            None

        Returns:
            str: All files in the current path(Separated by newlines)
        """
        try:
            entries = os.listdir(self.root_dir)
        except PermissionError:
            return "Permission denied: You don't have permission to read this file."
        return "\n".join(entries)


class CopyFileTool(Tool):
    name: str = "copy-file"
    description: str = (
        "Copy a file"
        "Useful when you need to copy a file."
        "It can copy the specified file in the specified directory/local directory."
    )
    parameters = CMToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str, destination_path: str) -> str:
        """Copy a file

        Args:
            file_name(Optional(str)): The name of the file you want to copy.
            destination_path(Optional(str)): The path you want to copy the file to.

        Returns:
            str: Copy file successfully
        """
        try:
            shutil.copy(
                f"{self.root_dir}/{file_name}", f"{destination_path}/{file_name}"
            )
        except FileNotFoundError:
            return "File not found: The file you are trying to read does not exist."
        except PermissionError:
            return "Permission denied: You don't have permission to read this file."
        except IOError:
            return "An error occurred while trying to copy the file."
        return "Copy file successfully"


class MoveFileTool(Tool):
    name: str = "move-file"
    description: str = (
        "Move a file"
        "Useful when you need to move a file."
        "It can move or rename the specified file \
        in the specified directory/local directory."
    )
    parameters = CMToolParameters

    def __init__(self, root_dir: str, *args, **kwargs) -> None:
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def _run(self, file_name: str, destination_path: str) -> str:
        """Move a file

        Args:
            file_name(Optional(str)): The name of the file you want to move.
            destination_path(Optional(str)): The path you want to move the file to.

        Returns:
            str: Move file successfully
        """
        try:
            shutil.move(
                f"{self.root_dir}/{file_name}", f"{destination_path}/{file_name}"
            )
        except FileNotFoundError:
            return "File not found: The file you are trying to read does not exist."
        except PermissionError:
            return "Permission denied: You don't have permission to read this file."
        except IOError:
            return "An error occurred while trying to move the file."
        return "Move file successfully"
