import os
import time
import logging
from datetime import datetime, timedelta


class UserPhotosCleaner:
    def __init__(self, folder_path, days=30, log_file=None):
        """
        Initialize the FolderCleaner with the folder path, age threshold in days, and log file path.

        :param folder_path: Path to the folder to clean.
        :param days: Age threshold in days for deleting files.
        :param log_file: Path to the log file for recording deleted files.
        """
        self.folder_path = folder_path
        self.days = days

        if log_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.log_file = os.path.join(script_dir, 'deleted_photos.log')

        self.setup_logger()

    def setup_logger(self):
        """
        Set up the logger to log deleted files to a specified log file.
        """
        self.logger = logging.getLogger('FolderCleanerLogger')
        self.logger.setLevel(logging.INFO)

        # Create a file handler to write log messages to a file
        handler = logging.FileHandler(self.log_file)
        handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(handler)

    def DeleteOldPhotos(self):
        """
        Delete files in the specified folder that are older than the age threshold.
        """

        print("Cleaning old photos\n------------")

        # Calculate the threshold time (days ago from now)
        now = time.time()
        threshold_time = now - self.days * 86400  # days * seconds/day
        # threshold_time = now - 10  # test - delete files older than 10 seconds

        # Iterate over the files in the directory
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)

            # Check if it's a file (and not a directory)
            if os.path.isfile(file_path):
                # Get the file's last modification time
                file_mtime = os.path.getmtime(file_path)

                # Compare the modification time with the threshold
                if file_mtime < threshold_time:
                    try:
                        # Remove the file if it's older than the threshold
                        os.remove(file_path)
                        # Log the deletion
                        self.logger.info(f"Deleted: {file_path}")
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")


# The following code is an example of how to use the FolderCleaner class
if __name__ == "__main__":
    # Define the folder path relative to this script's location
    user_photos_path = os.path.join('..', 'GUI', 'UserPhotos')
    log_file_path = 'deleted_files.log'

    folder_cleaner = UserPhotosCleaner(user_photos_path, days=30, log_file=log_file_path)
    folder_cleaner.DeleteOldPhotos()
