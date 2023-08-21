# Import required modules
import cv2
import numpy as np
import os
import glob

class CameraDistortionCorrection:
    def __init__(self):
        self.camera_matrix = None
        self.distortion_coefficients = None
        self.CHECKERBOARD = (6, 6)
        self.calibration_images = None

    def get_calibration_images(self):
        pass

    def get_images_from_video(self, interval):
        pass

    def update_checkerboard_dimensions(self, x, y):
        pass

    def get_camera_matrix_and_distortion_coefficients(self):
        pass
        