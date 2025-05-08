import os
from .workspace import get_workspace_path
from pathlib import Path


class Address:
    def __init__(
        self, 
        page: str, 
        relativePath: str, 
        workspaceName:str=None, 
        uuid:str=None,
        ip:str=None
    ):
        if workspaceName == '':
            workspaceName = None
        if uuid == '':
            uuid = None
        if ip == '':
            ip = None   
        self.page = page
        self.relativePath = relativePath
        self.workspaceName = workspaceName
        self.uuid = uuid
        self.ip = ip
        
    def is_fs(self):
        return self.workspaceName is not None
    
    def to_fs_path(self, is_local=True):
        if not is_local:
            raise Exception("Remote address is not supported")
        if self.workspaceName is None:
            return Path(self.relativePath).as_posix()

        workspace_path = get_workspace_path(self.workspaceName)
        if workspace_path is None :
            raise Exception("Workspace not found: " + self.workspaceName)
        
        fs_path = os.path.join(workspace_path, "User", "Local", self.page, self.relativePath)
        return Path(fs_path).as_posix()
    
    