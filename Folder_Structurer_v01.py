import sys
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QTextEdit,
    QMessageBox, QScrollArea, QFrame, QComboBox, QCheckBox,
    QSpinBox, QFormLayout
)
from PyQt5.QtCore import Qt


def apply_dark_theme(app):
    """
    A simple dark stylesheet for the entire application,
    including the QTabWidget and its tabs.
    """
    dark_stylesheet = """
    QMainWindow {
        background-color: #2e2e2e;
    }
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
    }
    QLineEdit, QTextEdit, QComboBox, QSpinBox {
        background-color: #3b3b3b;
        color: #ffffff;
        border: 1px solid #555555;
    }
    QPushButton {
        background-color: #444444;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 2px;
    }
    QPushButton:hover {
        background-color: #555555;
    }
    QLabel {
        color: #ffffff;
    }
    QScrollArea {
        background-color: #2e2e2e;
    }

    /* Style the tab widget */
    QTabWidget::pane {
        border: 1px solid #555555;
        background-color: #2e2e2e;
    }
    QTabBar::tab {
        background-color: #444444;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 4px;
        margin: 2px;
    }
    QTabBar::tab:hover {
        background-color: #555555;
    }
    QTabBar::tab:selected {
        background-color: #666666;
    }
    """
    app.setStyleSheet(dark_stylesheet)


# ===================== Shot & Sequence Widgets =====================

class ShotWidget(QWidget):
    def __init__(self, parent_sequence_widget):
        super().__init__()
        self.parent_sequence_widget = parent_sequence_widget
        
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.shot_name_edit = QLineEdit()
        self.shot_name_edit.setPlaceholderText("Shot Name (max 25 chars)")
        self.shot_name_edit.setMaxLength(25)
        
        self.btn_remove_shot = QPushButton("-")
        self.btn_add_shot = QPushButton("+")
        self.btn_remove_shot.setFixedWidth(25)
        self.btn_add_shot.setFixedWidth(25)
        
        self.layout.addWidget(self.shot_name_edit)
        self.layout.addWidget(self.btn_remove_shot)
        self.layout.addWidget(self.btn_add_shot)
        
        self.setLayout(self.layout)
        
        # Connect signals
        self.btn_remove_shot.clicked.connect(self.remove_self)
        self.btn_add_shot.clicked.connect(self.add_shot_below)
        
        # Update preview on text
        self.shot_name_edit.textChanged.connect(self.parent_sequence_widget.parent_main_window.update_preview)
    
    def remove_self(self):
        self.parent_sequence_widget.remove_shot(self)
        self.parent_sequence_widget.parent_main_window.update_preview()
    
    def add_shot_below(self):
        self.parent_sequence_widget.add_shot(after_shot_widget=self)
        self.parent_sequence_widget.parent_main_window.update_preview()
    
    def get_shot_name(self):
        return self.shot_name_edit.text().strip()

class SequenceWidget(QWidget):
    def __init__(self, parent_main_window, sequence_list_container):
        super().__init__()
        self.parent_main_window = parent_main_window
        self.sequence_list_container = sequence_list_container
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(0)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        self.sequence_name_edit = QLineEdit()
        self.sequence_name_edit.setPlaceholderText("Sequence Name (max 25 chars)")
        self.sequence_name_edit.setMaxLength(25)
        
        self.btn_remove_sequence = QPushButton("-")
        self.btn_add_sequence = QPushButton("+")
        self.btn_remove_sequence.setFixedWidth(25)
        self.btn_add_sequence.setFixedWidth(25)
        
        self.header_layout.addWidget(self.sequence_name_edit)
        self.header_layout.addWidget(self.btn_remove_sequence)
        self.header_layout.addWidget(self.btn_add_sequence)
        
        self.shots_layout = QVBoxLayout()
        self.shots_layout.setSpacing(0)
        self.shots_layout.setContentsMargins(16, 0, 0, 0)
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.shots_layout)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(sep)
        
        self.setLayout(self.main_layout)
        
        # Connect
        self.btn_remove_sequence.clicked.connect(self.remove_self)
        self.btn_add_sequence.clicked.connect(self.add_new_sequence_below)
        self.sequence_name_edit.textChanged.connect(self.parent_main_window.update_preview)
        
        # Start with one shot
        self.add_shot()
    
    def remove_self(self):
        self.sequence_list_container.remove_sequence(self)
        self.parent_main_window.update_preview()
    
    def add_new_sequence_below(self):
        self.sequence_list_container.add_sequence(after_sequence_widget=self)
        self.parent_main_window.update_preview()
    
    def add_shot(self, after_shot_widget=None):
        new_shot = ShotWidget(self)
        if not after_shot_widget:
            self.shots_layout.addWidget(new_shot)
        else:
            idx = self.shots_layout.indexOf(after_shot_widget) + 1
            self.shots_layout.insertWidget(idx, new_shot)
        return new_shot
    
    def remove_shot(self, shot_widget):
        shot_widget.setParent(None)
    
    def get_sequence_name(self):
        return self.sequence_name_edit.text().strip()
    
    def get_shot_names(self):
        shots = []
        for i in range(self.shots_layout.count()):
            item = self.shots_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, ShotWidget):
                s = widget.get_shot_name()
                if s:
                    shots.append(s)
        return shots

class SequenceListContainer(QWidget):
    def __init__(self, parent_main_window):
        super().__init__()
        self.parent_main_window = parent_main_window
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
    
    def add_sequence(self, after_sequence_widget=None):
        new_seq = SequenceWidget(self.parent_main_window, self)
        if after_sequence_widget:
            idx = self.layout.indexOf(after_sequence_widget) + 1
            self.layout.insertWidget(idx, new_seq)
        else:
            self.layout.addWidget(new_seq)
        return new_seq
    
    def remove_sequence(self, sequence_widget):
        sequence_widget.setParent(None)
    
    def get_all_sequences_and_shots(self):
        data = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            w = item.widget()
            if isinstance(w, SequenceWidget):
                seq = w.get_sequence_name()
                shots = w.get_shot_names()
                if seq:
                    data.append({'sequence': seq, 'shots': shots})
        return data


# ====================== Folder Names Tab ======================

class FolderNamesTab(QWidget):
    """
    Lets the user rename the 'Hardcoded' subfolders. 
    Ignored if 'Template' mode is chosen.
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        form = QFormLayout()
        form.setSpacing(5)
        form.setContentsMargins(10, 10, 10, 10)
        
        for key, line_edit in self.main_window.folder_config.items():
            label_text = key.replace("folder_", "").replace("_", " ")
            label_text = label_text.capitalize()
            form.addRow(QLabel(label_text + ":"), line_edit)
            line_edit.textChanged.connect(self.main_window.update_preview)
        
        self.setLayout(form)


# ====================== MainWindow ======================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Structure Creator (Hardcoded or Template) + Nuke Script")
        self.resize(800, 600)
        
        # Hardcoded config
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
        
        # Template approach
        self.template_folder = None
        self.template_paths = []
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # 1) Structure Tab
        self.tab_structure = QWidget()
        self.tab_widget.addTab(self.tab_structure, "Structure")
        
        # 2) Folder Names Tab
        self.tab_folders = FolderNamesTab(self)
        self.tab_widget.addTab(self.tab_folders, "Folder Names")
        
        self.build_structure_tab()
    
    def build_structure_tab(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        
        # -------------- Show Name Row --------------
        row_show = QHBoxLayout()
        lbl_show = QLabel("Show Name:")
        self.edit_show_name = QLineEdit()
        self.edit_show_name.setPlaceholderText("Project name (max 25 chars)")
        self.edit_show_name.setMaxLength(25)
        row_show.addWidget(lbl_show)
        row_show.addWidget(self.edit_show_name)
        main_layout.addLayout(row_show)
        
        # -------------- Destination Folder --------------
        row_dest = QHBoxLayout()
        lbl_dest = QLabel("Destination Folder:")
        self.edit_destination = QLineEdit()
        self.btn_browse_dest = QPushButton("Browse...")
        row_dest.addWidget(lbl_dest)
        row_dest.addWidget(self.edit_destination)
        row_dest.addWidget(self.btn_browse_dest)
        main_layout.addLayout(row_dest)
        
        # -------------- Creation Mode --------------
        row_mode = QHBoxLayout()
        lbl_mode = QLabel("Creation Mode:")
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Hardcoded")
        self.combo_mode.addItem("Template")
        row_mode.addWidget(lbl_mode)
        row_mode.addWidget(self.combo_mode)
        main_layout.addLayout(row_mode)
        
        # -------------- Template Folder --------------
        row_template = QHBoxLayout()
        lbl_template = QLabel("Template Folder:")
        self.edit_template_folder = QLineEdit()
        self.btn_browse_template = QPushButton("Browse...")
        row_template.addWidget(lbl_template)
        row_template.addWidget(self.edit_template_folder)
        row_template.addWidget(self.btn_browse_template)
        main_layout.addLayout(row_template)
        
        # -------------- Res / FPS / Proxy / ACES --------------
        # Row for resolution preset + width/height
        row_res = QHBoxLayout()
        lbl_res_presets = QLabel("Resolution Preset:")
        self.combo_res_presets = QComboBox()
        self.combo_res_presets.addItem("Custom")
        # Known resolutions
        self.presets = {
            "HD 1920x1080": (1920, 1080, "HD_1080"),
            "UHD_4K 3840x2160": (3840, 2160, "UHD_4K"),
            "4K_Super_35 4096x3112": (4096, 3112, "4K_Super_35"),
            "4K_DCP 4096x2160": (4096, 2160, "4K_DCP"),
            "4K_square 4096x4096": (4096, 4096, "4K_square"),
            "4K_Sphere 4000x4000": (4000, 4000, "4K_Sphere"),
            "8K_Sphere 8000x8000": (8000, 8000, "8K_Sphere"),
            "10K_Sphere 10000x10000": (10000, 10000, "10K_Sphere"),
            "12K_Sphere 12000x12000": (12000, 12000, "12K_Sphere")
        }
        for name in self.presets.keys():
            self.combo_res_presets.addItem(name)
        
        lbl_width = QLabel("Width:")
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 20000)
        self.spin_width.setValue(1920)
        lbl_height = QLabel("Height:")
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 20000)
        self.spin_height.setValue(1080)
        
        row_res.addWidget(lbl_res_presets)
        row_res.addWidget(self.combo_res_presets)
        row_res.addWidget(lbl_width)
        row_res.addWidget(self.spin_width)
        row_res.addWidget(lbl_height)
        row_res.addWidget(self.spin_height)
        
        main_layout.addLayout(row_res)
        
        # Row for FPS
        row_fps = QHBoxLayout()
        lbl_fps = QLabel("FPS:")
        self.combo_fps = QComboBox()
        known_fps = ["23.976","24","25","29.97","30","50","59.94","60","120"]
        for f in known_fps:
            self.combo_fps.addItem(f)
        row_fps.addWidget(lbl_fps)
        row_fps.addWidget(self.combo_fps)
        main_layout.addLayout(row_fps)
        
        # Row for Proxy / ACES checkboxes
        row_proxy_aces = QHBoxLayout()
        self.chk_proxy = QCheckBox("Use Proxies")
        self.chk_aces = QCheckBox("Use ACES Workflow")
        row_proxy_aces.addWidget(self.chk_proxy)
        row_proxy_aces.addWidget(self.chk_aces)
        main_layout.addLayout(row_proxy_aces)
        
        # Connect resolution/fps changes
        self.combo_res_presets.currentIndexChanged.connect(self.on_res_preset_changed)
        self.spin_width.valueChanged.connect(self.update_preview)
        self.spin_height.valueChanged.connect(self.update_preview)
        self.combo_fps.currentIndexChanged.connect(self.update_preview)
        self.chk_proxy.stateChanged.connect(self.update_preview)
        self.chk_aces.stateChanged.connect(self.update_preview)
        
        # -------------- Sequence/Shot Scroll --------------
        self.sequence_container = SequenceListContainer(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sequence_container)
        main_layout.addWidget(self.scroll_area)
        
        # -------------- Preview --------------
        lbl_preview = QLabel("Preview of Folder Structure:")
        main_layout.addWidget(lbl_preview)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        main_layout.addWidget(self.preview_text)
        
        # -------------- Create Button --------------
        self.btn_create = QPushButton("Create Folder Structure")
        main_layout.addWidget(self.btn_create)
        
        # Connect
        self.btn_browse_dest.clicked.connect(self.on_browse_dest)
        self.btn_browse_template.clicked.connect(self.on_browse_template)
        self.btn_create.clicked.connect(self.on_create)
        
        self.edit_show_name.textChanged.connect(self.update_preview)
        self.edit_destination.textChanged.connect(self.update_preview)
        self.combo_mode.currentIndexChanged.connect(self.update_preview)
        
        # Start with 1 sequence
        self.sequence_container.add_sequence()
        
        self.tab_structure.setLayout(main_layout)
    
    # ============== Resolution Preset Handler ==============
    def on_res_preset_changed(self):
        preset = self.combo_res_presets.currentText()
        if preset in self.presets:
            w, h, _label = self.presets[preset]
            self.spin_width.setValue(w)
            self.spin_height.setValue(h)
        self.update_preview()
    
    # ============== Browsing ==============
    def on_browse_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.edit_destination.setText(folder)
        self.update_preview()
    
    def on_browse_template(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Template Folder")
        if folder:
            self.edit_template_folder.setText(folder)
            self.template_folder = folder
            self.template_paths = self.read_template_structure(folder)
        self.update_preview()
    
    def read_template_structure(self, base_path):
        collected = []
        for root, dirs, files in os.walk(base_path):
            rel = os.path.relpath(root, base_path)
            if rel == ".":
                continue
            collected.append(rel.replace("\\", "/"))
        return collected
    
    # ============== on_create ==============
    def on_create(self):
        show_name = self.edit_show_name.text().strip()
        dest = self.edit_destination.text().strip()
        
        if not show_name:
            QMessageBox.warning(self, "Warning", "Please enter a valid Show Name.")
            return
        if not dest or not os.path.isdir(dest):
            QMessageBox.warning(self, "Warning", "Please choose a valid Destination Folder.")
            return
        
        final_show_name = f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        sequences_and_shots = self.sequence_container.get_all_sequences_and_shots()
        
        # gather nuke script settings
        fps_str = self.combo_fps.currentText()
        try:
            fps_val = float(fps_str)
        except ValueError:
            fps_val = 24.0
        width_val = self.spin_width.value()
        height_val = self.spin_height.value()
        use_proxy = self.chk_proxy.isChecked()
        use_aces = self.chk_aces.isChecked()
        
        # build a resolution label if it matches a known preset
        resolution_label = f"Custom_{width_val}x{height_val}"
        for nm, (pw, ph, lbl) in self.presets.items():
            if pw == width_val and ph == height_val:
                resolution_label = lbl
                break
        
        mode = self.combo_mode.currentText()
        
        try:
            # Step 1) Create the folder structure
            if mode == "Hardcoded":
                self.create_hardcoded_structure(final_show_name, dest, sequences_and_shots)
            else:
                if not self.template_folder or not os.path.isdir(self.template_folder):
                    QMessageBox.warning(self, "Warning", "Please select a valid Template Folder for Template mode.")
                    return
                self.create_template_structure(final_show_name, dest, sequences_and_shots)
            
            # Step 2) Create the Nuke scripts in 05_comp
            self.create_nuke_scripts_05_comp(
                final_show_name, dest,
                sequences_and_shots,
                fps_val, width_val, height_val,
                resolution_label, use_proxy, use_aces
            )
            
            QMessageBox.information(self, "Success", "Folders and Nuke scripts created successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    # ============== Hardcoded Structure ==============
    def get_folder_name(self, key):
        return self.folder_config[key].text().strip()
    
    def create_hardcoded_structure(self, show_name, destination, sequences_and_shots):
        """
        Same logic as before, building 01_plates, 02_support, etc.
        plus subfolders for each sequence/shot in e.g. 01_plates, 04_vfx, 05_comp, etc.
        """
        show_root = os.path.join(destination, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        # main subfolders
        f_plates = os.path.join(show_root, self.get_folder_name("folder_01_plates"))
        f_support = os.path.join(show_root, self.get_folder_name("folder_02_support"))
        f_references = os.path.join(show_root, self.get_folder_name("folder_03_references"))
        f_vfx = os.path.join(show_root, self.get_folder_name("folder_04_vfx"))
        f_comp = os.path.join(show_root, self.get_folder_name("folder_05_comp"))
        f_mograph = os.path.join(show_root, self.get_folder_name("folder_06_mograph"))
        f_shared = os.path.join(show_root, self.get_folder_name("folder_07_shared"))
        f_out = os.path.join(show_root, self.get_folder_name("folder_08_output"))
        
        os.makedirs(f_plates, exist_ok=True)
        os.makedirs(f_support, exist_ok=True)
        os.makedirs(f_references, exist_ok=True)
        os.makedirs(f_vfx, exist_ok=True)
        os.makedirs(f_comp, exist_ok=True)
        os.makedirs(f_mograph, exist_ok=True)
        os.makedirs(f_shared, exist_ok=True)
        os.makedirs(f_out, exist_ok=True)
        
        # 01_plates
        aspera_dir = os.path.join(f_plates, self.get_folder_name("folder_01_plates_aspera"))
        os.makedirs(aspera_dir, exist_ok=True)
        manifest = os.path.join(f_plates, self.get_folder_name("folder_01_plates_manifest"))
        if not os.path.isfile(manifest):
            with open(manifest, "w") as mf:
                mf.write("Plate manifest placeholder\n")
        
        # put seq/shots under 01_plates
        for seq_info in sequences_and_shots:
            seq = seq_info['sequence']
            seq_dir = os.path.join(f_plates, seq)
            os.makedirs(seq_dir, exist_ok=True)
            for s in seq_info['shots']:
                os.makedirs(os.path.join(seq_dir, s), exist_ok=True)
        
        # 02_support
        luts_dir = os.path.join(f_support, self.get_folder_name("folder_02_support_luts"))
        cam_lut_dir = os.path.join(luts_dir, self.get_folder_name("folder_02_support_luts_camera"))
        show_lut_dir = os.path.join(luts_dir, self.get_folder_name("folder_02_support_luts_show"))
        edl_dir = os.path.join(f_support, self.get_folder_name("folder_02_support_edl_xml"))
        guides_dir = os.path.join(f_support, self.get_folder_name("folder_02_support_guides"))
        cam_data = os.path.join(f_support, self.get_folder_name("folder_02_support_camera_data"))
        
        os.makedirs(luts_dir, exist_ok=True)
        os.makedirs(cam_lut_dir, exist_ok=True)
        os.makedirs(show_lut_dir, exist_ok=True)
        os.makedirs(edl_dir, exist_ok=True)
        os.makedirs(guides_dir, exist_ok=True)
        os.makedirs(cam_data, exist_ok=True)
        
        # 03_references
        client_brief = os.path.join(f_references, self.get_folder_name("folder_03_references_client_brief"))
        artw = os.path.join(f_references, self.get_folder_name("folder_03_references_artwork"))
        style_guides = os.path.join(f_references, self.get_folder_name("folder_03_references_style_guides"))
        os.makedirs(client_brief, exist_ok=True)
        os.makedirs(artw, exist_ok=True)
        os.makedirs(style_guides, exist_ok=True)
        
        # 04_vfx => [sequence]/[shot]/(project, render)
        for seq_info in sequences_and_shots:
            seq = seq_info['sequence']
            seq_vfx = os.path.join(f_vfx, seq)
            os.makedirs(seq_vfx, exist_ok=True)
            for s in seq_info['shots']:
                shot_vfx = os.path.join(seq_vfx, s)
                os.makedirs(shot_vfx, exist_ok=True)
                proj_dir = os.path.join(shot_vfx, "project")
                rend_dir = os.path.join(shot_vfx, "render")
                os.makedirs(proj_dir, exist_ok=True)
                os.makedirs(rend_dir, exist_ok=True)
        
        # 05_comp => [sequence]/[shot]/(project, render)
        for seq_info in sequences_and_shots:
            seq = seq_info['sequence']
            seq_comp = os.path.join(f_comp, seq)
            os.makedirs(seq_comp, exist_ok=True)
            for s in seq_info['shots']:
                shot_comp = os.path.join(seq_comp, s)
                os.makedirs(shot_comp, exist_ok=True)
                proj_dir = os.path.join(shot_comp, "project")
                rend_dir = os.path.join(shot_comp, "render")
                os.makedirs(proj_dir, exist_ok=True)
                os.makedirs(rend_dir, exist_ok=True)
        
        # 06_mograph
        mg_proj = os.path.join(f_mograph, self.get_folder_name("folder_06_mograph_projects"))
        mg_rend = os.path.join(f_mograph, self.get_folder_name("folder_06_mograph_render"))
        os.makedirs(mg_proj, exist_ok=True)
        os.makedirs(mg_rend, exist_ok=True)
        
        # 07_shared
        stock = os.path.join(f_shared, self.get_folder_name("folder_07_shared_stock_footage"))
        gfx = os.path.join(f_shared, self.get_folder_name("folder_07_shared_graphics"))
        fnts = os.path.join(f_shared, self.get_folder_name("folder_07_shared_fonts"))
        tmpl = os.path.join(f_shared, self.get_folder_name("folder_07_shared_templates"))
        os.makedirs(stock, exist_ok=True)
        os.makedirs(gfx, exist_ok=True)
        os.makedirs(fnts, exist_ok=True)
        os.makedirs(tmpl, exist_ok=True)
        
        # 08_output
        out_date = os.path.join(f_out, self.get_folder_name("folder_08_output_date"))
        os.makedirs(out_date, exist_ok=True)
        full_res = os.path.join(out_date, self.get_folder_name("folder_08_output_full_res"))
        proxy = os.path.join(out_date, self.get_folder_name("folder_08_output_proxy"))
        os.makedirs(full_res, exist_ok=True)
        os.makedirs(proxy, exist_ok=True)
    
    # ============== Template Structure ==============
    def create_template_structure(self, show_name, destination, sequences_and_shots):
        """
        Recreate the subfolders from self.template_paths (expanding [sequence] / [shot]).
        Then you might still create a 05_comp structure for each shot if you like,
        but we do that in create_nuke_scripts_05_comp to ensure it's there.
        """
        show_root = os.path.join(destination, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        for rel_path in self.template_paths:
            if "[sequence]" in rel_path or "[shot]" in rel_path:
                for seq_info in sequences_and_shots:
                    seq = seq_info['sequence']
                    for s in seq_info['shots']:
                        sub = rel_path.replace("[sequence]", seq)
                        sub = sub.replace("[shot]", s)
                        final_path = os.path.join(show_root, sub)
                        os.makedirs(final_path, exist_ok=True)
            else:
                final_path = os.path.join(show_root, rel_path)
                os.makedirs(final_path, exist_ok=True)
    
    # ============== Create Nuke Scripts ==============
    def create_nuke_scripts_05_comp(
        self, show_name, destination, sequences_and_shots,
        fps_val, width_val, height_val, resolution_label, use_proxy, use_aces
    ):
        """
        For each shot, create the .nk script in:
          05_comp/[sequence]/[shot]/project/[sequence]_[shot]_comp_v001.nk
        using the advanced ACES/proxy/fps logic from prior examples.
        """
        comp_folder = self.get_folder_name("folder_05_comp")
        show_root = os.path.join(destination, show_name)
        comp_root = os.path.join(show_root, comp_folder)
        
        # Ensure base comp root exists
        os.makedirs(comp_root, exist_ok=True)
        
        for seq_info in sequences_and_shots:
            seq = seq_info['sequence']
            seq_dir = os.path.join(comp_root, seq)
            for s in seq_info['shots']:
                project_dir = os.path.join(seq_dir, s, "project")
                os.makedirs(project_dir, exist_ok=True)
                
                nk_name = f"{seq}_{s}_comp_v001.nk"
                nk_path = os.path.join(project_dir, nk_name)
                
                script_text = self.build_nuke_script_template(
                    seq, s,
                    fps_val, width_val, height_val, resolution_label,
                    use_proxy, use_aces
                )
                
                with open(nk_path, "w", encoding="utf-8") as f:
                    f.write(script_text)
    
    def build_nuke_script_template(
        self, seq_name, shot_name,
        fps, width, height, resolution_label,
        use_proxy, use_aces
    ):
        """
        Incorporates format, fps, proxy, ACES color management, etc.
        (Adapted from prior examples.)
        """
        define_window_layout = """define_window_layout_xml {<?xml version="1.0" encoding="UTF-8"?>
<layout version="1.0">
    <window x="-1" y="-8" w="2560" h="1369" maximized="1" screen="0">
        <splitter orientation="1">
            <split size="53"/>
            <dock id="" hideTitles="1" activePageId="Toolbar.1">
                <page id="Toolbar.1"/>
            </dock>
            <split size="1895"/>
            <splitter orientation="2">
                <split size="1328"/>
                <dock id="" activePageId="DAG.1" focus="true">
                    <page id="Curve Editor.1"/>
                    <page id="DopeSheet.1"/>
                    <page id="DAG.1"/>
                </dock>
            </splitter>
            <split size="604"/>
            <splitter orientation="2">
                <split size="1127"/>
                <dock id="" activePageId="Properties.1">
                    <page id="Properties.1"/>
                </dock>
                <split size="197"/>
                <dock id="" activePageId="Progress.1">
                    <page id="Progress.1"/>
                </dock>
            </splitter>
        </splitter>
    </window>
    <window x="2560" y="-8" w="2560" h="1417" maximized="1" screen="1">
        <splitter orientation="2">
            <split size="1417"/>
            <dock id="" activePageId="Viewer.1">
                <page id="Viewer.1"/>
            </dock>
        </splitter>
    </window>
</layout>
}"""
        
        # Root start
        root_start = f"""Root {{
 inputs 0
 name {seq_name}_{shot_name}_comp_v001.nk
 fps {fps:.3f}
 format "{width} {height} 0 0 {width} {height} 1 {resolution_label}"
"""
        # Proxy lines
        if use_proxy:
            proxy_lines = """ proxy_format "4000 4000 0 0 4000 4000 1 4K Proxy LL180 Sphere"
 proxySetting always"""
        else:
            proxy_lines = """ proxy_type scale
 proxy_format "1024 778 0 0 1024 778 1 1K_Super_35(full-ap)" """
        
        # ACES lines
        if use_aces:
            color_lines = """ colorManagement OCIO
 OCIO_config aces_1.2
 defaultViewerLUT "OCIO LUTs"
 workingSpaceLUT scene_linear
 monitorLut "sRGB (ACES)"
 monitorOutLUT "sRGB (ACES)"
 int8Lut matte_paint
 int16Lut texture_paint
 logLut compositing_log
 floatLut scene_linear"""
        else:
            color_lines = """ colorManagement Nuke
 workingSpaceLUT linear
 monitorLut sRGB
 monitorOutLUT rec709
 int8Lut sRGB
 int16Lut sRGB
 logLut Cineon
 floatLut linear"""
        
        root_block = (
            f"{root_start}"
            f"{proxy_lines}\n"
            f"{color_lines}\n"
            f"}}\n"
        )
        
        # Viewer node
        viewer_block = f"""Viewer {{
 inputs 0
 frame 1
 frame_range 1-100
 fps {fps:.8f}
 name Viewer1
 xpos -40
 ypos -9
}}"""
        
        script_text = f"""#! C:/Program Files/Nuke15.1v5/nuke-15.1.5.dll -nx
version 15.1 v5
{define_window_layout}
{root_block}
{viewer_block}
"""
        return script_text
    
    # ============== Real-Time Preview ==============
    
    def update_preview(self):
        """
        If Hardcoded -> build a mini-tree of 01_plates, 02_support, etc.
        If Template -> show a 'dry-run' of the template subfolders, expanding [sequence]/[shot].
        Also mention the .nk script creation in 05_comp.
        """
        show_name = self.edit_show_name.text().strip()
        dest = self.edit_destination.text().strip()
        
        if not show_name or not dest:
            self.preview_text.setPlainText("Please enter Show Name and Destination to see a preview.")
            return
        
        final_show_name = f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        mode = self.combo_mode.currentText()
        
        lines = []
        lines.append(f"Destination: {os.path.join(dest, final_show_name)}")
        lines.append(f"Mode: {mode}")
        
        # Nuke script settings
        fps_str = self.combo_fps.currentText()
        lines.append(f"FPS: {fps_str}")
        w = self.spin_width.value()
        h = self.spin_height.value()
        lines.append(f"Resolution: {w}x{h}")
        lines.append(f"Use Proxies? {self.chk_proxy.isChecked()}")
        lines.append(f"Use ACES? {self.chk_aces.isChecked()}")
        
        # Sequences
        seq_shots = self.sequence_container.get_all_sequences_and_shots()
        
        if mode == "Hardcoded":
            # Build an ASCII tree of the folder structure
            lines.append("")
            lines.append("Hardcoded Folder Structure Preview:")
            lines.extend(self.build_preview_hardcoded(seq_shots))
        else:
            # Template folder
            if not self.template_folder:
                lines.append("")
                lines.append("No Template Folder selected.")
            else:
                lines.append("")
                lines.append(f"Template Folder: {self.template_folder}")
                
                if self.template_paths:
                    lines.append("Preview (expanding [sequence]/[shot]):")
                    for rel_path in self.template_paths:
                        if "[sequence]" in rel_path or "[shot]" in rel_path:
                            for sdict in seq_shots:
                                seq = sdict['sequence']
                                for s in sdict['shots']:
                                    sub = rel_path.replace("[sequence]", seq)
                                    sub = sub.replace("[shot]", s)
                                    lines.append(f"  {sub}")
                        else:
                            lines.append(f"  {rel_path}")
                else:
                    lines.append("No subfolders found in template or invalid folder.")
            
            # Also mention the .nk script creation
            lines.append("")
            lines.append("Will also create .nk scripts in 05_comp/[sequence]/[shot]/project.")
        
        self.preview_text.setPlainText("\n".join(lines))
    
    def build_preview_hardcoded(self, sequences_and_shots):
        """
        Return lines for the ASCII folder structure (like older versions),
        including the note about .nk scripts in 05_comp.
        """
        lines = []
        # short references
        f_plates = self.get_folder_name("folder_01_plates")
        f_aspera = self.get_folder_name("folder_01_plates_aspera")
        f_manifest = self.get_folder_name("folder_01_plates_manifest")
        
        f_support = self.get_folder_name("folder_02_support")
        f_luts = self.get_folder_name("folder_02_support_luts")
        f_luts_cam = self.get_folder_name("folder_02_support_luts_camera")
        f_luts_show = self.get_folder_name("folder_02_support_luts_show")
        f_edl = self.get_folder_name("folder_02_support_edl_xml")
        f_guides = self.get_folder_name("folder_02_support_guides")
        f_camdata = self.get_folder_name("folder_02_support_camera_data")
        
        f_ref = self.get_folder_name("folder_03_references")
        f_client = self.get_folder_name("folder_03_references_client_brief")
        f_art = self.get_folder_name("folder_03_references_artwork")
        f_style = self.get_folder_name("folder_03_references_style_guides")
        
        f_vfx = self.get_folder_name("folder_04_vfx")
        f_comp = self.get_folder_name("folder_05_comp")
        
        f_mg = self.get_folder_name("folder_06_mograph")
        f_mg_proj = self.get_folder_name("folder_06_mograph_projects")
        f_mg_rend = self.get_folder_name("folder_06_mograph_render")
        
        f_sh = self.get_folder_name("folder_07_shared")
        f_stock = self.get_folder_name("folder_07_shared_stock_footage")
        f_graph = self.get_folder_name("folder_07_shared_graphics")
        f_fonts = self.get_folder_name("folder_07_shared_fonts")
        f_templ = self.get_folder_name("folder_07_shared_templates")
        
        f_out = self.get_folder_name("folder_08_output")
        f_out_date = self.get_folder_name("folder_08_output_date")
        f_out_full = self.get_folder_name("folder_08_output_full_res")
        f_out_proxy = self.get_folder_name("folder_08_output_proxy")
        
        lines.append(f"├── {f_plates}/")
        lines.append(f"│   ├── {f_aspera}/")
        
        # sequences/shots
        for i, seq_info in enumerate(sequences_and_shots):
            seq = seq_info['sequence']
            shots = seq_info['shots']
            seq_prefix = "│   ├──"
            if i == len(sequences_and_shots) - 1:
                seq_prefix = "│   └──"
            lines.append(f"{seq_prefix} {seq}/")
            for j, shot in enumerate(shots):
                shot_prefix = "│   │   ├──"
                if j == len(shots) - 1:
                    shot_prefix = "│   │   └──"
                lines.append(f"{shot_prefix} {shot}/")
        
        lines.append(f"│   └── {f_manifest}")
        lines.append("│")
        
        lines.append(f"├── {f_support}/")
        lines.append(f"│   ├── {f_luts}/")
        lines.append(f"│   │   ├── {f_luts_cam}/")
        lines.append(f"│   │   └── {f_luts_show}/")
        lines.append(f"│   ├── {f_edl}/")
        lines.append(f"│   ├── {f_guides}/")
        lines.append(f"│   └── {f_camdata}/")
        lines.append("│")
        
        lines.append(f"├── {f_ref}/")
        lines.append(f"│   ├── {f_client}/")
        lines.append(f"│   ├── {f_art}/")
        lines.append(f"│   └── {f_style}/")
        lines.append("│")
        
        # 04_vfx
        lines.append(f"├── {f_vfx}/")
        for i, seq_info in enumerate(sequences_and_shots):
            seq = seq_info['sequence']
            lines.append(f"│   └── {seq}/")
            for shot in seq_info['shots']:
                lines.append(f"│       └── {shot}/")
                lines.append(f"│           ├── project/")
                lines.append(f"│           └── render/")
        lines.append("│")
        
        # 05_comp
        lines.append(f"├── {f_comp}/")
        for i, seq_info in enumerate(sequences_and_shots):
            seq = seq_info['sequence']
            lines.append(f"│   └── {seq}/")
            for shot in seq_info['shots']:
                lines.append(f"│       └── {shot}/")
                lines.append(f"│           ├── project/   (Nuke script here)")
                lines.append(f"│           └── render/")
        lines.append("│")
        
        # 06_mograph
        lines.append(f"├── {f_mg}/")
        lines.append(f"│   ├── {f_mg_proj}/")
        lines.append(f"│   └── {f_mg_rend}/")
        lines.append("│")
        
        # 07_shared
        lines.append(f"├── {f_sh}/")
        lines.append(f"│   ├── {f_stock}/")
        lines.append(f"│   ├── {f_graph}/")
        lines.append(f"│   ├── {f_fonts}/")
        lines.append(f"│   └── {f_templ}/")
        lines.append("│")
        
        # 08_output
        lines.append(f"└── {f_out}/")
        lines.append(f"    └── {f_out_date}/")
        lines.append(f"        ├── {f_out_full}/")
        lines.append(f"        └── {f_out_proxy}/")
        
        lines.append("")
        lines.append("Also creates a .nk script in 05_comp/[sequence]/[shot]/project/ named:")
        lines.append("[sequence]_[shot]_comp_v001.nk, with advanced fps/proxy/aces settings.")
        return lines


def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
