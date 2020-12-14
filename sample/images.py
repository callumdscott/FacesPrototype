import os
from os import path
import cv2 as cv

class ImageCollection:
    def __init__(self):
        self.raw_images = []
        self.face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def set_image_collection(self, image_list):
        self.raw_images = image_list

    def get_image_collection(self):
        return self.raw_images

    def add_image(self, image):
        self.raw_images.append(image)

    def clear(self):
        self.raw_images.clear()

    def get_image(self, i):
        return self.raw_images[i]

    def scrape_faces(self):
        images = []
        for image in self.get_image_collection():
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            equalized = cv.equalizeHist(gray)
            face = self.face_cascade.detectMultiScale(equalized, scaleFactor=1.5, minNeighbors=3)
            for (x, y, w, h) in face:
                images.append(image[y:(y + h), x:(x + w)])
                break
        self.clear()
        self.set_image_collection(images)

    def standardize_size(self):
        size = 1000
        images = []
        for image in self.raw_images:
            if image.shape[1] < size:
                size = image.shape[1]
        for image in self.raw_images:
            images.append(cv.resize(image, (size, size), interpolation=cv.INTER_AREA))
        self.clear()
        self.set_image_collection(images)

    def save_faces(self, dest):
        if not (path.exists(os.path.join(dest, "scraped"))):
            os.makedirs(os.path.join(dest, "scraped"))
            os.chmod(os.path.join(dest, "scraped"), 0o777)
        print("saving files in " + os.path.join(dest, "scraped"))
        for i, face in enumerate(self.raw_images):
            cv.imwrite(os.path.join(dest, "scraped", ("image" + str(i)) + ".jpg"), face)
