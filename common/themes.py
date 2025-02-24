# themes.py
def apply_dark_theme(app):
    """
    Original minimal dark theme.
    If you just want to keep it, that's fine; 
    or comment it out if you're using the new style below.
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


def apply_custom_stylesheet(app):
    """
    A more extended stylesheet for a 'rounded/gray' look 
    resembling your attached screenshots.
    """
    custom_stylesheet = """
    QMainWindow {
        background-color: #2e2e2e;
    }
    QWidget {
        background-color: #2e2e2e;
        color: #ffffff;
        font-size: 10pt;
    }

    /* Inputs */
    QLineEdit, QTextEdit, QComboBox, QSpinBox {
        background-color: #3b3b3b;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 4px;
    }

    /* Buttons */
    QPushButton {
        background-color: #444444;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 4px;
    }
    QPushButton:hover {
        background-color: #555555;
    }

    /* Labels */
    QLabel {
        color: #ffffff;
        font-weight: normal;
    }

    /* GroupBoxes for a slight border + radius */
    QGroupBox {
        border: 1px solid #555555;
        border-radius: 6px;
        margin-top: 6px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 3px;
    }

    /* ScrollArea, TreeWidget */
    QScrollArea, QTreeWidget {
        background-color: #2e2e2e;
        border: 1px solid #555;
        border-radius: 4px;
    }

    /* TabWidget */
    QTabWidget::pane {
        border: 1px solid #555555;
        background-color: #2e2e2e;
        border-radius: 4px;
    }
    QTabBar::tab {
        background-color: #444444;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
        margin: 2px;
    }
    QTabBar::tab:hover {
        background-color: #555555;
    }
    QTabBar::tab:selected {
        background-color: #666666;
    }
    """

    app.setStyleSheet(custom_stylesheet)
