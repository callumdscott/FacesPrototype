from PIL import Image
from time import sleep
import os
import cv2

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, 'data', 'raw')
commands_list = ["exit", "random_sort", "show_image", "classify", "classify_and_sort", "scrape_faces"]

# Deliverables
# split faces to 5 x 5 grid
# classify images to groups
# compare images using split for similarity ranking
# display results to command line

# 1. load images from file and save faces [x]
# 2. randomly group images on command line
# 3. classify images to groups on cmd line
# 4. display confidence rating for images in group
# 5. label blocks with similarity scores

def set_directory(directory_path):
    filepath = directory_path

def get_dir_contents():
    files = os.listdir(filepath)
    return files

def main():
    option = ""
    while option != "exit":
        display_title()
        display_instructions()
        option = input()
        if option is not None:
            execute_option(option)


def display_title():
    os.system('clear')
    print("\t**********************************************")
    print("\t********  Facial Recogniser Prototype ********")
    print("\t**********************************************")


def display_instructions():
    print("\n[")
    print("Run 'help' for more information on commands or 'exit' to exit.")



def execute_option(parameters):

    #############################################
    if isinstance(parameters, str):
        choice = parameters
    else:
        choice = parameters[0]
    #############################################

    if choice in commands_list:
        if choice == "show_image":
            image = Image.open(os.path.join(filepath, get_dir_contents()[0]))
            image.show()
            # TODO: display image referenced at index 0
        if choice == "classify":
            parameters[1]
            # TODO: group images in folder referenced at index 0
        if choice == "classify_and_sort":
            parameters[1]
            # TODO: group images in folder referenced at index 0

        if choice == "scrape_faces":

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            x = 0
            for file in get_dir_contents():
                image_path = os.path.join(filepath, file)
                img = cv2.imread(image_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

                for (x, y, w, h) in face:
                    im = Image.open(image_path)
                    im = im.crop((x, y, x + w, y + h))

                x += 1
                filename = f"face{x}.jpg"
                print(filename)
                im.save(os.path.join(filepath, "..", "scraped_faces", filename), "JPEG")

        if choice == "random_sort":
            pass
            # TODO: random basic sort

    else:
        print(f"Input Error: {0}".format(parameters))
        raise Exception("That is not a valid command")


if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
