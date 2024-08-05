# Music Exporter

- This is a simple desktop app made using Python and customTkinter framework. 
- It can be used to extract audio file names from a main selected directory as either '.csv' or '.xlsx' format.
- The saved data files can be found in the `C:/Music Exporter` directory.

## Repository Structure

- `LICENSE`: License file.
- `readme.md`: This readme file.
- `Application/`: Contains the executable `music_exporter.exe`.
- `src/`: Source code for the application.
  - `main/`: Main application code.
  - `extras/`: Related code files.

## Requirements

- Python 3.12.3 (64-bit)

## Installation

1. Ensure Python 3.12.3 (64-bit) is installed on your system.
2. Clone this repository or download the source code.
3. Navigate to the `src/main` directory.
4. Install the required Python packages using `requirements.txt`.

    ```sh
    pip install -r requirements.txt
    ```

## Usage

Navigate to the `src/main` directory and run the `music_exporter.py` file to start the application.

```sh
cd src/main
python music_exporter.py
```

## Convert to Executable

To convert the Python application to a standalone executable without a console window, follow these steps:

1. Install pyinstaller:
    ```sh
    pip install pyinstaller
    ```

2. Navigate to the `src/main` directory and run pyinstaller with the following command:
    ```sh
    pyinstaller --noconsole --onefile music_exporter.py
    ```

This will generate an executable file in the `dist` directory within `src/main`.