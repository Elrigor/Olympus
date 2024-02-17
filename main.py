import requests
import os
import re

bin_file_path = './LatestFileList.bin'
destination_folder = './wads'
base_url = 'http://versionec-es.eu.wizard101.com/WizPatcher/V_r747324.Wizard_1_490/LatestBuild/Data/GameData/'

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

def download_file(file_name):
    url = f"{base_url}{file_name}"
    destination_path = os.path.join(destination_folder, file_name)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Descargado: {file_name}")
    else:
        print(f"Error al descargar {file_name}: Estado HTTP {response.status_code}")

with open(bin_file_path, 'rb') as file:
    bin_content = file.read()

content_str = bin_content.decode('latin-1', 'ignore')

pattern = re.compile(r'Data/GameData/[^/]+?\.wad')
matches = pattern.findall(content_str)

for match in matches:
    file_name = match.split('/')[-1]
    if file_name:
        download_file(file_name)

print("Proceso de descarga completado.")
