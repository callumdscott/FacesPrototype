import os
import sample.dir_tools as dir_tool
import sample.recognition as recog
import sample.images as imgs
import sys
from time import sleep
import cv2 as cv


def main():
    print('\033c')
    print('\x1bc')
    images = imgs.ImageCollection()
    recogniser = recog.Recogniser()
    navigator = dir_tool.Manager(os.getcwd())

    option = ""
    display_title()
    display_instructions()
    while option != "exit":
        option = input(">> ").split()
        if option is not None:
            execute_option(option, images, recogniser, navigator)


def display_title():
    print("\t**********************************************")
    print("\t********  Facial Recogniser Prototype ********")
    print("\t**********************************************")
    print("\n")


def display_instructions():
    # TODO: UPDATE INSTRUCTIONS
    print("\n")
    print("Run 'help' for more information on commands or 'exit' to exit.")


def execute_option(parameters, image_set, recog_system, dir_nav):
    # exit func.
    if parameters[0] == "exit":
        os.system('clear')
        sys.exit()
    # navigate around directories
    elif parameters[0] == "cd":
        # going to parent dir
        if parameters[1] == "..":
            os.chdir('../')
            dir_nav.set_working_directory(os.getcwd())
            print(os.getcwd())
        # going to child dir
        else:
            os.chdir(os.path.join(os.path.join(os.getcwd(), parameters[1])))
            dir_nav.set_working_directory(os.getcwd())
            print(os.getcwd())
        print("\n")
    # collects images from working directory
    elif parameters[0] == "collect_images":
        dir_nav.set_target_directory(dir_nav.get_working_directory())
        dir_nav.collect_images()
        print("Loading images from " + dir_nav.get_target_directory())
        for path in dir_nav.get_image_collection():
            print(path)
            image_set.add_image(cv.imread(path))
        print("\n")
    # collects images from a given target directory
    elif parameters[0] == "load_images":
        # parameters[1] is the target dir
        dir_nav.set_target_directory(parameters[1])
        dir_nav.collect_images()
        print("Loading images from " + dir_nav.get_target_directory())
        for path in dir_nav.get_image_collection():
            print(path)
            image_set.add_image(cv.imread(path))
        print("\n")
    # mark directory as destination for saved files
    elif parameters[0] == "tag_dir":
        dir_nav.set_destination_directory(os.getcwd())
        print(os.getcwd() + " tagged as destination")
        print("\n")
    #
    elif parameters[0] == "analyse_images":
        image_set.scrape_faces()
        image_set.standardize_size()
        image_set.save_faces(dir_nav.get_destination_directory())
        recog_system.add_first_person(image_set.get_image(0))
        for image in image_set.get_image_collection()[1:]:
            recog_system.add_person(image)
        group_list = recog_system.get_labelled_list()
        print("Groupings: ")
        print("\n")
        for person in group_list:
            print(person)
        print("\n")
    elif parameters[0] == "group_images":
        # parameters[1] is the destination dir
        pass
    else:
        os.system('clear')
        sys.exit()


if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
