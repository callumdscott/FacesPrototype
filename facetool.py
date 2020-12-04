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

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, 'data', 'raw')
commands_list = ["exit", "random_sort", "show_image", "classify", "classify_and_sort", "scrape_faces", "compare_faces"]


# Deliverables
# classify images to groups

# 1. load images from file and save faces [x]
# 2. randomly group images on command line
# 3. classify images to groups on cmd line
# 4. display confidence rating for images in group
# 5. label blocks with similarity scores

def mse(image1, image2):
    # mean square error formula
    error = np.sum((image1.astype("float") - image2.astype("float")) ** 2) / (float(image1.shape[0] * image1[1]))
    return error


def set_directory(directory_path):
    filepath = directory_path


def get_dir_contents():
    files = os.listdir(filepath)
    return files


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


def grid_crop(image, n, m):
    h, w = image.shape[0:2]
    print(str(h) + " " + str(w))
    gridbox_height, gridbox_width = int(h / m), int(w / n)
    image_grid = []
    # nested for rows, inside columns
    for j in range(m):
        grid_row = []
        for i in range(n):
            left = i * gridbox_width
            right = (i + 1) * gridbox_width
            top = j * gridbox_height
            bottom = (j + 1) * gridbox_height
            # cropping boxes by row
            gridbox = image[left:right, top:bottom]
            grid_row.append(gridbox)
        image_grid.append(grid_row)
    return image_grid


def compare_box(this_box, that_box):
    similarity_score = ssim(this_box, that_box)
    return similarity_score


def compare_images(this_image_path, that_image_path, grid_size):
    this_image = cv2.imread(this_image_path)
    that_image = cv2.imread(that_image_path)
    # convert to greyscale
    this_image = cv2.cvtColor(this_image, cv2.COLOR_BGR2GRAY)
    that_image = cv2.cvtColor(that_image, cv2.COLOR_BGR2GRAY)
    # scrapes faces from image in opencv format
    this_image = scrape_face(this_image)
    that_image = scrape_face(that_image)
    # scale faces
    this_image = cv2.resize(this_image, (100, 100), interpolation=cv2.INTER_AREA)
    that_image = cv2.resize(that_image, (100, 100), interpolation=cv2.INTER_AREA)
    # split face into gridbox
    this_image_grid = grid_crop(that_image, grid_size, grid_size)
    that_image_grid = grid_crop(this_image, grid_size, grid_size)
    comparison_map = []
    # map comparisons to a n x n tensor for raw similarity and difference estimates

    for i in range(grid_size):
        comparison_row = []
        for j in range(grid_size):
            comparison_row.append(compare_box(this_image_grid[i][j], that_image_grid[i][j]))
        comparison_map.append(comparison_row)

    for i in range(grid_size):
        print("similarity scores:")
        for j in range(grid_size):
            print(comparison_map[i][j])
        print("\n")



def scrape_face(image):
    # load pre-trained classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # run face detector on greyscaled image
    face = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=3)

    # crop images for faces
    for (x, y, w, h) in face:
        image = image[y:y + h, x:x + w]
    return image


def scrape_faces():
    counter = 0
    # load pre-trained classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # run face detector on files
    for file in get_dir_contents():
        image_path = os.path.join(filepath, file)
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)

        # crop images for faces
        for (x, y, w, h) in face:
            im = Image.open(image_path)
            im = im.crop((x, y, (x + w), (y + h)))

        # save faces to folder "scraped faces"
        counter += 1
        filename = f"face{counter}.jpg"
        print(os.getcwd())
        im.save(os.path.join(filepath, "scraped_faces", filename), "JPEG")


def random_sort(total_groups):
    pics = os.listdir(filepath)
    # randomise list of images
    random.shuffle(pics)
    # folder creation
    for i in range(1, (int(total_groups) + 1)):
        if not (path.exists(os.path.join(filepath, "..", "groups", ("group" + str(i))))):
            os.makedirs(os.path.join(filepath, "..", "groups", ("group" + str(i))))
            os.chmod(os.path.join(filepath, "..", "groups", ("group" + str(i))), 0o777)
    # spread random ordered pics to files
    for i, pic in enumerate(pics):
        if (i + 1) % 3 == 1:
            copy2(os.path.join(filepath, pic), os.path.join(filepath, "..", "groups", "group1"))
        if (i + 1) % 3 == 2:
            copy2(os.path.join(filepath, pic), os.path.join(filepath, "..", "groups", "group2"))
        if (i + 1) % 3 == 0:
            copy2(os.path.join(filepath, pic), os.path.join(filepath, "..", "groups", "group3"))


def execute_option(parameters):
    choice = parameters[0]
    if choice in commands_list:
        if choice == "show_image":
            image = Image.open(os.path.join(filepath, get_dir_contents()[0]))
            image.show()
            # TODO: display image referenced at index 0
        elif choice == "classify":
            parameters[1]
            # TODO: group images in folder referenced at index 0
        elif choice == "classify_and_sort":
            parameters[1]
            # TODO: group images in folder referenced at index 0

        elif choice == "compare_faces":
            image1 = os.path.join(filepath, get_dir_contents()[3])
            image2 = os.path.join(filepath, get_dir_contents()[8])
            compare_images(image1, image2, 5)

        elif choice == "scrape_faces":
            scrape_faces()

        elif choice == "random_sort":
            # TODO: random basic sort
            random_sort(parameters[1])
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
