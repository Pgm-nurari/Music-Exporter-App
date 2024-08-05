import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from pathlib import Path
import customtkinter as ctk

class MusicFileExporter:
    def __init__(self, root):
        self.root = root
        self.music_dir = None
        self.init_ui()
        self.ensure_directory_exists()

    def init_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root.title("Music File Exporter")
        self.root.geometry("600x400")  # Adjust the initial size of the window

        # Directory Selection
        select_dir_btn = ctk.CTkButton(self.root, text="Select Main Music Directory", command=self.select_directory, font=("Helvetica", 12))
        select_dir_btn.grid(row=0, column=0, padx=20, pady=20, sticky='ew', columnspan=2)

        # Listbox for folder selection
        self.listbox_frame = ctk.CTkFrame(self.root)
        self.listbox_frame.grid(row=1, column=0, padx=20, pady=10, sticky='nswe')

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, font=("Helvetica", 12))
        self.listbox.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)

        # Save Options
        frame_options = ctk.CTkFrame(self.root)
        frame_options.grid(row=1, column=1, padx=20, pady=10, sticky='ns')

        # File type buttons
        self.file_type_var = tk.StringVar(value='CSV')

        csv_button = ctk.CTkButton(frame_options, text="CSV", font=("Helvetica", 12), command=lambda: self.file_type_var.set('CSV'))
        csv_button.pack(pady=5)

        excel_button = ctk.CTkButton(frame_options, text="Excel", font=("Helvetica", 12), command=lambda: self.file_type_var.set('Excel'))
        excel_button.pack(pady=5)

        # Select All Checkbox
        self.select_all_var = tk.BooleanVar()
        select_all_checkbox = ctk.CTkCheckBox(frame_options, text="Select All Folders", variable=self.select_all_var, command=self.select_all_folders, font=("Helvetica", 12))
        select_all_checkbox.pack(pady=10)

        # Save File Button
        save_btn = ctk.CTkButton(frame_options, text="Save File", command=self.save_file, font=("Helvetica", 12))
        save_btn.pack(pady=20)

        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

    def ensure_directory_exists(self):
        self.export_folder = Path("C:/Music Exporter")
        if not self.export_folder.exists():
            self.export_folder.mkdir(parents=True)

    def search_music_files(self, start_dir) -> list:
        """Recursively search for music files in sub-directories of start_dir."""
        files_list = []
        for root, dirs, files in os.walk(start_dir):
            if not os.path.commonpath([start_dir]) in os.path.commonpath([root, start_dir]):
                continue
            for file in files:
                if file.lower().endswith(('.mp3', '.m4a')):
                    base_name = file.rsplit('.', 1)[0]
                    if ' - ' in base_name:
                        title, authors_str = base_name.split(' - ', 1)
                        authors = ' | '.join(author.strip() for author in authors_str.split(','))
                        files_list.append((title, authors, os.path.basename(root)))  # Use only the folder name
                    else:
                        files_list.append((base_name, '', os.path.basename(root)))  # Use only the folder name
        return files_list

    def generate_files(self, file_type, selected_folders):
        """Generate CSV or Excel file with music data and save to the export folder."""
        data = self.search_music_files(self.music_dir)
        filtered_data = [entry for entry in data if entry[2] in selected_folders]

        df = pd.DataFrame(filtered_data, columns=['Song Name', 'Authors', 'Folder'])
        
        file_name = 'music_files'
        if file_type == 'CSV':
            file_path = self.export_folder / f'{file_name}.csv'
            df.to_csv(file_path, index=False, encoding='utf-8')
        else:
            file_path = self.export_folder / f'{file_name}.xlsx'
            df.to_excel(file_path, index=False, engine='openpyxl')
        
        messagebox.showinfo("Success", f'{file_type} file saved as: {file_path}')

    def select_directory(self):
        """Open a directory dialog and set the directory path."""
        self.music_dir = filedialog.askdirectory(title="Select the Main Music Directory")
        if not self.music_dir:
            return

        data = self.search_music_files(self.music_dir)
        if not data:
            messagebox.showerror("Error", f"No music files found in '{self.music_dir}'.")
        else:
            folder_names = sorted(set(entry[2] for entry in data))
            self.listbox.delete(0, tk.END)  # Clear previous entries
            for folder_name in folder_names:
                self.listbox.insert(tk.END, folder_name)
            self.select_all_var.set(False)

    def save_file(self):
        """Determine the file type and save the file to the export folder."""
        file_type = self.file_type_var.get()
        if file_type not in ['CSV', 'Excel']:
            messagebox.showerror("Error", "Please select a valid file type.")
            return
        if not self.music_dir:
            messagebox.showerror("Error", "No directory selected.")
            return
        
        selected_folders = [self.listbox.get(i) for i in self.listbox.curselection()]
        if self.select_all_var.get():
            # If "Select All" is checked, include all folders
            selected_folders = [self.listbox.get(i) for i in range(self.listbox.size())]

        if not selected_folders:
            messagebox.showerror("Error", "No folders selected.")
            return

        self.generate_files(file_type, selected_folders)

    def select_all_folders(self):
        """Select or deselect all folders in the listbox based on the 'Select All' checkbox."""
        if self.select_all_var.get():
            self.listbox.select_set(0, tk.END)  # Select all items
        else:
            self.listbox.select_clear(0, tk.END)  # Deselect all items

# Main execution
if __name__ == "__main__":
    root = ctk.CTk()  # Use CTk instead of Tk
    app = MusicFileExporter(root)
    root.mainloop()
