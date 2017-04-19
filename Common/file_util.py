import os
import re


def get_file_list(path):
    """Return file list with absolute path in a given path    
    :param path: 
    :return: file list with absolute path
    """
    current_files = os.listdir(path)
    all_files = []
    for file_name in current_files:
        full_file_name = os.path.join(path, file_name)
        all_files.append(full_file_name)

        if os.path.isdir(full_file_name):
            next_level_files = get_file_list(full_file_name)
            all_files.extend(next_level_files)
    return all_files

def get_file_list_with_filter(path,expression):
    """
    Return file list in a given path and given expression
    :param path: 
    :param expression: file name expression
    :return: absolute path file name list
    """
    re_file_name = re.compile(expression)
    filtered_files = []
    all_files = get_file_list(path)
    for f in all_files:
        #print("f = ", f)
        if re_file_name.match(f) is not None:
            filtered_files.append(f)
    return filtered_files

