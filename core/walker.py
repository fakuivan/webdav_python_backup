import os
import re
from pathlib import Path, PurePosixPath

class RemoteToPathFormatter:
    def __init__(self, local_root, remote_root):
        """
        local_root       This Path or string should be replaced by your local root directory.
        remote_root      This PurePosixPath or string should be put instead of the local root.
        """
        self.local_root = Path(local_root)
        self.remote_root = PurePosixPath(remote_root)
    def format(self, local_directory):
        """
        local_directory  This directory will have it's local root folder swapped by the remote one.
        """
        return self.remote_root.joinpath(PurePosixPath(Path(local_directory).relative_to(self.local_root)))

class WalkerUploader:
    """
    This is used to iterate over a folder and call an uploader object to create directories and 
    subdirectories and upload files
    """
    def __init__(self, local_root, remote_root, uploader):
        """
        local_root   The local root directory to upload
        remote_root  The remote root directory to upload files to
        uploader     The uploader object, you can use a warper to make things easier
        """
        self.local_root = Path(local_root)
        self.formatter = RemoteToPathFormatter(Path(self.local_root).parent, PurePosixPath(remote_root))
        self.uploader = uploader
    def walk_call(self):
        """
        Iterates over every file in the local root folder and calls the uploader when a directory needs to be created
        or a file needs to be uploaded.
        """
        for root, dirs, files in os.walk(str(self.local_root), topdown=True):
            root_path = Path(root)
            this_remote_folder = self.formatter.format(root)
            self.uploader.mkdir(this_remote_folder)
            for name in files:
                file_local_directory  = root_path.joinpath(name)
                file_remote_directory = self.formatter.format(file_local_directory)
                self.uploader.upload(file_local_directory, file_remote_directory)

class Uploader:
    """
    This is an example warper used as the uploader object passed to WalkerUploader
    """
    def __init__(self):
        pass
    def mkdir(self, dir):
        """
        This function will be called when a new directory needs to be created
        
        dir     path of the remote directory
        """
        print("Creating directory {}".format(str(dir)))
    def upload(self, local, remote):
        """
        This function will be called when a file is ready to be uploaded, checks in the local file should be done as usual
        
        local   the path to the local file
        remote  the path where to upload the local file
        """
        print("Uploading file {} to\n               {}".format(str(local), str(remote)))
