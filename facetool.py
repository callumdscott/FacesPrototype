import os
from os import path
import sys
from time import sleep
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim
import dlib

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


def mse(img_a, img_b):
    m_sq_err = (np.sum((img_a.astype("float") - img_b.astype("float")) ** 2)) / (float(img_a.shape[0] * img_a.shape[1]))
    return m_sq_err

def blur_image(image, blur_level):
    img = cv.GaussianBlur(image, (blur_level[0], blur_level[1]), 0)
    return img


def detect_edges(image, thresholds):
    img = cv.Canny(image, thresholds[0], thresholds[1])
    return img


def dilate_edges(image, kernal_size, iterations=1):
    kernel = np.ones((kernal_size[0], kernal_size[1]), np.uint8)
    img = cv.dilate(image, kernel, iterations)
    return img


def erode_edges(image, kernal_size, iterations=1):
    kernel = np.ones((kernal_size[0], kernal_size[1]), np.uint8)
    img = cv.erode(image, kernel, iterations)
    return img


def execute_option(parameters):
    destination_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\output"
    target_dir = "C:\\Projects\\FinalProject\\FacesPrototype\\data\\raw"
    face_list = []
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
        im = cv.resize(im, (100, 100), interpolation=cv.INTER_AREA)
        cv.imwrite(os.path.join(destination_dir, "scraped", parameters[1]), im)
    elif parameters[0] == "scrape_faces":
        if len(parameters) > 1:
            image_list = os.listdir(parameters[1])
        else:
            image_list = os.listdir(os.getcwd())
        for image in image_list:
            img = cv.imread(os.path.join(target_dir, image))
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
            face = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)
            for (x, y, w, h) in face:
                im = img[y:(y + h), x:(x + w)]
            if not (path.exists(os.path.join(destination_dir, "scraped"))):
                os.makedirs(os.path.join(destination_dir, "scraped"))
                os.chmod(os.path.join(destination_dir, "scraped"), 0o777)
            face_list.append(os.path.join(destination_dir, "scraped", image))
            cv.imwrite(os.path.join(destination_dir, "scraped", image), im)
        smallest_face = 100
        for face in face_list:
            print(face)
            if (cv.imread(face).shape[0]) < smallest_face:
                smallest_face = (cv.imread(face)).shape[0]
        for face in face_list:
            im = cv.resize(cv.imread(face), (smallest_face, smallest_face), interpolation=cv.INTER_AREA)
            cv.imwrite(face, im)
    elif parameters[0] == "compare_face":
        image_list = os.listdir(os.path.join(destination_dir, "scraped"))
        for image in image_list:
            face_list.append(os.path.join(destination_dir, "scraped", image))
        print(face_list[0])
        # comparing two photos first
        compare_faces(face_list[1], face_list[:1] + face_list[2:])
    else:
        os.chdir(parameters[0])
        print(os.getcwd())

def compare_faces(face, face_list):
    img = cv.imread(face)
    # throwaway rest for now
    _ = face_list
    img_blur = blur_image(img, (3, 3))

    # greying images
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_grey = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)

    # edge threshold tester
    img_edge_2 = detect_edges(img_grey, (150, 200))
    img_edge_3 = detect_edges(img, (100, 200))
    img_edge_4 = detect_edges(img, (150, 200))

    # dilated threshhold tester
    img_dilated = dilate_edges(img_edge_2, (2, 2), iterations=1)
    img_dilated2 = dilate_edges(img_edge_3, (2, 2), iterations=1)
    img_dilated3 = dilate_edges(img_edge_4, (3, 3), iterations=1)

    # eroding tester
    img_erode = erode_edges(img_dilated, (2, 2), iterations=1)
    img_erode2 = erode_edges(img_dilated2, (2, 2), iterations=1)
    img_erode3 = erode_edges(img_dilated3, (2, 2), iterations=1)

    person_analysis = []
    for other_face in face_list:
        other_img = cv.imread(other_face)
        _ = face_list
        other_img_blur = blur_image(other_img, (3, 3))
        image_analysis = []
        # images to analyse
        other_img = cv.cvtColor(other_img, cv.COLOR_BGR2GRAY)
        other_img_grey = cv.cvtColor(other_img_blur, cv.COLOR_BGR2GRAY)
        other_img_edge_2 = detect_edges(other_img_grey, (150, 200))
        other_img_edge_3 = detect_edges(other_img, (100, 200))
        other_img_edge_4 = detect_edges(other_img, (150, 200))
        other_img_dilated = dilate_edges(other_img_edge_2, (2, 2), iterations=1)
        other_img_dilated2 = dilate_edges(other_img_edge_3, (2, 2), iterations=1)
        other_img_dilated3 = dilate_edges(other_img_edge_4, (3, 3), iterations=1)
        other_img_erode = erode_edges(other_img_dilated, (2, 2), iterations=1)
        other_img_erode2 = erode_edges(other_img_dilated2, (2, 2), iterations=1)
        other_img_erode3 = erode_edges(other_img_dilated3, (2, 2), iterations=1)

        # analysis
        image_analysis.append(compare_pairs(img, other_img, "Greyed out"))
        image_analysis.append(compare_pairs(img_grey, other_img_grey, "blurred Greyed out"))
        image_analysis.append(compare_pairs(img_edge_2, other_img_edge_2, "blurred Greyed out edge detection"))
        image_analysis.append(compare_pairs(img_edge_3, other_img_edge_3, "Greyed out out edge detection"))
        image_analysis.append(compare_pairs(img_edge_4, other_img_edge_4, "Greyed out out sensitive edge detection"))
        image_analysis.append(compare_pairs(img_dilated, other_img_dilated, "blurred Greyed out edge - dilate"))
        image_analysis.append(compare_pairs(img_dilated2, other_img_dilated2, "Greyed out edge - dilate"))
        image_analysis.append(compare_pairs(img_dilated3, other_img_dilated3, "Greyed out edge - high dilation"))
        image_analysis.append(compare_pairs(img_erode, other_img_erode, "blurred Greyed out eroded"))
        image_analysis.append(compare_pairs(img_erode2, other_img_erode2, "Greyed out edge - dilate eroded"))
        image_analysis.append(compare_pairs(img_erode3, other_img_erode3, "Greyed out edge - high dilation eroded"))

        person_analysis.append(image_analysis)
    for i, person in enumerate(person_analysis):
        print("Image " + str(i+2))
        for j in range(11):
            print("Image analysis " + str(j))

            print("MSE: " + str(person[j][0]))
            print("SSIM: " + str(person[j][1]))
            print()

    # plt.scatter(person_analysis[:][0][0], person_analysis[:][0][1])
    # plt.show()
    # #cv.imshow("eroded", img_erode)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


def compare_pairs(img, other_img, title):
    mean_sq_err = mse(img, other_img)
    sim_score = ssim(img, other_img)
    #fig = plt.figure(title)
    #plt.suptitle("MSE: %.2f, SSIM: %.2f" % (mean_sq_err, sim_score))
    #ax = fig.add_subplot(1, 2, 1)
    #plt.imshow(img, cmap=plt.cm.gray)
    #plt.axis("off")
    #ax = fig.add_subplot(1, 2, 2)
    #plt.imshow(other_img, cmap=plt.cm.gray)
    #plt.axis("off")
    #plt.show()
    return (mean_sq_err, sim_score)


if __name__ == '__main__':
    main()
    print("goodbye!")
    sleep(1)
