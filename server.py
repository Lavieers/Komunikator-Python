import socket
import threading
import os
from datetime import datetime
import random

clients = {}
addresses = {}

facts = [
    "Delfiny mają swoje imiona i rozpoznają się po gwizdach.",
    "W ludzkim organizmie jest około 37,2 biliona komórek.",
    "Największy deszczowy las świata, Amazonia, produkuje 20% tlenu na Ziemi.",
    "Każda sekunda trwa dłużej na biegunach Ziemi niż na równiku z powodu różnic w grawitacji.",
    "Mrówki nie śpią w tradycyjnym sensie – mają cykle aktywności i odpoczynku.",
    "W przestrzeni kosmicznej nie ma dźwięku, ponieważ nie ma tam powietrza, które przenosi fale dźwiękowe.",
    "Najstarszy zapisany przepis na piwo pochodzi z około 4000 roku p.n.e.",
    "W Japonii istnieje wyspa zwana Tashirojima, znana jako 'kocia wyspa', ponieważ koty przewyższają liczbę ludzi."
]

commands = {
    "/exit": "Opuszczenie chatu.",
    "/msg <użytkownik> <wiadomość>": "Wysyłanie wiadomości prywatnej do użytkownika.",
    "/online": "Wyświetla listę aktualnie zalogowanych użytkowników.",
    "/all <wiadomość>": "Wysyłanie wiadomości do wszystkich użytkowników.",
    "/fact": "Wyświetla losowy, interesujący fakt.",
    "/help": "Wyświetla listę dostępnych komend.",
    "/clear": "Wyczyszczenie okna czatu.",
    "/whoami <użytkownik>": "Wyświetlenie informacji o użytkowniku (nazwa i czas dołączenia).",
    "/nickname <nowa_nazwa>": "Zmiana pseudonimu."
}


def save_message_to_history(sender, recipient, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('chat_history.txt', 'a', encoding='utf-8') as history_file:
        if recipient:
            history_file.write(f"[{timestamp}] {sender} -> {recipient}: {message}\n")
        else:
            history_file.write(f"[{timestamp}] {sender}: {message}\n")


def send_online_users(client):
    online_users = ', '.join([info["username"] for info in clients.values()])
    client.send(f"Zalogowani użytkownicy: {online_users}".encode('utf-8'))


def send_private_message(sender, recipient, message):
    for client_socket, user_info in clients.items():
        if user_info["username"] == recipient:
            client_socket.send(f"Wiadomość prywatna od {sender}: {message}".encode('utf-8'))
            break


def broadcast_message(sender, message):
    for client in clients.keys():
        try:
            client.send(f"{sender}: {message}".encode('utf-8'))
        except:
            remove_client(client)


def send_random_fact(client):
    fact = random.choice(facts)
    client.send(f"🧠 Ciekawostka: {fact}".encode('utf-8'))


def send_help(client):
    help_message = "Dostępne komendy:\n"
    for cmd, desc in commands.items():
        help_message += f"{cmd} - {desc}\n"
    client.send(help_message.encode('utf-8'))


def clear_chat(client):
    client.send("CLEAR_CHAT".encode('utf-8'))


def send_user_info(client, command):
    try:
        if len(command) > 1:
            requested_user = command[1]
            user_info = next(
                (info for info in clients.values() if info["username"] == requested_user),
                None
            )
            if user_info:
                client.send(
                    f"Użytkownik: {user_info['username']}\nCzas dołączenia: {user_info['joined']}".encode('utf-8'))
            else:
                client.send("Nie znaleziono takiego użytkownika.".encode('utf-8'))
        else:
            username = clients[client]["username"]
            joined_time = clients[client]["joined"]
            client.send(f"Twoje dane:\nUżytkownik: {username}\nCzas dołączenia: {joined_time}".encode('utf-8'))
    except Exception as e:
        client.send(f"Nie udało się pobrać danych: {e}".encode('utf-8'))


def change_nickname(client, new_username):
    if new_username in [info["username"] for info in clients.values()]:
        client.send(f"❌ Pseudonim '{new_username}' jest już zajęty. Wybierz inny.".encode('utf-8'))
    else:
        old_username = clients[client]["username"]
        clients[client]["username"] = new_username
        broadcast_message("Serwer", f"🔔 {old_username} zmienił nazwę na {new_username}.")
        client.send(f"✅ Twoja nowa nazwa to: {new_username}".encode('utf-8'))
        return new_username


def remove_client(client):
    username = clients[client]["username"]
    del clients[client]
    broadcast_message('Serwer', f"{username} opuścił chat.")
    send_online_users(client)


def handle_client(client, username):
    welcome_message = (
        f"\nWitaj, {username}! "
        "Możesz użyć komendy /help, aby zobaczyć listę dostępnych funkcji.\n"
        "Miłego korzystania z chatu! 😊\n"
    )
    client.send(welcome_message.encode('utf-8'))

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('/'):
                command = message.split(' ', 1)
                cmd = command[0]

                if cmd == '/exit':
                    remove_client(client)
                    break
                elif cmd == '/msg' and len(command) == 2:
                    recipient, msg = command[1].split(' ', 1)
                    send_private_message(username, recipient, msg)
                    save_message_to_history(username, recipient, msg)
                elif cmd == '/online':
                    send_online_users(client)
                elif cmd == '/all' and len(command) == 2:
                    broadcast_message(username, command[1])
                    save_message_to_history(username, None, command[1])
                elif cmd == '/fact':
                    send_random_fact(client)
                elif cmd == '/help':
                    send_help(client)
                elif cmd == '/clear':
                    clear_chat(client)
                elif cmd == '/whoami':
                    send_user_info(client, command)
                elif cmd == '/nickname' and len(command) == 2:
                    new_username = command[1]
                    username = change_nickname(client, new_username)
                else:
                    client.send("Nieznana komenda. Użyj /help, aby zobaczyć dostępne komendy.".encode('utf-8'))
            else:
                broadcast_message(username, message)
                save_message_to_history(username, None, message)
        except:
            remove_client(client)
            break


def start_server():
    if not os.path.exists('chat_history.txt'):
        with open('chat_history.txt', 'w', encoding='utf-8') as f:
            f.write("Chat History\n====================\n")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen()

    print("Serwer nasłuchuje połączeń...")

    while True:
        client, client_address = server.accept()
        print(f"Połączenie z {client_address}")

        client.send("Wpisz swoją nazwę użytkownika: ".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        joined_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        clients[client] = {"username": username, "joined": joined_time}
        addresses[client] = client_address

        broadcast_message('\nSerwer', f"{username} dołączył do chatu.\n")
        send_online_users(client)

        thread = threading.Thread(target=handle_client, args=(client, username))
        thread.start()


if __name__ == "__main__":
    start_server()