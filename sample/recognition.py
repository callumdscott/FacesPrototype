import face_recognition
import numpy as np


class Recogniser():

    def __init__(self):
        self.count = 0
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_encodings = []
        self.labelled_faces = []

    def add_first_person(self, image):
        self.count = 1
        image = image[:, :, ::-1]
        self.known_face_encodings.append(face_recognition.face_encodings(image)[0])
        self.known_face_names.append("face 1")
        self.labelled_faces.append("face 1")

    def add_person(self, image):
        image = image[:, :, ::-1]
        self.face_locations = face_recognition.face_locations(image)
        self.face_encodings = face_recognition.face_encodings(image, self.face_locations)[0]

        for face_encoding in self.face_encodings:
            self.count = len(self.known_face_encodings) + 1
            name = ""
            same_face = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

            if True in same_face:
                match_index = same_face.index(True)
                name = self.known_face_encodings[match_index]
            else:
                name = "face " + str(self.count)
                self.known_face_encodings.append(self.face_encodings)
                self.known_face_names.append(name)

        self.labelled_faces.append(name)

    def get_labelled_list(self):
        return self.labelled_faces
