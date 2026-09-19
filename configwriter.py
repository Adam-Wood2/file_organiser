from configparser import ConfigParser

def generateDefaultConfig():
    config = ConfigParser()

    config["FILETYPES"] = {
        "Images" : ".jpg, .png, .jpeg, .gif, .webp, .svg", 
        "Video" : ".mp4, .m4v, .mov, .mkv",
        "Audio" : ".wav, .mp3",
        "Documents" : ".doc, .docx, .pdf, .txt",
        "Ignore" : ""
    } 

    with open("config.ini", "w") as f:
        config.write(f)


if __name__ == "__main__":
    generateDefaultConfig()