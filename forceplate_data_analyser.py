import pandas as pd
import numpy as np
import math

class ForcePlateDataAnalyser:
    def __init__(self, txt_file_path, timestamp, camera_view, origin_coordinate, target_coordinate):
        self.txt_file_path = txt_file_path
        self.timestamp = timestamp
        self.force_data = None
        self.camera_view = camera_view
        self.f_angle = 0
        self.scaling_factor = 0 
        self.max_force = None
        self.f_magnitude = None
        self.origin_coordinate = origin_coordinate
        self.target_coordinate = target_coordinate
        self.force_vector_tip_coorindate = None
        self.target_to_vector_tip_coordinate = None
        self.max_force_vector_length = 400 #pixels
        self.external_moment = None
        self.f_to_target_perpendicular_distance = None
        
        self.load_data()
        self.get_maximum_force_magnitude()

    def load_data(self):
        # Load the data from the TXT file using pandas
        data = pd.read_csv(self.txt_file_path, delimiter='\t', header=(0), dtype='float32')
        data['ts'] = np.arange(0,data.shape[0])/1000
        # Extract the force and moment data
        force_data = data[['ts','fx', 'fy', 'fz']]

        # Downsample force data so that it aligns better with the video data
        # Tried this and it didn't work that well
        downsampling_ratio = 1000 // 50  # 1000Hz to 50Hz
        downsampled_force_data = force_data.groupby(force_data.index // downsampling_ratio).last()

        self.force_data = force_data

    def get_maximum_force_magnitude(self):
        if self.force_data is not None:
            normalised_force = np.linalg.norm(self.force_data[['fx', 'fy', 'fz']].values, axis=1)
            self.max_force = np.max(normalised_force)

    def get_force_vector_information(self):
        self.calculate_force_magnitude_and_direction()
        self.calculate_scaling_factor()
        self.calculate_force_vector_tip_coordinate()

        return_angle = np.round(np.rad2deg(self.f_angle), decimals=2)
        if return_angle < 0:
            return_angle += 180

        return np.round(self.f_magnitude, decimals=2), return_angle, self.force_vector_tip_coorindate

    def calculate_force_magnitude_and_direction(self):
        if self.force_data is not None:
            closest_index = np.abs(self.force_data['ts'] - self.timestamp).idxmin()
            if self.camera_view == 1: #Coronal
                fx = self.force_data.loc[closest_index, 'fx']
                fz = self.force_data.loc[closest_index, 'fz']
                self.f_magnitude = ((fx**2) + (fz**2))**0.5
                self.f_angle = -1 * math.atan(fz / fx) #self.calculate_angle_from_force(fx, fz)
                #self.scaling_factor = self.calculate_scaling_factor(fx, fz)
                
                #print(f"Coronal Force Data: Fy={fy}, Fz={fz}")
            elif self.camera_view == 2: #Sagittal
                fy = self.force_data.loc[closest_index, 'fy']
                fz = self.force_data.loc[closest_index, 'fz']
                self.f_magnitude = ((fy**2) + (fz**2))**0.5
                self.f_angle = math.atan(fz / fy) #self.calculate_angle_from_force(fy, fz)
                #self.scaling_factor = self.calculate_scaling_factor(fy, fz)
                #print(f"Sagittal Force Data: Fx={fx}, Fz={fz}")
            else:
                print("Invalid option selected.")
        else:
            print("Force data not loaded.")

    def calculate_scaling_factor(self):
        self.scaling_factor = self.f_magnitude/self.max_force

    def calculate_force_vector_tip_coordinate(self):
        x = self.max_force_vector_length * self.scaling_factor * math.cos(self.f_angle)
        y = self.max_force_vector_length * self.scaling_factor * math.sin(self.f_angle)
        if self.f_angle < 0:
            x = x * -1
        else:
            y = y * -1
        
        x = x + self.origin_coordinate[0]
        y = y + self.origin_coordinate[1]
        self.force_vector_tip_coorindate = [x, y]

    def get_external_moment_information(self):
        self.get_distance_between_force_vector_and_target()
        
        self.external_moment = self.f_magnitude * self.f_to_target_perpendicular_distance
        self.get_target_to_vector_tip_coordinate()
        
        return np.abs(np.round(self.external_moment, decimals=2)), self.target_to_vector_tip_coordinate, np.abs(np.round(self.f_to_target_perpendicular_distance, decimals=2))

    def get_distance_between_force_vector_and_target(self):
        # angle is still the angle of the force vector - need to be careful because of the silly refernce frame templo has created
        x = self.target_coordinate[0] - self.origin_coordinate[0]
        y = self.origin_coordinate[1] - self.target_coordinate[1]

        x = self.pixles_to_mm(x, 'x')
        y = self.pixles_to_mm(y, 'y')

        p = ((x**2) + (y**2))**0.5
        theta = np.arctan(x/y)
        beta = (np.pi/2) - self.f_angle - theta

        self.f_to_target_perpendicular_distance = p * np.sin(beta)

    def pixles_to_mm(self, distance, direction):
        return distance
    
    def get_target_to_vector_tip_coordinate(self):
        
        x = self.target_coordinate[0] - self.origin_coordinate[0]
        y = self.origin_coordinate[1] - self.target_coordinate[1]

        x = self.origin_coordinate[0] + (x + (self.f_to_target_perpendicular_distance * np.sin(self.f_angle)))
        y = self.origin_coordinate[1] - (y - (self.f_to_target_perpendicular_distance * np.cos(self.f_angle)))
        
        self.target_to_vector_tip_coordinate = [x, y]


