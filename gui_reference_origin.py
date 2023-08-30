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


root = Tk()
root.title("MRI Mask Viewer")


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


# Folder frame and components
folder_frm = Frame(root, relief=tkinter.GROOVE)
folder_lbl = Label(folder_frm, text="Folder Path")
folder_ent = Entry(folder_frm, width=165)
select_btn = Button(folder_frm, text="Select folder", command=folder_select)
run_btn = Button(folder_frm, text="Run", command=lambda: run_mask(foldername))


folder_frm.grid(row=0, column=0, padx=10, pady=5, sticky="NSEW")
folder_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
folder_ent.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
select_btn.grid(row=0, column=2, padx=5, pady=5, sticky="NSEW")
run_btn.grid(row=0, column=3, padx=5, pady=5, sticky="NSEW")

# Display frame and components
display_frm = Frame(root, relief=tkinter.GROOVE)
display_frm.grid(row=1, column=0, padx=10, pady=5, sticky="NSEW")

# Image frame and components
image_frm = Frame(display_frm)

image_fig = Figure(figsize=(6, 6), dpi=64)
image_plt = image_fig.add_subplot(111)
image_plt.imshow(np.zeros([320, 320]), cmap='gray')
image_plt.axis('off')
image_canvas = FigureCanvasTkAgg(image_fig, master=image_frm)
image_canvas.draw()
forward_btn = Button(image_frm, text=">>", width=5, state=DISABLED, command=forward)
back_btn = Button(image_frm, text="<<", width=5, state=DISABLED, command=back)

image_frm.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
image_canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
back_btn.grid(row=1, column=0, padx=5, pady=5, sticky="W")
forward_btn.grid(row=1, column=1, padx=5, pady=5, sticky="E")

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

mask_frm.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
mask_canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="NSEW")
thresh_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
threshval_lbl.grid(row=1, column=1, padx=5, pady=5, sticky="NSEW")

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
check_btn = Button(newmask_frm, text='Check', width=10, command=lambda: check_thresh(nthreshval_ent.get()))
delete_btn = Button(newmask_frm, text='Delete', width=10, command=delete_mask)
replace_btn = Button(newmask_frm, text='Replace', width=10, command=replace_mask)

newmask_frm.grid(row=0, column=2, padx=5, pady=5, sticky="NSEW")
newmask_canvas.get_tk_widget().grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="NSEW")
nthresh_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
nthreshval_ent.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="NSEW")
check_btn.grid(row=2, column=0, padx=5, pady=5, sticky="W")
replace_btn.grid(row=2, column=1, padx=5, pady=5)
delete_btn.grid(row=2, column=2, padx=5, pady=5, sticky="E")


root.mainloop()
