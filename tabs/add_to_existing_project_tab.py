# add_to_existing_project_tab.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QSpinBox, QTreeWidget, QTreeWidgetItem,
    QScrollArea, QMessageBox, QFileDialog, QGroupBox
)
from PyQt5.QtCore import Qt
from widgets.shot_sequence_widgets import SequenceListContainer

class AddToExistingProjectTab(QWidget):
    """
    Revised layout:
      [Left]   => QTreeWidget of the existing project (check a folder to add)
      [Center] => Add Sequences / Shots
      [Right]  => Preview QTreeWidget showing final structure of selected folders + new sequences/shots
    """
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
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
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
        #
        # 1) Top Grid: "Select Project," "Nuke Script?", resolution, fps, etc.
        #
        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(10)
        top_grid.setVerticalSpacing(5)
        
        # Row 0: Project Folder
        lbl_proj = QLabel("Select Project:")
        self.edit_project_folder = QLineEdit()
        self.btn_browse_proj = QPushButton("Browse...")
        top_grid.addWidget(lbl_proj, 0, 0)
        top_grid.addWidget(self.edit_project_folder, 0, 1, 1, 3)
        top_grid.addWidget(self.btn_browse_proj, 0, 4)
        
        # Row 1: Nuke Script? + FPS + Proxy + ACES
        self.chk_create_nk_under_comp = QCheckBox("Nuke Script?")
        
        lbl_fps = QLabel("FPS:")
        self.combo_fps = QComboBox()
        known_fps = ["23.976","24","25","29.97","30","50","59.94","60","120"]
        for ff in known_fps:
            self.combo_fps.addItem(ff)
        
        self.chk_proxy = QCheckBox("Enable Proxy Workflow")
        self.chk_aces = QCheckBox("Enable Aces Workflow")
        
        top_grid.addWidget(self.chk_create_nk_under_comp, 1, 0)
        top_grid.addWidget(lbl_fps, 1, 1)
        top_grid.addWidget(self.combo_fps, 1, 2)
        top_grid.addWidget(self.chk_proxy, 1, 3)
        top_grid.addWidget(self.chk_aces, 1, 4)
        
        # Row 2: Resolution Preset + W/H
        lbl_rp = QLabel("Resolution Preset:")
        self.combo_res_presets = QComboBox()
        self.combo_res_presets.addItem("Custom")
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
        
        top_grid.addWidget(lbl_rp, 2, 0)
        top_grid.addWidget(self.combo_res_presets, 2, 1)
        top_grid.addWidget(lbl_w, 2, 2)
        top_grid.addWidget(self.spin_width, 2, 3)
        top_grid.addWidget(lbl_h, 2, 4)
        top_grid.addWidget(self.spin_height, 2, 5)
        
        main_layout.addLayout(top_grid)
        
        #
        # 2) Middle area => HBox with:
        #    Left:   existing project tree (QTreeWidget)
        #    Center: "Add Sequences/Shots" (SequenceListContainer)
        #    Right:  final preview tree
        #
        middle_layout = QHBoxLayout()
        main_layout.addLayout(middle_layout, stretch=1)
        
        # 2a) LEFT => existing project tree
        left_box = QGroupBox("Existing Project Structure")
        left_box_layout = QVBoxLayout(left_box)
        
        self.tree_existing = QTreeWidget()
        self.tree_existing.setHeaderLabel("Folders (check to add)")
        left_box_layout.addWidget(self.tree_existing)
        
        middle_layout.addWidget(left_box, stretch=1)
        
        # 2b) CENTER => sequences/shots
        seq_box = QGroupBox("Add Sequences / Shots")
        seq_box_layout = QVBoxLayout(seq_box)
        
        self.seq_container = SequenceListContainer(self.main_window)
        # Start with one sequence by default
        self.seq_container.add_sequence()
        
        scroll_seq = QScrollArea()
        scroll_seq.setWidgetResizable(True)
        scroll_seq.setWidget(self.seq_container)
        seq_box_layout.addWidget(scroll_seq)
        
        middle_layout.addWidget(seq_box, stretch=1)
        
        # 2c) RIGHT => final preview tree
        right_box = QGroupBox("Preview of New Structure")
        right_layout = QVBoxLayout(right_box)
        
        self.tree_preview = QTreeWidget()
        self.tree_preview.setHeaderLabel("Final Structure")
        right_layout.addWidget(self.tree_preview)
        
        middle_layout.addWidget(right_box, stretch=1)
        
        #
        # 3) Bottom => "Add Folders & Shots" button
        #
        self.btn_execute = QPushButton("Add Folders & Shots")
        main_layout.addWidget(self.btn_execute)
        
        #
        # Connect signals
        #
        self.btn_browse_proj.clicked.connect(self.on_browse_project)
        self.btn_execute.clicked.connect(self.on_execute)
        
        self.chk_create_nk_under_comp.stateChanged.connect(self.update_preview_tab3)
        self.combo_fps.currentIndexChanged.connect(self.update_preview_tab3)
        self.chk_proxy.stateChanged.connect(self.update_preview_tab3)
        self.chk_aces.stateChanged.connect(self.update_preview_tab3)
        
        self.combo_res_presets.currentIndexChanged.connect(self.on_res_preset_changed)
        self.spin_width.valueChanged.connect(self.update_preview_tab3)
        self.spin_height.valueChanged.connect(self.update_preview_tab3)
        
        self.tree_existing.itemChanged.connect(self.update_preview_tab3)
    
    # --------------------------------------------------------------------------
    # Reorganized logic
    # --------------------------------------------------------------------------
    
    def on_browse_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Existing Project Folder")
        if folder:
            self.edit_project_folder.setText(folder)
            self.populate_existing_tree(folder)
        self.update_preview_tab3()
    
    def populate_existing_tree(self, project_folder):
        self.tree_existing.clear()
        if not os.path.isdir(project_folder):
            return
        for root, dirs, files in os.walk(project_folder):
            rel = os.path.relpath(root, project_folder)
            if rel == ".":
                continue
            segments = rel.split(os.path.sep)
            parent_item = self.tree_existing.invisibleRootItem()
            current_path = []
            for seg in segments:
                current_path.append(seg)
                partial_rel = os.path.join(*current_path)
                found = None
                for i in range(parent_item.childCount()):
                    c = parent_item.child(i)
                    if c.data(0, Qt.UserRole) == partial_rel:
                        found = c
                        parent_item = c
                        break
                if not found:
                    new_item = QTreeWidgetItem([seg])
                    new_item.setData(0, Qt.UserRole, partial_rel)
                    new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable)
                    new_item.setCheckState(0, Qt.Unchecked)
                    parent_item.addChild(new_item)
                    parent_item = new_item
        self.tree_existing.expandAll()
    
    def on_res_preset_changed(self):
        sel = self.combo_res_presets.currentText()
        if sel in self.res_presets:
            w, h, _ = self.res_presets[sel]
            self.spin_width.setValue(w)
            self.spin_height.setValue(h)
        self.update_preview_tab3()
    
    def update_preview_tab3(self, *args):
        """
        Builds a live preview (in self.tree_preview) of the final structure
        based on which folders are checked plus new sequences/shots.
        """
        self.tree_preview.clear()
        
        proj_folder = self.edit_project_folder.text().strip()
        if not proj_folder or not os.path.isdir(proj_folder):
            # No valid project => just show a placeholder
            QTreeWidgetItem(self.tree_preview, ["No valid project folder selected."])
            return
        
        # Gather checked folders in the existing project
        checked_folders = []
        def gather_checked(item):
            for i in range(item.childCount()):
                c = item.child(i)
                if c.checkState(0) == Qt.Checked:
                    checked_folders.append(c.data(0, Qt.UserRole))
                gather_checked(c)
        gather_checked(self.tree_existing.invisibleRootItem())
        
        seq_data = self.seq_container.get_all_sequences_and_shots()
        
        # For each checked folder => folder node in the preview
        # Then show sequences/shots as sub-nodes
        for cf in checked_folders:
            item_folder = QTreeWidgetItem([cf])  # path relative to project root
            self.tree_preview.addTopLevelItem(item_folder)
            
            # for each sequence => subfolder => shots
            for sd in seq_data:
                seqnm = sd['sequence'].strip()
                shots = [s for s in sd['shots'] if s.strip()]
                
                if seqnm:
                    seq_item = QTreeWidgetItem([seqnm])
                    item_folder.addChild(seq_item)
                    
                    for sh in shots:
                        shot_item = QTreeWidgetItem([sh])
                        seq_item.addChild(shot_item)
                        
                        # Check if we are making subfolders only if "comp" is in path:
                        is_comp_folder = self.chk_create_nk_under_comp.isChecked() and \
                                         self.folder_or_parents_has_comp(
                                             os.path.join(proj_folder, cf),
                                             proj_folder
                                         )
                        if is_comp_folder:
                            QTreeWidgetItem(shot_item, ["project/"])
                            QTreeWidgetItem(shot_item, ["render/"])
                else:
                    # No sequence => just shots
                    for sh in shots:
                        shot_item = QTreeWidgetItem([sh])
                        item_folder.addChild(shot_item)
                        
                        is_comp_folder = self.chk_create_nk_under_comp.isChecked() and \
                                         self.folder_or_parents_has_comp(
                                             os.path.join(proj_folder, cf),
                                             proj_folder
                                         )
                        if is_comp_folder:
                            QTreeWidgetItem(shot_item, ["project/"])
                            QTreeWidgetItem(shot_item, ["render/"])
        
        self.tree_preview.expandAll()
    
    def folder_or_parents_has_comp(self, folder_path, project_root):
        folder_path = os.path.abspath(folder_path)
        project_root = os.path.abspath(project_root)
        while True:
            base = os.path.basename(folder_path).lower()
            if "comp" in base:
                return True
            if folder_path == project_root:
                break
            new_folder = os.path.dirname(folder_path)
            if new_folder == folder_path:
                break
            folder_path = new_folder
        return "comp" in os.path.basename(project_root).lower()
    
    def on_execute(self):
        proj_folder = self.edit_project_folder.text().strip()
        if not proj_folder or not os.path.isdir(proj_folder):
            QMessageBox.warning(self, "Warning", "No valid existing project folder.")
            return
        
        create_nk_under_comp = self.chk_create_nk_under_comp.isChecked()
        
        sel_rp = self.combo_res_presets.currentText()
        w_val = self.spin_width.value()
        h_val = self.spin_height.value()
        res_label = f"Custom_{w_val}x{h_val}"
        if sel_rp in self.res_presets:
            pw, ph, lbl = self.res_presets[sel_rp]
            if w_val == pw and h_val == ph:
                res_label = lbl
        
        try:
            fps_val = float(self.combo_fps.currentText())
        except:
            fps_val = 24.0
        use_proxy = self.chk_proxy.isChecked()
        use_aces = self.chk_aces.isChecked()
        
        # gather checked subfolders
        checked_items = []
        def gather_checked(item):
            for i in range(item.childCount()):
                c = item.child(i)
                if c.checkState(0) == Qt.Checked:
                    checked_items.append(c)
                gather_checked(c)
        gather_checked(self.tree_existing.invisibleRootItem())
        
        # gather new sequences/shots
        seq_data = self.seq_container.get_all_sequences_and_shots()
        
        for citem in checked_items:
            relp = citem.data(0, Qt.UserRole)
            abspath = os.path.join(proj_folder, relp)
            
            is_comp_folder = create_nk_under_comp and self.folder_or_parents_has_comp(abspath, proj_folder)
            
            for sd in seq_data:
                seqnm = sd['sequence'].strip()
                shots = [s.strip() for s in sd['shots'] if s.strip()]
                
                if seqnm:
                    seq_folder = os.path.join(abspath, seqnm)
                    if os.path.exists(seq_folder):
                        QMessageBox.warning(self, "Collision",
                            f"Folder '{seqnm}' already exists under {abspath}, skipping.")
                        continue
                    os.makedirs(seq_folder, exist_ok=True)
                    
                    for sh in shots:
                        shot_folder = os.path.join(seq_folder, sh)
                        if os.path.exists(shot_folder):
                            QMessageBox.warning(self, "Collision",
                                f"Shot '{sh}' already exists under {seq_folder}, skipping.")
                            continue
                        os.makedirs(shot_folder, exist_ok=True)
                        
                        if is_comp_folder:
                            prj = os.path.join(shot_folder, "project")
                            rnd = os.path.join(shot_folder, "render")
                            os.makedirs(prj, exist_ok=True)
                            os.makedirs(rnd, exist_ok=True)
                            
                            nk_name = f"{seqnm}_{sh}_comp_v001.nk"
                            nk_path = os.path.join(prj, nk_name)
                            script_txt = self.main_window.build_nuke_script_template(
                                seqnm, sh, fps_val, w_val, h_val, res_label, use_proxy, use_aces
                            )
                            with open(nk_path, "w", encoding='utf-8') as ff:
                                ff.write(script_txt)
                else:
                    # No sequence => only shots
                    for sh in shots:
                        shot_folder = os.path.join(abspath, sh)
                        if os.path.exists(shot_folder):
                            QMessageBox.warning(self, "Collision",
                                f"Shot '{sh}' already exists under {abspath}, skipping.")
                            continue
                        os.makedirs(shot_folder, exist_ok=True)
                        
                        if is_comp_folder:
                            prj = os.path.join(shot_folder, "project")
                            rnd = os.path.join(shot_folder, "render")
                            os.makedirs(prj, exist_ok=True)
                            os.makedirs(rnd, exist_ok=True)
                            
                            nk_name = f"{sh}_comp_v001.nk"
                            nk_path = os.path.join(prj, nk_name)
                            script_txt = self.main_window.build_nuke_script_template(
                                "", sh, fps_val, w_val, h_val, res_label, use_proxy, use_aces
                            )
                            with open(nk_path, "w", encoding='utf-8') as ff:
                                ff.write(script_txt)
        
        QMessageBox.information(self, "Done", "Sequences/Shots added successfully.")
        # Optionally re-check the preview after creation
        self.update_preview_tab3()
