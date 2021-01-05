def get_default_constants():
    constants = {
        "thresh": 150,
         "min_ignore": 20.0,
         "warn_size": 5000.0,
         "scale" : 1.0
    }
    return constants

def get_default_options():
    #options put in by user these are just placeholders
    options ={
        "program_type": "light",
        "input_type":0,
        "job_name": "default_name",
        "frame_paths":[],
        #"name_ls_ls": [],
        "constants": get_default_constants(),
        "tags": ["NULL(lol)"],
        }
    return options
