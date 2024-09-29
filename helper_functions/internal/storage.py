import os

def read_from_storage_file(file_name: str, directories: list[str]):
    """
    Read the content of a file from the storage directory
    @param file_name: name of the file
    @param directories: list of directories to search for the file
    @return: content of the file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../'))
    if len(directories) == 0:
        directories = ['']
    for directory in directories:
        file_path = os.path.join(project_root, 'storage', directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read()
    return None