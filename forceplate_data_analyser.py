import pandas as pd
import numpy as np
import math

class ForcePlateDataAnalyser:
    def __init__(self, txt_file_path):
        self.txt_file_path = txt_file_path
        self.timestamp = None
        self.force_data = None
        self.camera_view = None
        self.angle = 0
        self.max_force = None
        
    def load_data(self):
        # Load the data from the TXT file using pandas
        data = pd.read_csv(self.txt_file_path, delimiter='\t', header=(0), dtype='float32')
        data['ts'] = np.arange(0,data.shape[0])/1000
        # Extract the force and moment data
        force_data = data[['ts','fx', 'fy', 'fz']]
        
        self.force_data = force_data
        self.get_maximum_force_magnitude()

    def process_force_data_at_timestamp(self, timestamp, camera_view):
        if self.force_data is not None:
            closest_index = np.abs(self.force_data['ts'] - timestamp).idxmin()
            if camera_view == 1: #Coronal
                fx = self.force_data.loc[closest_index, 'fx']
                fz = self.force_data.loc[closest_index, 'fz']
                return self.calculate_angle_from_force(fx, fz), self.calculate_scaling_factor(fx, fz)
                
                #print(f"Coronal Force Data: Fy={fy}, Fz={fz}")
            elif camera_view == 2: #Sagittal
                fy = self.force_data.loc[closest_index, 'fy']
                fz = self.force_data.loc[closest_index, 'fz']
                return self.calculate_angle_from_force(fy, fz), self.calculate_scaling_factor(fy, fz)
                #print(f"Sagittal Force Data: Fx={fx}, Fz={fz}")
            else:
                print("Invalid option selected.")
        else:
            print("Force data not loaded.")

    def get_maximum_force_magnitude(self):
        if self.force_data is not None:
            normalised_force = np.linalg.norm(self.force_data[['fx', 'fy', 'fz']].values, axis=1)
            self.max_force = np.max(normalised_force)

    def calculate_angle_from_force(self, fhorz, fz):
        # Calculate the angle from the force components
        # Replace this with your actual angle calculation logic
        angle = math.atan(fz / fhorz)  # Calculate the angle in radians
        print(math.degrees(angle))  # Convert the angle to degrees
        return angle
    
    def calculate_scaling_factor(self, fhorz, fz):
        return np.linalg.norm([fhorz, fz])/self.max_force
    
    def calcuate_x_and_y(self, angle, scaling_factor, max_pixel_length):
        #need to correct for the negative angles
        x = max_pixel_length * scaling_factor * math.cos(angle)
        y = max_pixel_length * scaling_factor * math.sin(angle)
        return x, y


