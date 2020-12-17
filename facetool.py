import os
import sample.dir_tools as dir_tool
import sample.recognition as recog
import sample.images as imgs
import sys
from time import sleep
import face_recognition
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
    print("\n")
    print("Run 'help' for more information on commands or 'exit' to exit.")


def execute_option(parameters, image_set, recog_system, dir_nav):
    #
    # exit func.
    if parameters[0] == "exit":
        os.system('clear')
        sys.exit()
    #
    # clears screen
    elif parameters[0] == "clear":
        os.system('clear')
        display_title()
        display_instructions()
    #
    # prints instructions
    elif parameters[0] == "help":
        print("\tBRIEF GUIDE")
        print("\n")
        print("\n")
        print("cd \t\t\t change directory (relative), next arg being foldername")
        print("\n")
        print("exit \t\t\t exits command line tool")
        print("\n")
        print("clear \t\t\t clears cli")
        print("\n")
        print("collect_images \t\t loads images located in current working directory")
        print("\n")
        print("load_images \t\t loads images, next arg being the target directory")
        print("\n")
        print("tag_dir \t\t sets the current working directory as the destination directory")
        print("\n")
        print("analyse_images \t\t classifies the images, and displays labelled images if '-show' flag is included")
        print("\n")
        print("file_images \t\t saves files to classified groups at tagged destination directory")
        print("\n")
        print("file_images_here \t saves files to classified groups, next arg being the destination directory")

    #
    # navigate around
    elif parameters[0] == "cd":
        if os.path.exists(parameters[1]):
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
        else:
            print("Error: dir does not exist")
            print("\n")
    #
    # collects images from working directory
    elif parameters[0] == "collect_images":
        dir_nav.set_target_directory(dir_nav.get_working_directory())
        dir_nav.collect_images()
        print("Loading images from " + dir_nav.get_target_directory())
        for path in dir_nav.get_image_collection():
            print(path)
            image_set.add_image(face_recognition.api.load_image_file(path, mode='RGB'))
        print("\n")
    # collects images from a given target directory
    elif parameters[0] == "load_images":
        # parameters[1] is the target dir
        dir_nav.set_target_directory(parameters[1])
        dir_nav.collect_images()
        print("Loading images from " + dir_nav.get_target_directory())
        for path in dir_nav.get_image_collection():
            print(path)
            image_set.add_image(face_recognition.api.load_image_file(path, mode='RGB'))
        print("\n")
    # mark directory as destination for saved files
    elif parameters[0] == "tag_dir":
        dir_nav.set_destination_directory(os.getcwd())
        print(os.getcwd() + " tagged as destination")
        print("\n")
    # classifies images to groups
    # printing unique list of groups
    # if arg appended with -show, displays labelled image of face
    elif parameters[0] == "analyse_images":
        opencv_images = []
        count = 1
        image_cv = recog_system.add_first_person(image_set.get_image(0))
        opencv_images.append(image_cv)

        for image in image_set.get_image_collection()[1:]:
            opencv_images.append(recog_system.add_person(image))


        print("Groupings: ")
        for group in recog_system.get_unique_list():
            print(group)
        print("\n")

        if len(parameters) == 2 and parameters[1] == "-show":
            for opencv_image in opencv_images:
                cv.imshow(f"image {count}", opencv_image)
                count += 1
                cv.waitKey()
                cv.destroyAllWindows()
    # saves images to tagged directory
    # creating folder for images to be grouped to
    # BUG: smurfifies some images??
    elif parameters[0] == "file_images":
        image_set.save_faces(dir_nav.get_destination_directory(), recog_system.get_unique_list(), recog_system.get_labelled_list())
    # saves files to the the directory location provided as the second cmd line arg
    # creating folder for images to be grouped to
    elif parameters[0] == "file_images_here":
        image_set.save_faces(parameters[1], recog_system.get_unique_list(),
                             recog_system.get_labelled_list())
    # exit command
    else:
        print("command not recognised...")
        print("please try again...")
        display_instructions()
    # nest steps incl. mapping landmarks to heatmap for analysing the most important classification features
    # TODO: GROUP HEATMAP
    # TODO: normalise facial landmarks
    # TODO: create blank heatmap NxN of face
    # TODO: map landmarks onto heatmap grid
    # TODO: get an average of each landmark point
    # TODO: set colours by smallest euclidean distance being darkest, as most similar
    # TODO: make heatmap transparent
    # TODO: overlay scraped face with heatmap


if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
