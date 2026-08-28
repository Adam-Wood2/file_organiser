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


#parses the config file to get the types of files and their matching file extensions. Returns a dictionary with this info.
def load_configs():
    config = ConfigParser()
    config.read("config.ini")
    filetypes = {}
    for filetype, extensions in config["FILETYPES"].items():
        filetypes[filetype] = [extension.strip() for extension in extensions.split(",")]
    return filetypes


def get_file_extension(file):
    return "." + file.split(".")[-1]

#Sorts all the files into a dictionary where they are paired with their repsective file type. All files of the same type will be stored in a list.
def get_file_info(dir_files, folders_config):
    sorted_files = {}
    for file in dir_files:
        file_extension = get_file_extension(file)
        for filetype, extensions in folders_config.items():
            if file_extension in extensions:
                if filetype in sorted_files:
                    print(file)
                    sorted_files[filetype] += [file]
                else:
                    sorted_files[filetype] = [file]

    return sorted_files

def main():
    folders_config = load_configs()
    dir, dir_files, dir_folders = get_directories()
    print(dir)
    print(dir_files)
    print(dir_folders)
    print(folders_config)
    print(get_file_info(dir_files, folders_config))
    #print(get_file_extension("text.txt"))



if __name__ == "__main__":
    main()