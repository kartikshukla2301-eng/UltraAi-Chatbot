import tkinter as tk
import threading
from datetime import datetime

#================ OPTIONAL AI =================
#Uncomment if you want real AI
import google.generativeai as genai
genai.configure(api_key="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")
model = genai.GenerativeModel("gemini-1.5-flash")

# ================= MEMORY =================
chat_history = []

# ================= BOT LOGIC =================
def get_bot_response(user_input):
    user_input_lower = user_input.lower()
    chat_history.append(user_input)

    if "hello" in user_input_lower:
        return "Hey 👋"
    elif "how are you" in user_input_lower:
        return "I'm running perfectly 🚀"
    elif "time" in user_input_lower:
        return f"Current time is {datetime.now().strftime('%H:%M:%S')}"
    elif "date" in user_input_lower:
        return f"Today's date is {datetime.now().strftime('%d-%m-%Y')}"
    elif "history" in user_input_lower:
        return "Recent: " + ", ".join(chat_history[-5:])
    elif "api" in user_input_lower:
        return "API stands for Application Programming Interface."
    elif "bye" in user_input_lower:
        return "Goodbye 👋"

    # AI fallback
    try:
        # response = model.generate_content(user_input)
        # return response.text
        return "I didn't understand that 🤔"
    except Exception as e:
        return f"Error: {str(e)}"

# ================= UI =================
root = tk.Tk()
root.title("⚡ Ultra Pro AI Chatbot")
root.geometry("540x650")
root.configure(bg="#0f172a")

# Header
header = tk.Label(root, text="⚡ Ultra Pro Chatbot", bg="#020617", fg="white", font=("Arial", 14, "bold"), pady=10)
header.pack(fill="x")

# Chat Area
chat_frame = tk.Frame(root, bg="#0f172a")
chat_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(chat_frame, bg="#0f172a", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#0f172a")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ================= MESSAGE =================
def add_message(message, sender):
    frame = tk.Frame(scrollable_frame, bg="#0f172a")
    time_label = tk.Label(frame, text=datetime.now().strftime("%H:%M"), font=("Arial", 7), bg="#0f172a", fg="gray")

    if sender == "user":
        msg = tk.Label(frame, text=message, bg="#2563eb", fg="white",
                       padx=10, pady=6, wraplength=320, justify="left")
        msg.pack(anchor="e", padx=10)
        time_label.pack(anchor="e", padx=12)
        frame.pack(fill="both", anchor="e", pady=4)
    else:
        msg = tk.Label(frame, text=message, bg="#1e293b", fg="white",
                       padx=10, pady=6, wraplength=320, justify="left")
        msg.pack(anchor="w", padx=10)
        time_label.pack(anchor="w", padx=12)
        frame.pack(fill="both", anchor="w", pady=4)

    root.update_idletasks()
    canvas.yview_moveto(1.0)

# ================= SEND =================
def send_message(event=None):
    user_text = entry.get().strip()
    if not user_text:
        return

    add_message(user_text, "user")
    entry.delete(0, tk.END)

    def bot_reply():
        reply = get_bot_response(user_text)
        if not reply:
            reply = "⚠️ No response"
        add_message(reply, "bot")

    threading.Thread(target=bot_reply).start()

# ================= INPUT =================
input_frame = tk.Frame(root, bg="#020617")
input_frame.pack(fill="x")

entry = tk.Entry(input_frame, bg="#0f172a", fg="white", insertbackground="white", relief="flat")
entry.pack(side="left", fill="x", expand=True, padx=10, pady=12, ipady=6)
entry.bind("<Return>", send_message)

send_btn = tk.Button(input_frame, text="Send", bg="#2563eb", fg="white", relief="flat", command=send_message)
send_btn.pack(side="right", padx=10)

# ================= START =================
add_message("⚡ Ultra Bot Ready! Type anything 😎", "bot")

root.mainloop()