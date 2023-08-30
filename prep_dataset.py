import numpy as np

from mask import mask
from save import save_file
from tkinter import messagebox
import os
import pydicom


def prep_dataset(root_dir: str):
    files = sorted(os.listdir(root_dir))
    image_list, mask_list, threshold_list, file_list = [], [], [], []
    for file in files:
        if not file.lower().endswith('.dcm'):
            messagebox.showinfo("Exception", "Not DICOM file")
            break
        file = os.path.join(root_dir, file)
        file_list.append(file)
        img = pydicom.dcmread(file)
        img = img.pixel_array
        image_list.append(img)
        save_file(img, file, 'image')
        mask_img, threshold = mask(img)
        threshold_list.append(threshold)
        mask_list.append(mask_img)
        save_file(mask_img, file, 'mask')
    return image_list, mask_list, threshold_list, file_list


if __name__ == '__main__':
    print("Enter file name: ")
    fname = input()
    prep_dataset(fname)

