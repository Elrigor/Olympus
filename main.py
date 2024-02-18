import requests
import os
import re
import sys
import argparse

parser = argparse.ArgumentParser(description="Download only not previously downloaded file.")
parser.add_argument('--new', action='store_true', help="Download new files only.")
args = parser.parse_args()

bin_file_path = './LatestFileList.bin'
destination_folder = './wads'
downloaded_files_log = './downloaded_files.txt'
base_url = 'http://versionec-es.eu.wizard101.com/WizPatcher/V_r747324.Wizard_1_490/LatestBuild/Data/GameData/'

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

if os.path.exists(downloaded_files_log):
    with open(downloaded_files_log, 'r') as log_file:
        downloaded_files = set(log_file.read().splitlines())
else:
    downloaded_files = set()

with open(bin_file_path, 'rb') as file:
    bin_content = file.read()
content_str = bin_content.decode('latin-1', 'ignore')

pattern = re.compile(r'Data/GameData/[^/]+?\.wad')
matches = pattern.findall(content_str)

file_names = [match.split('/')[-1] for match in matches]

total_downloaded_bytes = 0

reset = "\033[0m"
index_color = "\033[94m"
file_color = "\033[92m"
stats_color = "\033[96m"
error_color = "\033[91m"  
downloaded_size_color = "\033[93m"
total_size_color = "\033[95m"
percentage_color = "\033[96m"

def download_file(file_name, index, total):
    global total_downloaded_bytes
    destination_path = os.path.join(destination_folder, file_name)
    
    if args.new and file_name in downloaded_files:
        try:
            file_size = os.path.getsize(destination_path)
            downloaded_mb = file_size / (1024 * 1024)
            message = f"\r{index_color}File: {index + 1}/{total}{reset} - {file_color} {file_name}{reset} "
            message += f"{downloaded_size_color}[{downloaded_mb:.2f} MB{reset}/{total_size_color}{downloaded_mb:.2f} MB{reset} "
            message += f"({percentage_color}100.00%{reset})]"
            sys.stdout.write(f"{message: <150}")
            sys.stdout.flush()
        except FileNotFoundError:
            print(f"\r{error_color}Warning: {file_name} file system not found for {reset}")
        return
    
    url = f"{base_url}{file_name}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        with open(destination_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded_size += len(chunk)
                total_downloaded_bytes += len(chunk)
                downloaded_mb = downloaded_size / (1024 * 1024)
                total_size_mb = total_size_in_bytes / (1024 * 1024)
                percentage = (downloaded_size / total_size_in_bytes) * 100
                message = f"\r{index_color}File: {index + 1}/{total}{reset} - {file_color} {file_name}{reset} "
                message += f"{downloaded_size_color}[{downloaded_mb:.2f} MB{reset}/{total_size_color}{total_size_mb:.2f} MB{reset} "
                message += f"({percentage_color}{percentage:.2f}%{reset})]"
                sys.stdout.write(f"{message: <150}")
                sys.stdout.flush()
        with open(downloaded_files_log, 'a') as log_file:
            log_file.write(f"{file_name}\n")
    else:
        message = f"\r{error_color}File: {index + 1}/{total} - 'Error': {file_name}{reset}"
        sys.stdout.write(f"{message: <150}")
        sys.stdout.flush()

total_files = len(file_names)
for index, file_name in enumerate(file_names):
    download_file(file_name, index, total_files)

total_downloaded_gb = total_downloaded_bytes / (1024 * 1024 * 1024)
print(f"\r\033[92mCompleted: Downloaded {len(file_names)} files with a total of {total_downloaded_gb:.2f} GB.\033[0m")
