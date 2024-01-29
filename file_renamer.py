import os
import shutil
import json

def get_numeric_prefix(filename):
    return int(filename.split('.')[0])

def update_json_content(json_content, new_png_filename):
    # Update the 'uri' in 'properties' section
    if 'properties' in json_content and 'files' in json_content['properties']:
        for file_entry in json_content['properties']['files']:
            if 'uri' in file_entry and file_entry['uri'].endswith('.png'):
                file_entry['uri'] = new_png_filename

    # If there are other fields in the JSON that reference the image, update them here
    if 'image' in json_content and json_content['image'].endswith('.png'):
        json_content['image'] = new_png_filename

    return json_content

def rename_files(src_folder, dest_folder):
    all_files = os.listdir(src_folder)
    png_files = sorted([f for f in all_files if f.endswith('.png')], key=get_numeric_prefix)
    json_files = sorted([f for f in all_files if f.endswith('.json')], key=get_numeric_prefix)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for index, (png_file, json_file) in enumerate(zip(png_files, json_files)):
        new_png_filename = f"{index}.png"
        new_json_path = os.path.join(dest_folder, f"{index}.json")

        # Read and update JSON content
        with open(os.path.join(src_folder, json_file), 'r') as file:
            json_content = json.load(file)
        updated_json_content = update_json_content(json_content, new_png_filename)

        # Copy and rename PNG files
        shutil.copy(os.path.join(src_folder, png_file), os.path.join(dest_folder, new_png_filename))

        # Write updated JSON content to new file in the destination folder
        with open(new_json_path, 'w') as file:
            json.dump(updated_json_content, file, indent=4)

# Usage
source_folder = "qc_files"  # Replace with your source folder path
destination_folder = "renamed_assets"  # Replace with your destination folder path
rename_files(source_folder, destination_folder)
