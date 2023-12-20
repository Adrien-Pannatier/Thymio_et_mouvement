import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image, ImageTk
from threading import Thread
from CTkToolTip import *
from datetime import datetime
import time

import numpy as np

from app.config import *
from app.utils.console import * 

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

DARK_COLOR = "#242424"
LIGHT_COLOR = "#ebebeb"

DEFAULT_LIGHT = "#dbdbdb"
DEFAULT_DARK = "#2b2b2b"

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="")
        self.label.pack(padx=20, pady=20)

class App(customtkinter.CTk):
    def __init__(self, modules, application_path):
        super().__init__()

        # init setting window
        self.settings_window = None
        # settings status
        self.settings_changed = False

        self.application_path = application_path


        # bind key events
        self.bind("<Key>", self.key_pressed_event)

        self.modules = modules

        self.mode = "Info"

        # info mode variables
        self.choreographies_list = list(modules.choreographer.choreography_dict.keys())
        self.sequences_list = list(modules.choreographer.sequence_dict.keys())

        # configure window
        self.title("Thymio mouvement organique")
        self.geometry(f"{900}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Thymio\nMouvement\nOrganique", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, text="⚙", width=10, command=self.settings_event)
        self.settings_button.grid(row=1, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 60))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 0))
        # self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        # self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        # self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
        #                                                        command=self.change_scaling_event)
        # self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main tabview
        self.tabview = customtkinter.CTkTabview(self, width=250, command=self.tabview_change_event)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Play")
        self.tabview.add("Record")
        self.tabview.add("Info")
        self.tabview.add("Edit")
        self.tabview.tab("Play").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Record").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)  
        self.tabview.tab("Edit").grid_columnconfigure(0, weight=1)

        # INFO TAB CREATION =================================================================================================
        # add "refresh" button
        self.refresh_button = customtkinter.CTkButton(self.tabview.tab("Info"), text="⟳", command=self.refresh_event)
        self.refresh_button.place(relx=0.01, rely=0.01, relwidth=0.05, relheight=0.05)

        # add "choreography list" frame
        self.chor_label = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Choreographies ", anchor="w")
        self.chor_label.place(relx=0.01, rely=0.07)
        self.chor_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Info"), fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.chor_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.35)
        self.chor_radio_var = tkinter.IntVar(value=0)
        self.scrollable_frame_chor = []
        if self.choreographies_list is not None:
            for i in range(len(self.choreographies_list)):
                newbutton = customtkinter.CTkRadioButton(master=self.chor_radiobutton_frame, variable=self.chor_radio_var, value=i, text=self.choreographies_list[i], command=self.refresh_info_chor)
                newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
                self.scrollable_frame_chor.append(newbutton)

        # add "choreography info" frame
        self.chor_info_frame = customtkinter.CTkFrame(self.tabview.tab("Info"))
        self.chor_info_frame.place(relx=0.4, rely=0.13, relwidth=0.56, relheight=0.35)
        # add text widget
        self.chor_info_text = customtkinter.CTkTextbox(self.chor_info_frame, wrap='none')
        self.chor_info_text.place(relx=0.01, rely=0, relwidth=0.98, relheight=1)
        self.chor_info_text.insert("1.0", "Choreography info")
        # make the text read only
        self.chor_info_text.configure(state="disabled")

        # add "sequence list" frame
        self.seq_label = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Sequences ", anchor="w")
        self.seq_label.place(relx=0.01, rely=0.55)
        self.seq_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Info"), fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.seq_radiobutton_frame.place(relx=0.01, rely=0.61, relwidth=0.33, relheight=0.35)
        self.seq_radio_var = tkinter.IntVar(value=0)
        self.scrollable_frame_seq = []
        if self.sequences_list is not None:
            for i in range(len(self.sequences_list)):
                newbutton = customtkinter.CTkRadioButton(master=self.seq_radiobutton_frame, variable=self.seq_radio_var, value=i, text=self.sequences_list[i], command=self.refresh_info_seq)
                newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
                self.scrollable_frame_seq.append(newbutton)

        # add "sequence info" frame
        self.seq_info_frame = customtkinter.CTkFrame(self.tabview.tab("Info"))
        self.seq_info_frame.place(relx=0.4, rely=0.61, relwidth=0.56, relheight=0.35)
        # add text widget
        self.seq_info_text = customtkinter.CTkTextbox(self.seq_info_frame, wrap='none')
        self.seq_info_text.place(relx=0.01, rely=0, relwidth=0.98, relheight=1)
        self.seq_info_text.insert("1.0", "Sequence info")
        # make the text read only
        self.seq_info_text.configure(state="disabled")

        # add tooltip frame on the top right corner
        self.info_tooltip_frame = customtkinter.CTkFrame(self.tabview.tab("Info"))
        self.info_tooltip_frame.place(relx=0.4, rely=0.01, relwidth=0.55, relheight=0.05)
        # add tooltip label
        self.info_tooltip_label = customtkinter.CTkLabel(self.info_tooltip_frame, text="❓", anchor="center")
        self.info_tooltip_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        # add tooltip
        self.info_tooltip = CTkToolTip(self.info_tooltip_label, justify="left", message="🤖 This is the info mode, here you can see what\n"
                                       + " are the avaliable choreographies and sequences.\n"
                                       + " You can also refresh the list by using the refresh\n"
                                       + " button at the top left corner.")

        # PLAY TAB CREATION =================================================================================================
        self.play_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Play"), values=["Choreography", "Sequence"], command=self.play_select_event)
        self.play_optionemenu.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.05)
        # add "list" frame
        self.play_label = customtkinter.CTkLabel(self.tabview.tab("Play"), text="", anchor="w")
        self.play_label.place(relx=0.01, rely=0.07)
        self.play_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Play"), fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.play_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.75)
        self.play_radio_var = tkinter.IntVar(value=-1)
        self.scrollable_frame_play = []

        # add title on the right
        self.play_title_label = customtkinter.CTkLabel(self.tabview.tab("Play"), text="PLAY MODE", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.play_title_label.place(relx=0.4, rely=0.01, relwidth=0.25, relheight=0.05)
        self.play_title_label.place(relx=0.38, rely=0.02, relwidth=0.25, relheight=0.05)


        # add thymio connection status frame underneath
        self.play_thymio_status_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_thymio_status_frame.place(relx=0.4, rely=0.77, relwidth=0.55, relheight=0.10)
        # add thymio connection status label
        self.play_thymio_status_label = customtkinter.CTkLabel(self.play_thymio_status_frame, text="Thymio status: Not connected", anchor="w")
        self.play_thymio_status_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        # add connect switch
        self.play_connect_variable = tkinter.BooleanVar(value=False)
        self.play_connect_switch = customtkinter.CTkSwitch(self.play_thymio_status_frame, text="", variable=self.play_connect_variable, command=self.play_connect_event)
        self.play_connect_switch.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")

        # add playtab tooltip
        # add tooltip frame
        self.play_tooltip_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_tooltip_frame.place(relx=0.4, rely=0.01, relwidth=0.55, relheight=0.05)
        # add tooltip label
        self.play_tooltip_label = customtkinter.CTkLabel(self.play_tooltip_frame, text="❓", anchor="center")
        self.play_tooltip_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        # add tooltip
        self.play_tooltip = CTkToolTip(self.play_tooltip_label, justify="left", message="🤖 This is the play mode, here you can play\n"
                                        + " choreographies and sequences on the thymio.\n"
                                        + " You can select what to play on the left.\n"
                                        + " Be sure to connect the thymio before playing.")
        

        # update bar variable
        self.update_bar_update = False

        # select optionemenu
        self.play_select_event("Choreography")

        # RECORD TAB CREATION ==============================================================================================
        # add settings frame on the left
        self.record_settings_frame = customtkinter.CTkFrame(self.tabview.tab("Record"), fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.record_settings_frame.place(relx=0.02, rely=0.02, relwidth=0.35, relheight=0.98)
        # add name label inside
        self.record_name_label = customtkinter.CTkLabel(self.record_settings_frame, text="Name:", anchor="w")
        self.record_name_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.05)
        # add name entry inside
        self.record_name_entry = customtkinter.CTkEntry(self.record_settings_frame)
        self.record_name_entry.place(relx=0.1, rely=0.07, relwidth=0.8, relheight=0.05)
        # add description label inside
        self.record_description_label = customtkinter.CTkLabel(self.record_settings_frame, text="Description:", anchor="w")
        self.record_description_label.place(relx=0.01, rely=0.13, relwidth=0.98, relheight=0.05)
        # add description textbox inside
        self.record_description_textbox = customtkinter.CTkTextbox(self.record_settings_frame)
        self.record_description_textbox.place(relx=0.05, rely=0.19, relwidth=0.9, relheight=0.2)

        # add title on the top right
        self.record_title_label = customtkinter.CTkLabel(self.tabview.tab("Record"), text="RECORD MODE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.record_title_label.place(relx=0.4, rely=0.02, relwidth=0.25, relheight=0.05)

        # add server status frame underneath
        self.record_server_status_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_server_status_frame.place(relx=0.4, rely=0.93, relwidth=0.55, relheight=0.05)
        # add server status label
        self.record_server_status_label = customtkinter.CTkLabel(self.record_server_status_frame, text="Server status: Not running", anchor="w")
        self.record_server_status_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.98, anchor="w")
        # add server slider
        self.record_server_switch_var = tkinter.BooleanVar(value=False)
        self.record_server_switch = customtkinter.CTkSwitch(self.record_server_status_frame, variable=self.record_server_switch_var,  text="", command=self.record_server_event)
        self.record_server_switch.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")

        # record tooltip
        # add tooltip frame
        self.record_tooltip_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_tooltip_frame.place(relx=0.4, rely=0.01, relwidth=0.55, relheight=0.05)
        # add tooltip label
        self.record_tooltip_label = customtkinter.CTkLabel(self.record_tooltip_frame, text="❓", anchor="center")
        self.record_tooltip_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        try: self.record_tooltip.hide() 
        except: pass
        # add tooltip
        self.record_tooltip = CTkToolTip(self.record_tooltip_label, justify="left", message="🤖 This is the record mode, here you can record\n"
                                        + " choreographies with the Mimyo robot. Please\n"
                                        + " be sure to connect to it first.\n")

        # self.display_record_layout() # for DEBUG PURPOSES ONLY

        
        # EDIT TAB CREATION ================================================================================================
        # add option menu mode between Manager and Create sequence
        self.editor_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Edit"), values=["Manage", "Create Sequence", "Create rand chor", "Set emotions"], command=self.editor_mode_select_event)
        self.editor_optionemenu.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.05)
        
        # select optionemenu
        self.editor_mode_select_event("Manage")






















        # SET DEFAULT VALUES ===============================================================================================
        self.appearance_mode_optionemenu.set("System")
        # self.scaling_optionemenu.set("100%")
        # lock window size
        self.resizable(False, False)
        # put info buttons to zero
        self.chor_radio_var.set(-1)
        self.seq_radio_var.set(-1)
        # deselect all optionmenu

    def tabview_change_event(self):
        # get the new tab
        new_tab = self.tabview.get()
        # check if the new tab is the edit tab
        if new_tab == "Edit":
            # check the mode
            if self.editor_optionemenu.get() == "Manage":
                # refresh the list
                if self.editor_manage_optionemenu.get() == "Choreography":
                    self.editor_manage_refresh_chor_list()
                elif self.editor_manage_optionemenu.get() == "Sequence":
                    self.editor_manage_refresh_seq_list()
                else:
                    error("Unexpected error: editor_manage_optionemenu is not Choreography or Sequence")
            elif self.editor_optionemenu.get() == "Create Sequence":
                # refresh the list
                self.play_refresh_chor_list()
            elif self.editor_optionemenu.get() == "Create rand chor":
                # refresh the list
                self.play_refresh_seq_list()
        elif new_tab == "Info":
            # refresh the list
            self.refresh_choreographies_list()
            self.refresh_sequences_list()
        elif new_tab == "Play":
            # get the optionemenu
            opt = self.play_optionemenu.get()
            # refresh the list
            if opt == "Choreography":
                self.play_refresh_chor_list()
            elif opt == "Sequence":
                self.play_refresh_seq_list()
        elif new_tab == "Record":
            # refresh the list
            pass

    def settings_event(self):
        self.settings_window = ToplevelWindow(self)  # create window if its None or destroyed
        # set title
        self.settings_window.title("Settings")
        self.settings_window.after(100,self.settings_window.lift) # Workaround for bug where main window takes focus
        # give focus to the window
        self.settings_window.focus()

        # add path frame in settings window
        self.settings_path_frame = customtkinter.CTkFrame(self.settings_window, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.settings_path_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        # add path label
        self.settings_path_chor_label = customtkinter.CTkLabel(self.settings_path_frame, text="Choreography path:", anchor="w")
        self.settings_path_chor_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.05)
        # add path entry
        self.settings_path_chor_entry = customtkinter.CTkEntry(self.settings_path_frame)
        self.settings_path_chor_entry.place(relx=0.1, rely=0.2, relwidth=0.6, relheight=0.1)
        # put the actual path inside
        self.settings_path_chor_entry.insert(0, self.modules.choreographer.choreography_path)
        # add path button
        self.settings_path_chor_button = customtkinter.CTkButton(self.settings_path_frame, text="...", command=self.settings_path_chor_event)
        self.settings_path_chor_button.place(relx=0.75, rely=0.2, relwidth=0.1, relheight=0.1)
        # add path label
        self.settings_path_seq_label = customtkinter.CTkLabel(self.settings_path_frame, text="Sequence path:", anchor="w")
        self.settings_path_seq_label.place(relx=0.01, rely=0.4, relwidth=0.98, relheight=0.05)
        # add path entry
        self.settings_path_seq_entry = customtkinter.CTkEntry(self.settings_path_frame)
        self.settings_path_seq_entry.place(relx=0.1, rely=0.5, relwidth=0.6, relheight=0.1)
        # put the actual path inside
        self.settings_path_seq_entry.insert(0, self.modules.choreographer.sequence_path)
        # add path button
        self.settings_path_seq_button = customtkinter.CTkButton(self.settings_path_frame, text="...", command=self.settings_path_seq_event)
        self.settings_path_seq_button.place(relx=0.75, rely=0.5, relwidth=0.1, relheight=0.1)
        # add default button
        self.settings_default_button = customtkinter.CTkButton(self.settings_path_frame, text="Default", command=self.settings_default_event)
        self.settings_default_button.place(relx=0.01, rely=0.7, relwidth=0.98, relheight=0.1)
        # add save button
        self.settings_save_button = customtkinter.CTkButton(self.settings_path_frame, text="Save", command=self.settings_save_event)
        self.settings_save_button.place(relx=0.01, rely=0.9, relwidth=0.98, relheight=0.1)

    def settings_path_chor_event(self):
        path = tkinter.filedialog.askdirectory()
        if path != "":
            self.settings_path_chor_entry.delete(0, "end")
            self.settings_path_chor_entry.insert(0, path)
            self.settings_changed = True
            # refocus on settings window
        self.settings_window.focus()

    def settings_path_seq_event(self):
        path = tkinter.filedialog.askdirectory()
        if path != "":
            self.settings_path_seq_entry.delete(0, "end")
            self.settings_path_seq_entry.insert(0, path)
            self.settings_changed = True
        # refocus on settings window
        self.settings_window.focus()
    
    def settings_default_event(self):
        self.settings_path_chor_entry.delete(0, "end")
        self.settings_path_chor_entry.insert(0, DEFAULT_PATH_CHOREO)
        self.settings_path_seq_entry.delete(0, "end")
        self.settings_path_seq_entry.insert(0, DEFAULT_PATH_SEQUENCE)
        self.settings_changed = True
        # refocus on settings window
        self.settings_window.focus()

    def settings_save_event(self):
        # check if the path changed
        if self.settings_changed:
            # ask if the user wants to save
            answer = tkinter.messagebox.askyesno("Save settings", "Do you want to save the settings?")
            if answer == False:
                # close the settings window
                self.settings_window.destroy()
                self.settings_changed = False
                return
        # get the path
        path_chor = self.settings_path_chor_entry.get()
        path_seq = self.settings_path_seq_entry.get()
        self.modules.choreographer.choreography_path = path_chor
        self.modules.choreographer.sequence_path = path_seq
        self.modules.choreographer.save_settings()
        # close the settings window
        self.settings_window.destroy()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        # refresh the graph image if in manage editor mode
        if self.editor_optionemenu.get() == "Manage":
            if self.editor_manage_optionemenu.get() == "Choreography":
                self.refresh_editor_info_chor()

    # def change_scaling_event(self, new_scaling: str):
    #     new_scaling_float = int(new_scaling.replace("%", "")) / 100
    #     try:
    #         customtkinter.set_widget_scaling(new_scaling_float)
    #     except Exception as e:
    #         error(f"Unexpected error: {e}")

    def key_pressed_event(self, event):
        # debug(f"Key pressed: {event.keysym}")
        # if the key pressed is Enter
        if event.keysym == "Return":
        # delete mode
            pass
        if event.keysym == "Delete":
            # check the tab
            if self.tabview.tab("Edit").winfo_ismapped():
                # check the mode
                if self.editor_optionemenu.get() == "Manage":
                    info("Delete mode")
                    # call the delete function
                    self.editor_manage_delete_event()
         
    def save_choreographies(self):
        self.modules.choreographer.save_choreography_dict()

    def save_choreography(self, choreography_name: str):
        self.modules.choreographer.save_choreography(choreography_name)




    # INFO METHODS --------------------------------------------------------------------------------------------------------
    def refresh_event(self):
        self.refresh()
        self.refresh_choreographies_list()
        self.refresh_sequences_list()

    def refresh(self):
        # empty both lists
        self.choreographies_list = []
        self.sequences_list = []
        # asl choreographer for loading
        self.modules.choreographer.update_database()
        # refresh choreography list
        self.choreographies_list = list(self.modules.choreographer.choreography_dict.keys())
        # refresh sequence list
        self.sequences_list = list(self.modules.choreographer.sequence_dict.keys())

    def refresh_info_chor(self):
        index = self.chor_radio_var.get()
        name = self.choreographies_list[index]
        choreography_name, creation_date, last_modified, description, speed_factor, path = self.modules.choreographer.choreography_dict[name].get_info()
        self.chor_info_text.configure(state="normal")
        self.chor_info_text.delete("1.0", "end")
        # print every info
        self.chor_info_text.insert("insert", f"Name:\t\t{choreography_name}\nCreation date:\t\t{creation_date}\nLast modified:\t\t{last_modified}\nDescription:\t\t{description}\nSpeed factor:\t\t{str(speed_factor)}")
        self.chor_info_text.configure(state="disabled")
        self.chor_info_text.tag_config("bluename", foreground="#1e5eac")
        self.chor_info_text.tag_add("bluename", "1.0", "1.5")
        self.chor_info_text.tag_config("bluecreadate", foreground="#1e5eac")
        self.chor_info_text.tag_add("bluecreadate", "2.0", "2.14")
        self.chor_info_text.tag_config("bluelastmod", foreground="#1e5eac")
        self.chor_info_text.tag_add("bluelastmod", "3.0", "3.14")
        self.chor_info_text.tag_config("bluedesc", foreground="#1e5eac")
        self.chor_info_text.tag_add("bluedesc", "4.0", "4.13")
        self.chor_info_text.tag_config("bluespeed", foreground="#1e5eac")
        self.chor_info_text.tag_add("bluespeed", "5.0", "5.13")
        self.chor_info_text.configure(state="disabled")

    def refresh_info_seq(self):
        index = self.seq_radio_var.get()
        name = self.sequences_list[index]
        sequence_name, creation_date, description, path, sequence_order, emotions = self.modules.choreographer.sequence_dict[name].get_info()
        self.seq_info_text.configure(state="normal")
        self.seq_info_text.delete("1.0", "end")
        seq_names = self.info_seq_number_to_name(sequence_order)
        self.seq_info_text.insert("1.0", f"Name:\t\t{sequence_name}\nCreation date:\t\t{creation_date}\nDescription:\t\t{description}\nSequence order:\t\t{sequence_order}\nSequences:\t\t{seq_names}\nEmotions:\t\t{emotions}")
        self.seq_info_text.tag_config("bluename", foreground="#1e5eac")
        self.seq_info_text.tag_add("bluename", "1.0", "1.5")
        self.seq_info_text.tag_config("bluecreadate", foreground="#1e5eac")
        self.seq_info_text.tag_add("bluecreadate", "2.0", "2.14")
        self.seq_info_text.tag_config("bluedesc", foreground="#1e5eac")
        self.seq_info_text.tag_add("bluedesc", "3.0", "3.13")
        self.seq_info_text.tag_config("blueseqorder", foreground="#1e5eac")
        self.seq_info_text.tag_add("blueseqorder", "4.0", "4.15")
        self.seq_info_text.tag_config("blueseq", foreground="#1e5eac")
        self.seq_info_text.tag_add("blueseq", "5.0", "5.11")
        self.seq_info_text.tag_config("blueemotions", foreground="#1e5eac")
        self.seq_info_text.tag_add("blueemotions", "6.0", "6.9")
        self.seq_info_text.configure(state="disabled")
    
    def info_seq_number_to_name(self, sequence_order):
        sequence_names = ""
        for chor_index in sequence_order:
            sequence_names +=  " -> " + str(self.choreographies_list[chor_index-1])
        return sequence_names

    def refresh_choreographies_list(self):
        # remove all buttons
        for button in self.scrollable_frame_chor:
            # if in tab manage
            button.destroy() if button is not None else None
        self.scrollable_frame_chor = []
        for i in range(len(self.choreographies_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.chor_radiobutton_frame, variable=self.chor_radio_var, value=i, text=self.choreographies_list[i], command=self.refresh_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_chor.append(newbutton)
        self.chor_radio_var.set(-1)


    def remove_choreography(self, index):
        self.choreographies_list.pop(index)
        self.refresh_choreographies_list()

    def refresh_sequences_list(self):
        # remove all buttons
        for button in self.scrollable_frame_seq:
            button.destroy()
        self.scrollable_frame_seq = []
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.seq_radiobutton_frame, variable=self.seq_radio_var, value=i, text=self.sequences_list[i], command=self.refresh_info_seq)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_chor.append(newbutton)
        self.seq_radio_var.set(-1)

    def remove_sequence(self, index):
        self.sequences_list.pop(index)
        self.refresh_sequences_list()

    # PLAY METHODS --------------------------------------------------------------------------------------------------------
    def play_select_event(self, new_play_mode: str):
        if new_play_mode == "Choreography":
            self.play_refresh_chor_list()
        elif new_play_mode == "Sequence":
            self.play_refresh_seq_list()
    
    def play_refresh_chor_list(self):
        # remove all buttons
        for button in self.scrollable_frame_play:
            button.destroy()
        self.scrollable_frame_play = []
        for i in range(len(self.choreographies_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.play_radiobutton_frame, variable=self.play_radio_var, value=i, text=self.choreographies_list[i], command=self.refresh_play_info)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_play.append(newbutton)
        self.play_radio_var.set(-1)
    
    def play_refresh_seq_list(self):
        # remove all buttons
        for button in self.scrollable_frame_play:
            button.destroy()
        self.scrollable_frame_play = []
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.play_radiobutton_frame, variable=self.play_radio_var, value=i, text=self.sequences_list[i], command=self.refresh_play_info)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_play.append(newbutton)
        self.play_radio_var.set(-1)

    def refresh_play_info(self):
        # get the new play mode
        play_mode = self.play_optionemenu.get()
        # get the connection status
        connection_status = self.play_connect_switch.get()
        # progress bar to 0
        # self.play_progress_bar.set(0)
        if connection_status == True:
            # get the selection
            index = self.play_radio_var.get()
            if play_mode == "Choreography":
                # deactivate loop checkbox
                self.play_loop_checkbox.configure(state="normal")
                if index != -1:
                    name = self.choreographies_list[index]
                    choreography_name, _, _, _, speed_factor, _ = self.modules.choreographer.choreography_dict[name].get_info()
                    self.play_chor_name_label_across.configure(text=f"{choreography_name}")
                else:
                    speed_factor = 1
                # show the speed factor entry
                self.play_speed_factor_entry.configure(state="normal")
                self.play_speed_factor_entry.delete(0, "end")
                self.play_speed_factor_entry.insert(0, str(speed_factor))
                self.play_speed_factor_entry.configure(fg_color = ("#f9f9fa","#343638"))
                self.play_nbr_repetition_entry.configure(state="normal")
                self.play_nbr_repetition_entry.delete(0, "end")
                if self.play_loop_checkbox.get() == False:
                    self.play_nbr_repetition_entry.insert(0, "1")
            elif play_mode == "Sequence":
                if index != 0:
                    name = self.sequences_list[index]
                    sequence_name, _, _, _, _, _ = self.modules.choreographer.sequence_dict[name].get_info()
                    self.play_chor_name_label_across.configure(text=f"{sequence_name}") if index != -1 else None
                self.play_nbr_repetition_entry.delete(0, "end")
                self.play_nbr_repetition_entry.insert(0, "1")
                # deactivate loop checkbox
                self.play_loop_checkbox.deselect()
                self.play_loop_checkbox.configure(state="disabled")
                # activate the speed factor entry in case loop was selected
                self.play_nbr_repetition_entry.configure(state="normal")
                # set the color back to normal
                self.play_nbr_repetition_entry.configure(fg_color = ("#f9f9fa","#343638"))
                
        
    def play_loop_event(self):
        # get the loop status
        loop_tick_status = self.play_loop_checkbox.get()
        if loop_tick_status == True:
            # lock the nbr repetitions entry
            self.play_nbr_repetition_entry.delete(0, "end")
            self.play_nbr_repetition_entry.configure(state="disabled")
            # change the color of the entry
            self.play_nbr_repetition_entry.configure(fg_color = (LIGHT_COLOR,DARK_COLOR))
        elif loop_tick_status == False:
            # unlock the nbr repetitions entry
            self.play_nbr_repetition_entry.configure(state="normal")
            self.play_nbr_repetition_entry.delete(0, "end")
            # change the color of the entry
            self.play_nbr_repetition_entry.configure(fg_color = ("#f9f9fa","#343638"))

    def play_connect_event(self):
        # get the connection status
        connection_status = self.play_connect_switch.get()
        if connection_status == True:
            # try to connect the thymio
            self.play_thymio_status_label.configure(text="Thymio status: Connecting...", text_color=("#1a1a1a","#dce4ee"))
            self.play_connect_threading()

        if connection_status == False:
            # disconnect from the thymio
            self.modules.motion_control.disconnect_thymio()
            self.play_thymio_status_label.configure(text="Thymio status: Not connected")
            self.remove_play_layout()

    def play_connect_threading(self):
        # create the thread
        self.connect_thread = Thread(target=self.play_connect)
        # start the thread
        self.connect_thread.start()

    def play_connect(self):
        if not self.modules.motion_control.init_thymio_connection():
            # if the connection failed, set the slider back to false
            self.play_connect_variable.set(False)
            self.connection_status = False
            self.play_thymio_status_label.configure(text="Thymio status: Failed to connect", text_color="red")
        else:            
            # try to connect to the thymio
            self.play_thymio_status_label.configure(text="Thymio status: Connected")
            self.update_play_tooltip()
            self.display_play_layout()
            self.refresh_play_info()
            # # load emotions
            self.modules.choreographer.load_emotions(node=self.modules.motion_control.node, client=self.modules.motion_control.client)


    def display_play_layout(self):
        # add settings frame underneath
        self.play_settings_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_settings_frame.place(relx=0.4, rely=0.07, relwidth=0.55, relheight=0.35)
        # add settings widgets
        # add choreography name label
        self.play_chor_name_label = customtkinter.CTkLabel(self.play_settings_frame, text="Name:", anchor="w")
        self.play_chor_name_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.15)
        # add name label across
        self.play_chor_name_label_across = customtkinter.CTkLabel(self.play_settings_frame, text="", anchor="e")
        self.play_chor_name_label_across.place(relx=0.3, rely=0.1, relwidth=0.45, relheight=0.15)
        # add speed factor entry
        self.play_speed_factor_label = customtkinter.CTkLabel(self.play_settings_frame, text="Speed factor:", anchor="w")
        self.play_speed_factor_label.place(relx=0.01, rely=0.3, relwidth=0.98, relheight=0.15)
        self.play_speed_factor_entry = customtkinter.CTkEntry(self.play_settings_frame)
        self.play_speed_factor_entry.place(relx=0.65, rely=0.3, relwidth=0.1, relheight=0.15)
        # add nbr repetition entry
        self.play_nbr_repetition_label = customtkinter.CTkLabel(self.play_settings_frame, text="Nbr repetition:", anchor="w")
        self.play_nbr_repetition_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.15)
        self.play_nbr_repetition_entry = customtkinter.CTkEntry(self.play_settings_frame)
        self.play_nbr_repetition_entry.place(relx=0.65, rely=0.5, relwidth=0.1, relheight=0.15)
        # add loop checkbox
        self.play_loop_checkbox = customtkinter.CTkCheckBox(self.play_settings_frame, text="Loop", command=self.play_loop_event)
        self.play_loop_checkbox.place(relx=0.01, rely=0.7, relwidth=0.98, relheight=0.15)

        # add play frame underneath
        self.play_play_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_play_frame.place(relx=0.4, rely=0.53, relwidth=0.55, relheight=0.10)
        # add play pause and stop buttons
        self.play_play_button = customtkinter.CTkButton(self.play_play_frame, text="▶", command=self.play_event)
        self.play_play_button.place(relx=0.01, rely=0.5, relwidth=0.25, relheight=0.98, anchor="w")
        self.play_pause_button = customtkinter.CTkButton(self.play_play_frame, text="||", command=self.pause_event)
        self.play_pause_button.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.98, anchor="center")
        self.play_stop_button = customtkinter.CTkButton(self.play_play_frame, text="■", command=self.stop_event)
        self.play_stop_button.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")

        # add progress frame underneath
        self.play_progress_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_progress_frame.place(relx=0.4, rely=0.65, relwidth=0.55, relheight=0.10)
        # add progress bar inside
        self.play_progress_bar = customtkinter.CTkProgressBar(self.play_progress_frame, orientation="horizontal") # set value between 1 and 0
        self.play_progress_bar.set(0)
        self.play_progress_bar.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        # put progress bar to 0

        # add label play frame over the buttons
        self.play_play_label = customtkinter.CTkLabel(self.tabview.tab("Play"), text="", anchor="w")
        self.play_play_label.place(relx=0.4, rely=0.45, relwidth=0.5, relheight=0.1, anchor="w")

    def remove_play_layout(self):
        self.play_settings_frame.destroy() if hasattr(self, "play_settings_frame") else None
        self.play_play_frame.destroy() if hasattr(self, "play_play_frame") else None
        self.play_progress_frame.destroy() if hasattr(self, "play_progress_frame") else None
        self.play_play_label.destroy() if hasattr(self, "play_play_label") else None

    def play_event(self):
        # check if a choreography/sequence is selected
        if self.play_radio_var.get() == -1:
            tkinter.messagebox.showwarning("Warning", "Please select a choreography or sequence")
            return
        # check if a number of repetition is entered
        elif self.play_nbr_repetition_entry.get() == "" and self.play_loop_checkbox.get() == False:
            tkinter.messagebox.showwarning("Warning", "Please enter a number of repetition")
            return
        # check if a speed factor is entered
        elif self.play_speed_factor_entry.get() == "":
            tkinter.messagebox.showwarning("Warning", "Please enter a speed factor between 0 and 10")
            return
        # check if number of repetition is an int
        try:
            if self.play_loop_checkbox.get() == False:
                int(self.play_nbr_repetition_entry.get())
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter a number of repetition")
            return
        # check if speed factor is a float
        try:
            speed_fact = float(self.play_speed_factor_entry.get())
            if speed_fact<=0 or speed_fact>=10:
                raise 
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter a valid speed factor between 0 and 10")
            return
        
        if self.modules.motion_control.choreography_status != "play":
            self.play_progress_bar.set(0)
            self.play_threading_action()

    def play_threading_action(self):
        # thread for playing
        self.playthread = Thread(target=self.play, daemon=True)
        self.playthread.start()

    def play_threading_progress(self):
        # thread for progress bar
        self.progress_thread = Thread(target=self.update_progress, daemon=True)
        self.progress_thread.start()

    def play(self):
        # get the play mode
        play_mode = self.play_optionemenu.get()
        # get the selection
        index = self.play_radio_var.get()
        # get speed factor
        speed_factor = self.play_speed_factor_entry.get()
        # get the play status
        play_status = self.modules.motion_control.choreography_status
        # update bar update
        self.update_bar_update = True
        if play_status == "stop":
            # lock every entry and slider
            self.play_speed_factor_entry.configure(state="disabled")
            self.play_nbr_repetition_entry.configure(state="disabled")
            self.play_loop_checkbox.configure(state="disabled")
            self.play_connect_switch.configure(state="disabled")
            # set the play_status to play
            self.modules.motion_control.choreography_status = "play"
            self.play_threading_progress()
            if play_mode == "Choreography":
                name = self.choreographies_list[index]
                choreography = self.modules.choreographer.choreography_dict[name]
                self.play_play_label.configure(text=f"Now playing {name}")
                # get loop status
                loop_status = self.play_loop_checkbox.get()
                if loop_status == True:
                    self.modules.motion_control.play_choreography(choreography, float(speed_factor), "loop")
                    self.modules.motion_control.choreography_status = "stop"
                    self.modules.motion_control.stop_motors()
                    info("choreography played")
                elif loop_status == False:
                    # get nbr repetition
                    nbr_repetition = self.play_nbr_repetition_entry.get()
                    self.modules.motion_control.play_choreography(choreography, float(speed_factor), "mult", int(nbr_repetition))
                    info("choreography played")
                    self.modules.motion_control.choreography_status = "stop"
                    self.modules.motion_control.stop_motors()
                self.play_play_label.configure(text="")
            elif play_mode == "Sequence":
                name = self.sequences_list[index]
                sequence = self.modules.choreographer.sequence_dict[name]
                # get loop status
                # loop_status = self.play_loop_checkbox.get() # IMPLEMENT THAT °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
                # for every choreography in the sequence
                # get nbr repetition
                nbr_repetition = self.play_nbr_repetition_entry.get()
                # get first emotion name if any
                try:
                    emotion_name = self.modules.choreographer.sequence_dict[name].emotion_list[0]
                except:
                    emotion_name = None
                # create the emotion object
                emotion = self.modules.choreographer.emotion_dict[emotion_name] if emotion_name != None else None
                # debug(f"emotion name: {emotion_name}")
                # debug(f"emotion: {emotion}")
                for i in range(int(nbr_repetition)):
                    for choreography_index in sequence.sequence_l:
                        # transform the index into a name
                        choreography_name = self.choreographies_list[choreography_index-1]
                        self.play_play_label.configure(text=f"Now playing:\t{choreography_name}")
                        # get the choreography
                        choreography = self.modules.choreographer.choreography_dict[choreography_name]
                        info(f"now playing:\t{choreography_name}")
                        self.modules.motion_control.choreography_status = "play"
                        self.modules.motion_control.play_choreography(choreography, float(speed_factor), "mult", int(nbr_repetition), emotion)
                        if self.modules.motion_control.choreography_status == "stop":
                            self.modules.motion_control.stop_motors()
                            # unlock every entry and slider
                            self.play_speed_factor_entry.configure(state="normal")
                            self.play_nbr_repetition_entry.configure(state="normal") if self.play_loop_checkbox.get() == False else None
                            self.play_loop_checkbox.configure(state="normal")
                            self.play_connect_switch.configure(state="normal")
                            self.update_bar_update = False
                            return
                self.play_play_label.configure(text="")
                self.modules.motion_control.choreography_status = "stop"
                self.modules.motion_control.stop_motors()

        elif play_status == "pause":
            # set the play_status to play
            self.modules.motion_control.choreography_status = "play"
            self.play_threading_progress()
            return

        # unlock every entry and slider
        self.play_speed_factor_entry.configure(state="normal")
        self.play_nbr_repetition_entry.configure(state="normal") if self.play_loop_checkbox.get() == False else None
        self.play_loop_checkbox.configure(state="normal")
        self.play_connect_switch.configure(state="normal")
        self.update_bar_update = False
        return


    def pause_event(self):
        if self.modules.motion_control.choreography_status == "play":
            self.modules.motion_control.choreography_status = "pause"
            # debug("pause button pressed")
            self.modules.motion_control.pause_by_button = True

    def stop_event(self):
        self.modules.motion_control.choreography_status = "stop"

    def update_progress(self):
        # while thymio is connected
        while self.play_connect_switch.get() == True:
            if self.update_bar_update == True:
                self.set_progress(self.modules.motion_control.completion_percentage)
                time.sleep(0.1)
            else:
                return

    def set_progress(self, value):
        # between 0 and 1
        self.play_progress_bar.set(value)

    def update_play_tooltip(self):
        # update tooltip
        self.play_tooltip.hide()
        self.play_tooltip_2 = CTkToolTip(self.play_tooltip_label, justify="left", message="🤖 This is the play mode, here you can play\n"
                                        + " choreographies and sequences on the thymio.\n"
                                        + " You can select what to play on the left. You\n"
                                        + " can also change the speed factor, the number\n"
                                        + " of repetitions and wether you want a loop or not\n")

    # RECORD METHODS ------------------------------------------------------------------------------------------------------
    def record_server_event(self):
        # get the server status
        server_status = self.record_server_switch.get()
        if server_status == True:
            self.display_record_connecting_message()
            # try to connect to the thymio
            self.record_server_status_label.configure(text="Server status: Connecting")
            self.modules.process_controler_data.init_record()
            self.connect_threading()
        elif server_status == False:
            # disconnect from the thymio
            self.modules.process_controler_data.close_connection()
            self.record_server_status_label.configure(text="Server status: Not running")
            self.remove_record_layout()

    def display_record_connecting_message(self):
        # add text box in the middle
        self.record_connecting_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_connecting_frame.place(relx=0.5, rely=0.25, relwidth=0.55, relheight=0.65)
        # add label inside in the middle
        self.record_connecting_label = customtkinter.CTkLabel(self.record_connecting_frame, text="Connecting to Mimyo...", anchor="w")
        self.record_connecting_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

    def connect_threading(self):
        # thread for connecting
        self.connectthread = Thread(target=self.connect, daemon=True)
        self.connectthread.start()

    def connect(self):
        # try to connect to the thymio
        if self.modules.process_controler_data.accept_connection():
            self.record_server_status_label.configure(text="Server status: Running")
            self.display_record_layout()
        else:
            self.record_server_status_label.configure(text="Server status: Not connected")
            self.remove_record_layout()
            # if the connection failed, set the switch back to false
            self.record_server_switch_var.set(False)

    def display_record_layout(self):
        # add open settings button on top right
        self.record_settings_button = customtkinter.CTkButton(self.tabview.tab("Record"), text="⚙️", command=self.record_settings_event)
        self.record_settings_button.place(relx=0.85, rely=0.01, relwidth=0.05, relheight=0.05)
        # add record frame underneath
        self.record_record_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_record_frame.place(relx=0.4, rely=0.1, relwidth=0.55, relheight=0.10)
        # add record and stop buttons inside
        self.record_record_button = customtkinter.CTkButton(self.record_record_frame, text="◉", command=self.record_event)
        self.record_record_button.place(relx=0.01, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        # self.record_stop_button = customtkinter.CTkButton(self.record_record_frame, text="■", command=self.stop_event_record)
        # self.record_stop_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        # add debug button inside
        self.record_calibrate_button = customtkinter.CTkButton(self.record_record_frame, text="Calib", command=self.calibrate_event)
        self.record_calibrate_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")

        # add info box in the middle
        self.record_info_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_info_frame.place(relx=0.4, rely=0.25, relwidth=0.55, relheight=0.65)
        # add label inside
        self.record_info_label = customtkinter.CTkLabel(self.record_info_frame, text="Info:", anchor="w")
        self.record_info_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.15)
        # add textbox inside
        self.record_info_textbox = customtkinter.CTkTextbox(self.record_info_frame, wrap='none', state="disabled")
        self.record_info_textbox.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.78)

        # add calibration value display frame top right
        self.record_calibration_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_calibration_frame.place(relx=0.75, rely=0.2, relwidth=0.1, relheight=0.05)
        self.record_calibration_label = customtkinter.CTkLabel(self.record_calibration_frame, text="Calibration:", anchor="w")
        self.record_calibration_label.place(relx=0.01, rely=0.3, relwidth=1, relheight=0.5)
        loaded_calibration, self.gyro_offset = self.modules.process_controler_data.load_calibration()
        self.record_calibration_entrybox = customtkinter.CTkEntry(self.tabview.tab("Record"), fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.record_calibration_entrybox.place(relx=0.855, rely=0.2, relwidth=0.08, relheight=0.05)
        self.record_calibration_entrybox.insert(0, loaded_calibration)
        self.record_calibration_entrybox.configure(state="disabled")
        
        # add calbration button next to title, on the right
        # self.record_calibration_button = customtkinter.CTkButton(self.tabview.tab("Record"), text="Calibrate", command=self.calibrate_event)
        # self.record_calibration_button.place(relx=0.65, rely=0.02, relwidth=0.1, relheight=0.05)

        # change info tooltip
        # hide the old tooltip
        self.record_tooltip.hide()
        self.record_tooltip = CTkToolTip(self.record_tooltip_label, justify="left", message="🤖 This is the record mode, here you can record\n"
                                         + " by pressing the record button. You can also\n"
                                         + " calibrate the thymio by pressing the calibrate\n"
                                         + " button or change the calibration manually with\n"
                                         + " the option button on the top right.\n")

    def remove_record_layout(self):
        # remove all widgets
        self.record_connecting_frame.destroy() if hasattr(self, "record_connecting_frame") else None
        self.record_record_frame.destroy() if hasattr(self, "record_record_frame") else None
        self.record_info_frame.destroy() if hasattr(self, "record_info_frame") else None
        self.record_calibration_entrybox.destroy() if hasattr(self, "record_calibration_entrybox") else None
        self.record_calibration_frame.destroy() if hasattr(self, "record_calibration_frame") else None

    def record_settings_event(self):
        # load calibration and gyro scaling
        self.calibration_offset, self.gyro_scaling = self.modules.process_controler_data.load_calibration()
        # create the top level window
        self.record_settings_window = ToplevelWindow(self)
        self.record_settings_window.title("Settings")
        self.record_settings_window.geometry("200x100")
        # set location of the window
        self.record_settings_window.geometry("+%d+%d" % (self.record_settings_window.winfo_screenwidth()/2-100, self.record_settings_window.winfo_screenheight()/2-50))
        self.record_settings_window.resizable(False, False)
        self.record_settings_window.after(100,self.record_settings_window.lift) # Workaround for bug where main window takes focus
        # give the focus to the top level window
        self.record_settings_window.focus()
        self.record_settings_window.grab_set()
        # add calibration and gyro scaling labels and entry boxes
        self.record_calibration_label = customtkinter.CTkLabel(self.record_settings_window, text="Calibration:", anchor="w")
        self.record_calibration_label.place(relx=0.01, rely=0.1, relwidth=0.5, relheight=0.15)
        self.record_calibration_entrybox_tl = customtkinter.CTkEntry(self.record_settings_window, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.record_calibration_entrybox_tl.place(relx=0.6, rely=0.1, relwidth=0.3, relheight=0.2)
        self.record_calibration_entrybox_tl.insert(0, self.calibration_offset)
        self.record_gyro_label = customtkinter.CTkLabel(self.record_settings_window, text="Gyro scaling:", anchor="w")
        self.record_gyro_label.place(relx=0.01, rely=0.4, relwidth=0.5, relheight=0.15)
        self.record_gyro_entrybox = customtkinter.CTkEntry(self.record_settings_window, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.record_gyro_entrybox.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.2)
        self.record_gyro_entrybox.insert(0, self.gyro_scaling)
        # add save button
        self.record_save_button = customtkinter.CTkButton(self.record_settings_window, text="Save", command=self.save_event)
        self.record_save_button.place(relx=0.01, rely=0.75, relwidth=0.98, relheight=0.2)

    def save_event(self):
        # get the calibration offset
        self.calibration_offset = self.record_calibration_entrybox_tl.get()
        self.gyro_scaling = self.record_gyro_entrybox.get()
        # save the calibration offset
        self.modules.process_controler_data.save_calibration(self.calibration_offset, self.gyro_scaling)
        # destroy the top level window
        self.record_settings_window.destroy()
        # update the calibration offset label
        if self.record_calibration_entrybox != None:
            self.record_calibration_entrybox.configure(state="normal")
            self.record_calibration_entrybox.delete(0, "end")
            self.record_calibration_entrybox.insert(0, str(self.calibration_offset))
            self.record_calibration_entrybox.configure(state="disabled")
        
    def calibrate_event(self):
        self.calibration_offset = self.record_calibration_entrybox.get()

        # block connection slider
        self.record_server_switch.configure(state="disabled")

        # check if the calibration is already done
        loaded_calibration, _ = self.modules.process_controler_data.load_calibration()

        if loaded_calibration != None:
            # display the calibration value
            self.record_calibration_entrybox.configure(state="normal")
            self.record_calibration_entrybox.delete(0, "end")
            self.record_calibration_entrybox.insert(0, str(loaded_calibration))
            self.record_calibration_entrybox.configure(state="disabled")
            # ask the use if he wants to recalibrate
            answer = tkinter.messagebox.askquestion("Warning", f"A calibration already exists, do you want to recalibrate?\n The previous calibration is {loaded_calibration}")
            if answer == "no":
                # show the calibration parameter
                self.record_info_textbox.insert("end", f"\nOffset : {loaded_calibration}")
                self.calibration_offset = loaded_calibration
                # unblock connection slider
                self.record_server_switch.configure(state="normal")
                return
            
        # update the message in the info box
        self.record_info_textbox.configure(state="normal")
        self.record_info_textbox.delete("1.0", "end")
        self.record_info_textbox.insert("1.0", "Calibrating...")

        # ask to move the robot 20cm forward
        self.record_info_textbox.insert("end", "\nPlease move the robot 20cm forward")
        # change the calibration status to on
        self.modules.process_controler_data.calibration_on = True
        # activate the thread
        self.calibration_threading()

    def calibration_threading(self):
        # thread for calibration
        self.calibrationthread = Thread(target=self.calibrate, daemon=True)
        self.calibrationthread.start()
        # start progression thread
        self.record_progressthread = Thread(target=self.update_progress_record, daemon=True)
        self.record_progressthread.start()

    def calibrate(self):
        # get the calibration offset
        self.calibration_offset = self.modules.process_controler_data.calibration()
        last_cal = self.record_calibration_entrybox.get()
        # save the calibration offset
        self.modules.process_controler_data.save_calibration(self.calibration_offset, self.gyro_offset)
        time.sleep(2)
        # destroy the top level window
        self.record_progress_window.destroy()
        answer = tkinter.messagebox.askquestion("Warning", f"New calibration is {self.calibration_offset}, do you want to keep it?")
        if answer == "no":
            self.calibration_offset = last_cal
            self.modules.process_controler_data.save_calibration(self.calibration_offset, self.gyro_offset)
        # show the calibration parameter
        self.record_info_textbox.insert("end", f"\nOffset : {self.calibration_offset}")
        # start the calibration thread
        self.record_info_textbox.configure(state="disabled")
        # unblock connection slider
        self.record_server_switch.configure(state="normal")

    def record_event(self):
        # get name entry
        name = self.record_name_entry.get()
        if name == "":
            tkinter.messagebox.showwarning("Warning", "Please enter a name")
            return
        if name.isdigit():
            tkinter.messagebox.showwarning("Warning", "Please enter a valid name")
            return
        # check if name already exists
        if name in self.choreographies_list:
            # ask if the user wants to overwrite
            answer = tkinter.messagebox.askquestion("Warning", "This name already exists, do you want to overwrite it?")
            if answer == "no":
                return
        self.recorded_chor_name = name
        description =  self.record_description_textbox.get("1.0", "end")
        # delete all /n
        self.recorded_chor_description = description.replace("\n", " ")
        # load the calibration
        self.calibration_offset, self.gyro_offset = self.modules.process_controler_data.load_calibration()
        # check if the calibration is done
        if self.calibration_offset == 0:
            tkinter.messagebox.showwarning("Warning", "Please calibrate the robot first")
            return
        # update the message in the info box
        self.record_info_textbox.configure(state="normal")
        self.record_info_textbox.delete("1.0", "end")
        self.record_info_textbox.insert("1.0", "Recording...")
        # debug("recording")
        # create recording thread
        self.record_threading()        
        # debug("recording thread created")
            
    def record_threading(self):
        # thread for recording
        self.recordthread = Thread(target=self.record, daemon=True)
        self.recordthread.start()
        # start progression thread
        self.record_progressthread = Thread(target=self.update_progress_record, daemon=True)
        self.record_progressthread.start()

    def record(self):
        choreography_steps_unprocessed = []
        choreography_steps_processed = []
        # self.record_on = True
        choreography_steps_unprocessed = self.modules.process_controler_data.record()
        # debug("recording over")
        # self.record_on = False
        # display end of communication
        self.record_info_textbox.insert("end", "\nEnd of communication")
        self.record_info_textbox.configure(state="disabled")
        # process the data
        choreography_steps_processed = self.modules.process_controler_data.process_data_array(choreography_steps_unprocessed, float(self.calibration_offset), float(self.gyro_offset))

        # display choreography
        # debug(choreography_steps_processed)

        # get creation date
        creation_date = (str(datetime.now()))[:-7]
        last_modified = creation_date

        # create the choreography
        self.modules.choreographer.create_choreography(self.recorded_chor_name, creation_date, last_modified, choreography_steps_processed, self.recorded_chor_description)
        debug("choreography created")
        # refreshes the 
        self.refresh()


    def update_progress_record(self):
        time.sleep(3) # delay to start recording
        # while thymio is connected
        # open a top level window
        self.record_progress_window = ToplevelWindow(self)
        self.record_progress_window.geometry("300x100")
        self.record_progress_window.title("Recording")
        self.record_progress_window.after(100,self.record_progress_window.lift) # Workaround for bug where main window takes focus
        # give focus to the window
        self.record_progress_window.focus()
        self.record_progress_window.grab_set()  # Grab the top-level window
        # add progress bar inside
        self.record_progress_bar = customtkinter.CTkProgressBar(self.record_progress_window, orientation="horizontal") # set value between 1 and 0
        self.record_progress_bar.set(0)
        self.record_progress_bar.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.28, anchor="w")
        # add label underneath to say recording
        self.record_progress_label = customtkinter.CTkLabel(self.record_progress_window, text="Recording...", anchor="w")
        self.record_progress_label.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.15)
        time_recorded = 0
        standard_dt = 0.1
        while time_recorded <= RECORDING_DURATION:
            time.sleep(standard_dt)
            time_recorded += standard_dt
            # if window is not destroyed
            if self.record_progress_window.winfo_exists():
                self.record_progress_bar.set(time_recorded/(RECORDING_DURATION-0.1))
            else: 
                return
        # change the bar color to green
        self.record_progress_bar.set(0)
        self.record_progress_bar.configure(progress_color = ("#6a9955","#6a9955"))
        time_recorded = 0
        self.record_progress_label.configure(text="Processing...")
        while time_recorded <= DATA_PROCESSING_DURATION:
            time.sleep(standard_dt)
            time_recorded += standard_dt
            if self.record_progress_window.winfo_exists():
                self.record_progress_bar.set(time_recorded/DATA_PROCESSING_DURATION) 
            else:
                return
        self.record_progress_window.destroy()
        # recorded popup
        tkinter.messagebox.showinfo("Info", "Choreography recorded")

        # clean name and description boxes
        self.record_name_entry.delete(0, "end")
        self.record_description_textbox.delete("1.0", "end")
        
        # time_prog = 0
        # while time_prog < RECORDING_DURATION:
        #     time.sleep(0.1)
        #     time_prog += 0.1
        #     self.record_progress_bar.set(time_prog/RECORDING_DURATION)
        # self.record_progress_bar.set(0)
        
    # def stop_event_record(self):
    #     self.record_on = False
    #     debug("recording button stop")

    # def debug_event(self):
    #     pass
        # if self.debug_on == False:
        #     self.debug_on = True
        #     # load the calibration
        #     self.calibration_offset = self.modules.process_controler_data.load_calibration()
        #     if self.calibration_offset == None:
        #         tkinter.messagebox.showwarning("Warning", "Please calibrate the robot first")
        #         return
        #     else:
        #         # print(f"calibration offset: {self.calibration_offset}")
        #         # block connection slider
        #         self.record_server_switch.configure(state="disabled")
        #     # start the debug thread
        #     self.debug_threading()

    # def debug_threading(self):
    #     # thread for debug
    #     self.debugthread = Thread(target=self.debug, daemon=True)
    #     self.debugthread.start()

    # def debug(self):
    #     counter = 0
    #     x_position = 0
    #     y_position = 0
    #     # start the debug
    #     self.modules.process_controler_data.debug_start()
    #     # display the counter
    #     self.record_info_textbox.insert("end", f"\n Debuging started")

    #     # while counter <= 100:
    #     while self.debug_on:
    #         x_offset, y_offset = self.modules.process_controler_data.debug_step()
    #         if x_offset and y_offset is not None:
    #             self.record_info_textbox.configure(state="normal")
    #             self.record_info_textbox.delete("1.0", "end")
    #             self.record_info_textbox.insert("1.0", "Debugging...\nPress enter to stop")

    #             # display the counter
    #             self.record_info_textbox.insert("end", f"\nCounter : {counter}")
    #             # transform into cm
    #             x_offset = x_offset / self.calibration_offset
    #             y_offset = y_offset / self.calibration_offset 
    #             # print(f"x offset in cm: {x_offset}")
    #             # display in the info box
    #             # self.record_info_textbox.insert("end", f"\nOffset : {x_offset}")

    #             # add to x position
    #             x_position = np.round(x_position + x_offset,2)
    #             y_position = np.round(y_position + y_offset,2)
    #             # print(f"x position: {x_position}")  
    #             # display in the info box
    #             self.record_info_textbox.insert("end", f"\nX Position : {x_position}")
    #             self.record_info_textbox.insert("end", f"\nY Position : {y_position}")
    #             counter += 1
    #             # wait 0.1 second
    #             time.sleep(0.1)
    #             self.record_info_textbox.configure(state="disabled")

    #     # display end of communication
    #     self.record_info_textbox.configure(state="normal")
    #     self.record_info_textbox.delete("1.0", "end")
    #     self.record_info_textbox.insert("1.0", "\nDebugging ended")
    #     self.record_info_textbox.configure(state="disabled")
        

    #     # stop the debug
    #     self.modules.process_controler_data.debug_stop()


        

    # EDIT METHODS --------------------------------------------------------------------------------------------------------
    
    def editor_mode_select_event(self, new_editor_mode: str):
        self.editor_manage_delete_layout()
        self.editor_create_seq_delete_layout()
        self.editor_display_create_rand_chor_delete_layout()
        if new_editor_mode == "Manage":
            self.editor_display_manage_layout()
        elif new_editor_mode == "Create Sequence":
            self.editor_display_create_seq_layout()
        elif new_editor_mode == "Create rand chor":
            self.editor_display_create_rand_chor_layout()
        elif new_editor_mode == "Set emotions":
            self.editor_display_set_emotions_layout()

    def editor_display_set_emotions_layout(self):
        # display sequence list on the left
        self.editor_set_emotions_sequence_list_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_set_emotions_sequence_list_frame.place(relx=0, rely=0.08, relwidth=0.33, relheight=0.90)
        # add title
        self.editor_set_emotions_sequence_list_title_label = customtkinter.CTkLabel(self.editor_set_emotions_sequence_list_frame, text="SEQUENCES", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_set_emotions_sequence_list_title_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.05)
        # add scrollable frame
        self.editor_set_emotions_sequence_list_scrollable_frame = customtkinter.CTkScrollableFrame(self.editor_set_emotions_sequence_list_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_set_emotions_sequence_list_scrollable_frame.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.80)
        # desselect
        self.editor_set_emotions_sequence_radio_var = tkinter.IntVar(value=-1)
        # add sequence buttons
        self.scrollable_frame_set_emotions = []

        for i in range(len(self.sequences_list)):
            # add radio button
            self.scrollable_frame_set_emotions.append(customtkinter.CTkRadioButton(self.editor_set_emotions_sequence_list_scrollable_frame, text=self.sequences_list[i], variable=self.editor_set_emotions_sequence_radio_var, value=i, command=self.editor_set_emotions_sequence_select_event))
            self.scrollable_frame_set_emotions[i].pack(anchor="w")

        # create emotions frame on the left
        self.editor_set_emotions_emotions_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_set_emotions_emotions_frame.place(relx=0.35, rely=0.08, relwidth=0.63, relheight=0.90)
        # add title
        self.editor_set_emotions_emotions_title_label = customtkinter.CTkLabel(self.editor_set_emotions_emotions_frame, text="EMOTIONS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_set_emotions_emotions_title_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.05)
        # add frame do display actuator emotions
        self.editor_set_emotions_emotions_display_frame_act = customtkinter.CTkFrame(self.editor_set_emotions_emotions_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_set_emotions_emotions_display_frame_act.place(relx=0.01, rely=0.1, relwidth=0.32, relheight=0.70)
        # add frame to display light emotions
        self.editor_set_emotions_emotions_display_frame_light = customtkinter.CTkFrame(self.editor_set_emotions_emotions_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_set_emotions_emotions_display_frame_light.place(relx=0.34, rely=0.1, relwidth=0.32, relheight=0.70)
        # add frame to display sound emotions
        self.editor_set_emotions_emotions_display_frame_sound = customtkinter.CTkFrame(self.editor_set_emotions_emotions_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_set_emotions_emotions_display_frame_sound.place(relx=0.67, rely=0.1, relwidth=0.32, relheight=0.70)
        # add variable to select emotions
        self.editor_set_emotions_emotions_radio_var_act = tkinter.IntVar(value=-1)
        # add emotion radiobuttons "fear", "curiosity"
        self.editor_set_emotions_emotions_radiob_act = []
        for i in range(len(list(self.modules.choreographer.emotion_dict.keys()))):
            self.editor_set_emotions_emotions_radiob_act.append(customtkinter.CTkRadioButton(self.editor_set_emotions_emotions_display_frame_act, text=list(self.modules.choreographer.emotion_dict.keys())[i], variable=self.editor_set_emotions_emotions_radio_var_act, value=i, command=self.editor_set_emotions_emotions_select_event_act))
            self.editor_set_emotions_emotions_radiob_act[i].pack(anchor="w")

        # add a button to desselect emotions
        self.editor_set_emotions_emotions_desselect_button_act = customtkinter.CTkButton(self.editor_set_emotions_emotions_display_frame_act, text="Desselect", command=self.editor_set_emotions_emotions_desselect_event_act)
        self.editor_set_emotions_emotions_desselect_button_act.place(relx=0.01, rely=0.80, relwidth=0.98, relheight=0.15)

    def editor_set_emotions_emotions_desselect_event_act(self):
        # desselect emotions
        self.editor_set_emotions_emotions_radio_var_act.set(-1)
        # get the sequence selected
        index = self.editor_set_emotions_sequence_radio_var.get()
        if index != -1:
            sequence_name = self.sequences_list[index]
            # remove all emotions from the sequence
            self.modules.choreographer.sequence_dict[sequence_name].remove_emotions()
            # debug(f"emotions removed from sequence {sequence_name}")
            # debug(self.modules.choreographer.sequence_dict[sequence_name].emotion_list)
            self.modules.choreographer.sequence_dict[sequence_name].save_sequence()
            self.refresh()
            # popup
            tkinter.messagebox.showinfo("Info", "Emotions desselected")
        # display all sequences emotion lists
        # for i in range(len(self.sequences_list)):
        #     debug(f"{self.modules.choreographer.sequence_dict[self.sequences_list[i]]} : {self.modules.choreographer.sequence_dict[self.sequences_list[i]].emotion_list}")
    

    def editor_set_emotions_sequence_select_event(self):
        # check if the sequence has emotions
        # desselect emotions
        self.editor_set_emotions_emotions_radio_var_act.set(-1)
        # get the sequence selected
        index = self.editor_set_emotions_sequence_radio_var.get()
        sequence_name = self.sequences_list[index]
        # get the emotion_list of the sequence
        emotion_list = self.modules.choreographer.sequence_dict[sequence_name].emotion_list
        # select the emotions
        for i in range(len(emotion_list)):
            if emotion_list[i] in list(self.modules.choreographer.emotion_dict.keys()):
                self.editor_set_emotions_emotions_radiob_act[list(self.modules.choreographer.emotion_dict.keys()).index(emotion_list[i])].select()
                self.editor_set_emotions_emotions_select_event_act()

    def editor_set_emotions_emotions_select_event_act(self):
        # get the sequence selected
        index = self.editor_set_emotions_sequence_radio_var.get()
        if index != -1:    
            sequence_name = self.sequences_list[index]
            # add emotion to the sequence
            # get the emotion selected
            emotion_index = self.editor_set_emotions_emotions_radio_var_act.get()
            if emotion_index != -1:
                emotion_name = list(self.modules.choreographer.emotion_dict.keys())[emotion_index]
                # add the emotion to the sequence
                self.modules.choreographer.sequence_dict[sequence_name].add_emotion(emotion_name)
                # debug(f"emotion added to sequence {sequence_name}")
                # debug(self.modules.choreographer.sequence_dict[sequence_name].emotion_list)
                self.modules.choreographer.sequence_dict[sequence_name].save_sequence()
                # debug(f"emotion added to sequence {sequence_name}")
                self.refresh()
                # popup
                tkinter.messagebox.showinfo("Info", f"Emotion {emotion_name} added to sequence {sequence_name}")
            # display all sequences emotion lists
            # for i in range(len(self.sequences_list)):
            #     debug(f"{self.modules.choreographer.sequence_dict[self.sequences_list[i]]} : {self.modules.choreographer.sequence_dict[self.sequences_list[i]].emotion_list}")


    def editor_display_create_rand_chor_layout(self):
        # create rand chor frame
        self.editor_create_rand_chor_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_create_rand_chor_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.90)
        # add settings frame on the left
        self.editor_create_rand_chor_settings_frame = customtkinter.CTkFrame(self.editor_create_rand_chor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_create_rand_chor_settings_frame.place(relx=0.01, rely=0.01, relwidth=0.33, relheight=0.98)
        # add settings widgets min_speed, max_speed, max_time, timestep, samestart
        # add title
        self.editor_create_rand_chor_settings_title_label = customtkinter.CTkLabel(self.editor_create_rand_chor_settings_frame, text="SETTINGS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_create_rand_chor_settings_title_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.05)
        # add min speed entry
        self.editor_create_rand_chor_settings_min_speed_label = customtkinter.CTkLabel(self.editor_create_rand_chor_settings_frame, text="Min speed:", anchor="w")
        self.editor_create_rand_chor_settings_min_speed_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_min_speed_entry = customtkinter.CTkEntry(self.editor_create_rand_chor_settings_frame)
        self.editor_create_rand_chor_settings_min_speed_entry.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_min_speed_entry.insert(0, "0")
        # add max speed entry
        self.editor_create_rand_chor_settings_max_speed_label = customtkinter.CTkLabel(self.editor_create_rand_chor_settings_frame, text="Max speed:", anchor="w")
        self.editor_create_rand_chor_settings_max_speed_label.place(relx=0.01, rely=0.3, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_max_speed_entry = customtkinter.CTkEntry(self.editor_create_rand_chor_settings_frame)
        self.editor_create_rand_chor_settings_max_speed_entry.place(relx=0.01, rely=0.4, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_max_speed_entry.insert(0, "15")
        # add max time entry
        self.editor_create_rand_chor_settings_max_time_label = customtkinter.CTkLabel(self.editor_create_rand_chor_settings_frame, text="Max time [ms]:", anchor="w")
        self.editor_create_rand_chor_settings_max_time_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_max_time_entry = customtkinter.CTkEntry(self.editor_create_rand_chor_settings_frame)
        self.editor_create_rand_chor_settings_max_time_entry.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_max_time_entry.insert(0, "10000")
        # add timestep entry
        self.editor_create_rand_chor_settings_timestep_label = customtkinter.CTkLabel(self.editor_create_rand_chor_settings_frame, text="Timestep [ms]:", anchor="w")
        self.editor_create_rand_chor_settings_timestep_label.place(relx=0.01, rely=0.7, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_timestep_entry = customtkinter.CTkEntry(self.editor_create_rand_chor_settings_frame)
        self.editor_create_rand_chor_settings_timestep_entry.place(relx=0.01, rely=0.8, relwidth=0.98, relheight=0.05)
        self.editor_create_rand_chor_settings_timestep_entry.insert(0, "100")
        # add same start checkbox
        self.editor_create_rand_chor_settings_samestart_checkbox = customtkinter.CTkCheckBox(self.editor_create_rand_chor_settings_frame, text="Same start")
        self.editor_create_rand_chor_settings_samestart_checkbox.place(relx=0.01, rely=0.9, relwidth=0.98, relheight=0.1)
        self.editor_create_rand_chor_settings_samestart_checkbox_hover = CTkToolTip(self.editor_create_rand_chor_settings_samestart_checkbox, message="wether the motors start together or not")
        # add create button
        self.editor_create_rand_chor_settings_create_button = customtkinter.CTkButton(self.editor_create_rand_chor_frame, text="Create", command=self.editor_create_rand_chor_create_event)
        self.editor_create_rand_chor_settings_create_button.place(relx=0.55, rely=0.9, relwidth=0.3, relheight=0.05)
        # create choreography list on top
        self.editor_create_rand_chor_chor_list_frame = customtkinter.CTkFrame(self.editor_create_rand_chor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_create_rand_chor_chor_list_frame.place(relx=0.5, rely=0.01, relwidth=0.4, relheight=0.5)
        # add title
        self.editor_create_rand_chor_chor_list_title_label = customtkinter.CTkLabel(self.editor_create_rand_chor_chor_list_frame, text="CHOREOGRAPHIES", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_create_rand_chor_chor_list_title_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.1)
        # add choreography list
        self.editor_create_rand_chor_chor_list_scrollable_frame = customtkinter.CTkScrollableFrame(self.editor_create_rand_chor_chor_list_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_create_rand_chor_chor_list_scrollable_frame.place(relx=0.01, rely=0.2, relwidth=0.98, relheight=0.7)
        # add radio buttons inside
        self.editor_create_rand_chor_chor_list_radio_var = tkinter.IntVar(value=-1)
        self.scrollable_frame_editor_create_rand_chor_chor_list = []
        for i, name in enumerate(self.choreographies_list):
            self.scrollable_frame_editor_create_rand_chor_chor_list.append(customtkinter.CTkRadioButton(self.editor_create_rand_chor_chor_list_scrollable_frame,corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, text=name, variable=self.editor_create_rand_chor_chor_list_radio_var, value=i))
            self.scrollable_frame_editor_create_rand_chor_chor_list[i].pack(fill="both", expand=True)

        try: self.editor_tooltip.hide()
        except: pass
        # add tooltip
        self.editor_tooltip = CTkToolTip(self.editor_tooltip_label, justify="left", message="🤖 This is the create random choreograph mode.\n"
                                         + "You can create a random choreography and specify\n"
                                         + "its parameters. To generate the choreography\n"
                                         + "please click the 'create' button at the bottom\n"
                                         + "of the page."
                                        )

    def editor_create_rand_chor_create_event(self):
        # get the settings
        min_speed = self.editor_create_rand_chor_settings_min_speed_entry.get()
        max_speed = self.editor_create_rand_chor_settings_max_speed_entry.get()
        max_time = self.editor_create_rand_chor_settings_max_time_entry.get()
        timestep = self.editor_create_rand_chor_settings_timestep_entry.get()
        samestart = self.editor_create_rand_chor_settings_samestart_checkbox.get()
        # check if the settings are valid
        try:
            min_speed = int(min_speed)
            max_speed = int(max_speed)
            max_time = int(max_time)
            timestep = int(timestep)
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter valid settings")
            return
        if min_speed > max_speed:
            tkinter.messagebox.showwarning("Warning", "Please enter valid settings")
            return
        if max_time < timestep:
            tkinter.messagebox.showwarning("Warning", "Please enter valid settings")
            return
        # create the choreography
        self.modules.choreographer.random_choreography_generator(min_speed, max_speed, max_time, timestep, samestart)
        info("Choreography created")
        # refresh the choreography list
        self.refresh()
        self.refresh_editor_rand_chor_list()
        # popup
        tkinter.messagebox.showinfo("Info", "Choreography created")

    def refresh_editor_rand_chor_list(self):
        # remove all buttons
        for button in self.scrollable_frame_editor_create_rand_chor_chor_list:
            button.destroy()
        self.scrollable_frame_editor_create_rand_chor_chor_list = []
        for i, name in enumerate(self.choreographies_list):
            self.scrollable_frame_editor_create_rand_chor_chor_list.append(customtkinter.CTkRadioButton(self.editor_create_rand_chor_chor_list_scrollable_frame,corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, text=name, variable=self.editor_create_rand_chor_chor_list_radio_var, value=i))
            self.scrollable_frame_editor_create_rand_chor_chor_list[i].pack(fill="both", expand=True)

    def editor_display_create_rand_chor_delete_layout(self):
        self.editor_create_rand_chor_frame.destroy() if hasattr(self, "editor_create_rand_chor_frame") else None


    def editor_display_manage_layout(self):
        # add frame underneath
        self.editor_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.90)
        # add choregraphy or sequence option underneath
        self.editor_manage_optionemenu = customtkinter.CTkOptionMenu(self.editor_frame, values=["Choreography", "Sequence"], command=self.editor_manage_select_event)
        # self.editor_manage_optionemenu.set("Choreography")
        self.editor_manage_optionemenu.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.05)
        self.editor_manage_radiobutton_frame = customtkinter.CTkScrollableFrame(self.editor_frame)
        self.editor_manage_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.75)
        self.editor_manage_radio_var = tkinter.IntVar(value=0)
        self.scrollable_frame_editor_manage = []

        # add title on the right
        self.editor_manage_title_label = customtkinter.CTkLabel(self.editor_frame, text="MANAGE MODE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_manage_title_label.place(relx=0.38, rely=0.02, relwidth=0.25, relheight=0.05)

        # add labels on the right of title
        # add frame
        self.editor_manage_info_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_manage_info_frame.place(relx=0.66, rely=0, relwidth=0.25, relheight=0.08)
        # add label inside
        self.editor_manage_info_label_rs = customtkinter.CTkLabel(self.editor_manage_info_frame, text="right motor speed", anchor="w", font=customtkinter.CTkFont(size=12))
        self.editor_manage_info_label_rs.place(relx=0.05, rely=0.05, relwidth=0.98, relheight=0.35)
        self.editor_manage_info_label_ls = customtkinter.CTkLabel(self.editor_manage_info_frame, text="left motor speed", anchor="w", font=customtkinter.CTkFont(size=12))
        self.editor_manage_info_label_ls.place(relx=0.05, rely=0.55, relwidth=0.98, relheight=0.35)
        self.editor_manage_info_label_rscol = customtkinter.CTkLabel(self.editor_manage_info_frame, text="■", anchor="w", font=customtkinter.CTkFont(size=12), text_color="#d26c13")
        self.editor_manage_info_label_rscol.place(relx=0.8, rely=0.05, relwidth=0.1, relheight=0.35)
        self.editor_manage_info_label_lscol = customtkinter.CTkLabel(self.editor_manage_info_frame, text="■", anchor="w", font=customtkinter.CTkFont(size=12), text_color="#22628f")
        self.editor_manage_info_label_lscol.place(relx=0.8, rely=0.55, relwidth=0.1, relheight=0.35)


        # add buttons frame underneath
        self.editor_manage_buttons_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_buttons_frame.place(relx=0.4, rely=0.08, relwidth=0.55, relheight=0.1)
        # add delete button and trim button inside
        self.editor_manage_delete_button = customtkinter.CTkButton(self.editor_manage_buttons_frame, text="🗑", command=self.editor_manage_delete_event)
        self.editor_manage_delete_button.place(relx=0.01, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        self.editor_manage_delete_button_hover = CTkToolTip(self.editor_manage_delete_button, message="Delete")
        self.editor_manage_trim_button = customtkinter.CTkButton(self.editor_manage_buttons_frame, text="✂", command=self.editor_manage_trim_event)
        self.editor_manage_trim_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        self.editor_manage_trim_button_hover = CTkToolTip(self.editor_manage_trim_button, message="Trim")
        # add save as new choreography checkbox
        self.editor_manage_save_checkbox = customtkinter.CTkCheckBox(self.editor_manage_buttons_frame, text="Save as new choreography")
        self.editor_manage_save_checkbox.place(relx=0.4, rely=0.5, relwidth=0.5, relheight=0.7, anchor="w")
        # add second button frame underneath
        self.editor_manage_buttons_frame_2 = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_buttons_frame_2.place(relx=0.4, rely=0.18, relwidth=0.55, relheight=0.07)
        # add a rename button underneath
        self.editor_manage_rename_button = customtkinter.CTkButton(self.editor_manage_buttons_frame_2, text="✎", command=self.editor_manage_rename_event)
        self.editor_manage_rename_button.place(relx=0.01, rely=0.5, relwidth=0.15, relheight=1, anchor="w")
        self.editor_manage_rename_button_hover = CTkToolTip(self.editor_manage_rename_button, message="Rename")
        # add a copy button on the right
        self.copy_image = Image.open(self.application_path + "\\GUI_assets/copy.png")
        self.copy_image = customtkinter.CTkImage(self.copy_image,  size=(18,18))
        self.editor_manage_copy_button = customtkinter.CTkButton(self.editor_manage_buttons_frame_2, text="", image=self.copy_image, command=self.editor_manage_copy_event)
        self.editor_manage_copy_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=1, anchor="w")
        self.editor_manage_copy_button_hover = CTkToolTip(self.editor_manage_copy_button, message="Copy")

        # add graph display underneath
        # self.editor_manage_graph_frame = customtkinter.CTkFrame(self.editor_frame)
        self.editor_manage_graph_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_graph_frame.place(relx=0.4, rely=0.3, relwidth=0.55, relheight=0.5)
        # add canvas inside
        self.editor_manage_graph_canvas = tkinter.Canvas(self.editor_manage_graph_frame, width=500, height=250, background=DARK_COLOR)
        self.editor_manage_graph_canvas.pack()
        # get image
        img = (Image.open(self.application_path + "\\GUI_assets\\j_dark_graph.png"))
        resized_image = img.resize((500,250))
        self.editor_manage_graph_image= ImageTk.PhotoImage(resized_image)
        self.editor_manage_graph_image_in = self.editor_manage_graph_canvas.create_image(0, 0, image=self.editor_manage_graph_image, anchor="nw")

        # add trim sliders frame underneath
        self.editor_manage_trim_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_trim_frame.place(relx=0.4, rely=0.77, relwidth=0.55, relheight=0.20)

        # add tooltip frame
        self.editor_tooltip_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_tooltip_frame.place(relx=0.4, rely=0.01, relwidth=0.55, relheight=0.05)
        # add tooltip label
        self.editor_tooltip_label = customtkinter.CTkLabel(self.editor_tooltip_frame, text="❓", anchor="center")
        self.editor_tooltip_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        try: self.editor_tooltip.hide()
        except: pass
        # add tooltip
        self.editor_tooltip = CTkToolTip(self.editor_tooltip_label, justify="left", message="🤖 This is the manage mode, here you can manage\n"
                                        + " choreographies and sequences. you can do the"
                                        + " following:\n"
                                        + " 🗑\t - Delete a choreography/sequence\n"
                                        + " ✏️\t - Rename a choreography/sequence\n"
                                        + " ✂️\t - Trim a choreography\n"
                                        + " 🗒️\t - Copy a choreography/sequence\n"
                                        )

        # select optionemenu
        self.editor_manage_select_event("Choreography")
        
    def editor_manage_select_event(self, new_editor_manage_mode: str):
        # get the new editor manage mode
        if new_editor_manage_mode == "Choreography":
            self.editor_manage_refresh_chor_list()
        elif new_editor_manage_mode == "Sequence":
            self.editor_manage_refresh_seq_list()
            
    def editor_manage_refresh_chor_list(self):
        # remove all buttons
        for button in self.scrollable_frame_editor_manage:
            button.destroy()
        self.scrollable_frame_editor_manage = []
        for i in range(len(self.choreographies_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_manage_radiobutton_frame, variable=self.editor_manage_radio_var, value=i, text=self.choreographies_list[i], command=self.refresh_editor_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_editor_manage.append(newbutton)
        self.editor_manage_radio_var.set(-1)
        # graph all the choreographies
        for choreography_name in self.choreographies_list:
            self.modules.choreographer.choreography_dict[choreography_name].graph_speeds()

    def editor_manage_refresh_seq_list(self):
        # remove all buttons
        for button in self.scrollable_frame_editor_manage:
            button.destroy()
        self.scrollable_frame_editor_manage = []
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_manage_radiobutton_frame, variable=self.editor_manage_radio_var, value=i, text=self.sequences_list[i])
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_editor_manage.append(newbutton)
        self.editor_manage_radio_var.set(-1)

    def editor_manage_delete_event(self):
        # get if choreography or sequence
        index = self.editor_manage_radio_var.get()
        mode = self.editor_manage_optionemenu.get()
        name = self.choreographies_list[index] if mode == "Choreography" else self.sequences_list[index]
        # print(f"delete {mode} {index}")
        if index < 0:
            tkinter.messagebox.showwarning("Warning", f"Please select something to delete")
        # pop up window to ask if sure
        elif tkinter.messagebox.askyesno("Warning", f"Are you sure you want to delete the {mode}: {name}?"):
            if mode == "Choreography":
                self.modules.choreographer.delete_choreography(self.choreographies_list[index])
                self.remove_choreography(index)
                self.editor_manage_refresh_chor_list()
                self.editor_delete_image()
            elif mode == "Sequence":
                self.modules.choreographer.delete_sequence(self.sequences_list[index])
                self.remove_sequence(index)
                self.editor_manage_refresh_seq_list()
            self.editor_manage_deselect_button()
            self.refresh()
            # popup
            tkinter.messagebox.showinfo("Info", f"{mode} deleted")

    def editor_manage_deselect_button(self):
        # deselect the radiobutton
        self.editor_manage_radio_var.set(-1)

    def editor_manage_rename_event(self):
        # get if choreography or sequence
        option = self.editor_manage_optionemenu.get()
        # check if something is selected
        index = self.editor_manage_radio_var.get()
        if index < 0:
            tkinter.messagebox.showwarning("Warning", "Please select something to rename")
            return
        if option == "Sequence":
            # ask for a new sequence name
            while True:
                new_name = tkinter.simpledialog.askstring("Rename sequence", "Please enter a name for the new sequence")
                # check if name is valid
                if new_name == None:
                    return
                elif new_name == "":
                    tkinter.messagebox.showwarning("Warning", "Please enter a name")
                elif new_name.isdigit():
                    tkinter.messagebox.showwarning("Warning", "Please enter a valid name")
                elif new_name in self.sequences_list:
                    tkinter.messagebox.showwarning("Warning", "This name already exists")
                else:
                    break
            # get the sequence name
            sequence_name = self.sequences_list[index]
            # rename the sequence
            self.modules.choreographer.sequence_dict[sequence_name].rename(new_name)
            # also change the name in the sequence list
            self.sequences_list[index] = new_name
            # load again the sequence dict
            self.modules.choreographer.load_sequence_dict()
            # refresh the sequence list
            self.editor_manage_refresh_seq_list()
            # popup
            tkinter.messagebox.showinfo("Info", "Sequence renamed")
        elif option == "Choreography":
            # ask for a new choreography name
            while True:
                new_name = tkinter.simpledialog.askstring("Rename choreography", "Please enter a name for the new choreography")
                # check if name is valid
                if new_name == None:
                    return
                elif new_name == "":
                    tkinter.messagebox.showwarning("Warning", "Please enter a name")
                elif new_name.isdigit():
                    tkinter.messagebox.showwarning("Warning", "Please enter a valid name")
                elif new_name in self.choreographies_list:
                    tkinter.messagebox.showwarning("Warning", "This name already exists")
                else:
                    break
            # get the choreography name
            index = self.editor_manage_radio_var.get()
            choreography_name = self.choreographies_list[index]
            # rename the choreography
            self.modules.choreographer.choreography_dict[choreography_name].rename(new_name)
            # also change the name in the choreography list
            self.choreographies_list[index] = new_name
            # load again the choreography dict
            self.modules.choreographer.load_choreography_dict()
            # refresh the choreography list
            self.editor_manage_refresh_chor_list()
            # popup
            tkinter.messagebox.showinfo("Info", "Choreography renamed")
        self.refresh()

    def editor_manage_copy_event(self):
        # get if choreography or sequence
        option = self.editor_manage_optionemenu.get()
        # get what is selected
        index = self.editor_manage_radio_var.get()
        if index < 0:
            tkinter.messagebox.showwarning("Warning", "Please select something to copy")
            return
        if option == "Sequence":
            # get the sequence name
            sequence_name = self.sequences_list[index]
            new_name = sequence_name + "_copy"
            while True:
                # check if name is valid
                # debug(new_name)
                if new_name not in self.sequences_list:
                    break
                # add _copy to the name
                new_name = new_name + "_copy"
            self.modules.choreographer.copy_sequence(sequence_name, new_name)
            # refresh the sequence list
            self.refresh()
            self.editor_manage_refresh_seq_list()
            # popup
            tkinter.messagebox.showinfo("Info", "Sequence copied")
        elif option == "Choreography":
            # get the choreography name
            choreography_name = self.choreographies_list[index]
            while True:
                # add _copy to the name
                new_name = choreography_name + "_copy"
                # check if name is valid
                if new_name not in self.choreographies_list:
                    break
            self.modules.choreographer.copy_choreography(choreography_name, new_name)

            # refresh the choreography list
            self.refresh()
            self.editor_manage_refresh_chor_list()
            # popup
            tkinter.messagebox.showinfo("Info", "Choreography copied")


    def editor_manage_trim_event(self):
        # check the optionemenu
        mode = self.editor_manage_optionemenu.get()
        if mode == "Sequence":
            tkinter.messagebox.showwarning("Warning", "You can't trim a sequence")
            return
        # check if something is selected
        index = self.editor_manage_radio_var.get()
        if index < 0:
            tkinter.messagebox.showwarning("Warning", "Please select something to trim")
            return
        # check if save as new choreography is ticked
        save_as_new_choreography = self.editor_manage_save_checkbox.get()
        # get trim start
        trim_start = self.editor_manage_trim_start_slider_var.get()
        # get trim end
        trim_end = self.editor_manage_trim_end_slider_var.get()
        # get the choreography name
        name = self.choreographies_list[index]
        # check trim validity
        if trim_start >= trim_end:
            tkinter.messagebox.showwarning("Warning", "Trim start must be smaller than trim end")
            return
        # pop up window to ask if sure
        elif tkinter.messagebox.askyesno("Warning", f"Are you sure you want to trim the choreography: {name}?"):    
            if save_as_new_choreography == True:
                while True:
                    # ask for a name
                    new_name = tkinter.simpledialog.askstring("Save as new choreography", "Please enter a name for the new choreography")
                    # check if name is valid
                    if new_name == None:
                        return
                    elif new_name == "":
                        tkinter.messagebox.showwarning("Warning", "Please enter a name")
                    elif new_name.isdigit():
                        tkinter.messagebox.showwarning("Warning", "Please enter a valid name")
                    elif new_name in self.choreographies_list:
                        tkinter.messagebox.showwarning("Warning", "This name already exists")
                    else:
                        break
                # create choreography
                self.modules.choreographer.copy_choreography(name, new_name)
                # self.save_choreography(new_name)
                name = new_name
                self.refresh()
            # trim the choreography
            self.modules.choreographer.choreography_dict[name].trim(trim_start, trim_end)
            self.save_choreography(name) 
            # refresh the info
            # self.editor_refresh_image(name)
            self.editor_manage_refresh_chor_list()
            self.refresh()
            # select the new choreography
            self.editor_manage_radio_var.set(self.choreographies_list.index(name))
            self.refresh_editor_info_chor()
            # show the right picture
            self.editor_refresh_image(name)
            # popup
            tkinter.messagebox.showinfo("Info", "Choreography trimmed")

    def refresh_editor_info_chor(self):
        # get the choreography name
        index = self.editor_manage_radio_var.get()
        # get the choreography name
        name = self.choreographies_list[index] 
        self.editor_refresh_image(name)

        # get last time of the choreography
        last_time = self.modules.choreographer.choreography_dict[name].get_last_time()

        # delete bar objects if any
        try:
            self.editor_manage_graph_canvas.delete(self.editor_manage_graph_canvas_left_bar)
            self.editor_manage_graph_canvas.delete(self.editor_manage_graph_canvas_right_bar)
        except:
            pass
        # add rectangle bar 
        self.editor_manage_graph_canvas_left_bar = self.editor_manage_graph_canvas.create_rectangle(LEFTBAR_X0, LEFTBAR_Y0, LEFTBAR_X1, LEFTBAR_Y1, fill=BARSTART_COLOR, outline=BARSTART_COLOR)
        self.editor_manage_graph_canvas_right_bar = self.editor_manage_graph_canvas.create_rectangle(RIGHTBAR_X0, RIGHTBAR_Y0, RIGHTBAR_X1, RIGHTBAR_Y1, fill=BAREND_COLOR, outline=BAREND_COLOR)

        # add two sliders in the slider box for start and end of trim
        self.editor_manage_trim_start_label = customtkinter.CTkLabel(self.editor_manage_trim_frame, text="Start:", anchor="w")
        self.editor_manage_trim_start_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.2)
        self.editor_manage_trim_start_slider_var = tkinter.IntVar(value=0)
        self.editor_manage_trim_start_slider = customtkinter.CTkSlider(self.editor_manage_trim_frame, orientation="horizontal", to=last_time, variable=self.editor_manage_trim_start_slider_var, hover=False, button_color=BARSTART_COLOR, command=self.editor_manage_trim_start_event)
        self.editor_manage_trim_start_slider.place(relx=0.55, rely=0.4, relwidth=0.83, relheight=0.2, anchor="center")
        self.editor_manage_trim_end_label = customtkinter.CTkLabel(self.editor_manage_trim_frame, text="End:", anchor="w")
        self.editor_manage_trim_end_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.2)
        self.editor_manage_trim_end_slider_var = tkinter.IntVar(value=last_time)
        self.editor_manage_trim_end_slider = customtkinter.CTkSlider(self.editor_manage_trim_frame, orientation="horizontal", to=last_time, variable=self.editor_manage_trim_end_slider_var, hover=False, progress_color="#4a4d50", fg_color="#aab0b5", button_color=BAREND_COLOR, command=self.editor_manage_trim_end_event)
        self.editor_manage_trim_end_slider.place(relx=0.55, rely=0.8, relwidth=0.83, relheight=0.2, anchor="center")

    def editor_manage_trim_start_event(self, value):
        # round value to 2 decimals
        # value = round(float(value), 2)
        value = int(value)
        value_in_percentage = value/self.modules.choreographer.choreography_dict[self.choreographies_list[self.editor_manage_radio_var.get()]].get_last_time()
        x1,_,_,_= self.editor_manage_graph_canvas.coords(self.editor_manage_graph_canvas_left_bar)
        # create value label
        self.editor_manage_trim_start_label.configure(text=f"Start:\t\t\t\t\t         {np.round(value/1000,1)}")
        # move the bar
        self.editor_manage_graph_canvas.move(self.editor_manage_graph_canvas_left_bar, value_in_percentage*LENGTH_IN_PIX-x1+OFFSET_STARTGRAPH,0)
        # debug(f"x1 = {x1}, value in pix = {value/LENGTH_IN_PIX}")

    def editor_manage_trim_end_event(self, value):
        # round value to 2 decimals
        # value = round(float(value), 2)
        value = int(value)
        value_in_percentage = value/self.modules.choreographer.choreography_dict[self.choreographies_list[self.editor_manage_radio_var.get()]].get_last_time()
        _,_,x1,_= self.editor_manage_graph_canvas.coords(self.editor_manage_graph_canvas_right_bar)
        # create value label
        self.editor_manage_trim_end_label.configure(text=f"End:\t\t\t\t\t         {np.round(value/1000,1)}")
        # move the bar
        self.editor_manage_graph_canvas.move(self.editor_manage_graph_canvas_right_bar, value_in_percentage*LENGTH_IN_PIX-x1+OFFSET_STARTGRAPH,0)

    def editor_delete_image(self):
        self.editor_manage_graph_canvas.itemconfig(self.editor_manage_graph_image_in, image=self.editor_manage_graph_image)

    def editor_refresh_image(self, name):
        self.modules.choreographer.choreography_dict[name].graph_speeds()
        light_im = Image.open(f"{self.application_path}/GUI_assets/temp_fig/{name}_light_graph.png") # open the image
        dark_im = Image.open(f"{self.application_path}/GUI_assets/temp_fig/{name}_dark_graph.png") # open the image
        light_im_resized = light_im.resize((500,250))
        dark_im_resized = dark_im.resize((500,250))
        self.editor_manage_graph_image_light = ImageTk.PhotoImage(light_im_resized)
        self.editor_manage_graph_image_dark = ImageTk.PhotoImage(dark_im_resized)
        if self.appearance_mode_optionemenu.get() == "Light":
            self.editor_manage_graph_canvas.itemconfig(self.editor_manage_graph_image_in, image=self.editor_manage_graph_image_light)
        else:
            self.editor_manage_graph_canvas.itemconfig(self.editor_manage_graph_image_in, image=self.editor_manage_graph_image_dark)
        # self.editor_manage_graph_image_light = Image.open(f"app/GUI_assets/temp_fig/{name}_light_graph.png")
        # self.editor_manage_graph_image_dark = Image.open(f"app/GUI_assets/temp_fig/{name}_dark_graph.png")
        # self.editor_manage_graph_image = customtkinter.CTkImage(light_image=self.editor_manage_graph_image_light, dark_image=self.editor_manage_graph_image_dark, size=(400,200))
        # self.editor_manage_graph_image_label.configure(image=self.editor_manage_graph_image)



    def editor_manage_delete_layout(self):
        # removes all the manage frames if any
        if hasattr(self, "editor_frame"):
            self.editor_frame.destroy()

    # sequence creator
    def editor_display_create_seq_layout(self):
        # add frame underneath
        self.editor_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.90)
        # add "choreography list" frame
        self.editor_create_seq_chor_label = customtkinter.CTkLabel(self.editor_frame, text="Choreographies ", anchor="w")
        self.editor_create_seq_chor_label.place(relx=0.01, rely=0.07)
        self.editor_create_seq_chor_radiobutton_frame = customtkinter.CTkScrollableFrame(self.editor_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_create_seq_chor_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.35)
        self.editor_create_seq_chor_radio_var = tkinter.IntVar(value=-1)
        self.editor_create_seq_scrollable_frame_chor = []
        for i in range(len(self.choreographies_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_create_seq_chor_radiobutton_frame, corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, variable=self.editor_create_seq_chor_radio_var, value=i, text=f"{i+1} - {self.choreographies_list[i]}", command=self.editor_create_seq_refresh_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.editor_create_seq_scrollable_frame_chor.append(newbutton)
        # add "sequence list" frame
        self.editor_create_seq_seq_label = customtkinter.CTkLabel(self.editor_frame, text="Sequences ", anchor="w")
        self.editor_create_seq_seq_label.place(relx=0.01, rely=0.55)
        self.editor_create_seq_seq_radiobutton_frame = customtkinter.CTkScrollableFrame(self.editor_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_create_seq_seq_radiobutton_frame.place(relx=0.01, rely=0.61, relwidth=0.33, relheight=0.35)
        self.editor_create_seq_seq_radio_var = tkinter.IntVar(value=-1)
        self.editor_create_seq_scrollable_frame_seq = []
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_create_seq_seq_radiobutton_frame, corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, variable=self.editor_create_seq_seq_radio_var, value=i, text=self.sequences_list[i], command=self.editor_create_seq_refresh_info_seq)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.editor_create_seq_scrollable_frame_seq.append(newbutton)

        # add title on the right
        self.editor_create_seq_title_label = customtkinter.CTkLabel(self.editor_frame, text="CREATE SEQUENCE MODE", font=customtkinter.CTkFont(size=20, weight="bold"), anchor="center")
        self.editor_create_seq_title_label.place(relx=0.38, rely=0.02, relwidth=0.6, relheight=0.05)

        # add sequence settings frame underneath
        self.editor_create_seq_settings_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_create_seq_settings_frame.place(relx=0.4, rely=0.13, relwidth=0.55, relheight=0.5)
        # add name label inside
        self.editor_create_seq_name_label = customtkinter.CTkLabel(self.editor_create_seq_settings_frame, text="Name:", anchor="w")
        self.editor_create_seq_name_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.2)
        # add name entry inside
        self.editor_create_seq_name_entry = customtkinter.CTkEntry(self.editor_create_seq_settings_frame)
        self.editor_create_seq_name_entry.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
        # add description label inside
        self.editor_create_seq_description_label = customtkinter.CTkLabel(self.editor_create_seq_settings_frame, text="Description:", anchor="w")
        self.editor_create_seq_description_label.place(relx=0.01, rely=0.4, relwidth=0.98, relheight=0.2)
        # add description textbox inside
        self.editor_create_seq_description_textbox = customtkinter.CTkTextbox(self.editor_create_seq_settings_frame)
        self.editor_create_seq_description_textbox.place(relx=0.05, rely=0.6, relwidth=0.9, relheight=0.3)

        # add sequence order frame underneath
        self.editor_create_seq_order_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(LIGHT_COLOR, DARK_COLOR))
        self.editor_create_seq_order_frame.place(relx=0.4, rely=0.65, relwidth=0.55, relheight=0.2)
        # add sequence order button inside
        self.editor_create_seq_order_button = customtkinter.CTkButton(self.editor_create_seq_order_frame, text="Create Sequence", command=self.editor_create_seq_order_event)
        self.editor_create_seq_order_button.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.9, anchor="w")

        # add tooltip frame
        self.editor_tooltip_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_tooltip_frame.place(relx=0.4, rely=0.01, relwidth=0.55, relheight=0.05)
        # add tooltip label
        self.editor_tooltip_label = customtkinter.CTkLabel(self.editor_tooltip_frame, text="❓", anchor="center")
        self.editor_tooltip_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        try: self.editor_tooltip.hide()
        except: pass
        # add tooltip
        self.editor_tooltip = CTkToolTip(self.editor_tooltip_label, justify="left", message="🤖 This is the create sequence mode, here you can\n"
                                        + " create sequences. You can see the choreographies you\n"
                                        + " can add to the sequence on the left. You can also add\n"
                                        + " a description and a name to the sequence. To create\n"
                                        + " the sequence, you need to click on the button 'create\n"
                                        + " sequence' at the bottom of the screen. The sequence\n"
                                        + " order is the order of the choreographies by number.\n"
                                        + " For example, if you want to create a sequence with\n"
                                        + " the choreographies 1, 2 and 3, you need to enter\n"
                                        + " 1-2-3 in the input dialog.\n"
                                        )

        # self.refresh()

    def editor_create_seq_refresh_info_chor(self):
        # delete buttons
        for button in self.editor_create_seq_scrollable_frame_chor:
            button.destroy()
        self.editor_create_seq_scrollable_frame_chor = []
        # refresh list
        for i in range(len(self.choreographies_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_create_seq_chor_radiobutton_frame, corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, variable=self.editor_create_seq_chor_radio_var, value=i, text=f"{i+1} - {self.choreographies_list[i]}", command=self.editor_create_seq_refresh_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.editor_create_seq_scrollable_frame_chor.append(newbutton)
    
    def editor_create_seq_refresh_info_seq(self):
        # delete buttons
        for button in self.editor_create_seq_scrollable_frame_seq:
            button.destroy()
        self.editor_create_seq_scrollable_frame_seq = []
        # refresh list
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.editor_create_seq_seq_radiobutton_frame, corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, variable=self.editor_create_seq_seq_radio_var, value=i, text=self.sequences_list[i], command=self.editor_create_seq_refresh_info_seq)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.editor_create_seq_scrollable_frame_seq.append(newbutton)

    def editor_create_seq_refresh_lists(self):
        self.editor_create_seq_refresh_info_chor()
        self.editor_create_seq_refresh_info_seq()

    def editor_create_seq_order_event(self):
        # create input dialog
        # get the name
        name = self.editor_create_seq_name_entry.get()
        if name == "":
            tkinter.messagebox.showwarning("Warning", "Please enter a name")
            return
        # check if name is taken
        if name in self.sequences_list:
            tkinter.messagebox.showwarning("Warning", "This name is already taken")
            return
        # create input dialog
        self.editor_create_dialog = customtkinter.CTkInputDialog(text=f"Sequence order for: {name}", title="Create Sequence")
        sequence_string = self.editor_create_dialog.get_input()
        # get description
        description = self.editor_create_seq_description_textbox.get("1.0", "end")
        # delete every \n in description
        description = description.replace("\n", "")
        # get creation date
        creation_date = (str(datetime.now()))[:-7]
        # creates the sequence
        try:
            sequence_order = sequence_string.split("-")
            sequence_order = [int(i) for i in sequence_order]
            for element in sequence_order:
                if element < 1 or element > len(self.choreographies_list):
                    raise ValueError
                if element > len(self.choreographies_list):
                    raise ValueError
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter a valid sequence order")
            return
        self.modules.choreographer.create_sequence(name, creation_date, description, sequence_order)
        # refresh propositions
        self.refresh()
        self.editor_create_seq_refresh_lists()
        # popup
        tkinter.messagebox.showinfo("Info", "Sequence created")
        # clean description and name
        self.editor_create_seq_description_textbox.delete("1.0", "end")
        self.editor_create_seq_name_entry.delete(0, "end")

    def editor_create_seq_delete_layout(self):
        # removes all the create seq frames if any
        if hasattr(self, "editor_frame"):
            self.editor_frame.destroy()

    def editor_manage_mode_tooltip_update(self):
        # update tooltip
        self.editor_hide_all_tooltips()
        self.editor_manage_mode_tooltip_manage_mode = CTkToolTip(self.editor_manage_mode_label, justify="left", message="🤖 This is the manage mode, here you can manage\n"
                                        + " choreographies and sequences. You can select\n"
                                        + " what to manage on the left. You can also delete\n"
                                        + " and trim choreographies and sequences.\n")
        
    def editor_create_seq_mode_tooltip_update(self):
        # update tooltip
        self.editor_hide_all_tooltips()
        self.editor_create_seq_mode_tooltip_create_seq_mode = CTkToolTip(self.editor_create_seq_mode_label, justify="left", message="🤖 This is the create sequence mode, here you can\n"
                                        + " create sequences. You can see the choreographies you\n"
                                        + " can add to the sequence on the left.\n")
        
    def editor_hide_all_tooltips(self):
        self.editor_manage_mode_tooltip.hide()
        self.editor_manage_mode_tooltip_manage_mode()
        self.editor_create_seq_mode_tooltip.hide()
