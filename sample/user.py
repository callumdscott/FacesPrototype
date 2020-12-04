import os


class User():
    def __init__(self, directory, num_of_groups):
        self.directory = directory
        self.group_num = num_of_groups
        self.image_collection = []

        def set_directory(directory):
            self.directory = dir

        def get_directory():
            return self.directory

        def set_group_num(num_of_groups):
            self.group_num = num_of_groups

        def get_group_num():
            return self.group_num

        def collect_images():
            self.image_collection = os.listdir(self.directory)

        def get_dir_contents():
            return self.image_collection
