from tkinter import *
import time
import pyttsx3
import tkinter.messagebox
from bot import chat
import threading

saved_username = ["HUMAN"]
ans=["BOT"]
window_size = "500x500"


class ChatInterface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.human_icon = PhotoImage(file="human_icon.png")
        self.bot_icon = PhotoImage(file="bot_icon.png") 

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
        # Menu bar

        # File
        file = Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file)
        # file.add_command(label="Save Chat Log", command=self.save_chat)
        file.add_command(label="Clear Chat", command=self.clear_chat)
        #  file.add_separator()
        file.add_command(label="Exit", command=self.chatexit)

        # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        # username

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=self.color_theme_default)
        color_theme.add_command(label="Grey", command=self.color_theme_grey)
        color_theme.add_command(label="Blue", command=self.color_theme_dark_blue)
        color_theme.add_command(label="Torque", command=self.color_theme_turquoise)
        color_theme.add_command(label="Hacker", command=self.color_theme_hacker)

        #voice submenu
        voice_menu = Menu(options, tearoff=0)
        options.add_cascade(label="Voice", menu=voice_menu)
        voice_menu.add_command(label="Male", command=self.set_male_voice)
        voice_menu.add_command(label="Female", command=self.set_female_voice)

        #help menu
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="About Sanjeevini Bot", command=self.msg)
        help_option.add_command(label="Developer", command=self.about)
        #chat display frame
        self.text_frame = Frame(self.master, bd=6)
        self.text_frame.pack(expand=True, fill=BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)

        # chat messages text box
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # user entry field and send button
        self.entry_frame = Frame(self.master, bd=1)
        self.entry_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # entry field
       # self.entry_field = Entry(self.entry_frame, bd=1, justify=LEFT)
        #self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)

        # entry field
        self.entry_field = Entry(
            self.entry_frame,
            bd=1,
            justify=LEFT,
            font="Verdana 12",  # Increase font size for larger text
        )
        self.entry_field.pack(fill=X, padx=8, pady=10, ipady=8)  # Adjust padx, pady, and ipady as desired

        # self.users_message = self.entry_field.get()

        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.master, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
        self.send_button = Button(
            self.send_button_frame,
            text="Send",
            font="Verdana 12 bold",  # Larger font size for the button text
            relief=RAISED,
            bg='#4CAF50',
            fg='white',
            activebackground="#45a049",
            activeforeground="white",
            bd=3,
            width=8,  # Wider button
            command=lambda: self.send_message_insert(None)
        )
        self.send_button.pack(side=LEFT, padx=10, pady=10, ipady=10, ipadx=10)
        self.master.bind("<Return>", self.send_message_insert)

        self.last_sent_label(date="No messages sent.")
    
    # Initialize voice setting to female by default
        self.voice = 'female'

    def set_male_voice(self):
        self.voice = 'male'
        self.update_voice()

    def set_female_voice(self):
        self.voice = 'female'
        self.update_voice()

    def update_voice(self):
        x = pyttsx3.init()
        voices = x.getProperty('voices')

        if self.voice == 'male':
            x.setProperty('voice', voices[0].id)  # Male voice
        else:
            x.setProperty('voice', voices[1].id)  # Female voice

    def playResponce(self, responce):
        x = pyttsx3.init()
        print(responce)
        voices = x.getProperty('voices')
        li = []
        if len(responce) > 100:
            if responce.find('--') == -1:
                b = responce.split('--')
                print(b)
        if self.voice == 'male':
            x.setProperty('voice', voices[0].id)  # Male voice
        elif self.voice == 'female':
            x.setProperty('voice', voices[1].id)  # Female voice
        else:
            x.setProperty('voice', voices[1].id)  # Default to female if no selection

        x.setProperty('rate', 200)
        x.setProperty('volume', 1.0)
        x.say(responce)
        x.runAndWait()
        print("Played Successfully......")

    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)

    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def chatexit(self):
        exit()

    def msg(self):
        tkinter.messagebox.showinfo("Sanjeevini Bot",
                                    'Sanjeevini Bot is an intelligent chatbot designed to assist users with various queries efficiently and interactively. It uses Natural Language Processing (NLP) techniques to understand and respond to user inputs.\n\n'
                                    "How to Use This Chatbot:\n\n"
                                    "1. Retrieve Medicine Information\n"
                                    "   - Use the prefix `med.` followed by the condition to get medicine suggestions.\n"
                                    "   - Example: `med.headache`\n\n"
                                    "2. Get AI-Generated Responses\n"
                                    "   - Use the prefix `ai.` followed by your query to get responses generated by AI.\n"
                                    "   - Example: `ai.How does AI work?`\n\n"
                                    "3. Ask FAQs or Greetings\n"
                                    "   - For general questions, greetings, or commonly asked queries, simply type your message without any prefix.\n"
                                    "   - Example: `What are the symptoms of a cold?` or `Hello`\n\n"
                                    "4. Add New Medicine Information\n"
                                    "   - To add a new medicine suggestion, type it in the format `condition=medicine`.\n"
                                    "   - Example: `headache=paracetamol`\n\n"
                                    "5. Exit the Chat\n"
                                    "   - To exit, type `bye`, `exit`, or `quit`.\n")

    def about(self):
        developers = ["Azeem Sheikh","Chinmay Hegde","Aman Khan","Harshith Doijode"]
        developers_info = "\n".join(developers)
        tkinter.messagebox.showinfo("Sanjeevini Bot Developers", developers_info)
       
    def send_message_insert(self, message):
        user_input = self.entry_field.get()
        self.text_box.configure(state=NORMAL)
        self.text_box.image_create(END, image=self.human_icon)
        self.text_box.insert(END, f" ► {user_input}\n", "human")
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)
        
        #fetch bot response
        ob = chat(user_input)

        #display bot icon and message
        self.text_box.configure(state=NORMAL)
        self.text_box.image_create(END, image=self.bot_icon)  # Insert Bot Icon
        self.text_box.insert(END, f" ►{ob}\n", "bot")
        self.text_box.configure(state=DISABLED)
        self.text_box.see(END)

        #clear entry field and update last sent message label
        self.last_sent_label(str(time.strftime("Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
        self.entry_field.delete(0, END)
        time.sleep(0)
        t2 = threading.Thread(target=self.playResponce, args=(ob,))
        t2.start()
        #return ob

    def font_change_default(self):
        self.text_box.config(font="Verdana 10")
        self.entry_field.config(font="Verdana 10")
        self.font = "Verdana 10"

    def font_change_times(self):
        self.text_box.config(font="Times")
        self.entry_field.config(font="Times")
        self.font = "Times"

    def font_change_system(self):
        self.text_box.config(font="System")
        self.entry_field.config(font="System")
        self.font = "System"

    def font_change_helvetica(self):
        self.text_box.config(font="helvetica 10")
        self.entry_field.config(font="helvetica 10")
        self.font = "helvetica 10"

    def font_change_fixedsys(self):
        self.text_box.config(font="fixedsys")
        self.entry_field.config(font="fixedsys")
        self.font = "fixedsys"

    def color_theme_default(self):
        self.master.config(bg="#EEEEEE")
        self.text_frame.config(bg="#EEEEEE")
        self.entry_frame.config(bg="#EEEEEE")
        self.text_box.config(bg="#FFFFFF", fg="#000000")
        self.entry_field.config(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
        self.send_button_frame.config(bg="#EEEEEE")
        self.send_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.emoji_button.config(bg="#FFFFFF", fg="#000000", activebackground="#FFFFFF", activeforeground="#000000")
        self.sent_label.config(bg="#EEEEEE", fg="#000000")

        self.tl_bg = "#FFFFFF"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"

    # Dark
    def color_theme_dark(self):
        self.master.config(bg="#2a2b2d")
        self.text_frame.config(bg="#2a2b2d")
        self.text_box.config(bg="#212121", fg="#FFFFFF")
        self.entry_frame.config(bg="#2a2b2d")
        self.entry_field.config(bg="#212121", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#2a2b2d")
        self.send_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#212121", fg="#FFFFFF", activebackground="#212121", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#2a2b2d", fg="#FFFFFF")

        self.tl_bg = "#212121"
        self.tl_bg2 = "#2a2b2d"
        self.tl_fg = "#FFFFFF"

    # Grey
    def color_theme_grey(self):
        self.master.config(bg="#444444")
        self.text_frame.config(bg="#444444")
        self.text_box.config(bg="#4f4f4f", fg="#ffffff")
        self.entry_frame.config(bg="#444444")
        self.entry_field.config(bg="#4f4f4f", fg="#ffffff", insertbackground="#ffffff")
        self.send_button_frame.config(bg="#444444")
        self.send_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.emoji_button.config(bg="#4f4f4f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
        self.sent_label.config(bg="#444444", fg="#ffffff")

        self.tl_bg = "#4f4f4f"
        self.tl_bg2 = "#444444"
        self.tl_fg = "#ffffff"

    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

        # Blue

    def color_theme_dark_blue(self):
        self.master.config(bg="#263b54")
        self.text_frame.config(bg="#263b54")
        self.text_box.config(bg="#1c2e44", fg="#FFFFFF")
        self.entry_frame.config(bg="#263b54")
        self.entry_field.config(bg="#1c2e44", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#263b54")
        self.send_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#1c2e44", fg="#FFFFFF", activebackground="#1c2e44", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#263b54", fg="#FFFFFF")

        self.tl_bg = "#1c2e44"
        self.tl_bg2 = "#263b54"
        self.tl_fg = "#FFFFFF"

    # Torque
    def color_theme_turquoise(self):
        self.master.config(bg="#003333")
        self.text_frame.config(bg="#003333")
        self.text_box.config(bg="#669999", fg="#FFFFFF")
        self.entry_frame.config(bg="#003333")
        self.entry_field.config(bg="#669999", fg="#FFFFFF", insertbackground="#FFFFFF")
        self.send_button_frame.config(bg="#003333")
        self.send_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#669999", fg="#FFFFFF", activebackground="#669999", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#003333", fg="#FFFFFF")

        self.tl_bg = "#669999"
        self.tl_bg2 = "#003333"
        self.tl_fg = "#FFFFFF"

    # Hacker
    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"

    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_default()


root = Tk()

a = ChatInterface(root)
root.geometry(window_size)
root.title("Sanjeevini Bot")
root.iconbitmap('chatbot.ico')
root.mainloop()
