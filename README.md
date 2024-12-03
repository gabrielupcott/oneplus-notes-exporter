# OnePlus Notes Exporter

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Obtaining OnePlusNote.xml](#obtaining-oneplusnotexml)
  - [Step-by-Step Tutorial](#step-by-step-tutorial)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Cloning the Repository](#cloning-the-repository)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
  - [Activating the Virtual Environment](#activating-the-virtual-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

I recently switched to a new phone from an older OnePlus 6T and when migrating my data to my new device I found to easy way to export my Notes files in the native app! So I made this! OnePlus Notes Exporter is a Python script designed to help you export your OnePlus backed-up notes from an XML file into individual text files. This tool parses the XML backup, cleanses the data, and organizes each note into a separate, easily accessible text file.

## Features

- **Sanitizes Filenames**: Removes or replaces invalid characters to ensure compatibility across different operating systems.
- **Handles Invalid XML Characters**: Cleanses the XML content by removing invalid character references.
- **Escapes Quotes**: Ensures that unescaped quotes within attribute values do not cause parsing issues.
- **Batch Processing**: Converts all `<noteRecord>` entries in the XML to individual `.txt` files.
- **Easy to Use**: Simple command-line interface with minimal setup required.

## Obtaining OnePlusNote.xml

To use the OnePlus Notes Exporter, you first need to obtain your `OnePlusNote.xml` file, which contains your backed-up notes. Follow the steps below to create and locate this XML backup using the [Clone Phone OnePlus app](https://play.google.com/store/apps/details?id=com.oneplus.backuprestore&hl=en_CA&pli=1).

### Step-by-Step Tutorial

1. **Download the Clone Phone OnePlus App**

   - Click this link: [Clone Phone App](https://play.google.com/store/apps/details?id=com.oneplus.backuprestore&hl=en_CA&pli=1).
     
     ***OR***
     
   - Open the **Google Play Store** on your OnePlus device.
   - Search for **Clone Phone** by OnePlus.
   - Download and install the app.

1. **Open the Clone Phone App**
   
   - Launch the **Clone Phone** app from your app drawer.

2. **Access Settings**
   
   - In the Clone Phone app, click on the **Settings** icon located at the **top right corner** of the screen.

3. **Navigate to Back Up and Restore**
   
   - Within Settings, select **Back Up and Restore**.

4. **Initiate a New Backup**
   
   - Click on **New Backup** to start the backup process.

5. **Customize Backup Preferences**
   
   - **Uncheck All Items**: By default, all data categories might be selected for backup. We'll uncheck all of these since we're just exporting notes. Feel free to export additional files if you wish.
   - **Access Preference Settings**: Click on **Preference Settings** to choose specific data to back up.
   - **Select Notes**: Ensure the **Notes** option is checked to include your notes in the backup.

6. **Start the Backup Process**
   
   - After selecting Notes, click **OK** to confirm your choices.
   - Click **Start** to begin the backup process.
   - Wait for the backup to complete.

7. **Completion**
   
   - Once the backup is finished, press **Done**.

8. **Locate the OnePlusNote.xml File**
   
   - The `OnePlusNote.xml` file will be saved in the following directory on your device:
     
     ```
     /Android/data/com.oneplus.backuprestore/Backup/Data/{Export_Date}/Note/OnePlusNote.xml
     ```
     
     - **{Export_Date}**: This will be the date you exported the data (eg. 2024-12-02...)

9. **Transfer the XML File to Your Computer**
    
    - Connect your OnePlus device to your computer via USB.
    - Navigate to the directory mentioned above.
    - Copy the `OnePlusNote.xml` file to the **root directory** of the OnePlus Notes Exporter script on your computer.

    You could also achieve this by sending the file directly from your phone to your computer
    
    **Example:**
    
    If your script is located at `C:\Users\YourName\oneplus-notes-exporter`, place the `OnePlusNote.xml` file directly inside this folder.
    
    ```
    oneplus-notes-exporter/
    ├── OnePlusNote.xml
    ├── export_notes.py
    ├── parsed_notes/
    ├── README.md
    └── requirements.txt
    ```

## Installation

Setting up the OnePlus Notes Exporter involves creating a virtual environment, activating it, and installing the necessary dependencies. Follow the steps below to get your environment ready.

### Prerequisites

- **Python 3.7 or higher**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Cloning the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/oneplus-notes-exporter.git
cd oneplus-notes-exporter
```

### Creating a Virtual Environment
Creating a virtual environment helps manage dependencies and avoid conflicts with other Python projects on your system.

1. **Navigate to the Project Directory**

    Ensure you're in the root directory of the cloned repository.
    
    ```bash
    Copy code
    cd oneplus-notes-exporter
    ```
2. **Create the Virtual Environment**

    Run the following command to create a virtual environment named `venv`:
    
    ```bash
    Copy code
    python -m venv venv
    ```

### Activating the Virtual Environment
Before installing dependencies, activate the virtual environment.

- On Windows

    ```bash
    Copy code
    venv\Scripts\activate
    ```
- On macOS and Linux

    ```bash
    Copy code
    source venv/bin/activate
    ```
- Verification

    After activation, your terminal prompt should be prefixed with `(venv)`, indicating that the virtual environment is active.

    ```bash
    Copy code
    (venv) your-computer:oneplus-notes-exporter yourname$
    ```
### Installing Dependencies
With the virtual environment activated, install the required Python packages using pip and the provided `requirements.txt` file.

 **Install via requirements.txt**

  ```bash
  Copy code
  pip install -r requirements.txt
  ```
## Usage
1. **Prepare Your XML Backup**

    Ensure you have followed the [Obtaining `OnePlusNote.xml`](#obtaining-oneplusnotexml) section to obtain and place the `OnePlusNote.xml` file in the root directory of the cloned repo.

2. **Run the Script**

    With the virtual environment activated, execute the script:
    
    ```bash
    Copy code
    python export_notes.py
    ```
3. **Output**

    The script will create a directory named `parsed_notes` (or the specified output directory) containing individual `.txt` files for each note.

### Configuration
- XML File Path

    By default, the script looks for `OnePlusNote.xml` in the current directory. To change the XML file path, modify the `xml_file_path` variable in the `if __name__ == "__main__":` block.
    
    ```python
    Copy code
    xml_file_path = 'path/to/your/OnePlusNote.xml'
    ```
- Output Directory

    The output directory is set to `parsed_notes` within the root directory of the repo by default. You can change this by modifying the `output_directory` variable.
    
    ```python
    Copy code
    output_directory = 'desired_output_directory'
    ```
### Example
After running the script, your directory structure will look like this:

```Copy code
oneplus-notes-exporter/
├── OnePlusNote.xml
├── export_notes.py
├── parsed_notes/
│   ├── Meeting_With_Team.txt
│   ├── Shopping_List.txt
│   └── Ideas_for_Project.txt
├── README.md
└── requirements.txt
```
Each `.txt` file in the parsed_notes directory contains the title and content of a note from your OnePlus backup.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- [lxml Library](https://lxml.de/) for efficient XML parsing.




