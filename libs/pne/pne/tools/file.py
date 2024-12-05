import os
import shutil
from typing import Callable, List, Literal, Optional

from pne.tools.base import ToolKit


class FileToolKit(ToolKit):
    Mode = Literal["read", "write", "delete", "list", "copy", "move"]

    def __init__(self, root_dir: str = "./", modes: Optional[List[Mode]] = None):
        super().__init__()

        mapper: dict[FileToolKit.Mode, Callable] = {
            "read": self.read_file,
            "write": self.write_file,
            "delete": self.delete_file,
            "list": self.list_files,
            "copy": self.copy_file,
            "move": self.move_file,
        }

        self.root_dir: str = root_dir
        self.modes: List[FileToolKit.Mode] = modes or list(mapper.keys())

        for mode in self.modes:
            if mode in mapper:
                self.register(mapper[mode])
            else:
                raise ValueError(f"Unsupported mode: {mode}")

    def read_file(self, file_name: str) -> str:
        """Reads the content of a file.

        Args:
            file_name (str): The name of the file to read.

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = os.path.join(self.root_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_name}")

        with open(file_path, "r") as file:
            return file.read()

    def write_file(self, file_name: str, content: str) -> str:
        """Writes content to a file.

        Args:
            file_name (str): The name of the file to write to.
            content (str): The content to write to the file.

        Returns:
            str: A success message.
        """
        file_path = os.path.join(self.root_dir, file_name)

        with open(file_path, "w") as file:
            file.write(content)

        return f"File written successfully: {file_name}"

    def delete_file(self, file_name: str) -> str:
        """Deletes a file.

        Args:
            file_name (str): The name of the file to delete.

        Returns:
            str: A success message.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        file_path = os.path.join(self.root_dir, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_name}")

        os.remove(file_path)

        return f"File deleted successfully: {file_name}"

    def list_files(self) -> List[str]:
        """Lists all files in the root directory.

        Returns:
            List[str]: A list of file names in the root directory.
        """
        return [
            f
            for f in os.listdir(self.root_dir)
            if os.path.isfile(os.path.join(self.root_dir, f))
        ]

    def copy_file(self, file_name: str, destination_path: str) -> str:
        """Copies a file to the specified destination.

        Args:
            file_name (str): The name of the file to copy.
            destination_path (str): The destination path.

        Returns:
            str: A success message.

        Raises:
            FileNotFoundError: If the source file does not exist.
        """
        source_path = os.path.join(self.root_dir, file_name)
        destination_path = os.path.join(self.root_dir, destination_path)

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File not found: {file_name}")

        shutil.copy2(source_path, destination_path)

        return f"File copied successfully to {destination_path}"

    def move_file(self, file_name: str, destination_path: str) -> str:
        """Moves a file to the specified destination.

        Args:
            file_name (str): The name of the file to move.
            destination_path (str): The destination path.

        Returns:
            str: A success message.

        Raises:
            FileNotFoundError: If the source file does not exist.
        """
        source_path = os.path.join(self.root_dir, file_name)
        destination_path = os.path.join(self.root_dir, destination_path)

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File not found: {file_name}")

        shutil.move(source_path, destination_path)

        return f"File moved successfully to {destination_path}"
