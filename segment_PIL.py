import os
import numpy as np
import SimpleITK as sitk
from PIL import Image
from skimage.measure import find_contours
from skimage.draw import polygon2mask
import cv2

def convert_to_grayscale(image):
    return image

# Input Folder

#input_directory = r"/home/braillic/Braillic/Segmentation to remove black background/Otsu_Thresholding/Original Images/Chan_Sau_Lin_Sherring/t1_fl3d_sag_brain_lab_C_6"

input_directory = r"X:\Braillic\Otsu_Thresholding\Original Images\Chan_Sau_Lin_Sherring\t1_fl3d_sag_brain_lab_C_6"

dicom_files = [os.path.join(input_directory, file) for file in os.listdir(input_directory) if file.endswith('.dcm')]


# Output Folder where images will be saved

#output_base_folder = r"/home/braillic/Braillic/Segmentation to remove black background/Otsu_Thresholding/Segmentated Images"
output_base_folder = r"X:\Braillic\Otsu_Thresholding\Segmentated Images"

path_parts = input_directory.split(os.sep)
output_file_name = path_parts[-2] + "_" + path_parts[-1]

output_folder = os.path.join(output_base_folder,output_file_name)


# Create folder if does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Read DICOM files
for file in dicom_files:
    try:
        img = sitk.ReadImage(file)
        img_array = sitk.GetArrayFromImage(img)

        # Normalize the image
        img_array = img_array / np.iinfo(img_array.dtype).max

        # Convert the normalized image to 8-bit
        img_array = (img_array * 255).astype(np.uint8)

        # Loop through each slice in the 3D image
        for i in range(img_array.shape[0]):
            slice_img_array = img_array[i]

            # Apply 5x5 Gaussian filter
            blurred_img = cv2.GaussianBlur(slice_img_array, (5, 5), 0)

            # Convert the NumPy array back to a SimpleITK image
            slice_img = sitk.GetImageFromArray(blurred_img)

            # Apply Otsu's thresholding
            otsu_filter = sitk.OtsuThresholdImageFilter()
            otsu_filter.SetInsideValue(0)
            otsu_filter.SetOutsideValue(1)
            thresholded_img = otsu_filter.Execute(slice_img)

            # Perform morphological closing
            closing_filter = sitk.BinaryMorphologicalClosingImageFilter()
            closing_filter.SetKernelRadius(7)  # You might need to adjust this value
            closed_img = closing_filter.Execute(thresholded_img)

            # Get array from the closed image
            closed_img_array = sitk.GetArrayFromImage(closed_img)

            # Find contours and fill them
            contours, _ = cv2.findContours(closed_img_array.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            filled_img = cv2.drawContours(closed_img_array, contours, -1, (255,255,255), thickness=cv2.FILLED)

            # Create new RGBA image and paste segmented part using mask
            foreground = Image.new("RGBA", slice_img.GetSize()[::-1], (0, 0, 0, 0))
            image_pil = Image.fromarray(blurred_img).convert("RGBA")  # Use the blurred image here
            mask_pil = Image.fromarray(filled_img, mode="L")
            foreground.paste(image_pil, mask=mask_pil)

            # Save the output image
            foreground.save(os.path.join(output_folder, f"{os.path.basename(file).replace('.dcm', '')}_{i}.png"))
    except AttributeError as error:
        print(f"An AttributeError happened: {error}")
    except Exception as error:
        print(f"An unexpected error happened: {error}")
