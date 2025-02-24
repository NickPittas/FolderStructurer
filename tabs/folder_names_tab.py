# folder_names_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt

class FolderNamesTab(QWidget):
    """
    Shows the hardcoded folder structure in a hierarchical QTreeWidget.
    Each node is editable. Editing updates main_window.folder_config accordingly.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # Define the hierarchy to match your "hardcoded" structure
        # Each dict has:
        #   key: the folder_config key, if applicable
        #   children: list of sub-items
        #   label: a default label to display if no folder_config entry found
        self.hardcoded_structure = [
            {
                "key": "folder_01_plates",
                "label": "01_plates",
                "children": [
                    {"key": "folder_01_plates_aspera", "label": "Aspera"},
                    {"key": "folder_01_plates_manifest", "label": "plate_manifest.txt"}
                ]
            },
            {
                "key": "folder_02_support",
                "label": "02_support",
                "children": [
                    {
                        "key": "folder_02_support_luts",
                        "label": "luts",
                        "children": [
                            {"key": "folder_02_support_luts_camera", "label": "camera"},
                            {"key": "folder_02_support_luts_show", "label": "show"}
                        ]
                    },
                    {"key": "folder_02_support_edl_xml", "label": "edl_xml"},
                    {"key": "folder_02_support_guides", "label": "guides"},
                    {"key": "folder_02_support_camera_data", "label": "camera_data"}
                ]
            },
            {
                "key": "folder_03_references",
                "label": "03_references",
                "children": [
                    {"key": "folder_03_references_client_brief", "label": "client_brief"},
                    {"key": "folder_03_references_artwork", "label": "artwork"},
                    {"key": "folder_03_references_style_guides", "label": "style_guides"}
                ]
            },
            {"key": "folder_04_vfx", "label": "04_vfx"},
            {"key": "folder_05_comp", "label": "05_comp"},
            {
                "key": "folder_06_mograph",
                "label": "06_mograph",
                "children": [
                    {"key": "folder_06_mograph_projects", "label": "projects"},
                    {"key": "folder_06_mograph_render", "label": "render"}
                ]
            },
            {
                "key": "folder_07_shared",
                "label": "07_shared",
                "children": [
                    {"key": "folder_07_shared_stock_footage", "label": "stock_footage"},
                    {"key": "folder_07_shared_graphics", "label": "graphics"},
                    {"key": "folder_07_shared_fonts", "label": "fonts"},
                    {"key": "folder_07_shared_templates", "label": "templates"}
                ]
            },
            {
                "key": "folder_08_output",
                "label": "08_output",
                "children": [
                    {
                        "key": "folder_08_output_date",
                        "label": "[date]",
                        "children": [
                            {"key": "folder_08_output_full_res", "label": "full_res"},
                            {"key": "folder_08_output_proxy", "label": "proxy"}
                        ]
                    }
                ]
            }
        ]
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(5)
        self.setLayout(layout)
        
        # A QTreeWidget with a single column for "Folder Name"
        # We'll make it editable so the user can rename.
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel("Folder Structure (edit name)")
        layout.addWidget(self.tree)
        
        # Populate the tree from the self.hardcoded_structure
        self.populate_tree(self.hardcoded_structure, self.tree.invisibleRootItem())
        self.tree.expandAll()
        
        # Connect so if user edits an item, we update folder_config
        self.tree.itemChanged.connect(self.on_item_changed)
    
    def populate_tree(self, children_list, parent_item):
        """
        Recursive function that creates QTreeWidgetItem(s) from the nested dicts.
        """
        for node in children_list:
            key = node.get("key")
            # If the user has overridden the name in folder_config, use that.
            # Otherwise use 'label'.
            default_label = node.get("label", "")
            actual_text = self.main_window.folder_config.get(key)
            if actual_text:
                current_name = actual_text.text()
            else:
                current_name = default_label
            
            item = QTreeWidgetItem([current_name])
            # Make item editable
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            # Store key so we know which folder_config to update
            if key:
                item.setData(0, Qt.UserRole, key)
            
            parent_item.addChild(item)
            
            # Recurse if there are children
            if "children" in node:
                self.populate_tree(node["children"], item)
    
    def on_item_changed(self, item, column):
        new_name = item.text(column)
        key = item.data(column, Qt.UserRole)
        if key:
            # Update the corresponding QLineEdit in folder_config
            if key in self.main_window.folder_config:
                self.main_window.folder_config[key].setText(new_name)
                self.main_window.update_preview()
