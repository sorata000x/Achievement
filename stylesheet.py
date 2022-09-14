StyleSheet = """
    #panel {
        background-color: white;
        border-radius: 5px; 
    }
    QPushButton#menu_button {
        background-color: #acacbf;
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
    #menu_button_title {
        color: white;
    }
    #create_new_button {
        border: 2px solid #d8d8e3;
        color: #acacbf;
        border-radius: 5px; 
        height: 31px;
        font-size: 20pt;
        text-align: center;
        padding: 8px;
    }
    
    
    #current_achievement_button_progress_slider::groove:horizontal {
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
        background-color: white;
        border: 0;
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
        background-color: black;
        height: 50px;
        width: 226px;
        border-radius: 5px;
    }
    #progress::chunk {
        background-color: blue;
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
    
    
    
"""