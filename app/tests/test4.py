# from asyncio import create_task, sleep
# from tdmclient import ClientAsync, aw

# class Thymtest:
#     def __init__(self):
#         self.node = None

#     def init_thymio_connection(self):
#         try:

#             client = ClientAsync()
#             self.node = aw(client.wait_for_node())
#             aw(self.node.lock())

#             print("Thymio node connected")
#             print(f"Node lock on {self.node}")

#             return 1

#                     # Signal the Thymio to broadcast variable changes
#                     # await node.watch(variables=True)

#         except ConnectionRefusedError:
#             print("Thymio driver connection refused")

#         except ConnectionResetError:
#             print("Thymio driver connection closed")

#     # def process_messages(client: ClientAsync):
#     #     """Process waiting messages from the Thymio driver."""

#     #     try:
#     #         while True:
#     #             client.process_waiting_messages()

#     #     except Exception:
#     #         pass

#     def input(self):
#         aw(self.node.set_variables(  # apply the control on the wheels
#                     {"motor.left.target": [int(0)], "motor.right.target": [int(0)]}))


#     def test(self):
#         node = self.init_thymio_connection()
#         self.input()

# Thymtest().test()

# print('''　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　 　◇　　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　　ｉ　　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　　＼　　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　　　╲　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　　　〔　　　　　　　　　　　　　　　
# 　　　　　　　　　　　　╭～⌒ ～╮　　　　　　　　　　　　　
# 　　　　　　　　　　　　│　　　│　　　　　　　　　　　　　
# 　　　　　　　　　　　　│　　　│　　　　　　　　　　　　　
# 　　　　　　　　　 　　╭⌒ ╮  ╭⌒ ╮　　　　　　　　　　　　
# 　　　　　　　　　 　　│Ｏ│  │Ｏ│　　　　　　　　　　　　
# 　　　　　　　　　 　　╰╮ ╯  ╰ ╭╯　　　　　　　　　　　　
# 　　　　　　　　　　　　│　 v　│　　　　　　　　　　　　　
# 　　　　　　　　　　　　│      │　　　　　　　　　　　　　
# 　　　　　　　　　　　　│　  　│　　　　　　　　　　　　　
# 　　　　　　　　　▕︸︸︸︸︸︸︸︸︸－～　　　　　　　　　
# 　　　　　　　　　︷　　　　　　 　▕－～╲　　　　　　　　
# 　　　　　　　　╱＞〉　⌒╮　　＿　  ▕　  　╲╲　　　　　　　
# 　　　　　　　╱╱  ▕　〈　ノ　╱┐｝  ▕　  　　╲╲　　　　　　
# 　 　　　　　╱╱ 　▕　　︶　　＼　｝▕　　　　╲╲　　　　　
# 　　　　　╱╱　　  ▕　　　︷　　︶　▕　　　　　╮╮　　　　
# 　　　　∠╱　　  　▕　　〈　〉　　　▕　　　　　〈ｉ　　　　
# 　　　　□　　　 　▕　　　︶　　　　▕　　　　　▕⌒　　　　
# 　　　∠／　　　　　︳　　　　　　　▕　　　　　▕︷＼　　　
# 　　∠　︳　　　　　╰︷︷︷︷︷︷︷ ╯　　　　　〈︳︶　　　
# 　　　∩　　　 　  　　▕　︳　╲▕　　　　　　　　　　　　
# 　　　∪　　　   　　　▕︸︳　▕▕　　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳　▕▕　　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳　 ︳︳　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳　 ︳︳　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳ 　＼〕　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳ 　｛〕　　　　　　　　　　　
# 　　　　　　　　　　　▕︸︳ 　｛〉　　　　　　　　　　　
# 　　　　　　　　　　︵▕︸︳　 │︶￣︸～、　　　　　　　
# 　　　　　　　　　╱　￣￣︳　 ／　　　　｀　　　　　　　
# 　　　　　　　　╱︷︷︷︷︳ 　｜︷︷︷︷︷〉　　　　　　
# 　　　　　　　　　￣￣￣￣￣ 　　└─────┘　''')

# from tkinter import *
# INSERT
# END
# # GUI
# root = Tk()
# root.title("Chatbot")

# BG_GRAY = "#ABB2B9"
# BG_COLOR = "#17202A"
# TEXT_COLOR = "#EAECEE"

# FONT = "Helvetica 14"
# FONT_BOLD = "Helvetica 13 bold"

# # Send function
# def send():
# 	send = "You -> " + e.get()
# 	txt.insert(END, "\n" + send)

# 	user = e.get().lower()

# 	if (user == "hello"):
# 		txt.insert(END, "\n" + "Bot -> Hi there, how can I help?")

# 	elif (user == "hi" or user == "hii" or user == "hiiii"):
# 		txt.insert(END, "\n" + "Bot -> Hi there, what can I do for you?")

# 	elif (user == "how are you"):
# 		txt.insert(END, "\n" + "Bot -> fine! and you")

# 	elif (user == "fine" or user == "i am good" or user == "i am doing good"):
# 		txt.insert(END, "\n" + "Bot -> Great! how can I help you.")

# 	elif (user == "thanks" or user == "thank you" or user == "now its my time"):
# 		txt.insert(END, "\n" + "Bot -> My pleasure !")

# 	elif (user == "what do you sell" or user == "what kinds of items are there" or user == "have you something"):
# 		txt.insert(END, "\n" + "Bot -> We have coffee and tea")

# 	elif (user == "tell me a joke" or user == "tell me something funny" or user == "crack a funny line"):
# 		txt.insert(
# 			END, "\n" + "Bot -> What did the buffalo say when his son left for college? Bison.! ")

# 	elif (user == "goodbye" or user == "see you later" or user == "see yaa"):
# 		txt.insert(END, "\n" + "Bot -> Have a nice day!")

# 	else:
# 		txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that")

# 	e.delete(0, END)


# lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(
# 	row=0)

# txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
# txt.grid(row=1, column=0, columnspan=2)

# scrollbar = Scrollbar(txt)
# scrollbar.place(relheight=1, relx=0.974)

# e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
# e.grid(row=2, column=0)

# send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
# 			command=send).grid(row=2, column=1)

# root.mainloop()

#Import required libraries
from tkinter import *

#Create an instance of tkinter window
win =Tk()

#Define the geometry of the window
win.geometry("600x250")

#Create a text widget
text= Text(win)
text.insert(INSERT, "Hello World!\n")
text.insert(END, "This is a New Line")

text.pack(fill=BOTH)

#Configure the text widget with certain color
text.tag_config("start", foreground="red")
text.tag_add("start", "1.3", "1.12")

win.mainloop()