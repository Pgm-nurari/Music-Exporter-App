import os

def change_to_user_dir():
    """Navigate to the user's directory."""
    while True:
        previous_dir = os.getcwd().split(os.sep) 
        print('Previous dir: ',previous_dir) # Use os.sep for cross-platform compatibility
        if 'Users' == previous_dir[-2]:
            break
        os.chdir('..')
    print(f"Current Directory: {os.getcwd()}")

def change_to_music_dir() -> list:
    """Change to a directory containing music folders and return the folder names."""
    music_dirnames = ['music', 'Music', 'Audio']
    for dirname in music_dirnames:
        print(os.getcwd())
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

    output_file_path = os.path.join(pgm_file_path, 'music_file.txt')
    with open(output_file_path, 'w',encoding='utf-8') as file_header:
        file_header.write(f'Folder Names: {music_folder_names}\n\n')
        file_header.write(f"{'-' *80}\n")

    for folder_name in music_folder_names:
        folder_path = os.path.join(os.getcwd(), folder_name)
        try:
            print(f'Processing folder: {folder_name}')
            files_list = get_files_in_dir(folder_path)
            with open(output_file_path, 'a',encoding='utf-8') as file_header:
                file_header.write(f'\nFolder Name: {folder_name}\n')
                for title, authors in files_list:
                    file_header.write(f'Title: {title}\n')
                    if authors:
                        file_header.write(f'Authors: {authors}\n')
                    else:
                        file_header.write('Authors: None\n')  # Explicitly state 'None' if no authors
                file_header.write('\n')
        except Exception as e:
            # Catch and print the specific error without stopping the script
            print(f'An error occurred while processing the folder "{folder_name}": {e}')
        print()
