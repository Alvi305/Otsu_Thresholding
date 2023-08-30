import tkinter
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prep_dataset import prep_dataset
from new_mask import new_mask
from delete import delete_files
from save import save_file
import os
import numpy as np
import pydicom
import nibabel as nib
import dicom2nifti


# global variable for folder

foldername = "ax_t1"


# Convert the DICOM directory to a NIFTI file
def save_dicom_2_nifti(PathDicom):
    dicom2nifti.convert_directory(PathDicom, PathDicom)


def folder_select():
    global foldername
  
    foldername = filedialog.askdirectory(initialdir="ax_t1", title="Select DICOM folder")
    if len(foldername) < 1:
        if len(folder_ent.get()) == 0:
            messagebox.showinfo("Exception", "No path given")
        else:
            foldername = folder_ent.get()
    else:
        files = os.listdir(foldername)
        if len(files) < 1:
            messagebox.showinfo("Exception", "No files in folder")
        folder_ent.delete(0, tkinter.END)
        folder_ent.insert(0, foldername)


def run_mask(foldername):
    global images, masks, thresholds, files, count
    count = 0
    images, masks, thresholds, files = prep_dataset(foldername)

    image_plt.clear()
    image_plt.imshow(images[count], cmap='gray')
    image_plt.axis('off')
    image_plt.set_title(f"Image count: {count+1}/{len(images)}")
    image_canvas.draw_idle()

    mask_plt.clear()
    mask_plt.imshow(masks[count], cmap='gray')
    mask_plt.axis('off')
    mask_plt.set_title(f"Mask count: {count+1}/{len(masks)}")
    mask_canvas.draw_idle()

    newmask_plt.clear()
    newmask_plt.imshow(np.zeros([320,320]), cmap='gray')
    newmask_plt.axis('off')
    newmask_canvas.draw_idle()

    threshval_lbl.configure(text='%.5f'%(thresholds[count]))
    forward_btn.config(state=ACTIVE)
    back_btn.config(state=ACTIVE)


def forward():
    global count
    if count < len(images)-1:
        count += 1

        image_plt.clear()
        image_plt.imshow(images[count], cmap='gray')
        image_plt.axis('off')
        image_plt.set_title(f"Image count: {count+1}/{len(images)}")
        image_canvas.draw_idle()

        mask_plt.clear()
        mask_plt.imshow(masks[count], cmap='gray')
        mask_plt.axis('off')
        mask_plt.set_title(f"Mask count: {count+1}/{len(masks)}")
        mask_canvas.draw_idle()

        threshval_lbl.configure(text='%.5f' % (thresholds[count]))


def back():
    global count
    if count > 0:
        count -= 1

        image_plt.clear()
        image_plt.imshow(images[count], cmap='gray')
        image_plt.axis('off')
        image_plt.set_title(f"Image count: {count+1}/{len(images)}")
        image_canvas.draw_idle()

        mask_plt.clear()
        mask_plt.imshow(masks[count], cmap='gray')
        mask_plt.axis('off')
        mask_plt.set_title(f"Mask count: {count+1}/{len(masks)}")
        mask_canvas.draw_idle()

        threshval_lbl.configure(text='%.5f' % (thresholds[count]))


def check_thresh(thresh):
    global count, newmask, tmp_count, tmp_thresh
    if len(thresh) > 1:
        tmp_count = count
        tmp_thresh = float(thresh)
        newmask = new_mask(images[tmp_count], tmp_thresh)

        newmask_plt.clear()
        newmask_plt.imshow(newmask, cmap='gray')
        newmask_plt.axis('off')
        newmask_plt.set_title(f"New Mask count: {tmp_count}")
        newmask_canvas.draw_idle()


def replace_mask():
    masks[tmp_count] = newmask
    thresholds[tmp_count] = tmp_thresh
    file = files[tmp_count]
    save_file(newmask, file, 'mask')


def delete_mask():
    file = files[count]
    delete_files(file)



# GUI Components

root = Tk()
root.title("MRI Mask Viewer")
root.resizable(width=True, height=True)


# Folder frame and components
folder_frm = Frame(root, relief=tkinter.GROOVE)
folder_lbl = Label(folder_frm, text="Folder Path")
folder_ent = Entry(folder_frm, width=165)
select_btn = Button(folder_frm, text="Select folder", command=folder_select)
run_btn = Button(folder_frm, text="Run", command=lambda: run_mask(foldername))

# Folder frame alignment and dynamic resizing
folder_frm.pack(fill=tkinter.BOTH, padx=10, pady=5)
folder_lbl.pack(side=tkinter.LEFT, padx=5, pady=5)
folder_ent.pack(side=tkinter.LEFT, padx=5, pady=5, expand=True, fill=tkinter.BOTH)
select_btn.pack(side=tkinter.LEFT, padx=5, pady=5)
run_btn.pack(side=tkinter.LEFT, padx=5, pady=5)

# Display frame and components
display_frm = Frame(root, relief=tkinter.GROOVE)
display_frm.pack(fill=tkinter.BOTH, padx=10, pady=5)

# Image frame and components
image_frm = Frame(display_frm)

image_fig = Figure(figsize=(6, 6), dpi=64)
image_plt = image_fig.add_subplot(111)
image_plt.imshow(np.zeros([320, 320]), cmap='gray')
image_plt.axis('off')
image_canvas = FigureCanvasTkAgg(image_fig, master=image_frm)
image_canvas.draw()


# Alignment and Resizing
image_frm.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT, padx=5, pady=5)
image_canvas.get_tk_widget().pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT,padx=5, pady=5)


# Mask frame and components
mask_frm = Frame(display_frm)

mask_fig = Figure(figsize=(6, 6), dpi=64)
mask_plt = mask_fig.add_subplot(111)
mask_plt.imshow(np.zeros([320, 320]), cmap='gray')
mask_plt.axis('off')
mask_canvas = FigureCanvasTkAgg(mask_fig, master=mask_frm)
mask_canvas.draw()
thresh_lbl = Label(mask_frm, text="Auto Threshold Value")
threshval_lbl = Label(mask_frm, text="", width=10, bg="white")

# Alignment and Resizing
mask_frm.pack(expand=True,fill=tkinter.BOTH,side=tkinter.LEFT, padx=5, pady=5)
mask_canvas.get_tk_widget().pack(expand=True,fill=tkinter.BOTH,padx=5, pady=5)
thresh_lbl.pack(padx=5, pady=5)
threshval_lbl.pack(padx=5, pady=5)

# New mask frame and components
newmask_frm = Frame(display_frm)

newmask_fig = Figure(figsize=(6, 6), dpi=64)
newmask_plt = newmask_fig.add_subplot(111)
newmask_plt.imshow(np.zeros([320, 320]), cmap='gray')
newmask_plt.axis('off')
newmask_canvas = FigureCanvasTkAgg(newmask_fig, master=newmask_frm)
newmask_canvas.draw()
nthresh_lbl = Label(newmask_frm, text="New Threshold Value")
nthreshval_ent = Entry(newmask_frm, width=10)
check_btn = Button(newmask_frm, text='Check', width=10, command=None)
delete_btn = Button(newmask_frm, text='Delete', width=10, command=None)
replace_btn = Button(newmask_frm, text='Replace', width=10, command=None)
dcm2nifti_btn = Button(newmask_frm, text ='Save as .nii', width=10, command =save_dicom_2_nifti(foldername))

# Alignment and Resizing
newmask_frm.pack(expand=True, side=tkinter.LEFT, padx=5, pady=5)
newmask_canvas.get_tk_widget().pack(expand=True,padx=5, pady=5)
nthresh_lbl.pack(side=tkinter.BOTTOM,padx=5, pady=5)
nthreshval_ent.pack(side=tkinter.BOTTOM,padx=5, pady=5)
check_btn.pack(side=tkinter.RIGHT,padx=5, pady=5)
delete_btn.pack(side=tkinter.RIGHT,padx=5, pady=5)
replace_btn.pack(side=tkinter.RIGHT,padx=5, pady=5)
dcm2nifti_btn.pack(side=tkinter.RIGHT,padx=5,pady=5)

# Alignment and Resizing
newmask_frm.pack(expand=True, fill=tkinter.BOTH,side=tkinter.LEFT, padx=5, pady=5)
newmask_canvas.get_tk_widget().pack(expand=True,fill=tkinter.BOTH,padx=5, pady=5)
nthresh_lbl.pack(padx=5, pady=5)
nthreshval_ent.pack(padx=5, pady=5)
check_btn.pack(padx=5, pady=5)
replace_btn.pack(padx=5, pady=5)
delete_btn.pack(padx=5, pady=5)
# TODO : PLACE THIS AT LAST
forward_btn = Button(image_frm, text=">>", width=7, state=tkinter.DISABLED, command=None)
back_btn = Button(image_frm, text="<<", width=7, state=tkinter.DISABLED, command=None)
back_btn.pack(side=tkinter.TOP, padx=5, pady=5)
forward_btn.pack(side=tkinter.TOP, padx=5, pady=5)


root.mainloop()
