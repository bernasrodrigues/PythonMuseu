settings = {}

def ReadSettingsFromFile(file_path):
    print("------------\nLoading settings")

    with open(file_path, 'r') as file:
        for line in file:
            # Execute each line using exec
            exec(line, globals(), settings)

    print(f'settings loaded into "settings" dictionary\n------------')


# Example usage
# settingsFile = "settings.txt"
# settings_dict = ReadSettingsFromFile(settingsFile)

if __name__ == "__main__":
    print(settings)
    print(settings["variable1"])
