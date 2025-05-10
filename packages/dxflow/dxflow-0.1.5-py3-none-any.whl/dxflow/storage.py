import requests
import json
import datetime
import os
import base64

from .config import NAMESPACE_API_URL
from .utils.file_utils import list_files

class StorageManager:
    """
    Class for managing storage operations.

    Args:
        user_pointer (str): User pointer.
        user_secret (str): User secret.
        unit_secret (str): Unit secret.
        dxflow_url (str): DXFlow URL.
        provider (str): Storage provider (default: "AWS").
    """
    def __init__(self, user_pointer=None, user_secret=None, unit_secret=None, dxflow_url=None, provider="AWS"):
        pass
class UnitStorage:
    """
    Class for managing unit storage operations.

    Args:
        user_pointer (str): User pointer.
        user_secret (str): User secret.
        unit_secret (str): Unit secret.
        dxflow_url (str): DXFlow URL.
        provider (str): Storage provider (default: "AWS").
    """
    def __init__(self, user_pointer=None, user_secret=None, unit_secret=None, dxflow_url=None, provider="AWS"):
        self.provider = provider
        self.user_pointer = user_pointer
        self.user_secret = user_secret
        self.dxflow_url = dxflow_url
        self.content = {}
        self._unit_secret = unit_secret

    def list(self, path="/", recursive=False):
        """
        List storage items at the specified path.

        Args:
            path (str): Path to list contents of (default: "/").
            recursive (bool): List recursively if True (default: False).

        Returns:
            dict: List of storage items.
        """
        url = f"{self.dxflow_url}/storage/items/"
        headers = {"X-SECRET-KEY": self._unit_secret}
        params = {"path": path, "recursive": str(recursive).lower()}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            items = response.json()
            for item in items:
                item_type = "d" if item["directory"] else "-"
                size = item["size"]
                modification_time = datetime.datetime.fromtimestamp(item["modification"]).strftime("%Y-%m-%d %H:%M:%S")
                name = item["name"]
                print(f"{item_type} {size:>10} {modification_time} {name}")
            return items
        else:
            raise Exception(f"Failed to list items: {response.status_code}, {response.text}")
    def ls(self, path="/", recursive=False):
        """
            Alias for the list() function.
        """
        return self.list(path, recursive)
    def _b64(self, s: str) -> str:
        return base64.b64encode(s.encode("utf-8")).decode("ascii")

    def upload(self, src, dst):
        """
        Upload a file to the storage.

        Args:
            src (str): Source file path.
            dst (str): Destination path in the storage.
        """
        filename = os.path.basename(src)
        url = f"{self.dxflow_url}/storage/upload/"
        headers = {
            "X-SECRET-KEY": self._unit_secret,
            "Tus-Resumable": "1.0.0",
            "Upload-Length": str(os.path.getsize(src)),
            "Upload-Metadata":
                f"path {self._b64(dst)},"
                f"name {self._b64(filename)}",
        }
        
        if not os.path.exists(src):
            raise FileNotFoundError(f"Source file '{src}' does not exist.")
        
        with open(src, "rb") as file:
            response = requests.post(url, headers=headers, data=file)
            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to upload file: {response.status_code}, {response.text}")
        print(response.text)
        return response.text
    
    def download(self, src, dst):
        """
        Download a file from the storage.

        Args:
            src (str): Source path in the storage.
            dst (str): Destination file path.
        """
        url = f"{self.dxflow_url}/storage/download/"
        headers = {"X-SECRET-KEY": self._unit_secret}
        params = {"path": src}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            filename = os.path.basename(src)
            if not dst.endswith(filename):
                dst = os.path.join(dst, filename)
            with open(dst, "wb") as file:
                file.write(response.content)
        else:
            raise Exception(f"Failed to download file: {response.status_code}, {response.text}")

    def mkdir(self, path):
        """
        Create a directory in the storage.

        Args:
            path (str): Path of the directory to create.
        """
        # Use the upload function to create a folder by uploading an empty file named '.dx'
        temp_file_name = ".dx"
        empty_file_path = os.path.join(os.getcwd(), temp_file_name)
        try:
            # Create an empty file locally
            with open(empty_file_path, "wb") as empty_file:
                pass
            
            # Upload the empty file to the specified path
            upload_respose = self.upload(empty_file_path, path)
        finally:
            # Clean up the local empty file
            if os.path.exists(empty_file_path):
                os.remove(empty_file_path)
            temp_upload_path = os.path.join(path, temp_file_name).replace("\\", "/")
            # Delete the empty file from the storage
            print(temp_upload_path)
            self.delete(temp_upload_path)
        return upload_respose
    
    def delete(self, path):
        """
        Delete a file or directory from the storage.

        Args:
            path (str): Path of the file or directory to delete.
        """
        url = f"{self.dxflow_url}/storage/items/"
        headers = {"X-SECRET-KEY": self._unit_secret}
        params = {"path": path}

        response = requests.delete(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to delete item: {response.status_code}, {response.text}")

    def copy(self, src, dst):
        """
        Copy a file or directory within the storage.

        Args:
            src (str): Source path.
            dst (str): Destination path.
        """
        url = f"{self.dxflow_url}/storage/transfer/"
        headers = {"X-SECRET-KEY": self._unit_secret}
        params = {"path": src, "destination": dst}

        response = requests.put(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to copy item: {response.status_code}, {response.text}")

    def move(self, src, dst):
        """
        Move a file or directory within the storage.

        Args:
            src (str): Source path.
            dst (str): Destination path.
        """
        self.copy(src, dst)
        self.delete(src)
