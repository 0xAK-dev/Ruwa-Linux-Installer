widget_style = """
QWidget {
    background: transparent;
}
"""

label_style = """
QLabel {
    color: white;
    background: transparent;
}
"""
label_second_style = label_style.replace("color: white;", "color: #888888;")
label_success_style = label_style.replace("color: white;", "color: #44e585;")

text_edit_style = """
QTextEdit {
    background-color: rgba(30, 30, 30, 160);
    color: white;
    border: 1px solid rgba(255, 255, 255, 80);
    border-radius: 15px;
    padding: 12px;
    selection-background-color: rgba(255, 255, 255, 180);
    selection-color: white;
}
"""
text_edit_error_style = text_edit_style.replace("color: white;",  "color: #EB5D72;")
    
scrollbar_style = """
QScrollBar:vertical {
    background: transparent;
    width: 8px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 100);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 180);
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

progress_bar_style = """
QProgressBar {
    border: none;
    background: #404040;
    border-radius: 3px;
    height: 3px;
    font-size: 3px;
    color: white;
}

QProgressBar::chunk {
    background: #FFFFFF;
    border-radius: 3px;
}
"""

