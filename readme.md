# VFX Project Folder Creator

A Python application that helps you create standardized VFX project folder structures with support for Nuke script templates. This tool makes it easy to set up consistent project organization for visual effects work.

![VFX Project Folder Creator]

## Features

- **Create complete VFX project structures** with customizable folder naming
- **Add sequences and shots** to your project structure
- **Automatic Nuke script generation** with configurable resolution, FPS, and color management settings
- **Add to existing projects** with the ability to create new sequence/shot folders within specific project directories
- **Dark mode UI** for comfortable use in production environments
- **Customizable folder names** allowing you to adapt to different studio conventions
- **Template-based project creation** option for custom folder structures

## Installation

### Requirements

- Python 3.6 or higher
- PyQt5

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vfx-project-folder-creator.git
   cd vfx-project-folder-creator
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage

### Tab 1: Structure

This tab allows you to create a new VFX project from scratch.

1. **Show Name**: Enter your project name.
2. **Destination Folder**: Select where the project should be created.
3. **Creation Mode**:
   - **Hardcoded**: Uses the default folder structure configured in the "Folder Names" tab.
   - **Template**: Replicates a folder structure from an existing project.
4. **Resolution Settings**: Choose from presets or set custom width/height.
5. **FPS**: Select the frame rate for the project.
6. **Workflow Options**: Enable/disable proxy and ACES workflow.
7. **Sequences and Shots**: Add your sequences and shots using the "+" buttons.
8. Review the preview and click "Create Folder Structure" when ready.

### Tab 2: Folder Names

This tab allows you to customize the default folder structure.

- Edit any folder name by double-clicking on it.
- Changes made here will be applied when creating new projects.
- The hierarchy shows the relationship between folders.

### Tab 3: Add to Existing Project

This tab lets you add new sequences and shots to an existing project.

1. **Select Project**: Browse for an existing project folder.
2. **Nuke Script Options**: Configure if needed.
3. **Select Destination Folders**: Check the folders in the existing project tree where you want to add new content.
4. **Add Sequences/Shots**: Define the new sequences and shots to add.
5. Review the preview and click "Add Folders & Shots" when ready.

## Default Folder Structure

The default folder structure follows industry standards for VFX projects:

- **01_plates**: Original footage and source material
  - **Aspera**: Transfer/delivery files
  - **sequence/shot folders**: Organized by sequence and shot
  - **plate_manifest.txt**: Documentation for plates
- **02_support**: Supporting files for the project
  - **luts**: Look-Up Tables for color management
    - **camera**: Camera-specific LUTs
    - **show**: Show-specific LUTs
  - **edl_xml**: Edit decision lists and XMLs
  - **guides**: Reference guides and layouts
  - **camera_data**: Camera metadata and tracking information
- **03_references**: Reference materials
  - **client_brief**: Notes and directions from client
  - **artwork**: Concept art and visual references
  - **style_guides**: Visual style information
- **04_vfx**: Visual effects elements
  - Structure by sequence/shot with project and render folders
- **05_comp**: Compositing files
  - Structure by sequence/shot with project and render folders
  - Contains auto-generated Nuke scripts
- **06_mograph**: Motion graphics content
  - **projects**: Source project files
  - **render**: Rendered output from motion graphics
- **07_shared**: Common assets used across the project
  - **stock_footage**: Stock video assets
  - **graphics**: Graphic elements
  - **fonts**: Typography assets
  - **templates**: Reusable templates
- **08_output**: Delivery and output files
  - **[date]**: Organized by delivery date
    - **full_res**: Full resolution outputs
    - **proxy**: Lower resolution proxies

## Nuke Script Templates

The application automatically generates Nuke script templates with:

- Appropriate project name based on sequence and shot
- Correct FPS settings
- Resolution settings
- Optional ACES color management
- Optional proxy workflow settings
- A clean node graph with default viewer and settings

## Customization

All folder names can be customized through the "Folder Names" tab. Changes are stored during your session and applied to new projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
