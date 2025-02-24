# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QLineEdit
import datetime

from common.themes import apply_custom_stylesheet   # or apply_dark_theme
# from common.themes import apply_dark_theme  # if you prefer the older style

# Imports for your tabs
from tabs.structure_tab import StructureTab
from tabs.folder_names_tab import FolderNamesTab
from tabs.add_to_existing_project_tab import AddToExistingProjectTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Project Manager")
        self.resize(900,600)
        
        # Hardcoded config used by Tab2 and Tab1 folder creation:
        self.folder_config = {
            "folder_01_plates": QLineEdit("01_plates"),
            "folder_01_plates_aspera": QLineEdit("Aspera"),
            "folder_01_plates_manifest": QLineEdit("plate_manifest.txt"),
            
            "folder_02_support": QLineEdit("02_support"),
            "folder_02_support_luts": QLineEdit("luts"),
            "folder_02_support_luts_camera": QLineEdit("camera"),
            "folder_02_support_luts_show": QLineEdit("show"),
            "folder_02_support_edl_xml": QLineEdit("edl_xml"),
            "folder_02_support_guides": QLineEdit("guides"),
            "folder_02_support_camera_data": QLineEdit("camera_data"),
            
            "folder_03_references": QLineEdit("03_references"),
            "folder_03_references_client_brief": QLineEdit("client_brief"),
            "folder_03_references_artwork": QLineEdit("artwork"),
            "folder_03_references_style_guides": QLineEdit("style_guides"),
            
            "folder_04_vfx": QLineEdit("04_vfx"),
            "folder_05_comp": QLineEdit("05_comp"),
            
            "folder_06_mograph": QLineEdit("06_mograph"),
            "folder_06_mograph_projects": QLineEdit("projects"),
            "folder_06_mograph_render": QLineEdit("render"),
            
            "folder_07_shared": QLineEdit("07_shared"),
            "folder_07_shared_stock_footage": QLineEdit("stock_footage"),
            "folder_07_shared_graphics": QLineEdit("graphics"),
            "folder_07_shared_fonts": QLineEdit("fonts"),
            "folder_07_shared_templates": QLineEdit("templates"),
            
            "folder_08_output": QLineEdit("08_output"),
            "folder_08_output_date": QLineEdit("[date]"),
            "folder_08_output_full_res": QLineEdit("full_res"),
            "folder_08_output_proxy": QLineEdit("proxy"),
        }
        
        # The TabWidget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Tab1: Structure
        self.structure_tab = StructureTab(self)
        self.tab_widget.addTab(self.structure_tab, "Structure")
        
        # Tab2: Folder Names
        self.folder_names_tab = FolderNamesTab(self)
        self.tab_widget.addTab(self.folder_names_tab, "Folder Names")
        
        # Tab3: Add to Existing Project
        self.add_to_existing_project_tab = AddToExistingProjectTab(self)
        self.tab_widget.addTab(self.add_to_existing_project_tab, "Add to Existing Project")

    def update_preview(self):
        # Called by textChanged signals in Shots/Sequences 
        # to refresh Tab1 and Tab3 previews
        if hasattr(self, 'structure_tab'):
            self.structure_tab.update_preview()
        if hasattr(self, 'add_to_existing_project_tab'):
            self.add_to_existing_project_tab.update_preview_tab3()
    
    def build_nuke_script_template(
        self, seq_name, shot_name, fps, width, height, resolution_label, 
        use_proxy, use_aces
    ):
        # Just call your function from common.nuke_template or 
        # inline it here. For example:
        from common.nuke_template import build_nuke_script_template
        return build_nuke_script_template(
            seq_name, shot_name, fps, width, height, resolution_label, use_proxy, use_aces
        )

def main():
    app = QApplication(sys.argv)
    
    # Use the custom stylesheet for the "rounded corners" look:
    apply_custom_stylesheet(app)
    # or if you want the simpler dark style:
    # apply_dark_theme(app)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
