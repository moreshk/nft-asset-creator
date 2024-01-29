import os
import shutil

def move_files(src_folder):
    # Paths for the target directories
    images_folder = os.path.join(src_folder, 'images')
    metadata_folder = os.path.join(src_folder, 'metadata')

    # Create target directories if they don't exist
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(metadata_folder, exist_ok=True)

    # Move .png files to 'images' and .json files to 'metadata'
    for file_name in os.listdir(src_folder):
        if file_name.endswith('.png'):
            shutil.move(os.path.join(src_folder, file_name), os.path.join(images_folder, file_name))
        elif file_name.endswith('.json'):
            shutil.move(os.path.join(src_folder, file_name), os.path.join(metadata_folder, file_name))

# Usage
source_folder = "renamed_assets"  # Replace with your source folder path
move_files(source_folder)
