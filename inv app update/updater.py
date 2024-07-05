import requests
import zipfile
import shutil
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_for_updates():
    repo_owner = 'sterling5241'
    repo_name = 'inv-app-update'
    current_version = '1.0.0'  # Replace with your current version

    print("Checking for updates...")
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest')
    
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release['tag_name']
        
        if latest_version > current_version:
            download_url = latest_release['zipball_url']
            print(f"New version available: {latest_version}. Downloading update...")
            download_and_apply_update(download_url)
        else:
            print("No updates available.")
    else:
        print(f"Failed to check for updates: {response.status_code}")

def download_and_apply_update(download_url):
    response = requests.get(download_url)
    update_file_path = resource_path('update.zip')
    
    with open(update_file_path, 'wb') as file:
        file.write(response.content)
    
    print("Update downloaded. Applying update...")
    
    with zipfile.ZipFile(update_file_path, 'r') as zip_ref:
        zip_ref.extractall(resource_path('update_temp'))
    
    update_temp_path = resource_path('update_temp')
    
    for root, dirs, files in os.walk(update_temp_path):
        for file in files:
            source_file = os.path.join(root, file)
            relative_path = os.path.relpath(source_file, update_temp_path)
            destination_file = os.path.join(resource_path('.'), relative_path)
            destination_dir = os.path.dirname(destination_file)
            
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            
            shutil.move(source_file, destination_file)
    
    shutil.rmtree(update_temp_path)
    os.remove(update_file_path)
    
    print("Update installed successfully. Please restart the application.")
    sys.exit()

if __name__ == "__main__":
    check_for_updates()
