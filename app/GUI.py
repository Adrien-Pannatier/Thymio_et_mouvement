import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image
from threading import Thread
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

DARK_COLOR = "#242424"
LIGHT_COLOR = "#ebebeb"

DEFAULT_LIGHT = "#dbdbdb"
DEFAULT_DARK = "#2b2b2b"

class App(customtkinter.CTk):
    def __init__(self, modules):
        super().__init__()
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
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="GUI Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Tool", "Discovery"],
                                                                       command=self.mode_select_event)
        self.mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.add("Info")
        self.tabview.add("Edit")
        self.tabview.add("Record")
        self.tabview.add("Play")
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Edit").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Play").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Edit").grid_columnconfigure(0, weight=1)

        # INFO TAB CREATION =================================================================================================
        # add "refresh" button
        self.refresh_button = customtkinter.CTkButton(self.tabview.tab("Info"), text="⟳", command=self.refresh)
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
        self.chor_info_frame.place(relx=0.4, rely=0.13, relwidth=0.50, relheight=0.35)
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
        self.seq_info_frame.place(relx=0.4, rely=0.61, relwidth=0.50, relheight=0.35)
        # add text widget
        self.seq_info_text = customtkinter.CTkTextbox(self.seq_info_frame, wrap='none')
        self.seq_info_text.place(relx=0.01, rely=0, relwidth=0.98, relheight=1)
        self.seq_info_text.insert("1.0", "Sequence info")
        # make the text read only
        self.seq_info_text.configure(state="disabled")

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
        # add connect slider
        self.play_connect_variable = tkinter.BooleanVar(value=False)
        self.play_connect_slider = customtkinter.CTkSwitch(self.play_thymio_status_frame, text="", variable=self.play_connect_variable, command=self.play_connect_event)
        self.play_connect_slider.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")

        # update bar variable
        self.update_bar_update = False

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
        self.record_server_status_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")
        # add server slider
        self.record_server_slider = customtkinter.CTkSwitch(self.record_server_status_frame, text="", command=self.record_server_event)
        self.record_server_slider.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")
        
        # EDIT TAB CREATION ================================================================================================
        # add option menu mode between Manager and Create sequence
        self.editor_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("Edit"), values=["Manage", "Create Sequence"], command=self.editor_mode_select_event)
        self.editor_optionemenu.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.05)

        # SET DEFAULT VALUES ===============================================================================================
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.mode_optionemenu.set("Tool")
        self.play_optionemenu.set("Choreography")
        self.editor_optionemenu.set("Manage")
        # lock window size
        self.resizable(False, False)
        # put info buttons to zero
        self.chor_radio_var.set(-1)
        self.seq_radio_var.set(-1)
        # deselect all optionmenu
        





    def mode_select_event(self, new_mode: str):
        pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)









    # INFO METHODS --------------------------------------------------------------------------------------------------------
    def refresh(self):
        # asl choreographer for loading
        self.modules.choreographer.update_database()
        # refresh choreography list
        self.choreographies_list = list(self.modules.choreographer.choreography_dict.keys())
        self.refresh_choreographies_list()
        # refresh sequence list
        self.sequences_list = list(self.modules.choreographer.sequence_dict.keys())
        self.refresh_sequences_list()

    def refresh_info_chor(self):
        index = self.chor_radio_var.get()
        name = self.choreographies_list[index]
        choreography_name, description, speed_factor, path = self.modules.choreographer.choreography_dict[name].get_info()
        self.chor_info_text.configure(state="normal")
        self.chor_info_text.delete("1.0", "end")
        self.chor_info_text.insert("1.0", f"Name:\t\t{choreography_name}\nDescription:\t\t{description}\nSpeed factor:\t\t{str(speed_factor)}")
        self.chor_info_text.configure(state="disabled")

    def refresh_info_seq(self):
        index = self.seq_radio_var.get()
        name = self.sequences_list[index]
        sequence_name, description, path, sequence_order = self.modules.choreographer.sequence_dict[name].get_info()
        self.seq_info_text.configure(state="normal")
        self.seq_info_text.delete("1.0", "end")
        self.seq_info_text.insert("1.0", f"Name:\t\t{sequence_name}\nDescription:\t\t{description}\nSequence order:\t\t{sequence_order}")
        self.seq_info_text.configure(state="disabled")
    
    def refresh_choreographies_list(self):
        # remove all buttons
        for button in self.scrollable_frame_chor:
            button.destroy()
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
        # get the selection
        index = self.play_radio_var.get()
        # get the connection status
        connection_status = self.play_connect_slider.get()
        if connection_status == True:
            if play_mode == "Choreography":
                name = self.choreographies_list[index]
                choreography_name, _, speed_factor, _ = self.modules.choreographer.choreography_dict[name].get_info()
                self.play_chor_name_label.configure(text=f"Name:\t\t\t\t{choreography_name}")
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
                name = self.sequences_list[index]
                sequence_name, _, _, _ = self.modules.choreographer.sequence_dict[name].get_info()
                self.play_chor_name_label.configure(text=f"Name:\t\t\t\t{sequence_name}")
                # lock the speed factor entry
                self.play_speed_factor_entry.delete(0, "end")
                self.play_speed_factor_entry.configure(state="disabled")
                # change the color of the entry
                self.play_speed_factor_entry.configure(fg_color = (LIGHT_COLOR,DARK_COLOR))
        
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
        connection_status = self.play_connect_slider.get()
        if connection_status == True:
            # try to connect the thymio
            if not self.modules.motion_control.init_thymio_connection():
                # if the connection failed, set the slider back to false
                self.play_connect_variable.set(False)
                print("no connection")
                connection_status = False
                pass
            else:            
                # try to connect to the thymio
                self.play_thymio_status_label.configure(text="Thymio status: Connected")
                self.display_play_layout()
                self.refresh_play_info()
        if connection_status == False:
            # disconnect from the thymio
            self.modules.motion_control.disconnect_thymio()
            self.play_thymio_status_label.configure(text="Thymio status: Not connected")
            self.remove_play_layout()

    def display_play_layout(self):
        # add settings frame underneath
        self.play_settings_frame = customtkinter.CTkFrame(self.tabview.tab("Play"))
        self.play_settings_frame.place(relx=0.4, rely=0.07, relwidth=0.55, relheight=0.35)
        # add settings widgets
        # add choreography name label
        self.play_chor_name_label = customtkinter.CTkLabel(self.play_settings_frame, text="Name:", anchor="w")
        self.play_chor_name_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.15)
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
        self.play_progress_bar.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.48, anchor="w")

    def remove_play_layout(self):
        self.play_settings_frame.destroy() if hasattr(self, "play_settings_frame") else None
        self.play_play_frame.destroy() if hasattr(self, "play_play_frame") else None
        self.play_progress_frame.destroy() if hasattr(self, "play_progress_frame") else None

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
        elif self.play_speed_factor_entry.get() == "" and self.play_optionemenu.get() == "Choreography":
            tkinter.messagebox.showwarning("Warning", "Please enter a speed factor")
            return
        # check if number of repetition is an int
        try:
            if self.play_loop_checkbox.get() == False:
                int(self.play_nbr_repetition_entry.get())
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter a number of repetition")
            return
        # check if speed factor is an int
        try:
            # if in choreography mode
            if self.play_optionemenu.get() == "Choreography":
                int(self.play_speed_factor_entry.get())
        except:
            tkinter.messagebox.showwarning("Warning", "Please enter a valid speed factor")
            return
        
        if self.modules.motion_control.choreography_status != "play":
            self.play_progress_bar.set(0)
            self.play_threading_action()

    def play_threading_action(self):
        # thread for playing
        self.playthread = Thread(target=self.play, daemon=True)
        self.playthread.start()

    def play_threading_progress(self):
        print("creating thread")
        print(self.modules.motion_control.choreography_status)
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
            self.play_connect_slider.configure(state="disabled")
            # set the play_status to play
            self.modules.motion_control.choreography_status = "play"
            self.play_threading_progress()
            if play_mode == "Choreography":
                name = self.choreographies_list[index]
                choreography = self.modules.choreographer.choreography_dict[name]
                # get loop status
                loop_status = self.play_loop_checkbox.get()
                if loop_status == True:
                    self.modules.motion_control.play_choreography(choreography, int(speed_factor), "loop")
                    self.modules.motion_control.choreography_status = "stop"
                    self.modules.motion_control.stop_motors()
                    print("choreography played")
                elif loop_status == False:
                    # get nbr repetition
                    nbr_repetition = self.play_nbr_repetition_entry.get()
                    self.modules.motion_control.play_choreography(choreography, int(speed_factor), "mult", int(nbr_repetition))
                    print("choreography played")
                    self.modules.motion_control.choreography_status = "stop"
                    self.modules.motion_control.stop_motors()
            elif play_mode == "Sequence":
                name = self.sequences_list[index]
                sequence = self.modules.choreographer.sequence_dict[name]
                speed_factor = "1" # CHANGE THIS LATER °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
                # get loop status
                # loop_status = self.play_loop_checkbox.get() # IMPLEMENT THAT °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
                # for every choreography in the sequence
                # get nbr repetition
                nbr_repetition = self.play_nbr_repetition_entry.get()
                for i in range(int(nbr_repetition)):
                    for choreography_index in sequence.sequence_l:
                        # transform the index into a name
                        choreography_name = self.choreographies_list[choreography_index-1]
                        # get the choreography
                        choreography = self.modules.choreographer.choreography_dict[choreography_name]
                        print(f"now playing {choreography_name}")
                        self.modules.motion_control.choreography_status = "play"
                        self.modules.motion_control.play_choreography(choreography, int(speed_factor), "mult", int(nbr_repetition))
                        if self.modules.motion_control.choreography_status == "stop":
                            self.modules.motion_control.stop_motors()
                            # unlock every entry and slider
                            self.play_speed_factor_entry.configure(state="normal")
                            self.play_nbr_repetition_entry.configure(state="normal")
                            self.play_loop_checkbox.configure(state="normal")
                            self.play_connect_slider.configure(state="normal")
                            self.update_bar_update = False
                            return
                self.modules.motion_control.choreography_status = "stop"
                self.modules.motion_control.stop_motors()

        elif play_status == "pause":
            print("pause to play")
            # set the play_status to play
            self.modules.motion_control.choreography_status = "play"
            self.play_threading_progress()
            return

        # unlock every entry and slider
        self.play_speed_factor_entry.configure(state="normal")
        self.play_nbr_repetition_entry.configure(state="normal")
        self.play_loop_checkbox.configure(state="normal")
        self.play_connect_slider.configure(state="normal")
        self.update_bar_update = False
        return


    def pause_event(self):
        if self.modules.motion_control.choreography_status == "play":
            self.modules.motion_control.choreography_status = "pause"

    def stop_event(self):
        self.modules.motion_control.choreography_status = "stop"

    def update_progress(self):
        # while thymio is connected
        while self.play_connect_slider.get() == True:
            if self.update_bar_update == True:
                self.set_progress(self.modules.motion_control.completion_percentage)
                time.sleep(0.1)
            else:
                return

    def set_progress(self, value):
        # between 0 and 1
        self.play_progress_bar.set(value)

    # RECORD METHODS ------------------------------------------------------------------------------------------------------
    def record_server_event(self):
        # get the server status
        server_status = self.record_server_slider.get()
        if server_status == True:
            # try to connect to the thymio
            self.record_server_status_label.configure(text="Server status: Running")
            self.modules.process_controler_data.init_record()
            self.display_record_layout()
        elif server_status == False:
            # disconnect from the thymio
            self.record_server_status_label.configure(text="Server status: Not running")
            self.remove_record_layout()

    def display_record_layout(self):
        # add record frame underneath
        self.record_record_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_record_frame.place(relx=0.4, rely=0.1, relwidth=0.55, relheight=0.10)
        # add record and stop buttons inside
        self.record_record_button = customtkinter.CTkButton(self.record_record_frame, text="◉", command=self.record)
        self.record_record_button.place(relx=0.01, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        self.record_stop_button = customtkinter.CTkButton(self.record_record_frame, text="■", command=self.stop)
        self.record_stop_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        # add debug button inside
        self.record_debug_button = customtkinter.CTkButton(self.record_record_frame, text="Debug", command=self.debug)
        self.record_debug_button.place(relx=0.4, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")

        # add info box in the middle
        self.record_info_frame = customtkinter.CTkFrame(self.tabview.tab("Record"))
        self.record_info_frame.place(relx=0.4, rely=0.25, relwidth=0.55, relheight=0.65)
        # add label inside
        self.record_info_label = customtkinter.CTkLabel(self.record_info_frame, text="Info:", anchor="w")
        self.record_info_label.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.15)
        # add textbox inside
        self.record_info_textbox = customtkinter.CTkTextbox(self.record_info_frame, wrap='none', state="disabled")
        self.record_info_textbox.place(relx=0.01, rely=0.15, relwidth=0.98, relheight=0.78)

    def remove_record_layout(self):
        self.record_record_frame.destroy()
        self.record_info_frame.destroy()

    def record(self):
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

    def stop(self):
        # stop the recording
        
        pass

    def debug(self):
        pass

    # EDIT METHODS --------------------------------------------------------------------------------------------------------
    
    def editor_mode_select_event(self, new_editor_mode: str):
        if new_editor_mode == "Manage":
            self.editor_display_manage_layout()
        elif new_editor_mode == "Create Sequence":
            self.editor_manage_delete_layout()
            self.editor_display_create_seq_layout()

    def editor_display_manage_layout(self):
        # add frame underneath
        self.editor_frame = customtkinter.CTkFrame(self.tabview.tab("Edit"))
        self.editor_frame.place(relx=0, rely=0.08, relwidth=1, relheight=0.90)
        # add choregraphy or sequence option underneath
        self.editor_manage_optionemenu = customtkinter.CTkOptionMenu(self.editor_frame, values=["Choreography", "Sequence"], command=self.editor_manage_select_event)
        self.editor_manage_optionemenu.set("Chore or Seq")
        self.editor_manage_optionemenu.place(relx=0.01, rely=0.01, relwidth=0.25, relheight=0.05)
        self.editor_manage_radiobutton_frame = customtkinter.CTkScrollableFrame(self.editor_frame)
        self.editor_manage_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.75)
        self.editor_manage_radio_var = tkinter.IntVar(value=0)
        self.scrollable_frame_editor_manage = []

        # add title on the right
        self.editor_manage_title_label = customtkinter.CTkLabel(self.editor_frame, text="MANAGE MODE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.editor_manage_title_label.place(relx=0.38, rely=0.02, relwidth=0.25, relheight=0.05)

        # add buttons frame underneath
        self.editor_manage_buttons_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_buttons_frame.place(relx=0.4, rely=0.13, relwidth=0.55, relheight=0.10)
        # add delete button and trim button inside
        self.editor_manage_delete_button = customtkinter.CTkButton(self.editor_manage_buttons_frame, text="🗑", command=self.editor_manage_delete_event)
        self.editor_manage_delete_button.place(relx=0.01, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")
        self.editor_manage_trim_button = customtkinter.CTkButton(self.editor_manage_buttons_frame, text="✂", command=self.editor_manage_trim_event)
        self.editor_manage_trim_button.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.7, anchor="w")

        # add graph display underneath
        self.editor_manage_graph_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_graph_frame.place(relx=0.4, rely=0.25, relwidth=0.55, relheight=0.5)
        # add image inside
        self.editor_manage_graph_image = Image.open("app\\GUI_assets\\thymio-nuitg.jpg")
        self.editor_manage_graph_image = customtkinter.CTkImage(self.editor_manage_graph_image,  size=(300,200))
        self.editor_manage_graph_image_label = customtkinter.CTkLabel(self.editor_manage_graph_frame, image=self.editor_manage_graph_image, text="")
        self.editor_manage_graph_image_label.place(relx=0.5, rely=0.5, relwidth=0.98, relheight=0.98, anchor="center")

        # add trim sliders frame underneath
        self.editor_manage_trim_frame = customtkinter.CTkFrame(self.editor_frame, fg_color=(DEFAULT_LIGHT, DEFAULT_DARK))
        self.editor_manage_trim_frame.place(relx=0.4, rely=0.77, relwidth=0.55, relheight=0.20)
        
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
        print(f"delete {mode} {index}")
        if index < 0:
            tkinter.messagebox.showwarning("Warning", f"Please select something to delete")
        # pop up window to ask if sure
        elif tkinter.messagebox.askyesno("Warning", f"Are you sure you want to delete the {mode}: {index}?"):
            if mode == "Choreography":
                self.remove_choreography(index)
                self.editor_manage_refresh_chor_list()
                self.editor_delete_image()
            elif mode == "Sequence":
                self.remove_sequence(index)
                self.editor_manage_refresh_seq_list()
            self.editor_manage_deselect_button()

    def editor_manage_deselect_button(self):
        # deselect the radiobutton
        self.editor_manage_radio_var.set(-1)

    def editor_manage_trim_event(self):
        pass

    def refresh_editor_info_chor(self):
        # get the choreography name
        index = self.editor_manage_radio_var.get()
        # get the choreography name
        name = self.choreographies_list[index] 
        self.editor_manage_graph_image_light = Image.open(f"app/GUI_assets/temp_fig/{name}_light_graph.png") # open the image
        self.editor_manage_graph_image_dark = Image.open(f"app/GUI_assets/temp_fig/{name}_dark_graph.png") # open the image
        self.editor_manage_graph_image = customtkinter.CTkImage(light_image=self.editor_manage_graph_image_light, dark_image=self.editor_manage_graph_image_dark, size=(400,200)) # convert the image to tkinter format
        self.editor_manage_graph_image_label.configure(image=self.editor_manage_graph_image) # display the image

        # add two sliders in the slider box for start and end of trim
        self.editor_manage_trim_start_label = customtkinter.CTkLabel(self.editor_manage_trim_frame, text="Start:", anchor="w")
        self.editor_manage_trim_start_label.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.2)
        self.editor_manage_trim_start_slider_var = tkinter.IntVar(value=0)
        self.editor_manage_trim_start_slider = customtkinter.CTkSlider(self.editor_manage_trim_frame, orientation="horizontal", variable=self.editor_manage_trim_start_slider_var, command=self.editor_manage_trim_start_event)
        self.editor_manage_trim_start_slider.configure()
        self.editor_manage_trim_start_slider.place(relx=0.01, rely=0.3, relwidth=0.98, relheight=0.2)
        self.editor_manage_trim_end_label = customtkinter.CTkLabel(self.editor_manage_trim_frame, text="End:", anchor="w")
        self.editor_manage_trim_end_label.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.2)
        self.editor_manage_trim_end_slider_var = tkinter.IntVar(value=1)
        self.editor_manage_trim_end_slider = customtkinter.CTkSlider(self.editor_manage_trim_frame, orientation="horizontal", variable=self.editor_manage_trim_end_slider_var, command=self.editor_manage_trim_end_event)
        self.editor_manage_trim_end_slider.place(relx=0.01, rely=0.7, relwidth=0.98, relheight=0.2)

    def editor_manage_trim_start_event(self, value):
        # round value to 2 decimals
        value = round(float(value), 2)
        # create value label
        self.editor_manage_trim_start_label.configure(text=f"Start:\t\t\t\t\t         {value}")

    def editor_manage_trim_end_event(self, value):
        # round value to 2 decimals
        value = round(float(value), 2)
        # create value label
        self.editor_manage_trim_end_label.configure(text=f"End:\t\t\t\t\t         {value}")

    def editor_delete_image(self):
        self.editor_manage_graph_image = Image.open("app\\GUI_assets\\thymio-nuitg.jpg")
        self.editor_manage_graph_image = customtkinter.CTkImage(self.editor_manage_graph_image, size=(400,200))
        self.editor_manage_graph_image_label.configure(image=self.editor_manage_graph_image)

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
            newbutton = customtkinter.CTkRadioButton(master=self.editor_create_seq_chor_radiobutton_frame, corner_radius=0, state="disabled", radiobutton_width=5, radiobutton_height=5, variable=self.editor_create_seq_chor_radio_var, value=i, text=self.choreographies_list[i], command=self.editor_create_seq_refresh_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="w")
            self.scrollable_frame_chor.append(newbutton)
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
            self.scrollable_frame_seq.append(newbutton)

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

        

    def editor_create_seq_refresh_info_chor(self):
        pass
    
    def editor_create_seq_refresh_info_seq(self):
        pass

    def editor_create_seq_order_event(self):
        # create input dialog
        # get the name
        name = self.editor_create_seq_name_entry.get()
        if name == "":
            tkinter.messagebox.showwarning("Warning", "Please enter a name")
            return
        # create input dialog
        self.editor_create_dialog = customtkinter.CTkInputDialog(text=f"Sequence order for: {name}", title="Create Sequence")
        sequence_string = self.editor_create_dialog.get_input()
        print(sequence_string)
        
    def editor_create_seq_order_dialog_event(self, button):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()  