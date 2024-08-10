from tkinter import *
from PIL import Image, ImageTk
import os
import threading

class ImageCaptionApp:
    def __init__(self, root, image_folder, caption_folder):
        self.root = root
        self.image_folder = image_folder
        self.caption_folder = caption_folder
        self.current_index = 0

        self.image_files = sorted(os.listdir(image_folder))
        self.caption_files = sorted(os.listdir(caption_folder))

        self.image_label = Label(root)
        self.caption_label = Label(root, wraplength=600)
        self.edit_button = Button(root, text="Edit Caption", command=self.edit_caption)
        self.prev_button = Button(root, text="Previous", command=self.prev_image)
        self.next_button = Button(root, text="Next", command=self.next_image)
        self.file_location_label = Label(root, text="File Location: ")
        self.textfile_location_label = Label(root, text="Text File Location: ")

        self.image_info_frame = Frame(root)  # Frame to hold image info
        self.image_info_label = Label(self.image_info_frame)  # Label to display image info
        self.image_info_frame.pack(side=TOP, fill=X)  # Packing the frame at the top

        self.image_listbox = Listbox(root)
        for file_name in self.image_files:
            self.image_listbox.insert(END, file_name)
        self.image_listbox.bind('<<ListboxSelect>>', self.on_select_image)
        self.image_listbox.pack(side=RIGHT, fill=Y)

        self.load_image_thread = None

        self.file_location_label.pack(pady=5)
        self.textfile_location_label.pack(pady=5)
        self.image_label.pack()
        self.caption_label.pack()

        button_frame = Frame(root)
        button_frame.pack(fill=X, padx=10, pady=10)

        self.prev_button.pack(side=LEFT, padx=10, pady=5, expand=True, fill=X)
        self.edit_button.pack(side=LEFT, padx=10, pady=5, expand=True, fill=X)
        self.next_button.pack(side=LEFT, padx=10, pady=5, expand=True, fill=X)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root_width = int(screen_width * 0.8)
        root_height = int(screen_height * 0.8)
        root.geometry(f"{root_width}x{root_height}")

        self.root.update_idletasks()
        listbox_height = root_height - 100
        self.image_listbox.configure(height=listbox_height)

        self.update_image_info()  # Update image info initially
        self.display_image_caption()

    def update_image_info(self):
        total_images = len(self.image_files)
        current_image_index = self.current_index + 1
        self.image_info_label.config(text=f"Totoal Image: {current_image_index}/{total_images}")
        self.image_info_label.pack()  # Packing the label

    def display_image_caption(self):
        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
        caption_path = os.path.join(self.caption_folder, self.caption_files[self.current_index])

        self.file_location_label.config(text=f"File Location: {image_path}")
        self.textfile_location_label.config(text=f"Text File Location: {caption_path}")

        if self.load_image_thread is not None:
            self.load_image_thread.join()  # Wait for previous thread to finish
        
        self.load_image_thread = threading.Thread(target=self.load_image, args=(image_path,))
        self.load_image_thread.start()

        with open(caption_path, 'r') as f:
            caption_text = f.read()
        self.caption_label.config(text=caption_text)

    def load_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((400, 400))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def edit_caption(self):
        caption_path = os.path.join(self.caption_folder, self.caption_files[self.current_index])
        with open(caption_path, 'r+') as f:
            current_caption = f.read()

        edit_dialog = Toplevel(self.root)
        edit_dialog.title("Edit Caption")
        edit_dialog.geometry("500x250")
        edit_dialog.transient(self.root)

        caption_textbox = Text(edit_dialog, wrap=WORD, width=50, height=10)
        caption_textbox.insert(END, current_caption)
        caption_textbox.pack(fill=BOTH, expand=True)

        undo_button = Button(edit_dialog, text="Undo Changes", command=lambda: self.undo_changes(caption_textbox, current_caption))
        undo_button.pack()

        save_button = Button(edit_dialog, text="Save", command=lambda: self.save_caption(edit_dialog, caption_path, caption_textbox))
        save_button.pack()

    def save_caption(self, edit_dialog, caption_path, caption_textbox):
        new_caption = caption_textbox.get("1.0", END)
        with open(caption_path, 'w') as f:
            f.write(new_caption)
        edit_dialog.destroy()
        self.caption_label.config(text=new_caption)

    def undo_changes(self, caption_textbox, original_text):
        caption_textbox.delete("1.0", END)
        caption_textbox.insert(END, original_text)

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image_info()  # Update image info when changing image
            self.display_image_caption()

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.update_image_info()  # Update image info when changing image
            self.display_image_caption()

    def on_select_image(self, event):
        selected_index = self.image_listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            self.update_image_info()  # Update image info when selecting from listbox
            self.display_image_caption()

if __name__ == "__main__":
    root = Tk()
    root.title("Text Annotation")
    
    img_subfolder = "/Users/jahid.hasan/Desktop/Example/images"
    caption_subfolder = "/Users/jahid.hasan/Desktop/Example/captions"

    app = ImageCaptionApp(root, img_subfolder, caption_subfolder)
    root.mainloop()
