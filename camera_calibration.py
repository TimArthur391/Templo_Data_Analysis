import cv2
import 

class CameraCalibration:
    def __init__(self, image_path):
        # Create the main Tkinter window
        root = tk.Tk()

        # Set the window title
        root.title("Video Player GUI")
        root.configure(bg='#2d2d2d')

        # Create an instance of the VideoPlayerGUI class
        gui = VideoPlayerGUI(root)

        # Run the GUI
        gui.run()
        self.image_path = image_path


    def calibrate_pixels_to_distance(self, object_size_pixels, object_physical_size):
        # Load the image
        image = cv2.imread(self.image_path)

        # Calculate the conversion factor
        conversion_factor = object_physical_size / object_size_pixels

        # Example: Convert a distance in pixels to meters
        distance_pixels = 100
        distance_meters = distance_pixels * conversion_factor
        print(f"Distance in meters: {distance_meters} m")

        # Display the image with a line indicating the object's size
        image_with_line = image.copy()
        cv2.line(image_with_line, (0, 50), (object_size_pixels, 50), (0, 255, 0), 2)
        cv2.imshow("Image with Line", image_with_line)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Example usage

cc = CameraCalibration(''path)
cc.calibrate_pixels_to_distance('path/to/your/image.jpg', object_size_pixels=50, object_physical_size=10)
