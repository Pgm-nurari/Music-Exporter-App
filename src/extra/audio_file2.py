import os
import csv

def change_to_user_dir():
    """Navigate to the user's directory."""
    while True:
        previous_dir = os.getcwd().split(os.sep)  # Use os.sep for cross-platform compatibility
        if 'Users' == previous_dir[-2]:
            break
        os.chdir('..')
    print(f"Current Directory: {os.getcwd()}")

def change_to_music_dir() -> list:
    """Change to a directory containing music folders and return the folder names."""
    music_dirnames = ['music', 'Music', 'Audio']
    for dirname in music_dirnames:
        dir_path = os.path.join(os.getcwd(), dirname)
        if os.path.exists(dir_path):
            os.chdir(dir_path)
            return os.listdir(dir_path)
    return []

def get_files_in_dir(file_path: str):
    """Return a list of (title, authors) tuples from the files in the directory."""
    files_list = []
    for f_name in os.listdir(file_path):
        # Skip 'desktop.ini' and other non-music files
        if f_name.lower() == 'desktop.ini':
            continue
        if f_name.lower().endswith(('.mp3', '.m4a')):
            base_name = f_name.rsplit('.', 1)[0]
            if ' - ' in base_name:
                title, authors_str = base_name.split(' - ', 1)
                authors = ' | '.join(author.strip() for author in authors_str.split(','))
                files_list.append((title, authors))
    return files_list

if __name__ == '__main__':
    pgm_file_path = os.getcwd()

    change_to_user_dir()

    music_folder_names = change_to_music_dir()
    print('The folders are:', music_folder_names)

    csv_file_path = os.path.join(pgm_file_path, 'music_files.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        csv_writer.writerow(['Song Name', 'Authors', 'Folder'])

        for folder_name in music_folder_names:
            folder_path = os.path.join(os.getcwd(), folder_name)
            try:
                print(f'Processing folder: {folder_name}')
                files_list = get_files_in_dir(folder_path)
                for title, authors in files_list:
                    csv_writer.writerow([title, authors, folder_name])
            except Exception as e:
                print(f'An error occurred while processing the folder "{folder_name}": {e}')
            print()
