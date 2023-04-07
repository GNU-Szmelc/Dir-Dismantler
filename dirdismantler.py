import os
import shutil
import yaml

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def move_files(source_path, target_path, log_file):
    log('Moving files...', log_file)
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_path, file)
            if os.path.exists(target_file_path):
                # If file already exists, append a numerical suffix
                i = 1
                while True:
                    new_file_name = f"log-{i}.txt"
                    new_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', new_file_name)
                    if not os.path.exists(new_log_file):
                        log_file = new_file_name
                        break
                    i += 1
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            shutil.move(file_path, target_file_path)
            log(f"Moved file: {file_path} -> {target_file_path}", log_file)

def remove_empty_folders(source_path, log_file):
    log('Removing empty folders...', log_file)
    for root, dirs, files in os.walk(source_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                log(f"Removed empty folder: {dir_path}", log_file)

def log(message, log_file):
    log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_path = os.path.join(log_folder, log_file)
    with open(log_file_path, 'a') as f:
        f.write(message + '\n')
    print(message)

if __name__ == '__main__':
    config_file = 'config.yml'
    config = load_config(config_file)
    source_path = config['source_path']
    target_path = config['target_path']
    log_file = 'log.txt'
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', log_file)):
        i = 1
        while True:
            new_file_name = f"log-{i}.txt"
            new_log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', new_file_name)
            if not os.path.exists(new_log_file):
                log_file = new_file_name
                break
            i += 1

    if not os.path.exists(source_path):
        log(f"Source path '{source_path}' does not exist. Exiting...", log_file)
        exit(1)

    if not os.path.exists(target_path):
        log(f"Target path '{target_path}' does not exist. Creating directory...", log_file)
        os.makedirs(target_path)

    move_files(source_path, target_path, log_file)

    remove_empty_folders(source_path, log_file)

    print('Files moved successfully!')
