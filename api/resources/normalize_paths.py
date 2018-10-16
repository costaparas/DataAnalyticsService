import os
import sys
def get_this_dir(file):
    path_of_this_script = os.path.realpath(file)
    dir_ = os.path.dirname(path_of_this_script)
    return dir_


def append_ml_dir_to_syspath(file):
    path_to_append = get_this_dir(file)
    path_to_append = os.path.join(path_to_append, "../../ml")
    path_to_append = os.path.abspath(path_to_append)
    sys.path.append(path_to_append)


