#!/usr/bin/env python3
import socket
import pickle
"""This is the module for CLI args"""
import arguments


class Option:
    """A Class which contain main function on the server"""
    def __init__(self):
        """initial function for Option class"""
        self.var = ""

    @staticmethod
    def server(host, packet_size):
        """Function for server side"""
        header_size = 10
        print("\nWelcome to Chat Room\n")
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        port = 9000
        server_socket.bind((host, port))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        msg_protocol = "PY"
        msg_type = "RESPONSE"

        full_msg = b''
        new_msg = True
        while True:
            msg_rcv = conn.recv(packet_size)
            if new_msg:
                msg_len = int(msg_rcv[:header_size])
                new_msg = False

            full_msg += msg_rcv

            if len(full_msg)-header_size == msg_len:
                final_msg = pickle.loads(full_msg[header_size:])
                print("Full message received:")
                print("Client :", final_msg)
                new_msg = True
                full_msg = b""

                packet_items = final_msg.split('|')
                prev_packet_id = packet_items[1]
                next_packet_id = int(prev_packet_id)

                input_message = input(str("Me : "))
                message_format = f"{msg_protocol}|{next_packet_id}|{msg_type}| {input_message}"
                user_input = pickle.dumps(message_format)
                user_input = bytes(f"{len(user_input):<{header_size}}", 'utf-8') + user_input
                conn.send(user_input)


if __name__ == "__main__":
    VAR = arguments.Option()
    ARGUMENT = VAR.arguments_list()
    VAR.arguments_option(ARGUMENT)
    if ARGUMENT.packet is not None:
        Option.server(ARGUMENT.hostname, ARGUMENT.packet)
