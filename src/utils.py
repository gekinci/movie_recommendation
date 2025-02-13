import urllib.request
import zipfile
import yaml, os


def get_full_path(root, file):
    return f"{root}{file}"


def download_and_unzip_from_url(url, root_path):
    filehandle, _ = urllib.request.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, 'r')
    for file_name in zip_file_object.namelist()[1:]:
        file = zip_file_object.open(file_name)
        content = file.read()
        path = get_full_path(root_path, file_name)
        with open(path, mode="wb") as f:
            f.write(content)


def load_yml(path_to_file):
    """
    Load a YAML file from the specified path.

    Args:
        path_to_file (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    with open(path_to_file) as f:
        file = yaml.safe_load(f)
    return file


def save_to_yml(data, name, save_path=''):
    """
    Save data to a YAML file at the specified path.

    Args:
        data (dict): Data to be saved.
        name (str): Name of the YAML file.
        save_path (str, optional): Directory path to save the file. Defaults to ''.

    Returns:
        str: Path to the saved YAML file.
    """
    data_path = os.path.join(save_path, name)
    with open(data_path, 'w') as f:
        yaml.safe_dump(data, f)
    return data_path