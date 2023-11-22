import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


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
        self.chor_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Info"))
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
        self.seq_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Info"))
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
        self.play_radiobutton_frame = customtkinter.CTkScrollableFrame(self.tabview.tab("Play"))
        self.play_radiobutton_frame.place(relx=0.01, rely=0.13, relwidth=0.33, relheight=0.75)
        self.play_radio_var = tkinter.IntVar(value=0)
        self.scrollable_frame_play = []

        # add title on the right
        self.play_title_label = customtkinter.CTkLabel(self.tabview.tab("Play"), text="PLAY MODE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.play_title_label.place(relx=0.4, rely=0.01, relwidth=0.25, relheight=0.05)

        # add settings frame underneath
        self.play_settings_frame = customtkinter.CTkFrame(self.tabview.tab("Play"), fg_color="#c5deea")
        self.play_settings_frame.place(relx=0.4, rely=0.07, relwidth=0.55, relheight=0.35)

        # add play frame underneath
        self.play_play_frame = customtkinter.CTkFrame(self.tabview.tab("Play"), fg_color="#c5deea")
        self.play_play_frame.place(relx=0.4, rely=0.53, relwidth=0.55, relheight=0.10)
        # add play pause and stop buttons
        self.play_play_button = customtkinter.CTkButton(self.play_play_frame, text="▶️", command=self.play)
        self.play_play_button.place(relx=0.01, rely=0.5, relwidth=0.25, relheight=0.98, anchor="w")
        self.play_pause_button = customtkinter.CTkButton(self.play_play_frame, text="⏸️", command=self.pause)
        self.play_pause_button.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.98, anchor="center")
        self.play_stop_button = customtkinter.CTkButton(self.play_play_frame, text="⏹️", command=self.stop)
        self.play_stop_button.place(relx=0.99, rely=0.5, relwidth=0.25, relheight=0.98, anchor="e")

        # add progress frame underneath
        self.play_progress_frame = customtkinter.CTkFrame(self.tabview.tab("Play"), fg_color="#c5deea")
        self.play_progress_frame.place(relx=0.4, rely=0.65, relwidth=0.55, relheight=0.10)


    def mode_select_event(self, new_mode: str):
        pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # INFO METHODS
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

    def remove_choreography(self, index):
        self.scrollable_frame_chor[index].destroy()
        self.scrollable_frame_chor.pop(index)
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

    def remove_sequence(self, index):
        self.seq_radio_button.destroy()
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
            newbutton = customtkinter.CTkRadioButton(master=self.play_radiobutton_frame, variable=self.play_radio_var, value=i, text=self.choreographies_list[i], command=self.refresh_info_chor)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_play.append(newbutton)
    
    def play_refresh_seq_list(self):
        # remove all buttons
        for button in self.scrollable_frame_play:
            button.destroy()
        self.scrollable_frame_play = []
        for i in range(len(self.sequences_list)):
            newbutton = customtkinter.CTkRadioButton(master=self.play_radiobutton_frame, variable=self.play_radio_var, value=i, text=self.sequences_list[i], command=self.refresh_info_seq)
            newbutton.grid(row=i, column=0, padx=10, pady=(0, 10),sticky="w")
            self.scrollable_frame_play.append(newbutton)

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

class Gui:
    def __init__(self, modules):
        self.app = App(modules=modules)
        self.app.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()