StyleSheet = """
    #panel {
        background-color: #34373b;
        border-radius: 5px; 
    }
    QPushButton#menu_button {
        background-color: #3f4a5e;
        border-radius: 5px; 
        height: 34px;
        font-size: 46pt;
        text-align: left;
        padding: 8px;
    }
    QPushButton#menu_button:hover {
        background-color: #8c8c9c;
    }
    QPushButton#menu_button:pressed {
        background-color: #6f6f7d;
    }
    QPushButton#create_new_button {
        border: 2px solid #d8d8e3;
        color: #acacbf;
        border-radius: 5px; 
        height: 31px;
        font-size: 20pt;
        text-align: center;
        padding: 8px;
    }
    QSlider#current_achievement_button_progress_slider::groove:horizontal {
        background-color: black;
        height: 19px;
        width: 36px;
        border-radius: 2px;
    }
    QPushButton#back_button {
        border: 1px solid black;
        height: 36px;
        width: 36px;
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
    QPushButton#current_achievement_button {
        background-color: black;
        border-radius: 5px; 
        height: 34px;
        text-align: left;
        padding: 8px;
    }
    
    #current_achievement_button_title {
        color: white;
        font-size: 18pt;
    }
    
    #current_achievement_button_summary {
        color: white;
        font-size: 13pt;
    }
    
    #progress {
        text-align: center;
        border: 0;
        background-color: #202429;
        border-radius: 5px;
    }
    #progress:hover {
        border: 3px solid green;
    }
    #progress::chunk {
        background-color: #344f6e;
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
    }
    
    #icon {
        background-color: black;
        border: 0;
    }
    
    #current_achievement_info_page {
        background-color: white;
        border-radius: 5px; 
        padding: 8px;
    }
    
    
    
    #info_progress::groove:horizontal {
        background-color: black;
        height: 18px;
    }
    
    #info_progress::handle:horizontal {
        background-color: green;
        width: 3px;
        border-radius: 0px;
        margin: -2px 0px;
    }
    
    #info_progress::sub-page:horizontal {
        background-color: blue;
    }
    
    QPushButton#back_button {
        background-color: transparent;
        border: none;
        color: #437ccc;
    }
    
"""