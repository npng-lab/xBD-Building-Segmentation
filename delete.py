import numpy as np
from PIL import Image
import os

def check_and_delete_images(folder_path):
    images_folder_path = os.path.join(folder_path, 'images')
    targets_folder_path = os.path.join(folder_path, 'targets')
    target_images_to_delete = []

    # Check if both images and targets folders exist
    if not (os.path.exists(images_folder_path) and os.path.exists(targets_folder_path)):
        print("Images or targets folder does not exist.")
        return

    # Get list of image files in images folder
    image_files = [f for f in os.listdir(images_folder_path) if os.path.isfile(os.path.join(images_folder_path, f))]

    for image_file in image_files:
        # Get corresponding target file name
        target_file_name = image_file.replace('pre_disaster', 'pre_disaster_target')  # Rename to target file name
        target_file_path = os.path.join(targets_folder_path, target_file_name)

        # Check if corresponding target file exists
        if os.path.exists(target_file_path):
            # Extract the common part of the file names
            image_name_parts = image_file.split('_')
            target_name_parts = target_file_name.split('_')
            if len(image_name_parts) >= 7 and len(target_name_parts) >= 8:
                if image_name_parts[5] == target_name_parts[6] and image_name_parts[6] == target_name_parts[7]:
                    # Check if target image contains class 1
                    with open(target_file_path, 'rb') as target_file:
                        label_image = Image.open(target_file)
                        label_image_array = np.array(label_image)
                        unique = np.unique(label_image_array)
                        if 1 not in unique:
                            # If the parts after the third underscore are equal and class 1 is not in the target image, mark the image file for deletion
                            print(f"Marking for deletion: {image_file}")
                            target_images_to_delete.append(target_file_path)
                            image_file_path = os.path.join(images_folder_path, image_file)
                            os.remove(image_file_path)
                            # os.remove(target_file_path)
                            
    for file_to_delete in target_images_to_delete:
        print(f"Deleting {file_to_delete}")
        os.remove(file_to_delete)

# Path to the folder containing images and targets folders
folder_path = 'train'

check_and_delete_images(folder_path)
