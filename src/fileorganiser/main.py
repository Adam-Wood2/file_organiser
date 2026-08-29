import os
from configparser import ConfigParser
from time import sleep

class File:
    def __init__(self, file_name, location):
        self.file_name = file_name
        self.location = location
        self.full_path = os.path.join(self.location, self.file_name)
        self.file_extension = self.__get_file_extension()
        self.file_type = self.__get_file_type()
        self.size = self.get_file_size()
        self.is_ignored = self.file_extension in ignore_lookup
        self.destination = self.get_destination()
    
    def format_size(self):
        units = ["B","KB","MB","GB"]
        unit_index = 0

        size = self.size
        while size >= 1024 and unit_index < len(units) -1:
            size /= 1024
            unit_index +=1
        return f"{size:.2f} {units[unit_index]}"

    def __get_file_extension(self):
        return "." + self.file_name.split(".")[-1]

    def __get_file_type(self):
        if self.file_extension in ignore_lookup:
            return self.file_extension
        elif self.file_extension in extension_lookup:
            return extension_lookup[self.file_extension]
        else:
            return "Other"
        
    def get_file_size(self):
        stats = os.stat(self.full_path)
        size = stats.st_size
        return size

    def get_destination(self):
        if self.file_extension in ignore_lookup:
            return "N/A"
        elif self.file_extension in extension_lookup:
            return extension_lookup[self.file_extension]
        else:
            return "Other"


def draw_progress_bar(val1, val2):

    progress = int(((val1 / val2)*100) // 2)
    progress_bar = "[" + "\u001b[47m.\u001b[0m"*progress + "."*(50-progress) + "]" + f" {val1}/{val2}"
    #return progress_bar
    if val1 != val2:
        print(progress_bar, end="\r")
    else:
        print(progress_bar)
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

def generate_lookup(folders_config):
    extension_lookup = {}
    ignore_lookup = []
    for file_type, extensions in folders_config.items():
        for extension in extensions:
            if file_type != "ignore":
                extension_lookup[extension] = file_type
            else:
                ignore_lookup.append(extension)
    return extension_lookup, ignore_lookup

#Scans through all directories in the given location to get all the files within. Returns a list of all existing files
#and of which folders will be needed.
def scan_dir(dir, dir_files, dir_folders):

    needed_folders = []
    files = []
    total_files = len(dir_files)
    current_file_num = 0
    for file_name in dir_files:
        file = File(file_name, dir)

        file_destination = file.get_destination()

        if not file.is_ignored and file_destination not in needed_folders and file_destination not in dir_folders:
            needed_folders.append(file_destination)
        files.append(file)
        current_file_num += 1
        draw_progress_bar(current_file_num,total_files)

    return files, needed_folders

def main():
    dir, dir_files, dir_folders = get_directories()
    #print(dir)
    #print(dir_files)
    #print(dir_folders)
    #print(folders_config)
    #file = File("test.png", dir)

    

folders_config = load_configs()
extension_lookup, ignore_lookup = generate_lookup(folders_config)

if __name__ == "__main__":
    main()
