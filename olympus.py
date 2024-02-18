import aiohttp
import asyncio
import os
import re
from datetime import datetime
import argparse
from colorama import Fore, Style, init
import sys

init(autoreset=True)

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

if args.new:
    file_names = [file_name for file_name in file_names if file_name not in downloaded_files]

download_progress = {}
start_time = datetime.now()
download_progress = {}
start_time = datetime.now()
async def download_file(session, file_name, index, total):
    destination_path = os.path.join(destination_folder, file_name)
    if args.new and file_name in downloaded_files:
        download_progress[file_name] = (1, 1)
        return

    url = f"{base_url}{file_name}"
    async with session.get(url) as response:
        if response.status == 200:
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            with open(destination_path, 'wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    download_progress[file_name] = (downloaded_size, total_size_in_bytes)
            with open(downloaded_files_log, 'a') as log_file:
                log_file.write(f"{file_name}\n")

async def print_progress(total_files):
    while len(download_progress) < total_files or not all(progress == total for progress, total in download_progress.values()):
        downloaded_files = sum(1 for progress, total in download_progress.values() if progress == total)
        elapsed_time = datetime.now() - start_time
        formatted_time = str(elapsed_time).split('.')[0]
        sys.stdout.write(f"\r{Fore.GREEN}Downloaded {Fore.RED}{downloaded_files}{Fore.GREEN}/{Fore.CYAN}{total_files} {Fore.GREEN}files. " +
                         f"{Fore.YELLOW}Elapsed time: {formatted_time}")
        sys.stdout.flush()
        await asyncio.sleep(1)
    print()

async def main():
    if not file_names:
        print(f"{Fore.YELLOW}No new files to download. Exiting.")
        return

    connector = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession(connector=connector) as session:
        download_tasks = [download_file(session, file_name, index, len(file_names)) for index, file_name in enumerate(file_names)]
        progress_task = print_progress(len(file_names))
        await asyncio.gather(*download_tasks, progress_task)
    
    total_time = datetime.now() - start_time
    formatted_total_time = str(total_time).split('.')[0]
    print(f"{Fore.CYAN}{len(file_names)} files downloaded in {formatted_total_time}.")

if __name__ == "__main__":
    asyncio.run(main())

