from email import message
from logging import root
from sqlite3 import connect
import tkinter as tk
import socket
import threading
from tkinter import scrolledtext
from tkinter import font
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

DARK_GREY = '#749E9F'
MEDIUM_GREY = '#B8D8D8'
WHITE = "white"
OCEAN_BLUE = '#4F6367'
FONT = ('Helvetica', 17)
BUTTON_FONT = ('Helvetica', 15)
SMALL_FONT = ('Helvetica', 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server {HOST} and port {PORT}".format(
            HOST=HOST, PORT=PORT))
        add_message("Successfully connected to server")
    except:
        messagebox.showerror("Unable to connect to server", "Unable to connect to host {HOST} and port {PORT}".format(
            HOST=HOST, PORT=PORT))

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode('utf-8'))
    else:
        messagebox.showerror("Invalid Username", "Username cannot be empty")
    threading.Thread(target=listen_for_messages, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode('utf-8'))
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


root = tk.Tk()
root.geometry("600x600")
root.title("Chat Room")
root.resizable(0, 0)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(
    top_frame, text="Enter username: ", bg=DARK_GREY, fg=WHITE, font=FONT)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(
    top_frame, width=23, bg=MEDIUM_GREY, fg=WHITE, font=FONT)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT,
                            bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT,
                           width=38, bg=MEDIUM_GREY, fg=WHITE)
message_textbox.pack(side=tk.LEFT, padx=10)
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT,
                           bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(
    middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split(':')[0]
            content = message.split(':')[1]

            add_message("{username}: {content}".format(
                username=username, content=content))
        else:
            messagebox.showerror("Error", "The message from client is empty")


def main():

    root.mainloop()


if __name__ == '__main__':
    main()
