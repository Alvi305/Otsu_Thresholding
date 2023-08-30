import os
import numpy as np
from pathlib import Path
import pydicom

# save dir
dir = r"X:\Braillic\Segmentation to remove black background\braillic-segmentation-main\contour-extraction\saved_dataset"

def save_file(matrix, path: str, type: str, root=dir):
    parts = os.path.normpath(path).split(os.path.sep)
    subject_name, sequence_name, filename = parts[-4], parts[-2], parts[-1]
    subject_parts = subject_name.split('_')
    if len(subject_parts) > 2:
        new_name = f'{subject_parts[0]}_{subject_parts[1][0]}{subject_parts[2][0]}_{sequence_name}'
    else:
        new_name = f'{subject_parts[0]}_{subject_parts[1][0]}_{sequence_name}'
    folder = os.path.normpath(os.path.join(root, 'dataset', type, new_name))
    Path(folder).mkdir(parents=True, exist_ok=True)

    dicomfile = pydicom.dcmread(path)
    dicomfile.PixelData = matrix.astype(np.uint16).tobytes()
    dicomfile.save_as(os.path.join(folder, filename))


if __name__ == '__main__':
    matrix = np.random.rand(256,256)
    # save_file(matrix, 'ax_t1/Chan_Hiu_Tung/Brain - MRBR001C/AX_T1_5004/IM-0015-0001.dcm', 'image')
    save_file(matrix, 'ax_t1/Hau_Timy/Brain_ + _Internal_Acoustic_Meatus_(Iam)_(W_Contrast) - 27323/+C_AX_T1_3D_19/IM-0015-0001.dcm', 'image')
