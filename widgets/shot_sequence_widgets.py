from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QFrame
from PyQt5.QtCore import Qt

class ShotWidget(QWidget):
    def __init__(self, parent_sequence_widget):
        super().__init__()
        self.parent_sequence_widget = parent_sequence_widget
        
        lay = QHBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0,0,0,0)
        
        self.shot_name_edit = QLineEdit()
        self.shot_name_edit.setPlaceholderText("Shot Name (max 25 chars)")
        self.shot_name_edit.setMaxLength(25)
        
        self.btn_remove_shot = QPushButton("-")
        self.btn_add_shot = QPushButton("+")
        self.btn_remove_shot.setFixedWidth(25)
        self.btn_add_shot.setFixedWidth(25)
        
        lay.addWidget(self.shot_name_edit)
        lay.addWidget(self.btn_remove_shot)
        lay.addWidget(self.btn_add_shot)
        
        self.setLayout(lay)
        
        # Connect signals
        self.btn_remove_shot.clicked.connect(self.remove_self)
        self.btn_add_shot.clicked.connect(self.add_shot_below)
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
        
        # Connect signals
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
        s = ShotWidget(self)
        if not after_shot_widget:
            self.shots_layout.addWidget(s)
        else:
            idx = self.shots_layout.indexOf(after_shot_widget) + 1
            self.shots_layout.insertWidget(idx, s)
        return s
    
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
        
        lay = QVBoxLayout()
        lay.setSpacing(0)
        lay.setContentsMargins(0,0,0,0)
        self.setLayout(lay)
    
    def add_sequence(self, after_sequence_widget=None):
        seq_widget = SequenceWidget(self.parent_main_window, self)
        if after_sequence_widget:
            idx = self.layout().indexOf(after_sequence_widget) + 1
            self.layout().insertWidget(idx, seq_widget)
        else:
            self.layout().addWidget(seq_widget)
        return seq_widget
    
    def remove_sequence(self, seq_widget):
        seq_widget.setParent(None)
    
    def get_all_sequences_and_shots(self):
        data = []
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            w = item.widget()
            if isinstance(w, SequenceWidget):
                s = w.get_sequence_name()
                shots = w.get_shot_names()
                # Append the entry if there is a sequence name or if there are shots.
                if s or shots:
                    data.append({'sequence': s, 'shots': shots})
        return data
