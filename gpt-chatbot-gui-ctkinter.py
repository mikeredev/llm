import customtkinter as tk
import openai_chat

# constants
DARK_MODE = False

class ChatbotUI:
    def __init__(self):
        self.root = tk.CTk()
        tk.set_appearance_mode("dark") if DARK_MODE else tk.set_appearance_mode("light")
        self.ui_text_color = ("black","white")
        self.ui_bg_color = ("#dedede", "#444444")
        custom_width =  int(self.root.winfo_screenwidth() * 0.2)
        custom_height =  int(self.root.winfo_screenheight() * 0.8)
        custom_resolution = f"{str(custom_width)}x{str(custom_height)}"
        screen_resolution = custom_resolution
        self.root.geometry(screen_resolution)
        self.root.attributes("-type", "splash")
        self.create_widgets()
        self.canvas.bind("<Configure>", self.resize_canvas(None))
        self.root.bind("<Shift-Return>", self.send_message)
        self.title="chatbot"
        self.run()

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.destroy()

    def resize_canvas(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def auto_scroll_to_bottom(self):
        self.canvas.yview_moveto(1.0)

    def create_widgets(self):
        # configure root frame to expand
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # configure master frame
        master = tk.CTkFrame(self.root, border_width=1, fg_color=self.ui_bg_color)
        master.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        # configure master frame to expand
        master.rowconfigure(0, weight=99) # navmain row (for chats)
        master.rowconfigure(1, weight=1) # navbottom row
        master.columnconfigure(0, weight=1) # expand column to fit

        # configure navmain
        navmain = tk.CTkFrame(master, border_width=1, fg_color="transparent")
        navmain.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        navmain.rowconfigure(0, weight=1) # expand row to fit
        navmain.columnconfigure(0, weight=1) # expand column to fit
    
        # configure canvas
        self.canvas = tk.CTkCanvas(navmain, background=self.ui_bg_color[1] if DARK_MODE else self.ui_bg_color[0], highlightbackground=self.ui_bg_color[1] if DARK_MODE else self.ui_bg_color[0])
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # expand canvas to fit

        # configure scrollbar
        scrollbar = tk.CTkScrollbar(navmain, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=1, pady=5)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # create frame within canvas to hold chats
        self.chat_window = tk.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0,0), window=self.chat_window)
        self.chat_window.configure(width=self.root.winfo_width())

        # configure navbottom
        navbottom=tk.CTkFrame(master, border_width=0, fg_color="transparent")
        navbottom.grid(row=1, column=0, sticky="nsew", padx=6, pady=5)
        navbottom.rowconfigure(0, weight=1)
        navbottom.rowconfigure(1, weight=1)
        navbottom.columnconfigure(0, weight=99)
        navbottom.columnconfigure(1, weight=1)

        # user input area
        self.user_input= tk.CTkTextbox(navbottom, height=50, border_width=1, text_color=self.ui_text_color)
        self.user_input.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        button_send = tk.CTkButton(navbottom, width=40, text="send", command=lambda:self.send_message(event=None))
        button_send.grid(row=0, column=1, padx=5, pady=5, sticky="s")
        button_quit = tk.CTkButton(navbottom, width=40, text="quit", command=self.quit)
        button_quit.grid(row=1, column=1, padx=5, pady=5, sticky="n")

        self.update_message_display("Hello!")

    def send_message(self, event):
        user_prompt = (self.user_input.get("0.0", "end")).strip()
        if user_prompt:
            self.user_input.configure(text_color="#666666")
            self.user_input.configure(state="disabled")
            chat = openai_chat.response("Reply to the user!", user_prompt)
            self.update_message_display(user_prompt,isUser=True)
            self.update_message_display(chat["output"])
            self.user_input.configure(state="normal")
            self.user_input.delete("0.0", "end")
            self.user_input.configure(text_color=self.ui_text_color)

    def update_message_display(self, message, isUser=False):
        message_frame = tk.CTkFrame(self.chat_window, fg_color="transparent")
        message_label = tk.CTkLabel(
            message_frame,
            text=message,
            anchor="e" if isUser else "w",
            justify="l",
            fg_color="#A7D3FF" if isUser else "#D0C3FF",
            wraplength=self.root.winfo_width() - 150,
            width=self.root.winfo_width() - 80,
            padx=10,
            pady=10,
            corner_radius=20,
            bg_color="transparent"
        )
        # update frame width here to allow for resizing smaller?

        if isUser:
            message_frame.grid(sticky="e", padx=5, pady=5)
            message_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        else:
            message_frame.grid(sticky="w", padx=5, pady=5)
            message_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    
        self.chat_window.update_idletasks()
        self.resize_canvas(None)
        self.auto_scroll_to_bottom()

if __name__ == "__main__":
    ChatbotUI()