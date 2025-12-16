# client3.py
import socket
import threading
import customtkinter as ctk # Poprawiony import, aby używać ctk
import winsound

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sent_messages = 0
        self.unread_messages = 0 # Zmieniona nazwa zmiennej licznika

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("MessBOX")
        self.root.geometry("600x400")

        self.init_ui()
        self.start_connection()

    def init_ui(self):
        self.chat_log = ctk.CTkTextbox(self.root, state='disabled', width=550, height=250)
        self.chat_log.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.msg_entry = ctk.CTkEntry(self.root, placeholder_text="Wpisz tutaj swoją wiadomość...", width=450)
        self.msg_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.msg_entry.bind("<Return>", self.send_message_event)

        # Użycie fg_color="#006400"
        self.send_button = ctk.CTkButton(self.root, text="Wyślij", command=self.send_message, width=80,
                                         fg_color="#006400", text_color="black")
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        self.emoji_button = ctk.CTkButton(self.root, text="Emotki", command=self.open_emoji_window, width=80,
                                          fg_color="#006400", text_color="black")
        self.emoji_button.grid(row=1, column=2, padx=10, pady=10)

        self.online_button = ctk.CTkButton(self.root, text="Użytkownicy Online", command=self.send_online_request,
                                           width=80, fg_color="#006400", text_color="black")
        self.online_button.grid(row=1, column=3, padx=10, pady=10)

        # Użycie self.unread_label (zgodne z kodem)
        self.unread_label = ctk.CTkLabel(self.root, text="Odebrane wiadomości: 0", font=("Arial", 14))
        self.unread_label.grid(row=2, column=2, columnspan=2, padx=10, pady=5)

        self.sent_label = ctk.CTkLabel(self.root, text="Wysłane wiadomości: 0", font=("Arial", 14))
        self.sent_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def start_connection(self):
        try:
            self.client_socket.connect((self.host, self.port))
            username = self.ask_username()
            if username:
                self.client_socket.send(username.encode('utf-8'))
                winsound.PlaySound("C:\\Windows\\Media\\Ring06.wav", winsound.SND_FILENAME)
                self.receive_thread = threading.Thread(target=self.receive_messages)
                self.receive_thread.start()
            else:
                self.root.destroy()
        except Exception as e:
            print(f"Błąd w dołączaniu do serwera: {e}")
            self.root.destroy()

    def ask_username(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Witamy w MessBOX")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        label = ctk.CTkLabel(dialog, text="Wpisz swoją nazwę użytkownika:", font=("Arial", 14))
        label.pack(pady=20)

        entry = ctk.CTkEntry(dialog, placeholder_text="Nazwa użytkownika", width=250)
        entry.pack(pady=10)

        username = []

        def on_confirm(event=None):
            username.append(entry.get())
            dialog.destroy()

        confirm_button = ctk.CTkButton(dialog, text="Dołącz", command=on_confirm, fg_color="#006400",
                                       text_color="black")
        confirm_button.pack(pady=8)

        entry.bind("<Return>", on_confirm)
        dialog.grab_set()
        self.root.wait_window(dialog)

        return username[0] if username else None

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')

                if message == "CLEAR_CHAT":
                    self.clear_chat()
                else:
                    message = self.emoji_conversion(message)
                    self.update_chat_log(message)
                    self.unread_messages += 1 # Użycie unread_messages
                    self.update_unread_label() # Użycie unread_label

                winsound.PlaySound("C:\\Windows\\Media\\Windows Pop-up Blocked.wav", winsound.SND_FILENAME)

            except Exception as e:
                print(f"Błąd w odebraniu wiadomości: {e}")
                break

    def clear_chat(self):
        self.chat_log.configure(state='normal')
        self.chat_log.delete(1.0, ctk.END)
        self.chat_log.configure(state='disabled')

    def emoji_conversion(self, message):
        emojis = {
            ":)": "😊", ":(": "😞", ";)": "😉", ":D": "😁", ":c": "😭",
            "<3": "❤", ":P": "😜", ":O": "😮", ":*": "😘", ":|": "😐",
            ":3": "😸", ":/": "😕", ":v": "✌️", ":L": "😬", ":S": "😖",
            ":b": "😋", ";D": "😏", ":T": "😓"
        }
        for code, emoji in emojis.items():
            message = message.replace(code, emoji)
        return message

    def send_message(self):
        message = self.msg_entry.get()
        if message:
            message = self.emoji_conversion(message)
            self.client_socket.send(message.encode('utf-8'))
            self.msg_entry.delete(0, ctk.END)
            self.sent_messages += 1
            self.update_sent_label()

    def send_message_event(self, event):
        self.send_message()

    def send_online_request(self):
        self.client_socket.send('/online'.encode('utf-8'))

    def exit_chat(self):
        self.client_socket.send('/exit'.encode('utf-8'))
        self.client_socket.close()
        self.root.quit()

    def update_chat_log(self, message):
        self.chat_log.configure(state='normal')
        self.chat_log.insert(ctk.END, message + '\n')
        self.chat_log.yview(ctk.END)
        self.chat_log.configure(state='disabled')

    def update_unread_label(self): # Poprawiona metoda aktualizacji
        self.unread_label.configure(text=f"Odebrane wiadomości: {self.unread_messages}")

    def update_sent_label(self):
        self.sent_label.configure(text=f"Wysłane wiadomości: {self.sent_messages}")

    def on_closing(self):
        self.exit_chat()
        self.root.destroy()

    def open_emoji_window(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Wybierz emotkę")
        dialog.geometry("300x300")
        dialog.resizable(False, False)

        emojis = ["👍", "👎", "❤", "😂", "😞", "😉", "😁", "😭", "😜", "😲", "💩", "🤔"]
        row_count = 0
        column_count = 0
        for emoji in emojis:
            button = ctk.CTkButton(dialog, text=emoji, width=80, height=60, font=("Arial", 22),
                                   command=lambda e=emoji: self.insert_emoji(e), fg_color="#006400", text_color="black",
                                   corner_radius=10)
            button.grid(row=row_count, column=column_count, padx=5, pady=5)
            column_count += 1
            if column_count == 3:
                column_count = 0
                row_count += 1

    def insert_emoji(self, emoji):
        current_text = self.msg_entry.get()
        self.msg_entry.delete(0, ctk.END)
        self.msg_entry.insert(0, current_text + emoji)

if __name__ == "__main__":
    client = ChatClient()
    client.root.mainloop()