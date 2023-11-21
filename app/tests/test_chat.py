from tkinter import *

# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
TEXT_COLOR_USER = "#1E1E1E"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Send function
def send(event=None):
    user_msg = f"{e.get()} <- You "
    txt.insert(END, "\n" + user_msg,'user')

    user = e.get().lower()

    if (user == "hello"):
        txt.insert(END, "\n" + "Bot -> Hi there, how can I help?", 'bot')
    elif (user == "hi" or user == "hii" or user == "hiiii"):
	    txt.insert(END, "\n" + "Bot -> Hi there, what can I do for you?", 'bot')
    elif (user == "how are you"):
        txt.insert(END, "\n" + "Bot -> fine! and you", 'bot')
    elif (user == "fine" or user == "i am good" or user == "i am doing good"):
	    txt.insert(END, "\n" + "Bot -> Great! how can I help you.", 'bot')
    elif (user == "thanks" or user == "thank you" or user == "now its my time"):
	    txt.insert(END, "\n" + "Bot -> My pleasure !", 'bot')
    elif (user == "what do you sell" or user == "what kinds of items are there" or user == "have you something"):
	    txt.insert(END, "\n" + "Bot -> We have coffee and tea", 'bot')
    elif (user == "tell me a joke" or user == "tell me something funny" or user == "crack a funny line"):
	    txt.insert(
			END, "\n" + "Bot -> What did the buffalo say when his son left for college? Bison.! ", 'bot')
    elif (user == "goodbye" or user == "see you later" or user == "see yaa"):
	    txt.insert(END, "\n" + "Bot -> Have a nice day!", 'bot')
    else:
	    txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that", 'bot')
		
    e.delete(0, END)
	
# Bind main function to enter key
root.bind('<Return>', send)

lable1 = Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0)

# Create a frame
frame = Frame(root, bg=BG_COLOR)
frame.grid(row=1, column=0, columnspan=2)

# Create a scrollbar and place it on the right side of the frame
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

# Create a text widget and attach the scrollbar to it
txt = Text(frame, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60, yscrollcommand=scrollbar.set)
txt.pack(side=LEFT, fill=BOTH)

# Configure the scrollbar to scroll the text widget
scrollbar.config(command=txt.yview)

# Create tags for user and bot messages
txt.tag_config('user', justify='right', background=BG_GRAY, foreground=TEXT_COLOR_USER )

txt.tag_config('bot', justify='left', background=BG_COLOR)

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

e.focus_set()

send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

root.mainloop()