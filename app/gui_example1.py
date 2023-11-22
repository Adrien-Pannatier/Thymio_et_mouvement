import customtkinter


class GeneralTab(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Info")
        self.add("Editor")
        self.add("Record")
        self.add("Play")

        # create frame in the "Info" tab
        self.info_frame = customtkinter.CTkFrame(self.tab("Info"))
        self.info_frame.pack(fill="y", expand=True, side="left")  # Set side="left" to align the frame to the left

        # configure the frame to take half of the left space
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)

        # create label inside the frame
        self.info_label = customtkinter.CTkLabel(self.info_frame, text="Chor1\nChor2", anchor="w")
        self.info_label.pack(fill="both", expand=True, padx=10, pady=10, anchor="w")  # Set anchor="w" to align the text to the left
    
    def test(self):
        print("test")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tab_view = GeneralTab(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.mainloop()