import os
import shutil


def organize_files_by_extension(folder_name):
    if not os.path.exists(folder_name):
        print(f"The folder {folder_name} does not exist.")
        return

    for filename in os.listdir(folder_name):
        file_path = os.path.join(folder_name, filename)

        # Skip directories, we are only organizing files
        if os.path.isfile(file_path):
            # Get the file extension (e.g., ".txt", ".jpg")
            file_extension = os.path.splitext(filename)[1].lower()[1:]  # Get extension without a dot

            # If the file has no extension, move it to 'no_extension' folder
            if not file_extension:
                file_extension = "no_extension"

            # Create a directory for this extension if it doesn't exist
            destination_folder = os.path.join(folder_name, file_extension)  # Skip the dot in extension
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Move the file to the destination folder
            shutil.move(file_path, os.path.join(destination_folder, filename))
            print(f"Moved {filename} to {destination_folder}")


if __name__ == "__main__":
    # Path to the folder you want to organize
    source_folder = input("Enter the path to the folder you want to organize: ").strip()

    # Organize files by their extensions
    organize_files_by_extension(source_folder)
