# Text File Analyzer

## Overview

Text File Analyzer is a powerful desktop application designed to process and analyze large text files. It provides a user-friendly interface for splitting text files into separate files based on custom delimiters, creating directory structures, and compressing the results into ZIP archives.

## Features

- **Custom Delimiter Support**: Easily parse files using user-defined delimiter patterns.
- **Large File Processing**: Efficiently handle large text files with memory-optimized chunk processing.
- **Directory Structure Creation**: Automatically create directory structures based on file content.
- **ZIP Compression**: Compress processed files into ZIP archives without data loss.
- **Plugin System**: Extend functionality with custom plugins.
- **Dark Mode**: Toggle between light and dark themes for comfortable viewing.
- **Localization**: Support for multiple languages (currently includes English and Spanish).
- **Auto-Updates**: Automatically check for and install the latest updates.
- **Recent Files**: Quick access to recently processed files.

## Installation

### Prerequisites

- Python 3.7 or higher
- wxPython 4.1 or higher
- Other dependencies listed in `requirements.txt`

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/text-file-analyzer.git
   ```

2. Navigate to the project directory:
   ```
   cd text-file-analyzer
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python main.py
   ```

## Usage

1. Launch the application by running `main.py`.
2. Click on "Open File" or use the keyboard shortcut Ctrl+O to select a text file for processing.
3. Follow the wizard steps to configure processing options:
   - Set the custom delimiter pattern if needed (default is `^/project_root/`).
   - Choose output options for the processed files.
4. Preview the file structure before processing.
5. Click "Process" to start the file analysis and processing.
6. Once complete, you can find the processed files in the output directory, along with a ZIP archive.

## Configuration

Access the settings dialog (Ctrl+,) to configure:
- Application theme (Light/Dark)
- Custom delimiter pattern
- Auto-update preferences

## Plugin Development

To create a plugin for Text File Analyzer:

1. Create a new Python file in the `plugins` directory.
2. Implement the required plugin structure:
   ```python
   PLUGIN_NAME = "Your Plugin Name"
   PLUGIN_DESCRIPTION = "A brief description of your plugin"

   def main(main_frame):
       # Your plugin logic here
       pass

   def config_ui(parent):
       # Optional: Create a configuration UI for your plugin
       pass
   ```
3. Restart the application to load the new plugin.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- wxPython team for the excellent GUI framework
- All open-source contributors whose libraries made this project possible

