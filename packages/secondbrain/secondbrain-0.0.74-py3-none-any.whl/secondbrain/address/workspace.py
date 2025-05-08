from secondbrain import utils


workspace_setting = utils.read_json_file("workspace.json")

def get_workspace_path(workspace_name):
    if workspace_name is None:
        None
    all_workspace_paths = workspace_setting["allWorkspacePaths"]
    if workspace_name in all_workspace_paths:
        return all_workspace_paths[workspace_name]
    else:
        raise Exception("Workspace not found: " + workspace_name)