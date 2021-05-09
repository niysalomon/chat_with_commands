#!/usr/bin/env python3
import socket
import sys
import pickle
"""This the import for th CLI args module"""
import arguments


class Client:
    """Class for client side"""
    def __init__(self):
        """initial function for Option class"""
        self.var = ""

    @staticmethod
    def client_side(host, packet_size):
        """Function for client side"""
        header_size = 10
        print("\nWelcome to Chat Room\n")
        client_socket = socket.socket()
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 9000
        client_socket.connect((host, port))
        print("Connected...\n")
        id_rec1 = 1
        msg_protocol= "PY"
        msg_type = "REQUEST"
        input_message = input(str("Me Outside : "))
        message_format = f"{msg_protocol}|{id_rec1}|{msg_type}| {input_message}"
        user_input = pickle.dumps(message_format)
        user_input = bytes(f"{len(user_input ):<{header_size}}", 'utf-8') + user_input
        client_socket.send(user_input)
        full_msg = b''
        new_msg = True

        while True:
            msg_rcv = client_socket.recv(packet_size)
            if new_msg:
                msg_len = int(msg_rcv[:header_size])
                new_msg = False
            full_msg += msg_rcv
            if len(full_msg) - header_size == msg_len:
                final_msg = pickle.loads(full_msg[header_size:])
                print("Full message received:")
                print("Server : ", final_msg)
                new_msg = True
                full_msg = b""
                packet_items = final_msg.split('|')
                prev_packet_id = packet_items[1]
                next_packet_id = int(prev_packet_id)
                next_packet_id = next_packet_id + 1
                input_message = input(str("Me Inside: "))
                message_format = f"{msg_protocol}|{next_packet_id}|{msg_type}| {input_message}"
                user_input = pickle.dumps(message_format)
                user_input = bytes(f"{len(user_input ):<{header_size}}", 'utf-8') + user_input
                client_socket.send(user_input)


if __name__ == "__main__":
    VAR = arguments.Option()
    ARGUMENT = VAR.arguments_list()
    VAR.arguments_option(ARGUMENT)
    if ARGUMENT.packet is None:
        Client.client_side(ARGUMENT.hostname, 1024)
    else:
        Client.client_side(ARGUMENT.hostname, ARGUMENT.packet)
        sys.exit(0)
