import os
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QTextEdit, QScrollArea, QMessageBox,
    QFileDialog, QCheckBox, QGroupBox
)
from widgets.shot_sequence_widgets import SequenceListContainer

class StructureTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.parent_main_window = main_window
        self.template_folder = None
        self.template_paths = []
        
        # Same dictionary of resolution presets as before
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
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10,10,10,10)
        self.setLayout(main_layout)

        #
        # Top Grid: show name, destination, mode/template, resolution, etc.
        #
        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(10)
        top_grid.setVerticalSpacing(5)

        # Row 0: Show Name
        lbl_show = QLabel("Show Name:")
        self.edit_show_name = QLineEdit()
        self.edit_show_name.setMaxLength(25)
        self.edit_show_name.setPlaceholderText("Project name (max 25 chars)")
        top_grid.addWidget(lbl_show, 0, 0)
        top_grid.addWidget(self.edit_show_name, 0, 1, 1, 3)

        # Row 1: Destination Folder
        lbl_dest = QLabel("Destination Folder:")
        self.edit_destination = QLineEdit()
        self.btn_browse_dest = QPushButton("Browse...")
        top_grid.addWidget(lbl_dest, 1, 0)
        top_grid.addWidget(self.edit_destination, 1, 1, 1, 2)
        top_grid.addWidget(self.btn_browse_dest, 1, 3)

        # Row 2: Creation Mode
        lbl_mode = QLabel("Creation Mode:")
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Hardcoded")
        self.combo_mode.addItem("Template")
        top_grid.addWidget(lbl_mode, 2, 0)
        top_grid.addWidget(self.combo_mode, 2, 1)

        # Row 3: Template Folder
        lbl_tmpl = QLabel("Template Folder:")
        self.edit_template = QLineEdit()
        self.btn_browse_template = QPushButton("Browse...")
        top_grid.addWidget(lbl_tmpl, 3, 0)
        top_grid.addWidget(self.edit_template, 3, 1, 1, 2)
        top_grid.addWidget(self.btn_browse_template, 3, 3)

        # Row 4: Resolution Preset + custom W/H
        lbl_pres = QLabel("Resolution Presets:")
        self.combo_res_presets = QComboBox()
        self.combo_res_presets.addItem("Custom")
        for nm in self.res_presets:
            self.combo_res_presets.addItem(nm)

        lbl_w = QLabel("Width:")
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 20000)
        self.spin_width.setValue(1920)

        lbl_h = QLabel("Height:")
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 20000)
        self.spin_height.setValue(1080)

        top_grid.addWidget(lbl_pres, 4, 0)
        top_grid.addWidget(self.combo_res_presets, 4, 1)
        top_grid.addWidget(lbl_w, 4, 2)
        top_grid.addWidget(self.spin_width, 4, 3)
        top_grid.addWidget(lbl_h, 4, 4)
        top_grid.addWidget(self.spin_height, 4, 5)

        # Row 5: FPS, Proxy, ACES
        lbl_fps = QLabel("FPS:")
        self.combo_fps = QComboBox()
        known_fps = ["23.976", "24", "25", "29.97", "30", "50", "59.94", "60", "120"]
        for ff in known_fps:
            self.combo_fps.addItem(ff)

        self.chk_proxy = QCheckBox("Enable Proxy Workflow")
        self.chk_aces = QCheckBox("Enable Aces Workflow")

        top_grid.addWidget(lbl_fps, 5, 0)
        top_grid.addWidget(self.combo_fps, 5, 1)
        top_grid.addWidget(self.chk_proxy, 5, 2)
        top_grid.addWidget(self.chk_aces, 5, 3)

        main_layout.addLayout(top_grid)

        #
        # Middle layout: left column => sequences/shots, right column => preview
        #
        middle_layout = QHBoxLayout()
        main_layout.addLayout(middle_layout, stretch=1)

        # LEFT: group box containing sequences/shots
        seq_box = QGroupBox("Add Sequences / Shots")
        seq_box_layout = QVBoxLayout(seq_box)
        seq_box_layout.setContentsMargins(5,5,5,5)

        self.sequence_container = SequenceListContainer(self.parent_main_window)
        # Optionally start with 1 sequence
        self.sequence_container.add_sequence()

        scroll_seq = QScrollArea()
        scroll_seq.setWidgetResizable(True)
        scroll_seq.setWidget(self.sequence_container)
        seq_box_layout.addWidget(scroll_seq)

        middle_layout.addWidget(seq_box, stretch=1)

        # RIGHT: preview of folder structure
        preview_box = QGroupBox("")
        preview_layout = QVBoxLayout(preview_box)
        preview_layout.setContentsMargins(5,5,5,5)

        lbl_prev = QLabel("Folder Structure Preview:")
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)

        preview_layout.addWidget(lbl_prev)
        preview_layout.addWidget(self.preview_text)

        middle_layout.addWidget(preview_box, stretch=1)

        #
        # Bottom: create button
        #
        self.btn_create = QPushButton("Create Folder Structure")
        main_layout.addWidget(self.btn_create)

        #
        # Connect signals
        #
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

    #
    # Implementation of your existing logic
    #
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
            collected.append(rel.replace("\\", "/"))
        return collected

    def on_res_preset_changed(self):
        sel = self.combo_res_presets.currentText()
        if sel in self.res_presets:
            w, h, _ = self.res_presets[sel]
            self.spin_width.setValue(w)
            self.spin_height.setValue(h)
        self.update_preview()

    def on_create(self):
        show_name = self.edit_show_name.text().strip()
        dst = self.edit_destination.text().strip()
        if not show_name:
            QMessageBox.warning(self, "Warning", "Please enter Show Name.")
            return
        if not dst or not os.path.isdir(dst):
            QMessageBox.warning(self, "Warning", "Please pick a valid Destination Folder.")
            return

        final_name = f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        final_path = os.path.join(dst, final_name)
        if os.path.exists(final_path):
            QMessageBox.warning(self, "Collision",
                f"Folder '{final_path}' already exists.\nAborting.")
            return

        seq_shots = self.sequence_container.get_all_sequences_and_shots()
        fps_str = self.combo_fps.currentText()
        try:
            fps_val = float(fps_str)
        except:
            fps_val = 24.0
        w_val = self.spin_width.value()
        h_val = self.spin_height.value()
        use_proxy = self.chk_proxy.isChecked()
        use_aces = self.chk_aces.isChecked()

        resolution_label = f"Custom_{w_val}x{h_val}"
        for nm, (pw, ph, lbl) in self.res_presets.items():
            if w_val == pw and h_val == ph:
                resolution_label = lbl
                break

        mode = self.combo_mode.currentText()
        try:
            if mode == "Hardcoded":
                self.create_hardcoded_structure(final_name, dst, seq_shots)
                self.create_nuke_scripts_in_05_comp(
                    final_name, dst, seq_shots,
                    fps_val, w_val, h_val, resolution_label,
                    use_proxy, use_aces
                )
            else:
                if not self.template_folder or not os.path.isdir(self.template_folder):
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
        show_name = self.edit_show_name.text().strip()
        dst = self.edit_destination.text().strip()
        if not show_name or not dst:
            self.preview_text.setPlainText("No Show Name or Destination => no preview.")
            return

        final_name = f"{show_name}_{datetime.date.today():%Y-%m-%d}"
        lines = []
        lines.append(f"Destination => {os.path.join(dst, final_name)}")
        mode = self.combo_mode.currentText()
        lines.append(f"Mode => {mode}")

        fps_str = self.combo_fps.currentText()
        lines.append(f"FPS => {fps_str}")
        w_val = self.spin_width.value()
        h_val = self.spin_height.value()
        lines.append(f"Resolution => {w_val}x{h_val}")
        lines.append(f"Use Proxies => {self.chk_proxy.isChecked()}")
        lines.append(f"Use ACES => {self.chk_aces.isChecked()}")

        seq_shots = self.sequence_container.get_all_sequences_and_shots()
        if mode == "Hardcoded":
            lines.append("")
            lines.append("Hardcoded Folder Structure Preview:")
            lines.extend(self.build_preview_hardcoded(seq_shots))
        else:
            if not self.template_folder:
                lines.append("No Template Folder chosen.")
            else:
                lines.append(f"Template => {self.template_folder}")
                if self.template_paths:
                    lines.append("Subfolders (dry-run):")
                    for rel_path in self.template_paths:
                        segs = rel_path.split("/")
                        last_seg = segs[-1].lower() if segs else ""
                        is_comp = last_seg.startswith("comp")
                        if is_comp:
                            lines.append(f"  {rel_path}")
                            lines.append("    -> For each sequence/shot => subfolder + project/render + .nk")
                        else:
                            if "[sequence]" in rel_path or "[shot]" in rel_path:
                                for sdict in seq_shots:
                                    seq = sdict['sequence']
                                    for sh in sdict['shots']:
                                        sub = rel_path.replace("[sequence]", seq).replace("[shot]", sh)
                                        lines.append(f"  {sub}")
                            else:
                                lines.append(f"  {rel_path}")

        self.preview_text.setPlainText("\n".join(lines))
    
    def build_preview_hardcoded(self, sequences_and_shots):
        lines = []
        get_folder = lambda key: self.parent_main_window.folder_config[key].text().strip()
        
        f_plates = get_folder("folder_01_plates")
        f_aspera = get_folder("folder_01_plates_aspera")
        f_manifest = get_folder("folder_01_plates_manifest")
        
        f_support = get_folder("folder_02_support")
        f_luts = get_folder("folder_02_support_luts")
        f_luts_cam = get_folder("folder_02_support_luts_camera")
        f_luts_show = get_folder("folder_02_support_luts_show")
        f_edl = get_folder("folder_02_support_edl_xml")
        f_guides = get_folder("folder_02_support_guides")
        f_camdat = get_folder("folder_02_support_camera_data")
        
        f_ref = get_folder("folder_03_references")
        f_client = get_folder("folder_03_references_client_brief")
        f_art = get_folder("folder_03_references_artwork")
        f_style = get_folder("folder_03_references_style_guides")
        
        f_vfx = get_folder("folder_04_vfx")
        f_comp = get_folder("folder_05_comp")
        
        f_mg = get_folder("folder_06_mograph")
        f_mg_proj = get_folder("folder_06_mograph_projects")
        f_mg_rend = get_folder("folder_06_mograph_render")
        
        f_sh = get_folder("folder_07_shared")
        f_stock = get_folder("folder_07_shared_stock_footage")
        f_graph = get_folder("folder_07_shared_graphics")
        f_fonts = get_folder("folder_07_shared_fonts")
        f_temps = get_folder("folder_07_shared_templates")
        
        f_out = get_folder("folder_08_output")
        f_out_date = get_folder("folder_08_output_date")
        f_out_full = get_folder("folder_08_output_full_res")
        f_out_proxy = get_folder("folder_08_output_proxy")
        
        lines.append(f"├── {f_plates}/")
        lines.append(f"│   ├── {f_aspera}/")
        for i, seq_info in enumerate(sequences_and_shots):
            seq = seq_info['sequence']
            shots = seq_info['shots']
            prefix_seq = "│   ├──" if i < len(sequences_and_shots)-1 else "│   └──"
            lines.append(f"{prefix_seq} {seq}/")
            for j, sh in enumerate(shots):
                prefix_sh = "│   │   ├──" if j < len(shots)-1 else "│   │   └──"
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
            seq = seq_info['sequence']
            lines.append(f"│   └── {seq}/")
            for sh in seq_info['shots']:
                lines.append(f"│       └── {sh}/")
                lines.append(f"│           ├── project/")
                lines.append(f"│           └── render/")
        lines.append("│")
        lines.append(f"├── {f_comp}/")
        for seq_info in sequences_and_shots:
            seq = seq_info['sequence']
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
        show_root = os.path.join(dest, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        f_plates = os.path.join(show_root, self.parent_main_window.folder_config["folder_01_plates"].text().strip())
        f_support = os.path.join(show_root, self.parent_main_window.folder_config["folder_02_support"].text().strip())
        f_refs = os.path.join(show_root, self.parent_main_window.folder_config["folder_03_references"].text().strip())
        f_vfx = os.path.join(show_root, self.parent_main_window.folder_config["folder_04_vfx"].text().strip())
        f_comp = os.path.join(show_root, self.parent_main_window.folder_config["folder_05_comp"].text().strip())
        f_mg = os.path.join(show_root, self.parent_main_window.folder_config["folder_06_mograph"].text().strip())
        f_sh = os.path.join(show_root, self.parent_main_window.folder_config["folder_07_shared"].text().strip())
        f_out = os.path.join(show_root, self.parent_main_window.folder_config["folder_08_output"].text().strip())
        
        os.makedirs(f_plates, exist_ok=True)
        os.makedirs(f_support, exist_ok=True)
        os.makedirs(f_refs, exist_ok=True)
        os.makedirs(f_vfx, exist_ok=True)
        os.makedirs(f_comp, exist_ok=True)
        os.makedirs(f_mg, exist_ok=True)
        os.makedirs(f_sh, exist_ok=True)
        os.makedirs(f_out, exist_ok=True)
        
        # 01_plates subfolders
        f_aspera = os.path.join(f_plates, self.parent_main_window.folder_config["folder_01_plates_aspera"].text().strip())
        os.makedirs(f_aspera, exist_ok=True)
        man = os.path.join(f_plates, self.parent_main_window.folder_config["folder_01_plates_manifest"].text().strip())
        if not os.path.isfile(man):
            with open(man, "w") as f:
                f.write("Plate manifest placeholder\n")
        
        for seq_info in seq_shots:
            seq = seq_info['sequence']
            seq_dir = os.path.join(f_plates, seq)
            os.makedirs(seq_dir, exist_ok=True)
            for sh in seq_info['shots']:
                os.makedirs(os.path.join(seq_dir, sh), exist_ok=True)
        
        # 02_support
        f_luts = os.path.join(f_support, self.parent_main_window.folder_config["folder_02_support_luts"].text().strip())
        f_luts_cam = os.path.join(f_luts, self.parent_main_window.folder_config["folder_02_support_luts_camera"].text().strip())
        f_luts_show = os.path.join(f_luts, self.parent_main_window.folder_config["folder_02_support_luts_show"].text().strip())
        f_edl = os.path.join(f_support, self.parent_main_window.folder_config["folder_02_support_edl_xml"].text().strip())
        f_guides = os.path.join(f_support, self.parent_main_window.folder_config["folder_02_support_guides"].text().strip())
        f_camdat = os.path.join(f_support, self.parent_main_window.folder_config["folder_02_support_camera_data"].text().strip())
        
        os.makedirs(f_luts, exist_ok=True)
        os.makedirs(f_luts_cam, exist_ok=True)
        os.makedirs(f_luts_show, exist_ok=True)
        os.makedirs(f_edl, exist_ok=True)
        os.makedirs(f_guides, exist_ok=True)
        os.makedirs(f_camdat, exist_ok=True)
        
        # 03_references
        f_clibr = os.path.join(f_refs, self.parent_main_window.folder_config["folder_03_references_client_brief"].text().strip())
        f_art = os.path.join(f_refs, self.parent_main_window.folder_config["folder_03_references_artwork"].text().strip())
        f_sty = os.path.join(f_refs, self.parent_main_window.folder_config["folder_03_references_style_guides"].text().strip())
        os.makedirs(f_clibr, exist_ok=True)
        os.makedirs(f_art, exist_ok=True)
        os.makedirs(f_sty, exist_ok=True)
        
        # 04_vfx => [sequence]/[shot]/(project,render)
        for seq_info in seq_shots:
            seq = seq_info['sequence']
            seq_vfx = os.path.join(f_vfx, seq)
            os.makedirs(seq_vfx, exist_ok=True)
            for shot in seq_info['shots']:
                shot_dir = os.path.join(seq_vfx, shot)
                os.makedirs(shot_dir, exist_ok=True)
                prj = os.path.join(shot_dir, "project")
                rnd = os.path.join(shot_dir, "render")
                os.makedirs(prj, exist_ok=True)
                os.makedirs(rnd, exist_ok=True)
        
        # 05_comp => [sequence]/[shot]/(project,render)
        for seq_info in seq_shots:
            seq = seq_info['sequence']
            seq_comp = os.path.join(f_comp, seq)
            os.makedirs(seq_comp, exist_ok=True)
            for shot in seq_info['shots']:
                shot_dir = os.path.join(seq_comp, shot)
                os.makedirs(shot_dir, exist_ok=True)
                prj = os.path.join(shot_dir, "project")
                rnd = os.path.join(shot_dir, "render")
                os.makedirs(prj, exist_ok=True)
                os.makedirs(rnd, exist_ok=True)
        
        # 06_mograph
        f_mg_proj = os.path.join(f_mg, self.parent_main_window.folder_config["folder_06_mograph_projects"].text().strip())
        f_mg_rend = os.path.join(f_mg, self.parent_main_window.folder_config["folder_06_mograph_render"].text().strip())
        os.makedirs(f_mg_proj, exist_ok=True)
        os.makedirs(f_mg_rend, exist_ok=True)
        
        # 07_shared
        f_stock = os.path.join(f_sh, self.parent_main_window.folder_config["folder_07_shared_stock_footage"].text().strip())
        f_gfx = os.path.join(f_sh, self.parent_main_window.folder_config["folder_07_shared_graphics"].text().strip())
        f_fonts = os.path.join(f_sh, self.parent_main_window.folder_config["folder_07_shared_fonts"].text().strip())
        f_tmps = os.path.join(f_sh, self.parent_main_window.folder_config["folder_07_shared_templates"].text().strip())
        os.makedirs(f_stock, exist_ok=True)
        os.makedirs(f_gfx, exist_ok=True)
        os.makedirs(f_fonts, exist_ok=True)
        os.makedirs(f_tmps, exist_ok=True)
        
        # 08_output
        f_out_date = os.path.join(f_out, self.parent_main_window.folder_config["folder_08_output_date"].text().strip())
        os.makedirs(f_out_date, exist_ok=True)
        f_out_full = os.path.join(f_out_date, self.parent_main_window.folder_config["folder_08_output_full_res"].text().strip())
        f_out_proxy = os.path.join(f_out_date, self.parent_main_window.folder_config["folder_08_output_proxy"].text().strip())
        os.makedirs(f_out_full, exist_ok=True)
        os.makedirs(f_out_proxy, exist_ok=True)
    
    def create_nuke_scripts_in_05_comp(self, show_name, dest, seq_shots, fps_val, w_val, h_val, resolution_label, use_proxy, use_aces):
        comp_name = self.parent_main_window.folder_config["folder_05_comp"].text().strip()
        show_root = os.path.join(dest, show_name)
        comp_root = os.path.join(show_root, comp_name)
        os.makedirs(comp_root, exist_ok=True)
        
        for seq_info in seq_shots:
            seq = seq_info['sequence']
            seq_dir = os.path.join(comp_root, seq)
            for shot in seq_info['shots']:
                shot_dir = os.path.join(seq_dir, shot, "project")
                os.makedirs(shot_dir, exist_ok=True)
                nk_file = f"{seq}_{shot}_comp_v001.nk"
                nk_path = os.path.join(shot_dir, nk_file)
                txt = self.parent_main_window.build_nuke_script_template(
                    seq, shot, fps_val, w_val, h_val, resolution_label, use_proxy, use_aces
                )
                with open(nk_path, "w", encoding="utf-8") as ff:
                    ff.write(txt)
    
    def replicate_template_structure(self, show_name, dest, seq_shots, fps_val, w_val, h_val, resolution_label, use_proxy, use_aces):
        show_root = os.path.join(dest, show_name)
        os.makedirs(show_root, exist_ok=True)
        
        if not self.template_paths:
            return
        
        for rel_path in self.template_paths:
            segs = rel_path.split("/")
            last_seg = segs[-1].lower() if segs else ""
            is_comp = last_seg.startswith("comp")
            
            if is_comp:
                comp_abs = os.path.join(show_root, rel_path)
                os.makedirs(comp_abs, exist_ok=True)
                for seq_info in seq_shots:
                    seq = seq_info['sequence']
                    for shot in seq_info['shots']:
                        shot_sub = os.path.join(comp_abs, seq, shot)
                        os.makedirs(shot_sub, exist_ok=True)
                        prj = os.path.join(shot_sub, "project")
                        rnd = os.path.join(shot_sub, "render")
                        os.makedirs(prj, exist_ok=True)
                        os.makedirs(rnd, exist_ok=True)
                        nk_file = f"{seq}_{shot}_comp_v001.nk"
                        nk_path = os.path.join(prj, nk_file)
                        txt = self.parent_main_window.build_nuke_script_template(
                            seq, shot, fps_val, w_val, h_val, resolution_label, use_proxy, use_aces
                        )
                        with open(nk_path, "w", encoding="utf-8") as f:
                            f.write(txt)
            else:
                if "[sequence]" in rel_path or "[shot]" in rel_path:
                    for seq_info in seq_shots:
                        seq = seq_info['sequence']
                        for s in seq_info['shots']:
                            path_sub = rel_path.replace("[sequence]", seq).replace("[shot]", s)
                            final_path = os.path.join(show_root, path_sub)
                            os.makedirs(final_path, exist_ok=True)
                else:
                    final_path = os.path.join(show_root, rel_path)
                    os.makedirs(final_path, exist_ok=True)
