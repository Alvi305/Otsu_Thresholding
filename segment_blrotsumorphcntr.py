import os
import numpy as np
import SimpleITK as sitk
from PIL import Image
from skimage.measure import find_contours
from skimage.draw import polygon2mask
import cv2
import pydicom



# Input Folder

#input_directory = r"/home/braillic/Braillic/Segmentation to remove black background/Otsu_Thresholding/Original Images/Chan_Sau_Lin_Sherring/t1_fl3d_sag_brain_lab_C_6"

input_directory = r"X:\Braillic\Otsu_Thresholding\Original Images\CT2"

dicom_files = [os.path.join(input_directory, file) for file in os.listdir(input_directory)]


# Output Folder where images will be saved

#output_base_folder = r"/home/braillic/Braillic/Segmentation to remove black background/Otsu_Thresholding/Segmentated Images"
output_base_folder = r"X:\Braillic\Otsu_Thresholding\Segmentated Images"

path_parts = input_directory.split(os.sep)
output_file_name =path_parts[-1]

output_folder = os.path.join(output_base_folder,output_file_name)


# Create folder if does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Read DICOM files
for file in dicom_files:
    try:
            ds = pydicom.dcmread(file)
            img = ds.pixel_array

            # Normalize the Image
            normalize = img / np.iinfo(img.dtype).max

            # Convert the normalized image to 8-bit
            normalize = cv2.normalize(normalize, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            # Apply Gaussian blur
            normalize = cv2.GaussianBlur(normalize, (1, 1), 0)

            # Otsu's thresholding
            _, img_thresh = cv2.threshold(normalize, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Morphological operations
            kernel = np.ones((10, 10), np.uint8)
            img_open = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel, iterations = 2)

            # Find largest contour
            contours, _ = cv2.findContours(img_open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt = max(contours, key = cv2.contourArea)

            # Create mask
            mask = np.zeros_like(normalize)
            cv2.drawContours(mask, [cnt], -1, (255), thickness=cv2.FILLED)


            ### TO save as png file

            # Convert mask to PIL Image for easier manipulation
            mask = Image.fromarray(mask)

            foreground = Image.new("RGBA", img.shape, (0, 0, 0, 0))  # Create new blank (transparent) image
            image_pil = Image.fromarray(normalize).convert("RGBA")  # Convert the normalized image to RGBA
            foreground.paste(image_pil, mask=mask)  # Paste in the segmented part using the mask
            # Display the resulting image
            foreground.save(os.path.join(output_folder, os.path.basename(file) + '_segmented.png'))
    except AttributeError as error:
        print(f"An AttributeError happened: {error}")
    except Exception as error:
        print(f"An unexpected error happened: {error}")
        
        
        
print("Processing done ....")
