import face_recognition
import cv2 as cv


def name_generator():
    name = "group "
    num = 1
    while True:
        yield name + str(num)
        num += 1

class Recogniser():

    def __init__(self):
        self.known_encodings = []
        self.known_faces = []
        self.labelled_faces = []
        self.generate = name_generator()
        self.unique_list = []

    def add_first_person(self, image):
        image_cv = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        landmarks = face_recognition.face_landmarks(image)
        locations = face_recognition.face_locations(image)
        encoding = face_recognition.api.face_encodings(image, known_face_locations=locations, num_jitters=100, model='large')[0]
        self.known_encodings.append(encoding)
        name = next(self.generate)
        self.known_faces.append(name)
        self.labelled_faces.append(name)
        self.unique_list.append(name)

        top_left = (locations[0][3], locations[0][0])
        bottom_right = (locations[0][1], locations[0][2])
        colour = [0, 255, 0]
        cv.rectangle(image_cv, top_left, bottom_right, colour, 2)

        top_left = (locations[0][3], locations[0][2])
        bottom_right = (locations[0][1], locations[0][2] + 22)
        cv.rectangle(image_cv, top_left, bottom_right, colour, cv.FILLED)
        text_location = (locations[0][3] + 10, locations[0][2] + 15)
        font_colour = (255, 255, 255)
        cv.putText(image_cv, name, text_location, cv.FONT_HERSHEY_SIMPLEX, 0.5, font_colour, 1)

        return image_cv

    def add_person(self, image):
        image = image
        image_cv = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        landmarks = face_recognition.face_landmarks(image)
        locations = face_recognition.face_locations(image)
        encoding = face_recognition.api.face_encodings(image, known_face_locations=locations, num_jitters=100, model='large')[0]

        name = ""
        match = face_recognition.compare_faces(self.known_encodings, encoding)

        if True in match:
            name_index = match.index(True)
            name = self.known_faces[name_index]
            self.labelled_faces.append(name)
        else:
            name = next(self.generate)
            self.known_encodings.append(encoding)
            self.known_faces.append(name)
            self.labelled_faces.append(name)
            self.unique_list.append(name)

        top_left = (locations[0][3], locations[0][0])
        bottom_right = (locations[0][1], locations[0][2])
        colour = [0, 255, 0]
        cv.rectangle(image_cv, top_left, bottom_right, colour, 2)

        top_left = (locations[0][3], locations[0][2])
        bottom_right = (locations[0][1], locations[0][2] + 22)
        cv.rectangle(image_cv, top_left, bottom_right, colour, cv.FILLED)
        text_location = (locations[0][3] + 10, locations[0][2] + 15)
        font_colour = (255, 255, 255)
        cv.putText(image_cv, name, text_location, cv.FONT_HERSHEY_SIMPLEX, 0.5, font_colour, 1)

        return image_cv

    def print_landmarks(self, image):
        face_landmarks_list = face_recognition.face_landmarks(image)
        for face_landmarks in face_landmarks_list:
            for facial_feature in face_landmarks.keys():
                print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))


    def get_labelled_list(self):
        return self.labelled_faces

    def get_unique_list(self):
        return self.unique_list