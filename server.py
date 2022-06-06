from email import message
from http import server
import socket
import threading
from typing import final
from urllib import response

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []


def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = "{username}: {message}".format(
                username=username, message=message)
            send_message_to_all(final_msg)
        else:
            print("The message from client {username} is empty".format(
                username=username))


def send_message_to_client(client, message):
    client.sendall(message.encode('utf-8'))


def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            promt_message = "SERVER: Welcome {username} to the chat room.".format(
                username=username)
            send_message_to_all(promt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages,
                     args=(client, username)).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print("Running the server on {HOST} and port {PORT}".format(
            HOST=HOST, PORT=PORT))
    except:
        print("Unable to bind to host {HOST} and port {PORT}".format(
            HOST=HOST, PORT=PORT))

    server.listen(LISTENER_LIMIT)

    while True:
        client, address = server.accept()
        print("Successfully connected to client {address[0]}:{address[1]}".format(
            address=address))

        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == '__main__':
    main()
