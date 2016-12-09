#!/usr/bin/python3
from core.connection import Uploader
from core.walker import WalkerUploader
from core.walker import Uploader as Printer
from time import time
from pathlib import Path, PurePosixPath
import json
import os



def main():
    parent_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(parent_path, "config/conf.json")
    
    with open(config_path, "r") as conf_file:
        conf = json.load(conf_file)
    connection = conf["connection"]
    
    uploader = Uploader(hostname   = connection["hostname"],
                        username   = connection["username"],
                        password   = connection["password"],
                        protocol   = connection["protocol"],
                        path       = connection["path"],
                        verify_ssl = connection["verify_ssl"])
    
    remote_path = PurePosixPath(connection["path_bk"]).joinpath(PurePosixPath(str(int(time()))))
    uploader.mkdir(remote_path)
    worlds = conf["worlds"]
    for world in worlds:
        local_path = Path(world["path"]).resolve()
        WalkerUploader(local_path, remote_path, uploader).walk_call()
    
if __name__ == "__main__" : main()