import numpy as np

class ForcePlatePixelToMm:
    def __init__(self, calibration_parameters, camera_view):
        self.forceplate_length = None #mm
        self.calibration_parameters = calibration_parameters # dict format
        self.camera_view = camera_view
        self.midline_coordinates = []
        self.midline_length = None
        self.origin_point = None

    # the dimensions of the forceplate are hard coded. These were measured to be 595 x 400 mm.
    # choose which length to use based on camera direction
    def get_forceplate_length(self):
        if self.camera_view == 'sagittal':
            self.forceplate_length = 595 #mm
        elif self.camera_view == 'coronal':
            self.forceplate_length = 400 #mm

    def set_origin_coordinate(self, xy):
        self.origin_point = xy

    # get the coordinates of the end points of the midline of the forceplate for that camera direction.
    def get_midline_coordinates(self):
        self.midline_coordinates.append((np.array(self.calibration_parameters[self.camera_view]["top left"]) + np.array(self.calibration_parameters[self.camera_view]["bottom left"]))/2)
        self.midline_coordinates.append((np.array(self.calibration_parameters[self.camera_view]["top right"]) + np.array(self.calibration_parameters[self.camera_view]["bottom right"]))/2)

    # calculate the length of the midline - for now, the assumption is that CoP of the force vector is ~ in line with the mid-line (this could be changed later to use the origin point y coordinate)
    def calculate_midline_length(self):
        self.midline_length = np.linalg.norm(self.midline_coordinates[1]-self.midline_coordinates[0])

    # compare the length of midline to the actual length of the midline 
    def calculate_pixel_mm_ratio(self):
        self.get_forceplate_length()

        if self.origin_point:
            self.get_not_midline_coordinates()
        else:
            self.get_midline_coordinates()

        self.calculate_midline_length()

        return np.round(self.forceplate_length/self.midline_length, decimals=3)

    # calculate the midline if the mid line is not in the middle, but passes through the origin point        
    def get_not_midline_coordinates(self):
        # clearly define coordinates
        a = np.array(self.calibration_parameters[self.camera_view]["top left"])
        b = np.array(self.calibration_parameters[self.camera_view]["top right"])
        c = np.array(self.calibration_parameters[self.camera_view]["bottom left"])
        d = np.array(self.calibration_parameters[self.camera_view]["bottom right"])
        p = np.array(self.origin_point)

        # initiate weighting factor - this is always between 0 and 1
        w = 0.0
    
        # iterate until line passes the y coordinate of p is less than 0.5 pixels from the force vector origin y coordinate
        self.midline_coordinates = self.converge_on_origin_y(a, b, c, d, p, w)
        if not self.midline_coordinates:
            self.get_midline_coordinates()

    def converge_on_origin_y(self, a, b, c, d, p, w):
        xp = p[0]
        yp = p[1]

        k = c + (w * (a - c))
        x1 = k[0]
        y1 = k[1]

        k = d + (w * (b - d))
        x2 = k[0]
        y2 = k[1]

        y = (1/(x2 - x1)) * (xp*(y2 - y1) + ((x2*y1) - (x1*y2)))

        if (y - yp) < 0.5:
            return [np.array([x1, y1]),np.array([x2, y2])]
        elif w == 1:
            print('could not converge on a point')
            return None
        else:
            #print('iterating')
            return self.converge_on_origin_y(a, b, c, d, p, w + 0.02)
            