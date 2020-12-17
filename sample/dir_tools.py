import os
import os.path


class Manager:

    def __init__(self, working_dir):
        self.target_dir = working_dir
        self.destination_dir = working_dir
        self.working_dir = working_dir
        self.image_collection = []

    def set_target_directory(self, directory):
        self.target_dir = directory

    def get_target_directory(self):
        return self.target_dir

    def set_destination_directory(self, directory):
        self.destination_dir = directory

    def get_destination_directory(self):
        return self.destination_dir

    def set_working_directory(self, directory):
        self.working_dir = directory

    def get_working_directory(self):
        return self.working_dir

    def collect_images(self):
        self.image_collection.clear()
        dir_content = os.listdir(self.target_dir)
        for item in dir_content:
            if item.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.image_collection.append(os.path.join(self.target_dir, item))

    def get_image_collection(self):
        return self.image_collection

    def set_image_collection(self, image_collection):
        self.image_collection = image_collection