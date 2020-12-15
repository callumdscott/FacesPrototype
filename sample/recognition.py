import face_recognition
import numpy as np


def name_generator():
    name = "face "
    num = 1
    while True:
        yield name + str(num)
        num += 1

class Recogniser():

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.labelled_faces = []
        self.generate = name_generator()

    def add_first_person(self, image):
        image = image[:, :, ::-1]
        name = next(self.generate)
        face_locations = face_recognition.face_locations(image)
        self.known_face_encodings.append(face_recognition.face_encodings(image, face_locations)[0])
        self.known_face_names.append(name)
        self.labelled_faces.append(name)

    def add_person(self, image):
        image = image[:, :, ::-1]
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)[0]
        #self.count += 1
        same_face =[]
        # TODO: FIX BROKEN COMPARISON
        for face_encoding in face_encodings:
            same_face = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            print(same_face)
        if True in same_face:
            print("found a match!!!!!!")
            index = same_face.index(True)
            self.labelled_faces.append(self.known_face_names[index])
        else:
            print("no match")
            name = next(self.generate)
            self.known_face_encodings.append(face_encodings)
            self.known_face_names.append(name)
            self.labelled_faces.append(name)


    def get_labelled_list(self):
        return self.labelled_faces

