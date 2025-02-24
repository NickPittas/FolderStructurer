import sys
import os
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog, QTextEdit,
    QMessageBox, QScrollArea, QFrame, QComboBox, QCheckBox,
    QSpinBox, QFormLayout, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt

def apply_dark_theme(app):
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
    QScrollArea, QTreeWidget {
        background-color: #2e2e2e;
    }
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

# =========== Shot/Sequence Widgets ===========

class ShotWidget(QWidget):
    def __init__(self, parent_sequence_widget):
        super().__init__()
        self.parent_sequence_widget = parent_sequence_widget
        
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        
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
        
        self.btn_remove_shot.clicked.connect(self.remove_self)
        self.btn_add_shot.clicked.connect(self.add_shot_below)
        
        # Update preview (Tab 1) on text change
        self.shot_name_edit.textChanged.connect(
            self.parent_sequence_widget.parent_main_window.update_preview
        )
    
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
        self.main_layout.setContentsMargins(0,0,0,0)
        
        self.header_layout = QHBoxLayout()
        self.header_layout.setSpacing(0)
        self.header_layout.setContentsMargins(0,0,0,0)
        
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
        self.shots_layout.setContentsMargins(16,0,0,0)
        
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.shots_layout)
        
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(sep)
        
        self.setLayout(self.main_layout)
        
        self.btn_remove_sequence.clicked.connect(self.remove_self)
        self.btn_add_sequence.clicked.connect(self.add_new_sequence_below)
        self.sequence_name_edit.textChanged.connect(
            self.parent_main_window.update_preview
        )
        
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
        results = []
        for i in range(self.shots_layout.count()):
            item = self.shots_layout.itemAt(i)
            w = item.widget()
            if isinstance(w, ShotWidget):
                nm = w.get_shot_name()
                if nm:
                    results.append(nm)
        return results

class SequenceListContainer(QWidget):
    def __init__(self, parent_main_window):
        super().__init__()
        self.parent_main_window = parent_main_window
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
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


# ---------------- Folder Names Tab (Hardcoded) ----------------

class FolderNamesTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        form = QFormLayout()
        form.setSpacing(5)
        form.setContentsMargins(10,10,10,10)
        
        for key, line_edit in self.main_window.folder_config.items():
            label_txt = key.replace("folder_","").replace("_"," ")
            label_txt = label_txt.capitalize()
            lbl = QLabel(label_txt + ":")
            form.addRow(lbl, line_edit)
            line_edit.textChanged.connect(self.main_window.update_preview)
        
        self.setLayout(form)


# --------------- Tab 3: Add to Existing Project ---------------

class AddToExistingProjectTab(QWidget):
    """
    This tab:
     - existing project folder
     - "Create Nuke Script under comp"
     - resolution/fps/proxy/aces
     - QTreeWidget with checkable subfolders
     - SequenceListContainer
     - preview
     - "Execute" button
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10,10,10,10)
        self.setLayout(self.layout)
        
        # 1) Existing Project Folder
        row_proj= QHBoxLayout()
        lbl_proj= QLabel("Existing Project Folder:")
        self.edit_project_folder= QLineEdit()
        self.btn_browse_proj= QPushButton("Browse...")
        row_proj.addWidget(lbl_proj)
        row_proj.addWidget(self.edit_project_folder)
        row_proj.addWidget(self.btn_browse_proj)
        self.layout.addLayout(row_proj)
        
        # 2) "Create Nuke Script under comp"
        self.chk_create_nk_under_comp= QCheckBox("Create Nuke Script under comp")
        self.layout.addWidget(self.chk_create_nk_under_comp)
        
        # 3) Resolution / FPS / Proxy / ACES
        row_res= QHBoxLayout()
        lbl_rp= QLabel("Resolution Preset:")
        self.combo_res_presets= QComboBox()
        self.combo_res_presets.addItem("Custom")
        self.res_presets= {
            "HD 1920x1080": (1920,1080,"HD_1080"),
            "4K_Super_35 4096x3112": (4096,3112,"4K_Super_35")
        }
        for nm in self.res_presets.keys():
            self.combo_res_presets.addItem(nm)
        
        lbl_w= QLabel("Width:")
        self.spin_width= QSpinBox()
        self.spin_width.setRange(1,20000)
        self.spin_width.setValue(1920)
        lbl_h= QLabel("Height:")
        self.spin_height= QSpinBox()
        self.spin_height.setRange(1,20000)
        self.spin_height.setValue(1080)
        
        row_res.addWidget(lbl_rp)
        row_res.addWidget(self.combo_res_presets)
        row_res.addWidget(lbl_w)
        row_res.addWidget(self.spin_width)
        row_res.addWidget(lbl_h)
        row_res.addWidget(self.spin_height)
        
        self.layout.addLayout(row_res)
        
        row_fps= QHBoxLayout()
        lbl_fps= QLabel("FPS:")
        self.combo_fps= QComboBox()
        known_fps = ["23.976","24","25","29.97","30","50","59.94","60","120"]
        for ff in known_fps:
            self.combo_fps.addItem(ff)
        row_fps.addWidget(lbl_fps)
        row_fps.addWidget(self.combo_fps)
        self.layout.addLayout(row_fps)
        
        row_proxy_aces= QHBoxLayout()
        self.chk_proxy= QCheckBox("Use Proxies")
        self.chk_aces= QCheckBox("Use ACES Workflow")
        row_proxy_aces.addWidget(self.chk_proxy)
        row_proxy_aces.addWidget(self.chk_aces)
        self.layout.addLayout(row_proxy_aces)
        
        # 4) QTreeWidget
        self.tree= QTreeWidget()
        self.tree.setHeaderLabel("Folders in Existing Project (Check to add Seq/Shots)")
        self.layout.addWidget(self.tree)
        
        # 5) SequenceListContainer
        self.seq_container= SequenceListContainer(self.main_window)
        self.seq_container.add_sequence()  # so user sees one sequence by default
        scroll_seq= QScrollArea()
        scroll_seq.setWidgetResizable(True)
        scroll_seq.setWidget(self.seq_container)
        self.layout.addWidget(scroll_seq)
        
        # 6) Preview
        lbl_preview= QLabel("Preview of changes:")
        self.text_preview= QTextEdit()
        self.text_preview.setReadOnly(True)
        self.layout.addWidget(lbl_preview)
        self.layout.addWidget(self.text_preview)
        
        # 7) Execute
        self.btn_execute= QPushButton("Add Folders & Shots")
        self.layout.addWidget(self.btn_execute)
        
        # Connect
        self.btn_browse_proj.clicked.connect(self.on_browse_project)
        self.btn_execute.clicked.connect(self.on_execute)
        
        self.combo_res_presets.currentIndexChanged.connect(self.on_res_preset_changed)
        self.spin_width.valueChanged.connect(self.update_preview_tab3)
        self.spin_height.valueChanged.connect(self.update_preview_tab3)
        self.combo_fps.currentIndexChanged.connect(self.update_preview_tab3)
        self.chk_proxy.stateChanged.connect(self.update_preview_tab3)
        self.chk_aces.stateChanged.connect(self.update_preview_tab3)
    
    def on_browse_project(self):
        folder= QFileDialog.getExistingDirectory(self, "Select Existing Project Folder")
        if folder:
            self.edit_project_folder.setText(folder)
            self.populate_tree(folder)
        self.update_preview_tab3()
    
    def populate_tree(self, project_folder):
        self.tree.clear()
        if not os.path.isdir(project_folder):
            return
        for root, dirs, files in os.walk(project_folder):
            rel = os.path.relpath(root, project_folder)
            if rel==".":
                continue
            segments= rel.split(os.path.sep)
            
            parent_item= self.tree.invisibleRootItem()
            current_path=[]
            for seg in segments:
                current_path.append(seg)
                partial_rel= os.path.join(*current_path)
                found=None
                for i in range(parent_item.childCount()):
                    c= parent_item.child(i)
                    if c.data(0, Qt.UserRole)== partial_rel:
                        found=c
                        parent_item=c
                        break
                if not found:
                    new_item= QTreeWidgetItem([seg])
                    new_item.setData(0, Qt.UserRole, partial_rel)
                    new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable)
                    new_item.setCheckState(0, Qt.Unchecked)
                    parent_item.addChild(new_item)
                    parent_item= new_item
        self.tree.expandAll()
    
    def on_res_preset_changed(self):
        sel= self.combo_res_presets.currentText()
        if sel in self.res_presets:
            w,h,lbl= self.res_presets[sel]
            self.spin_width.setValue(w)
            self.spin_height.setValue(h)
        self.update_preview_tab3()
    
    def update_preview_tab3(self):
        lines=[]
        
        proj_folder= self.edit_project_folder.text().strip()
        if not proj_folder or not os.path.isdir(proj_folder):
            lines.append("No valid existing project folder selected.")
            self.text_preview.setPlainText("\n".join(lines))
            return
        
        lines.append(f"Existing Project => {proj_folder}")
        lines.append(f"Create Nuke Script under comp => {self.chk_create_nk_under_comp.isChecked()}")
        
        w_val= self.spin_width.value()
        h_val= self.spin_height.value()
        res_label= f"Custom_{w_val}x{h_val}"
        sel_rp= self.combo_res_presets.currentText()
        if sel_rp in self.res_presets:
            pw,ph,plbl= self.res_presets[sel_rp]
            if w_val==pw and h_val==ph:
                res_label= plbl
        lines.append(f"Resolution => {w_val}x{h_val} ({res_label})")
        lines.append(f"FPS => {self.combo_fps.currentText()}, Proxy => {self.chk_proxy.isChecked()}, ACES => {self.chk_aces.isChecked()}")
        
        # which folders are checked
        checked_folders=[]
        def gather_checked(item):
            for i in range(item.childCount()):
                c= item.child(i)
                if c.checkState(0)== Qt.Checked:
                    checked_folders.append(c.data(0, Qt.UserRole))
                gather_checked(c)
        gather_checked(self.tree.invisibleRootItem())
        
        lines.append("Checked Folders =>")
        if not checked_folders:
            lines.append("  (none)")
        else:
            for cf in checked_folders:
                lines.append(f"  {cf}")
        
        # sequences/shots
        seq_data= self.seq_container.get_all_sequences_and_shots()
        lines.append("New sequences/shots =>")
        if seq_data:
            for sd in seq_data:
                lines.append(f"  Sequence='{sd['sequence']}', Shots={sd['shots']}")
        else:
            lines.append("  (none)")
        
        self.text_preview.setPlainText("\n".join(lines))
    
    def folder_or_parents_has_comp(self, folder_path, project_root):
        folder_path= os.path.abspath(folder_path)
        project_root= os.path.abspath(project_root)
        while len(folder_path) >= len(project_root):
            base= os.path.basename(folder_path).lower()
            if base.startswith("comp"):
                return True
            if folder_path == project_root:
                break
            folder_path= os.path.dirname(folder_path)
        return False
    
    def on_execute(self):
        proj_folder= self.edit_project_folder.text().strip()
        if not proj_folder or not os.path.isdir(proj_folder):
            QMessageBox.warning(self, "Warning", "No valid existing project folder.")
            return
        
        create_nk_under_comp= self.chk_create_nk_under_comp.isChecked()
        
        w_val= self.spin_width.value()
        h_val= self.spin_height.value()
        res_label= f"Custom_{w_val}x{h_val}"
        sel_rp= self.combo_res_presets.currentText()
        if sel_rp in self.res_presets:
            pw,ph,plbl= self.res_presets[sel_rp]
            if w_val==pw and h_val==ph:
                res_label= plbl
        try:
            fps_val= float(self.combo_fps.currentText())
        except:
            fps_val= 24.0
        use_proxy= self.chk_proxy.isChecked()
        use_aces= self.chk_aces.isChecked()
        
        # gather checked
        checked_items=[]
        def gather_checked(item):
            for i in range(item.childCount()):
                c= item.child(i)
                if c.checkState(0)==Qt.Checked:
                    checked_items.append(c)
                gather_checked(c)
        gather_checked(self.tree.invisibleRootItem())
        
        # sequences/shots
        seq_data= self.seq_container.get_all_sequences_and_shots()
        
        for citem in checked_items:
            relp= citem.data(0, Qt.UserRole)
            absp= os.path.join(proj_folder, relp)
            is_comp_folder= (create_nk_under_comp and self.folder_or_parents_has_comp(absp, proj_folder))
            
            for sd in seq_data:
                seqnm= sd['sequence'].strip()
                shots= [s.strip() for s in sd['shots'] if s.strip()]
                
                if seqnm:
                    seq_folder= os.path.join(absp, seqnm)
                    if os.path.exists(seq_folder):
                        QMessageBox.warning(self, "Collision",
                            f"Folder '{seqnm}' already exists under {absp}, skipping.")
                        continue
                    os.makedirs(seq_folder, exist_ok=True)
                    
                    for sh in shots:
                        shot_folder= os.path.join(seq_folder, sh)
                        if os.path.exists(shot_folder):
                            QMessageBox.warning(self, "Collision",
                                f"Shot '{sh}' already exists under {seq_folder}, skipping.")
                            continue
                        os.makedirs(shot_folder, exist_ok=True)
                        
                        if is_comp_folder:
                            prj= os.path.join(shot_folder,"project")
                            rnd= os.path.join(shot_folder,"render")
                            os.makedirs(prj,exist_ok=True)
                            os.makedirs(rnd,exist_ok=True)
                            
                            nk_name= f"{seqnm}_{sh}_comp_v001.nk"
                            nk_path= os.path.join(prj, nk_name)
                            script_txt= self.main_window.build_nuke_script_template(
                                seqnm, sh, fps_val, w_val, h_val, res_label,
                                use_proxy, use_aces
                            )
                            with open(nk_path,"w",encoding='utf-8') as ff:
                                ff.write(script_txt)
                else:
                    # no sequence => only shots
                    for sh in shots:
                        shot_folder= os.path.join(absp, sh)
                        if os.path.exists(shot_folder):
                            QMessageBox.warning(self, "Collision",
                                f"Shot '{sh}' already exists under {absp}, skipping.")
                            continue
                        os.makedirs(shot_folder, exist_ok=True)
                        
                        if is_comp_folder:
                            prj= os.path.join(shot_folder,"project")
                            rnd= os.path.join(shot_folder,"render")
                            os.makedirs(prj,exist_ok=True)
                            os.makedirs(rnd,exist_ok=True)
                            
                            nk_name= f"{sh}_comp_v001.nk"
                            nk_path= os.path.join(prj, nk_name)
                            script_txt= self.main_window.build_nuke_script_template(
                                "", sh, fps_val, w_val, h_val, res_label,
                                use_proxy, use_aces
                            )
                            with open(nk_path,"w",encoding='utf-8') as ff:
                                ff.write(script_txt)
        
        QMessageBox.information(self, "Done", "Sequences/Shots added successfully.")


# ---------------- Main Window with 3 Tabs ----------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Structurer with Hardcoded & Template, plus 'Add to Existing'")
        self.resize(900,600)
        
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
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Tab1: "Structure"
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "Structure")
        
        # Tab2: "Folder Names"
        self.tab2 = FolderNamesTab(self)
        self.tab_widget.addTab(self.tab2, "Folder Names")
        
        # Build the Tab1 UI
        self.build_structure_tab()
        
        # Tab3: "Add to Existing Project"
        self.tab3 = AddToExistingProjectTab(self)
        self.tab_widget.addTab(self.tab3, "Add to Existing Project")
    
    def build_structure_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10,10,10,10)
        
        # Show Name
        row_show = QHBoxLayout()
        lbl_show = QLabel("Show Name:")
        self.edit_show_name = QLineEdit()
        self.edit_show_name.setPlaceholderText("Project name (max 25 chars)")
        self.edit_show_name.setMaxLength(25)
        row_show.addWidget(lbl_show)
        row_show.addWidget(self.edit_show_name)
        layout.addLayout(row_show)
        
        # Destination
        row_dest = QHBoxLayout()
        lbl_dest = QLabel("Destination Folder:")
        self.edit_destination = QLineEdit()
        self.btn_browse_dest = QPushButton("Browse...")
        row_dest.addWidget(lbl_dest)
        row_dest.addWidget(self.edit_destination)
        row_dest.addWidget(self.btn_browse_dest)
        layout.addLayout(row_dest)
        
        # Creation Mode
        row_mode = QHBoxLayout()
        lbl_mode = QLabel("Creation Mode:")
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Hardcoded")
        self.combo_mode.addItem("Template")
        row_mode.addWidget(lbl_mode)
        row_mode.addWidget(self.combo_mode)
        layout.addLayout(row_mode)
        
        # Template folder
        row_template = QHBoxLayout()
        lbl_tmpl = QLabel("Template Folder:")
        self.edit_template = QLineEdit()
        self.btn_browse_template = QPushButton("Browse...")
        row_template.addWidget(lbl_tmpl)
        row_template.addWidget(self.edit_template)
        row_template.addWidget(self.btn_browse_template)
        layout.addLayout(row_template)
        
        # Res / FPS / Proxy / ACES
        row_res = QHBoxLayout()
        lbl_preset = QLabel("Resolution Preset:")
        self.combo_res_presets = QComboBox()
        self.combo_res_presets.addItem("Custom")
        
        # the known presets
        self.res_presets = {
            "HD 1920x1080": (1920,1080,"HD_1080"),
            "UHD_4K 3840x2160": (3840,2160,"UHD_4K"),
            "4K_Super_35 4096x3112": (4096,3112,"4K_Super_35"),
            "4K_DCP 4096x2160": (4096,2160,"4K_DCP"),
            "4K_square 4096x4096": (4096,4096,"4K_square"),
            "4K_Sphere 4000x4000": (4000,4000,"4K_Sphere"),
            "8K_Sphere 8000x8000": (8000,8000,"8K_Sphere"),
            "10K_Sphere 10000x10000": (10000,10000,"10K_Sphere"),
            "12K_Sphere 12000x12000": (12000,12000,"12K_Sphere")
        }
        for nm in self.res_presets.keys():
            self.combo_res_presets.addItem(nm)
        
        lbl_w = QLabel("Width:")
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1,20000)
        self.spin_width.setValue(1920)
        lbl_h = QLabel("Height:")
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1,20000)
        self.spin_height.setValue(1080)
        
        row_res.addWidget(lbl_preset)
        row_res.addWidget(self.combo_res_presets)
        row_res.addWidget(lbl_w)
        row_res.addWidget(self.spin_width)
        row_res.addWidget(lbl_h)
        row_res.addWidget(self.spin_height)
        layout.addLayout(row_res)
        
        # FPS
        row_fps = QHBoxLayout()
        lbl_fps = QLabel("FPS:")
        self.combo_fps = QComboBox()
        known_fps = ["23.976","24","25","29.97","30","50","59.94","60","120"]
        for ff in known_fps:
            self.combo_fps.addItem(ff)
        row_fps.addWidget(lbl_fps)
        row_fps.addWidget(self.combo_fps)
        layout.addLayout(row_fps)
        
        # Proxy / ACES
        row_proxy_aces = QHBoxLayout()
        self.chk_proxy = QCheckBox("Use Proxies")
        self.chk_aces = QCheckBox("Use ACES Workflow")
        row_proxy_aces.addWidget(self.chk_proxy)
        row_proxy_aces.addWidget(self.chk_aces)
        layout.addLayout(row_proxy_aces)
        
        # Sequences
        self.sequence_container = SequenceListContainer(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.sequence_container)
        layout.addWidget(self.scroll_area)
        
        # Start with 1 sequence
        self.sequence_container.add_sequence()
        
        # Preview
        lbl_prev = QLabel("Preview of Folder Structure:")
        layout.addWidget(lbl_prev)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        layout.addWidget(self.preview_text)
        
        # Create Button
        self.btn_create = QPushButton("Create Folder Structure")
        layout.addWidget(self.btn_create)
        
        self.tab1.setLayout(layout)
        
        # Connect
        self.btn_browse_dest.clicked.connect(self.on_browse_dest)
        self.btn_browse_template.clicked.connect(self.on_browse_template)
        self.btn_create.clicked.connect(self.on_create)
        
        self.edit_show_name.textChanged.connect(self.update_preview)
        self.edit_destination.textChanged.connect(self.update_preview)
        self.combo_mode.currentIndexChanged.connect(self.update_preview)
        
        self.combo_res_presets.currentIndexChanged.connect(self.on_res_preset_changed)
        self.spin_width.valueChanged.connect(self.update_preview)
        self.spin_height.valueChanged.connect(self.update_preview)
        self.combo_fps.currentIndexChanged.connect(self.update_preview)
        self.chk_proxy.stateChanged.connect(self.update_preview)
        self.chk_aces.stateChanged.connect(self.update_preview)

    # -------------- Tab1 supporting methods --------------

    def on_browse_dest(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.edit_destination.setText(folder)
        self.update_preview()

    def on_browse_template(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Template Folder")
        if folder:
            self.edit_template.setText(folder)
            self.template_folder = folder
            self.template_paths = self.read_template_structure(folder)
        self.update_preview()

    def read_template_structure(self, base_path):
        collected = []
        for root, dirs, files in os.walk(base_path):
            rel = os.path.relpath(root, base_path)
            if rel == ".":
                continue
            collected.append(rel.replace("\\","/"))
        return collected
    
    def on_res_preset_changed(self):
        sel= self.combo_res_presets.currentText()
        if sel in self.res_presets:
            w,h,_lbl= self.res_presets[sel]
            self.spin_width.setValue(w)
            self.spin_height.setValue(h)
        self.update_preview()

    def on_create(self):
        show_name= self.edit_show_name.text().strip()
        dst= self.edit_destination.text().strip()
        if not show_name:
            QMessageBox.warning(self, "Warning", "Please enter Show Name.")
            return
        if not dst or not os.path.isdir(dst):
            QMessageBox.warning(self, "Warning", "Please pick a valid Destination Folder.")
            return
        
        final_name= f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        
        # collision check
        final_path= os.path.join(dst, final_name)
        if os.path.exists(final_path):
            QMessageBox.warning(self, "Collision",
                f"Folder '{final_path}' already exists.\nAborting.")
            return
        
        seq_shots= self.sequence_container.get_all_sequences_and_shots()
        
        # gather nuke script settings
        fps_str= self.combo_fps.currentText()
        try:
            fps_val= float(fps_str)
        except:
            fps_val= 24.0
        w_val= self.spin_width.value()
        h_val= self.spin_height.value()
        use_proxy= self.chk_proxy.isChecked()
        use_aces= self.chk_aces.isChecked()
        
        # resolution label
        resolution_label= f"Custom_{w_val}x{h_val}"
        for nm,(pw,ph,lbl) in self.res_presets.items():
            if w_val==pw and h_val==ph:
                resolution_label= lbl
                break
        
        mode= self.combo_mode.currentText()
        
        try:
            if mode=="Hardcoded":
                self.create_hardcoded_structure(final_name, dst, seq_shots)
                self.create_nuke_scripts_in_05_comp(
                    final_name, dst, seq_shots,
                    fps_val, w_val, h_val, resolution_label,
                    use_proxy, use_aces
                )
            else:
                if not hasattr(self, 'template_folder') or not os.path.isdir(self.template_folder):
                    QMessageBox.warning(self, "Warning", "Please pick a valid Template folder for Template mode.")
                    return
                self.replicate_template_structure(
                    final_name, dst, seq_shots,
                    fps_val, w_val, h_val, resolution_label,
                    use_proxy, use_aces
                )
            
            QMessageBox.information(self, "Success", "Folders & Nuke scripts created successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_preview(self):
        show_name= self.edit_show_name.text().strip()
        dst= self.edit_destination.text().strip()
        if not show_name or not dst:
            self.preview_text.setPlainText("No Show Name or Destination => no preview.")
            return
        
        final_name= f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        lines= []
        lines.append(f"Destination => {os.path.join(dst, final_name)}")
        mode= self.combo_mode.currentText()
        lines.append(f"Mode => {mode}")
        
        fps_str= self.combo_fps.currentText()
        lines.append(f"FPS => {fps_str}")
        w_val= self.spin_width.value()
        h_val= self.spin_height.value()
        lines.append(f"Resolution => {w_val}x{h_val}")
        lines.append(f"Use Proxies => {self.chk_proxy.isChecked()}")
        lines.append(f"Use ACES => {self.chk_aces.isChecked()}")
        
        seq_shots= self.sequence_container.get_all_sequences_and_shots()
        
        if mode=="Hardcoded":
            lines.append("")
            lines.append("Hardcoded Folder Structure Preview:")
            lines.extend(self.build_preview_hardcoded(seq_shots))
        else:
            if not hasattr(self, 'template_folder') or not self.template_folder:
                lines.append("No Template Folder chosen.")
            else:
                lines.append(f"Template => {self.template_folder}")
                if hasattr(self, 'template_paths') and self.template_paths:
                    lines.append("Subfolders (dry-run):")
                    for rel_path in self.template_paths:
                        segs= rel_path.split("/")
                        last_seg= segs[-1].lower() if segs else ""
                        is_comp= last_seg.startswith("comp")
                        
                        if is_comp:
                            lines.append(f"  {rel_path}")
                            lines.append("    -> For each sequence/shot => subfolder + project/render + .nk")
                        else:
                            if "[sequence]" in rel_path or "[shot]" in rel_path:
                                for sdict in seq_shots:
                                    seq= sdict['sequence']
                                    for sh in sdict['shots']:
                                        sub= rel_path.replace("[sequence]", seq).replace("[shot]", sh)
                                        lines.append(f"  {sub}")
                            else:
                                lines.append(f"  {rel_path}")
        
        self.preview_text.setPlainText("\n".join(lines))

    # -------------- Hardcoded creation logic --------------
    
    def get_folder_name(self, key):
        return self.folder_config[key].text().strip()
    
    def build_preview_hardcoded(self, sequences_and_shots):
        lines=[]
        # (Identical to older code)
        f_plates= self.get_folder_name("folder_01_plates")
        f_aspera= self.get_folder_name("folder_01_plates_aspera")
        f_manifest= self.get_folder_name("folder_01_plates_manifest")
        
        f_support= self.get_folder_name("folder_02_support")
        f_luts= self.get_folder_name("folder_02_support_luts")
        f_luts_cam= self.get_folder_name("folder_02_support_luts_camera")
        f_luts_show= self.get_folder_name("folder_02_support_luts_show")
        f_edl= self.get_folder_name("folder_02_support_edl_xml")
        f_guides= self.get_folder_name("folder_02_support_guides")
        f_camdat= self.get_folder_name("folder_02_support_camera_data")
        
        f_ref= self.get_folder_name("folder_03_references")
        f_client= self.get_folder_name("folder_03_references_client_brief")
        f_art= self.get_folder_name("folder_03_references_artwork")
        f_style= self.get_folder_name("folder_03_references_style_guides")
        
        f_vfx= self.get_folder_name("folder_04_vfx")
        f_comp= self.get_folder_name("folder_05_comp")
        
        f_mg= self.get_folder_name("folder_06_mograph")
        f_mg_proj= self.get_folder_name("folder_06_mograph_projects")
        f_mg_rend= self.get_folder_name("folder_06_mograph_render")
        
        f_sh= self.get_folder_name("folder_07_shared")
        f_stock= self.get_folder_name("folder_07_shared_stock_footage")
        f_graph= self.get_folder_name("folder_07_shared_graphics")
        f_fonts= self.get_folder_name("folder_07_shared_fonts")
        f_temps= self.get_folder_name("folder_07_shared_templates")
        
        f_out= self.get_folder_name("folder_08_output")
        f_out_date= self.get_folder_name("folder_08_output_date")
        f_out_full= self.get_folder_name("folder_08_output_full_res")
        f_out_proxy= self.get_folder_name("folder_08_output_proxy")
        
        lines.append(f"├── {f_plates}/")
        lines.append(f"│   ├── {f_aspera}/")
        
        # place sequences/shots in 01_plates
        for i,seq_info in enumerate(sequences_and_shots):
            seq= seq_info['sequence']
            shots= seq_info['shots']
            prefix_seq= "│   ├──"
            if i == len(sequences_and_shots)-1:
                prefix_seq= "│   └──"
            lines.append(f"{prefix_seq} {seq}/")
            for j,sh in enumerate(shots):
                prefix_sh= "│   │   ├──"
                if j== len(shots)-1:
                    prefix_sh= "│   │   └──"
                lines.append(f"{prefix_sh} {sh}/")
        
        lines.append(f"│   └── {f_manifest}")
        lines.append("│")
        
        lines.append(f"├── {f_support}/")
        lines.append(f"│   ├── {f_luts}/")
        lines.append(f"│   │   ├── {f_luts_cam}/")
        lines.append(f"│   │   └── {f_luts_show}/")
        lines.append(f"│   ├── {f_edl}/")
        lines.append(f"│   ├── {f_guides}/")
        lines.append(f"│   └── {f_camdat}/")
        lines.append("│")
        
        lines.append(f"├── {f_ref}/")
        lines.append(f"│   ├── {f_client}/")
        lines.append(f"│   ├── {f_art}/")
        lines.append(f"│   └── {f_style}/")
        lines.append("│")
        
        lines.append(f"├── {f_vfx}/")
        for seq_info in sequences_and_shots:
            seq= seq_info['sequence']
            lines.append(f"│   └── {seq}/")
            for sh in seq_info['shots']:
                lines.append(f"│       └── {sh}/")
                lines.append(f"│           ├── project/")
                lines.append(f"│           └── render/")
        lines.append("│")
        
        lines.append(f"├── {f_comp}/")
        for seq_info in sequences_and_shots:
            seq= seq_info['sequence']
            lines.append(f"│   └── {seq}/")
            for sh in seq_info['shots']:
                lines.append(f"│       └── {sh}/")
                lines.append(f"│           ├── project/ (.nk script here)")
                lines.append(f"│           └── render/")
        lines.append("│")
        
        lines.append(f"├── {f_mg}/")
        lines.append(f"│   ├── {f_mg_proj}/")
        lines.append(f"│   └── {f_mg_rend}/")
        lines.append("│")
        
        lines.append(f"├── {f_sh}/")
        lines.append(f"│   ├── {f_stock}/")
        lines.append(f"│   ├── {f_graph}/")
        lines.append(f"│   ├── {f_fonts}/")
        lines.append(f"│   └── {f_temps}/")
        lines.append("│")
        
        lines.append(f"└── {f_out}/")
        lines.append(f"    └── {f_out_date}/")
        lines.append(f"        ├── {f_out_full}/")
        lines.append(f"        └── {f_out_proxy}/")
        
        lines.append("")
        lines.append("Nuke scripts in 05_comp/[sequence]/[shot]/project/[sequence]_[shot]_comp_v001.nk")
        return lines

    def create_hardcoded_structure(self, show_name, dest, seq_shots):
        """
        FULL logic to create subfolders for Hardcoded mode:
         01_plates, 02_support, 03_references, 04_vfx, 05_comp, 06_mograph, 07_shared, 08_output
         + place seq/shots in 01_plates, 04_vfx, 05_comp
        """
        show_root = os.path.join(dest, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        f_plates= os.path.join(show_root, self.get_folder_name("folder_01_plates"))
        f_support= os.path.join(show_root, self.get_folder_name("folder_02_support"))
        f_refs= os.path.join(show_root, self.get_folder_name("folder_03_references"))
        f_vfx= os.path.join(show_root, self.get_folder_name("folder_04_vfx"))
        f_comp= os.path.join(show_root, self.get_folder_name("folder_05_comp"))
        f_mg= os.path.join(show_root, self.get_folder_name("folder_06_mograph"))
        f_sh= os.path.join(show_root, self.get_folder_name("folder_07_shared"))
        f_out= os.path.join(show_root, self.get_folder_name("folder_08_output"))
        
        os.makedirs(f_plates, exist_ok=True)
        os.makedirs(f_support, exist_ok=True)
        os.makedirs(f_refs, exist_ok=True)
        os.makedirs(f_vfx, exist_ok=True)
        os.makedirs(f_comp, exist_ok=True)
        os.makedirs(f_mg, exist_ok=True)
        os.makedirs(f_sh, exist_ok=True)
        os.makedirs(f_out, exist_ok=True)
        
        # 01_plates subfolders
        f_aspera= os.path.join(f_plates, self.get_folder_name("folder_01_plates_aspera"))
        os.makedirs(f_aspera, exist_ok=True)
        man= os.path.join(f_plates, self.get_folder_name("folder_01_plates_manifest"))
        if not os.path.isfile(man):
            with open(man,"w") as f:
                f.write("Plate manifest placeholder\n")
        
        # place sequences/shots in 01_plates
        for seq_info in seq_shots:
            seq= seq_info['sequence']
            seq_dir= os.path.join(f_plates, seq)
            os.makedirs(seq_dir, exist_ok=True)
            for sh in seq_info['shots']:
                os.makedirs(os.path.join(seq_dir, sh), exist_ok=True)
        
        # 02_support
        f_luts= os.path.join(f_support, self.get_folder_name("folder_02_support_luts"))
        f_luts_cam= os.path.join(f_luts, self.get_folder_name("folder_02_support_luts_camera"))
        f_luts_show= os.path.join(f_luts, self.get_folder_name("folder_02_support_luts_show"))
        f_edl= os.path.join(f_support, self.get_folder_name("folder_02_support_edl_xml"))
        f_guides= os.path.join(f_support, self.get_folder_name("folder_02_support_guides"))
        f_camdat= os.path.join(f_support, self.get_folder_name("folder_02_support_camera_data"))
        
        os.makedirs(f_luts, exist_ok=True)
        os.makedirs(f_luts_cam, exist_ok=True)
        os.makedirs(f_luts_show, exist_ok=True)
        os.makedirs(f_edl, exist_ok=True)
        os.makedirs(f_guides, exist_ok=True)
        os.makedirs(f_camdat, exist_ok=True)
        
        # 03_references
        f_clibr= os.path.join(f_refs, self.get_folder_name("folder_03_references_client_brief"))
        f_art= os.path.join(f_refs, self.get_folder_name("folder_03_references_artwork"))
        f_sty= os.path.join(f_refs, self.get_folder_name("folder_03_references_style_guides"))
        os.makedirs(f_clibr, exist_ok=True)
        os.makedirs(f_art, exist_ok=True)
        os.makedirs(f_sty, exist_ok=True)
        
        # 04_vfx => [sequence]/[shot]/(project,render)
        for seq_info in seq_shots:
            seq= seq_info['sequence']
            seq_vfx= os.path.join(f_vfx, seq)
            os.makedirs(seq_vfx, exist_ok=True)
            for shot in seq_info['shots']:
                shot_dir= os.path.join(seq_vfx, shot)
                os.makedirs(shot_dir, exist_ok=True)
                prj= os.path.join(shot_dir,"project")
                rnd= os.path.join(shot_dir,"render")
                os.makedirs(prj, exist_ok=True)
                os.makedirs(rnd, exist_ok=True)
        
        # 05_comp => [sequence]/[shot]/(project,render)
        for seq_info in seq_shots:
            seq= seq_info['sequence']
            seq_comp= os.path.join(f_comp, seq)
            os.makedirs(seq_comp, exist_ok=True)
            for shot in seq_info['shots']:
                shot_dir= os.path.join(seq_comp, shot)
                os.makedirs(shot_dir, exist_ok=True)
                prj= os.path.join(shot_dir,"project")
                rnd= os.path.join(shot_dir,"render")
                os.makedirs(prj, exist_ok=True)
                os.makedirs(rnd, exist_ok=True)
        
        # 06_mograph
        f_mg_proj= os.path.join(f_mg, self.get_folder_name("folder_06_mograph_projects"))
        f_mg_rend= os.path.join(f_mg, self.get_folder_name("folder_06_mograph_render"))
        os.makedirs(f_mg_proj, exist_ok=True)
        os.makedirs(f_mg_rend, exist_ok=True)
        
        # 07_shared
        f_stock= os.path.join(f_sh, self.get_folder_name("folder_07_shared_stock_footage"))
        f_gfx= os.path.join(f_sh, self.get_folder_name("folder_07_shared_graphics"))
        f_fonts= os.path.join(f_sh, self.get_folder_name("folder_07_shared_fonts"))
        f_tmps= os.path.join(f_sh, self.get_folder_name("folder_07_shared_templates"))
        os.makedirs(f_stock, exist_ok=True)
        os.makedirs(f_gfx, exist_ok=True)
        os.makedirs(f_fonts, exist_ok=True)
        os.makedirs(f_tmps, exist_ok=True)
        
        # 08_output
        f_out_date= os.path.join(f_out, self.get_folder_name("folder_08_output_date"))
        os.makedirs(f_out_date, exist_ok=True)
        f_out_full= os.path.join(f_out_date, self.get_folder_name("folder_08_output_full_res"))
        f_out_proxy= os.path.join(f_out_date, self.get_folder_name("folder_08_output_proxy"))
        os.makedirs(f_out_full, exist_ok=True)
        os.makedirs(f_out_proxy, exist_ok=True)

    def create_nuke_scripts_in_05_comp(
        self, show_name, dest, seq_shots,
        fps_val, w_val, h_val, resolution_label,
        use_proxy, use_aces
    ):
        comp_name = self.get_folder_name("folder_05_comp")
        show_root = os.path.join(dest, show_name)
        comp_root = os.path.join(show_root, comp_name)
        os.makedirs(comp_root, exist_ok=True)
        
        for seq_info in seq_shots:
            seq= seq_info['sequence']
            seq_dir= os.path.join(comp_root, seq)
            for shot in seq_info['shots']:
                shot_dir= os.path.join(seq_dir, shot, "project")
                os.makedirs(shot_dir, exist_ok=True)
                nk_file= f"{seq}_{shot}_comp_v001.nk"
                nk_path= os.path.join(shot_dir, nk_file)
                
                txt= self.build_nuke_script_template(
                    seq, shot, fps_val, w_val, h_val,
                    resolution_label, use_proxy, use_aces
                )
                with open(nk_path, "w", encoding="utf-8") as ff:
                    ff.write(txt)

    def replicate_template_structure(
        self, show_name, dest, seq_shots,
        fps_val, w_val, h_val, resolution_label,
        use_proxy, use_aces
    ):
        show_root = os.path.join(dest, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        if not hasattr(self, 'template_paths'):
            return
        
        for rel_path in self.template_paths:
            segs= rel_path.split("/")
            last_seg= segs[-1].lower() if segs else ""
            is_comp= last_seg.startswith("comp")
            
            if is_comp:
                comp_abs= os.path.join(show_root, rel_path)
                os.makedirs(comp_abs, exist_ok=True)
                for seq_info in seq_shots:
                    seq= seq_info['sequence']
                    for shot in seq_info['shots']:
                        shot_sub= os.path.join(comp_abs, seq, shot)
                        os.makedirs(shot_sub, exist_ok=True)
                        
                        prj= os.path.join(shot_sub,"project")
                        rnd= os.path.join(shot_sub,"render")
                        os.makedirs(prj,exist_ok=True)
                        os.makedirs(rnd,exist_ok=True)
                        
                        nk_file= f"{seq}_{shot}_comp_v001.nk"
                        nk_path= os.path.join(prj, nk_file)
                        txt= self.build_nuke_script_template(
                            seq, shot, fps_val, w_val, h_val,
                            resolution_label, use_proxy, use_aces
                        )
                        with open(nk_path,"w",encoding="utf-8") as f:
                            f.write(txt)
            else:
                # normal folder
                if "[sequence]" in rel_path or "[shot]" in rel_path:
                    for seq_info in seq_shots:
                        seq= seq_info['sequence']
                        for s in seq_info['shots']:
                            path_sub= rel_path.replace("[sequence]", seq).replace("[shot]", s)
                            final_path= os.path.join(show_root, path_sub)
                            os.makedirs(final_path,exist_ok=True)
                else:
                    final_path= os.path.join(show_root, rel_path)
                    os.makedirs(final_path, exist_ok=True)

    def build_nuke_script_template(
        self, seq_name, shot_name,
        fps, width, height, resolution_label,
        use_proxy, use_aces
    ):
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
                    <page id="Pixel Analyzer.1"/>
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
        
        root_start= f"""Root {{
 inputs 0
 name {seq_name}_{shot_name}_comp_v001.nk
 fps {fps:.2f}
 format "{width} {height} 0 0 {width} {height} 1 {resolution_label}"
"""
        if use_proxy:
            proxy_lines= """ proxy_format "4000 4000 0 0 4000 4000 1 4K Proxy LL180 Sphere"
 proxySetting always"""
        else:
            proxy_lines= """ proxy_type scale
 proxy_format "1024 778 0 0 1024 778 1 1K_Super_35(full-ap)" """
        
        if use_aces:
            color_lines= """ colorManagement OCIO
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
            color_lines= """ colorManagement Nuke
 workingSpaceLUT linear
 monitorLut sRGB
 monitorOutLUT rec709
 int8Lut sRGB
 int16Lut sRGB
 logLut Cineon
 floatLut linear"""
        
        root_block= f"{root_start}{proxy_lines}\n{color_lines}\n}}\n"
        
        viewer_block= f"""Viewer {{
 inputs 0
 frame 1
 frame_range 1-100
 fps {fps:.8f}
 name Viewer1
 xpos -40
 ypos -9
}}"""
        
        script_text= f"""#! C:/Program Files/Nuke15.1v5/nuke-15.1.5.dll -nx
version 15.1 v5
{define_window_layout}
{root_block}
{viewer_block}
"""
        return script_text

def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
