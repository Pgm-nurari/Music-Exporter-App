
# Music Exporter Documentation

## Overview

The Music Exporter application allows users to export music data and save it in the `C:/Music Exporter` directory. It uses the following Python libraries:

- `pandas` for data manipulation and analysis
- `tk` and `customtkinter` for the graphical user interface

## Prerequisites

- Python 3.12.3 (64-bit)

## Installation

To install the required packages, navigate to the `src/main` directory and use the `requirements.txt` file:

```sh
pip install -r requirements.txt
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