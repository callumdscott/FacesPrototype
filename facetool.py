from PIL import Image
from time import sleep
import os
import cv2
import random
from shutil import copy2
import os.path
from os import path
import sys
import numpy as np
from skimage.measure import compare_ssim as ssim
from sample.user import User as settings

# global settings
user = settings(os.path.join(os.path.dirname(__file__), 'data', 'raw'), 3)
commands_list = ["exit", "set_cd", "get_cd", "collect_images"]

def main():
    option = ""
    while option != "exit":
        os.system('clear')
        display_title()
        display_instructions()
        option = input().split()
        if option is not None:
            execute_option(option)

def display_title():
    print("\t**********************************************")
    print("\t********  Facial Recogniser Prototype ********")
    print("\t**********************************************")

def display_instructions():
    # TODO: UPDATE INSTRUCTIONS
    print("\n")
    print("Run 'help' for more information on commands or 'exit' to exit.")

def execute_option(parameters):
    choice = parameters[0]
    if choice in commands_list:
        if choice == "set_cd":
            user.set_directory(parameters[1])
        elif choice == "get_cd":
            print(user.get_directory())
        elif choice == "collect_images":
            user.collect_images()
            print(user.get_dir_contents())
        else:
            os.system('clear')
            sys.exit()
    else:
        print(f"Input Error: {0}".format(parameters))
        raise Exception("That is not a valid command")


if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
