import sys
import json
try:
    import easywebdav
except ImportError:
    print("The 'easywebdav' module is not installed, do so by issuing 'pip install easywebdav'")
    sys.exit()

class Uploader:
    def __init__(self, hostname, username, password, protocol, path, verify_ssl):
            self.connection = easywebdav.connect( hostname,
                                     username   = username,
                                     password   = password,
                                     protocol   = protocol,
                                     path       = path,
                                     verify_ssl = verify_ssl)
    def mkdir(self, dir):
        print("Creating directory {}".format(str(dir)))
        self.connection.mkdir(str(dir))
    def upload(self, local, remote):
        print("Uploading file {} to \n               {}".format(str(local), str(remote)))
        self.connection.upload(str(local), str(remote))