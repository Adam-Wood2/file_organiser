import os
from configparser import ConfigParser

class File:
    def __init__(self, file_name,location):
        self.file_name = file_name
        self.location = location
        self.full_path = os.path.join(self.location, self.file_name)
        self.file_extension = self.__get_file_extension()
        self.file_type = self.__get_file_type()
        self.size = self.get_file_size()

    
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
        return extension_lookup[self.file_extension]

    def get_file_size(self):
        stats = os.stat(self.full_path)
        size = stats.st_size
        return size

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
    for file_type, extensions in folders_config.items():
        for extension in extensions:
            extension_lookup[extension] = file_type
    return extension_lookup



def main():
    dir, dir_files, dir_folders = get_directories()
    #print(dir)
    #print(dir_files)
    #print(dir_folders)
    #print(folders_config)
    file = File("test.txt", dir)
    print(file.format_size())

folders_config = load_configs()
extension_lookup = generate_lookup(folders_config)

if __name__ == "__main__":
    main()