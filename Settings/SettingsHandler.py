settings = {}


def read_variables_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            # Execute each line using exec
            exec(line, globals(), settings)
    return settings


# Example usage
settingsFile = "settings.txt"
settings_dict = read_variables_from_file(settingsFile)

if __name__ == "__main__":
    print(settings)
    print(settings["variable1"])
