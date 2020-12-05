import os
import numpy as np
import os.path
from os import path

class User():
    def __init__(self, directory, num_of_groups):
        self.directory = directory
        self.group_num = num_of_groups
        self.image_collection = []
        self.primary_image_target = np.zeros((100, 100, 3), np.uint8)
        self.secondary_image_target = np.zeros((100, 100, 3), np.uint8)
        self.comparison_heatmap = []

    def set_directory(self, directory):
        self.directory = directory

    def get_directory(self):
        return self.directory

    def set_group_num(self, num_of_groups):
        self.group_num = num_of_groups

    def get_group_num(self):
        return self.group_num

    def collect_images(self):
        self.image_collection = os.listdir(self.directory)

    def get_dir_contents(self):
        return self.image_collection

    def set_primary_image(self, image):
        self.primary_image_target = image

    def get_primary_image(self):
        return self.primary_image_target

    def set_secondary_image(self, image):
        self.secondary_image_target = image

    def get_secondary_image(self):
        return self.secondary_image_target

    def set_heatmap(self, heatmap):
        self.comparison_heatmap = heatmap

    def get_heatmap(self):
        return self.comparison_heatmap

    def show_heatmap(self):
        # TODO: display plot
        pass