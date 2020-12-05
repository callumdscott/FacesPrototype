import os
from os import path
import sys
from time import sleep
import cv2 as cv

destination_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\output"
target_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\raw"

def main():
    option = ""
    display_title()
    display_instructions()
    while option != "exit":
        option = input(">> ").split()
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
    destination_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\output"
    target_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\raw"

    if parameters[0] == "exit":
            os.system('clear')
            sys.exit()
    elif parameters[0] == "set_destination_dir":
        if not (path.exists(parameters[1])):
            os.makedirs(parameters[1])
            os.chmod(parameters[1], 0o777)
        destination_dir = parameters[1]
    elif parameters[0] == "set_target_dir":
        if not (path.exists(parameters[1])):
            os.makedirs(parameters[1])
            os.chmod(parameters[1], 0o777)
        target_dir = parameters[1]
    elif parameters[0] == "cd":
        # going to parent dir
        if parameters[1] == "..":
            os.chdir('../')
            print(os.getcwd())
        # going to child dir
        else:
            os.chdir(os.path.join(os.path.join(os.getcwd(), parameters[1])))
            print(os.getcwd())
    elif parameters[0] == "ls":
        # list contects of folder
        for item in os.listdir(os.getcwd()):
            print(item)
        print()
    elif parameters[0] == "make_groups":
        total_groups = parameters[1]
        for i in range(1, (int(total_groups) + 1)):
            if not (path.exists(os.path.join(destination_dir, "groups", ("group" + str(i))))):
                os.makedirs(os.path.join(destination_dir, "..", "groups", ("group" + str(i))))
                os.chmod(os.path.join(destination_dir, "..", "groups", ("group" + str(i))), 0o777)
    elif parameters[0] == "scrape_face":
        img = cv.imread(os.path.join(target_dir, parameters[1]))
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # load pre-trained classifier for face detection
        face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # run face detector on greyscaled image
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
        # crop images for faces
        for (x, y, w, h) in face:
            im = img[y:(y + h), x:(x + w)]
        if not (path.exists(os.path.join(destination_dir, "scraped"))):
            os.makedirs(os.path.join(destination_dir, "scraped"))
            os.chmod(os.path.join(destination_dir, "scraped"), 0o777)
        final_image = cv.resize(im, (100, 100), interpolation=cv.INTER_AREA)
        cv.imwrite(os.path.join(destination_dir, "scraped", parameters[1]), final_image)
    elif parameters[0] == "scrape_faces":
        if len(parameters) > 1:
            image_list = os.listdir(parameters[1])
        else:
            image_list = os.listdir(os.getcwd())
        for image in image_list:
            img = cv.imread(os.path.join(target_dir, image))
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # load pre-trained classifier for face detection
            face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
            # run face detector on greyscaled image
            face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
            # crop images for faces
            for (x, y, w, h) in face:
                im = img[y:(y + h), x:(x + w)]
            if not (path.exists(os.path.join(destination_dir, "scraped"))):
                os.makedirs(os.path.join(destination_dir, "scraped"))
                os.chmod(os.path.join(destination_dir, "scraped"), 0o777)
            final_image = cv.resize(im, (100, 100), interpolation=cv.INTER_AREA)
            cv.imwrite(os.path.join(destination_dir, "scraped", image), final_image)

    else:
        os.chdir(parameters[0])
        print(os.getcwd())

if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
