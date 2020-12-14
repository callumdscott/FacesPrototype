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
        self.face_locations = face_recognition.face_locations(image)
        self.known_face_encodings.append(face_recognition.face_encodings(image, self.face_locations)[0])
        self.known_face_names.append("face 1")
        self.labelled_faces.append("face 1")

    def add_person(self, image):
        image = image[:, :, ::-1]
        self.face_locations = face_recognition.face_locations(image)
        self.face_encodings = face_recognition.face_encodings(image, self.face_locations)[0]
        self.count += 1
        # TODO: FIX BROKEN COMPARISON
        #for face_encoding in self.face_encodings:
        #    same_face = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

        #    if True in same_face:
        #        print("found a match!")
        #        match_index = same_face.index(True)
        #        name = self.known_face_names[match_index]
        #    else:
        #        print("no match found...")
        #        name = "face " + str(self.count)
        #        self.known_face_encodings.append(self.face_encodings)
        #        self.known_face_names.append(name)

        face_distances = face_recognition.face_distance(self.known_face_encodings, self.face_encodings)
        for i, face_distance in enumerate(face_distances):
            if face_distance < 0.6:
                print("found a match!")
                name = self.known_face_names[i]
            else:
                print("no match found...")
                name = "face " + str(self.count)
                self.known_face_encodings.append(self.face_encodings)
                self.known_face_names.append(name)
        self.labelled_faces.append(name)

    def get_labelled_list(self):
        return self.labelled_faces
