import os
from configparser import ConfigParser

#C:\Users\Adam\OneDrive\Documents\Programs\Test Folder
#Gets the directory from the user and extracts all files and folders from it
def get_directories():
    while True:
        dir = input("Input the path for the file to sort: ")
        if not os.path.isdir(dir):
            print("This folder path does not exist")
        else:
            if not os.listdir(dir):
                print("This folder is empty")
            else:
                break


    dir_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    dir_folders = [f for f in os.listdir(dir) if not os.path.isfile(os.path.join(dir, f))]
    return dir, dir_files, dir_folders

def load_configs():
    config = ConfigParser()
    config.read("config.ini")
    filetypes = {}
    for filetype, extensions in config["FILETYPES"].items():
        filetypes[filetype] = [extension.strip() for extension in extensions.split(",")]
    return filetypes


def main():
    folders = load_configs()
    dir, dir_files, dir_folders = get_directories()



if __name__ == "__main__":
    main()