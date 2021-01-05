import os
from dash_core_components import Checklist
def get_folder_checks(basePath= "/Users/jackkelly/PycharmProjects/win_break/frames_folder"):

    folder_ls = os.listdir(basePath)
    folder_options = []
    for folder in folder_ls:
        #num = len(os.listdir(folder))
        item = {'label': folder, 'value': folder},
        folder_options.append(item)

    folder_checks =Checklist(id = "folder-checks",
        options=[{'label': folder, 'value': str(basePath + '/' + folder)}
                 for folder in folder_ls],
        labelStyle = dict(display='block')
    )
    return folder_checks