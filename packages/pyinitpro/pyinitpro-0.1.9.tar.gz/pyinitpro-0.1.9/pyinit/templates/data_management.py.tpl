import json
from email.policy import default
from pathlib import Path
from typing import Dict, Any, Union, List, Optional, TypeVar

import yaml

T = TypeVar("T")


class TestDataManager:
    """
    Manages test utils by saving and loading from files in different formats.

    Supports operations on JSON and YAML files with flexible directory management.

    Attributes:
        base_dir (Path): Base directory for storing test utils files
    """

    def __init__(self, base_dir: Union[str, Path] = "./test_data"):
        """
        Initialize TestDataManager with a base directory for test utils.

        Args:
            base_dir (str or Path, optional): Directory to store test utils files.
                Defaults to "./test_data"
        """
        project_root_dir = Path.cwd().resolve()
        while (
            not (project_root_dir / ".git").exists()
            and project_root_dir != project_root_dir.parent
        ):
            project_root_dir = project_root_dir.parent
        self.base_dir = project_root_dir / base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, filename: str, extension: str) -> Path:
        """
        Generate full file path, handling both absolute and relative paths.

        Args:
            filename (str): Name of the file (without extension)
            extension (str): File extension (e.g., 'json', 'yaml')

        Returns:
            Path: Resolved absolute file path
        """
        if Path(filename).is_absolute():
            base = Path(filename).parent
            name = Path(filename).stem
        else:
            base = self.base_dir
            name = filename

        return base / f"{name}.{extension}"

    def save_json(self, data: T, filename: str) -> str:
        """
        Save utils as a JSON file in the base directory.

        Args:
            data (Dict[str, Any]): Data to be saved
            filename (str): Name of the file (without .json extension)

        Returns:
            str: Full path of the saved file
        """
        file_path = self._get_file_path(filename, "json")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return str(file_path)
        except (OSError, TypeError, ValueError) as e:
            raise IOError(f"Error while saving JSON file {file_path}: {str(e)}")

    def load_json(self, filename: str) -> T:
        """
        Load utils from a JSON file in the base directory.

        Args:
            filename (str): Name of the file (without .json extension)

        Returns:
            Dict[str, Any]: Loaded JSON utils

        Raises:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file is not a valid JSON
        """
        file_path = self._get_file_path(filename, "json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            if default is not None:
                self.save_json(default, filename)
                return default
            raise
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file {file_path}: {str(e)}")

    def save_yaml(self, data: Dict[str, Any], filename: str) -> str:
        """
        Save utils as a YAML file in the base directory.

        Args:
            data (Dict[str, Any]): Data to be saved
            filename (str): Name of the file (without .yaml extension)

        Returns:
            str: Full path of the saved file
        """
        file_path = self._get_file_path(filename, "yaml")
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
        return str(file_path)

    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """
        Load utils from a YAML file in the base directory.

        Args:
            filename (str): Name of the file (without .yaml extension)

        Returns:
            Dict[str, Any]: Loaded YAML utils

        Raises:
            FileNotFoundError: If the file does not exist
            yaml.YAMLError: If the file is not a valid YAML
        """
        file_path = self._get_file_path(filename, "yaml")
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def list_files(self, extension: Optional[str] = None) -> List[str]:
        """
        List files in the base directory, optionally filtered by extension.

        Args:
            extension (str, optional): File extension to filter by
                (e.g., 'json', 'yaml'). If None, lists all files.

        Returns:
            List[str]: List of filenames matching the criteria
        """
        if extension:
            return [f.stem for f in self.base_dir.glob(f"*.{extension}")]
        return [f.stem for f in self.base_dir.glob("*")]

    def delete_file(self, filename: str, extension: str) -> bool:
        """
        Delete a file from the base directory.

        Args:
            filename (str): Name of the file (without extension)
            extension (str): File extension

        Returns:
            bool: True if file was successfully deleted, False if file not found
        """
        file_path = self._get_file_path(filename, extension)
        try:
            file_path.unlink()
            return True
        except FileNotFoundError:
            return False

    def save_data(
        self, data: Dict[str, Any], filename: str, file_type: str = "json"
    ) -> str:
        """
        Save utils to a file with flexible file type selection.

        Args:
            data (Dict[str, Any]): Data to be saved
            filename (str): Name of the file (without extension)
            file_type (str, optional): File type to save. Defaults to 'json'

        Returns:
            str: Full path of the saved file

        Raises:
            ValueError: If an unsupported file type is provided
        """
        if file_type.lower() == "json":
            return self.save_json(data, filename)
        elif file_type.lower() in ["yml", "yaml"]:
            return self.save_yaml(data, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")