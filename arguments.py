#!/usr/bin/env python3
"""This is file for the commandline option"""
from argparse import ArgumentParser
import sys


class Option:
    """Class which contain all possible commandline options"""
    @staticmethod
    def arguments_option(option):
        """Function for the arguments options"""
        if option.hostname:
            print("you are using default localhost")
        if option.port:
            print("Connecting to the port")
        if option.packet <= 100:
            print("you are in the right packet size")
        # if option.run:
        #     print("Running the server")

        else:
            print("you have exceeded the packet size")
            sys.exit(0)

    @staticmethod
    def arguments_list():
        """Function for the list of the arguments options """
        parser = ArgumentParser()
        parser.add_argument("-p", "--port", type=int, default=8080, help="port")
        parser.add_argument("-host", "--hostname", default="localhost", required=True)
        parser.add_argument("-pck", "--packet", type=int, help="Add packet size", required=True)
        return parser.parse_args()
