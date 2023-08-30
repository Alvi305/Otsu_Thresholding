import os


def delete_files(path: str, root='C:\\Users\\rspem\PycharmProjects\\contour-extraction'):
    parts = os.path.normpath(path).split(os.path.sep)
    subject_name, sequence_name, filename = parts[-4], parts[-2], parts[-1]
    subject_parts = subject_name.split('_')
    if len(subject_parts) > 2:
        new_name = f'{subject_parts[0]}_{subject_parts[1][0]}{subject_parts[2][0]}_{sequence_name}'
    else:
        new_name = f'{subject_parts[0]}_{subject_parts[1][0]}_{sequence_name}'
    img_folder = os.path.normpath(os.path.join(root, 'dataset', 'image', new_name))
    mask_folder = os.path.normpath(os.path.join(root, 'dataset', 'mask', new_name))
    img_path = os.path.join(img_folder, filename)
    mask_path = os.path.join(mask_folder, filename)
    os.remove(img_path)
    os.remove(mask_path)