import urllib.request
import zipfile

def download_and_unzip_from_url(url, folder):
    filehandle, _ = urllib.request.urlretrieve(url)
    zip_file_object = zipfile.ZipFile(filehandle, 'r')
    for file_name in zip_file_object.namelist()[1:]:
        file = zip_file_object.open(file_name)
        content = file.read()
        with open(f"../{file_name}", mode="wb") as f:
            f.write(content)
