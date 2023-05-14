import customtkinter as ui
import openai

ui.set_appearance_mode("dark")
ui.set_default_color_theme("dark-blue")


# function to generate chat completion
def chat(messages):
    user_prompt = user_input.get()
    messages += [{"role": "user", "content": user_prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", max_tokens=150, temperature=0, messages=messages
    )
    reply = response.choices[0].message.content
    tokens = response.usage.total_tokens

    chat_messages.insert(
        "end",
        user_prompt + "\n",
        ("user"),
    )

    chat_messages.insert(
        "end",
        reply + "\n",
        ("bot"),
    )

    chat_messages.see("end")
    user_input.delete(0, "end")  # Clear the user input field
    chat_messages.yview_moveto(1.0)

    messages += [{"role": "assistant", "content": reply}]
    global counter_tokens
    counter_tokens += tokens
    counter_cost = round(counter_tokens * 0.000002, 3)
    info_bar.configure(text=str(counter_cost) + " USD")
    print(messages)

    # return {"reply": reply, "tokens": tokens}


# function to close window
def close_window():
    root.destroy()


# initialise environment
root = ui.CTk()
# custom_width = int(root.winfo_screenwidth() * 0.33)
custom_width = 480
# custom_height = int(root.winfo_screenheight() * 0.73)
custom_height = 640
screen_resolution = str(custom_width) + "x" + str(custom_height)
root.geometry(screen_resolution)
# root.attributes("-type", "splash")
counter_tokens = 0
messages = []
messages += [{"role": "system", "content": "Be polite and chat with the user"}]

# create a frame to hold the grid
frame = ui.CTkFrame(root)
frame.pack(expand=True, fill="both")

# info bar
info_bar = ui.CTkLabel(
    master=frame, font=("Monaco", 24), text=counter_tokens, bg_color="red"
)
info_bar.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# chat window
chat_window = ui.CTkFrame(master=frame)
chat_window.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# chat messages appear here
chat_messages = ui.CTkTextbox(
    chat_window,
    font=("JetBrains Mono", 14),
    pady=0,
    padx=5,
    height=custom_height * 0.7,
)
chat_messages.tag_config(
    "user",
    background="#4080ff",
    foreground="white",
    justify="right",
    wrap="word",
    spacing3=5,
    spacing2=3,
    spacing1=5,
)
chat_messages.tag_config(
    "bot",
    background="lightgrey",
    foreground="black",
    justify="left",
    wrap="word",
    spacing3=5,
    spacing2=3,
    spacing1=5,
)
chat_messages.pack(side="top", fill="both", expand=True)

# user input text box
user_input = ui.CTkEntry(
    master=frame,
    font=("Arial", 14),
    width=custom_width * 0.75,
)
user_input.grid(row=2, column=0, padx=20, sticky="w")

# send user input button
send_message = ui.CTkButton(
    master=frame,
    command=lambda: chat(messages),
    text="sendit",
    font=("Arial", 14),
    width=frame.winfo_width() * 0.1,
)
send_message.grid(row=2, column=1, padx=20, sticky="e")


# user_input.bind("<Return>", lambda event: (send_message(), "break"))

# start
root.mainloop()
