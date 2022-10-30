StyleSheet = """
    #background_primary {
        background-color: #34373b;
    }
    #background_secondary {
        background-color: #484b4f;
    }


    #panel {
        background-color: #34373b;
        border-radius: 5px; 
    }
    
    
    
    
    
    QSlider#current_achievement_button_progress_slider::groove:horizontal {
        background-color: black;
        height: 19px;
        width: 36px;
        border-radius: 2px;
    }

    QScrollArea {
        background-color: #34373b;
        border: 0;
        padding: 0;
    }
    QScrollBar {
        background-color: #2f3236;
        width: 14px;
        border-radius: 2px;
    }
    QScrollBar::handle {
        background-color: #1d1f21;
        border: 7px solid transparent;
        border-radius: 6px;
        width: 6px;
    }
    QScrollBar::add-line, QScrollBar::sub-line {
        border: none;
        background: none;
    }
    #white-background {
        background-color: white;
    }
    
    QPushButton#back_button {
        background-color: transparent;
        border: none;
        color: #437ccc;
    }
    
    QLabel {
        color: white;
    }
    
    QLineEdit {
                background: #484b4f;
                color: white;
                border: none;
                font-size: 14pt;
                border-radius: 1px;
                padding: 3px;
            }
            QLineEdit::read-only {
                background: transparent;
            }
    QTextEdit {
        border: none;
        color: white;   
    }
    QTextEdit::read-only {
        background-color: transparent;
        color: white;
        border: none;
    }
"""