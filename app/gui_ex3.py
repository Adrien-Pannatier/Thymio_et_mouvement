import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.mode = "Info"

            # configure window
        self.title("Thymio mouvement organique")
        self.geometry(f"{1100}x{580}")

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

        # INFO TAB CREATION
        # create frame in the "Info" tab
        self.tabview.tab("Info").grid_columnconfigure((0, 1), weight=0)
        self.tabview.tab("Info").grid_rowconfigure((0, 1, 2), weight=0, minsize=10)

        # add "refresh" button
        self.refresh_button = customtkinter.CTkButton(self.tabview.tab("Info"), text="⟳", command=self.refresh)
        self.refresh_button.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nw")

        # add "choreography list" frame
        self.chor_radiobutton_frame = customtkinter.CTkFrame(self.tabview.tab("Info"),)
        self.chor_radiobutton_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nw")
        self.chor_radio_var = tkinter.IntVar(value=0)
        self.chor_label_radio_group = customtkinter.CTkLabel(master=self.chor_radiobutton_frame, text="CTkRadioButton Group:")
        self.chor_label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.chor_radio_button_1 = customtkinter.CTkRadioButton(master=self.chor_radiobutton_frame, variable=self.chor_radio_var, value=0)
        self.chor_radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")

    
    def mode_select_event(self, new_mode: str):
        pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # INFO METHODS
    def refresh(self):
        print("refresh")

if __name__ == "__main__":
    app = App()
    app.mainloop()