import os
from .workspace import get_workspace_path
from pathlib import Path


class Address:
    def __init__(
        self, 
        page: str, 
        relative_path: str, 
        workspace_name:str=None, 
        uuid:str=None,
        ip:str=None
    ):
        if workspace_name == '':
            workspace_name = None
        if uuid == '':
            uuid = None
        if ip == '':
            ip = None   
        self.page = page
        self.relative_path = relative_path
        self.workspace_name = workspace_name
        self.uuid = uuid
        self.ip = ip

    
    def to_fs_path(self, is_local=True):
        if not is_local:
            raise Exception("Remote address is not supported")
        if self.workspace_name is None:
            return Path(self.relative_path).as_posix()

        workspace_path = get_workspace_path(self.workspace_name)
        if workspace_path is None :
            raise Exception("Workspace not found: " + self.workspace_name)
        
        fs_path = os.path.join(workspace_path, "User", "Local", self.page, self.relative_path)
        return Path(fs_path).as_posix()
    
    
    
def from_js_dict(js_dict):
    return Address(
        page=js_dict["page"],
        relative_path=js_dict["relativePath"],
        workspace_name=js_dict.get("workspaceName"),
        uuid=js_dict.get("uuid"),
        ip=js_dict.get("ip")
    )