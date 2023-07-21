import tkinter as tk
import tkinter.filedialog
from tkinter import Toplevel
from tkinter.ttk import Style, Button, Label, Checkbutton
import cv2
from PIL import Image, ImageTk
import forceplate_data_analyser as fda

class VideoPlayerGUI:
    def __init__(self, root):

        self.root = tk.Frame(root)
        self.video_path = None
        self.txt_file_path = None
        self.video_capture = None
        self.paused = False
        self.canvas = None
        self.image_widget = None
        self.coordinates_list = []
        self.origin_oval_id = None
        self.target_oval_id = None
        self.data_analyser = None
        self.camera_view = tk.IntVar(value=0)
        self.timestamp = None
        self.external_moment = None
        self.origin_coordinate = None
        self.target_coordinate = None
        self.f_magnitude = None
        self.f_angle = None
        self.perp_distance = None

        # Create the necessary GUI elements
        self.create_widgets()

    def create_widgets(self):
     
        # Create a custom style for the interface
        style = Style()
        style.theme_use('clam')  # Use the 'clam' theme as a base

        # Configure the colors for the dark theme
        style.configure('.', foreground='white', background='#2d2d2d')  # Set text and background color for all elements
        style.configure('TButton', foreground='white', background='#444444', bordercolor='#666666',
                        lightcolor='#444444', darkcolor='#444444')  # Customize Button widget
        style.configure('TLabel', foreground='white', background='#2d2d2d')  # Customize Label widget
        style.configure('TCheckbutton', foreground='white', background='#2d2d2d', indicatorcolor='white',
                        selectcolor='#2d2d2d', troughcolor='#2d2d2d')  # Customize Checkbutton widget

        # Override hover behavior for Checkbutton
        style.map('TCheckbutton',
                  background=[('active', '#2d2d2d'), ('selected', '#2d2d2d')],
                  foreground=[('active', 'white'), ('selected', 'white')])


        self.root.grid(row=0, column=0, padx=10, pady=10)
        self.root.configure(background='#2d2d2d')
        

        # Create the Open Video button
        self.open_button = Button(self.root, text="Open Video", command=self.open_video, style='TButton')
        self.open_button.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=5, pady=2)

        # Create the Pause button
        self.pause_button = Button(self.root, text="Pause", command=self.toggle_pause, style='TButton')
        self.pause_button.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=2)

        #Create Frame, Timestamp, Forward and Backwards Buttons
        nested_frame = tk.Frame(self.root, bg='#2d2d2d')
        nested_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=0, pady=0)

        self.frame_label = Label(nested_frame, text="Frame: ", style='TLabel')
        self.frame_label.grid(row=0, column=2, columnspan=1, padx=5, pady=2)

        self.timestamp_label = Label(nested_frame, text="Timestamp: ", style='TLabel')
        self.timestamp_label.grid(row=0, column=3, columnspan=1, sticky='nsew', padx=15, pady=2)

        self.forward_button = Button(nested_frame, text="Forward", command=self.move_forward, style='TButton')
        self.forward_button.grid(row=0, column=1, columnspan=1, sticky='nsew', padx=15, pady=2)
        self.forward_button.config(state=tk.DISABLED)

        self.backward_button = Button(nested_frame, text="Backward", command=self.move_backward, style='TButton')
        self.backward_button.grid(row=0, column=0, columnspan=1, sticky='nsew', padx=5, pady=2)
        self.backward_button.config(state=tk.DISABLED)

        # Create the canvas for displaying the video frames
        self.canvas = tk.Canvas(self.root,  width=1280, height=720, bg='black')
        self.canvas.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=5, pady=2)

        # Create the listbox for displaying the coordinates
        self.coordinates_listbox = tk.Listbox(self.root, width=35, background='#444444', foreground='white')
        self.coordinates_listbox.grid(row=2, column=2, columnspan=2, sticky='nsew', padx=5, pady=2)

        # Create the Remove button
        self.remove_button = Button(self.root, text="Remove", command=self.remove_coordinates, style='TButton')
        self.remove_button.grid(row=4, column=2, columnspan=2, sticky='nsew', padx=5, pady=2)

        # Create the Origin button
        self.origin_button = Button(self.root, text="Origin", command=self.set_origin, style='TButton')
        self.origin_button.grid(row=3, column=2, columnspan=1, sticky='nsew', padx=5, pady=2)

        # Create the Target button
        self.target_button = Button(self.root, text="Target", command=self.set_target, style='TButton')
        self.target_button.grid(row=3, column=3, columnspan=1, sticky='nsew', padx=5, pady=2)


        self.coronal_check = Checkbutton(self.root, text='Coronal', variable=self.camera_view, onvalue=1,
                                    command=lambda: self.set_camera_view(1), style='TCheckbutton')#, foreground='white', background='#2d2d2d')
        self.coronal_check.grid(row=1, column=0, columnspan=1, padx=5, pady=2)

        self.sagittal_check = Checkbutton(self.root, text='Sagittal', variable=self.camera_view, onvalue=2,
                                    command=lambda: self.set_camera_view(2), style='TCheckbutton')#, foreground='white', background='#2d2d2d')
        self.sagittal_check.grid(row=1, column=1, columnspan=1, padx=5, pady=2)

        # Create a button to open the calibrate window
        self.calibrate_button = tk.Button(self.root, text="Calibration", command=self.open_calibration_window, bg='#2d2d2d', foreground='grey', relief=tk.FLAT)
        self.calibrate_button.grid(row=1, column=3, columnspan=1, sticky='nsew', padx=5, pady=2)

        self.calculate_button = Button(self.root, text="Calculate", command=self.calculate, style='TButton')
        self.calculate_button.grid(row=5, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        self.calculate_button.config(state=tk.DISABLED)


        # Bind mouse click events to the canvas
        self.canvas.bind("<Button-1>", self.handle_click)

        # Bind the events for changing the mouse cursor
        list_of_buttons = [self.open_button, self.pause_button, self.remove_button, self.origin_button, 
                           self.target_button, self.calculate_button, self.coronal_check, self.sagittal_check,
                           self.calibrate_button, self.forward_button, self.backward_button]
        for button in list_of_buttons:
            button.bind('<Enter>', self.handle_enter)
            button.bind('<Leave>', self.handle_leave)

    def open_video(self):
        self.canvas.delete('all')  # Clear the canvas
        self.reset_coordinates()

        # Open a file dialog to select the MP4 video file
        video_file_path  = tk.filedialog.askopenfilename(filetypes=[("AVI files", "*.avi"),("MP4 files", "*.mp4")])

        if video_file_path:
            self.video_path = video_file_path

            # Prompt the user to select a TXT file
            txt_file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            

            if txt_file_path:
                self.txt_file_path = txt_file_path
            # Initialize video capture object
            self.video_capture = cv2.VideoCapture(self.video_path)

            # Start playing the video
            self.play_video()

    def play_video(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()

            if ret:
                # Convert the OpenCV BGR image to PIL Image
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Resize the image to fit the canvas
                image = image.resize((1280, 720))

                # Create an ImageTk object from the PIL Image
                self.image_widget = ImageTk.PhotoImage(image)

                # Update the canvas image
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_widget)

                # Get the current frame number
                frame_number = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))

                # Get the current timestamp
                timestamp = self.video_capture.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

                if self.paused:
                    # Update the frame number label
                    self.frame_label.config(text=f"Frame: {frame_number}")

                    # Update the timestamp label
                    self.timestamp_label.config(text=f"Timestamp: {timestamp:.2f}")

                    self.timestamp = timestamp
                else:
                    # Reset the coordinates list when the video is played
                    self.reset_coordinates()

        if not self.paused:
            self.root.after(20, self.play_video)

    def move_forward(self):
        if self.video_capture is not None:
            self.reset_coordinates()
            # Move the video forward by one frame
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            # Play the video from the new frame
            self.play_video()

    def move_backward(self):
        if self.video_capture is not None:
            self.reset_coordinates()
            # Get the current frame number
            current_frame = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            # Move the video backward by one frame (if possible)
            new_frame = max(0, current_frame - 2)  # Subtract 2 to go back by one frame and account for the next frame in play_video
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            # Play the video from the new frame
            self.play_video()


    def handle_click(self, event):
        if self.image_widget:
            # Draw a red dot at the clicked coordinates
            oval_id = self.canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill="red")

            # Add the coordinates and oval ID to the list
            self.coordinates_list.append((event.x, event.y, oval_id))

            # Update the coordinates listbox
            self.update_coordinates_listbox()

        if not self.paused:
            self.toggle_pause()

    def update_coordinates_listbox(self):
        # Clear the listbox
        self.coordinates_listbox.delete(0, tk.END)

        # Add the coordinates to the listbox
        for coord in self.coordinates_list:
            if coord[2] == self.target_oval_id:
                self.coordinates_listbox.insert(tk.END, f"X: {coord[0]}, Y: {coord[1]} (Target)")
                self.target_coordinate = [coord[0], coord[1]]
            elif coord[2] == self.origin_oval_id:
                self.coordinates_listbox.insert(tk.END, f"X: {coord[0]}, Y: {coord[1]} (Origin)")
                self.origin_coordinate = [coord[0], coord[1]]
            else:
                self.coordinates_listbox.insert(tk.END, f"X: {coord[0]}, Y: {coord[1]}")

        if self.f_magnitude:
            self.coordinates_listbox.insert(tk.END, f"Force vector magnitude: {self.f_magnitude} N")

        if self.f_angle:
            self.coordinates_listbox.insert(tk.END, f"Force vector angle to horz: {self.f_angle} deg")

        if self.perp_distance:
            self.coordinates_listbox.insert(tk.END, f"Perpendicular distance: {self.perp_distance} pixels")

        if self.external_moment:
            self.coordinates_listbox.insert(tk.END, f"External joint moment: {self.external_moment} Npixles")

    def remove_coordinates(self):
        # Get the selected index from the listbox
        selected_index = self.coordinates_listbox.curselection()

        if selected_index:
            # Retrieve the corresponding coordinates and oval ID
            selected_index = selected_index[0]
            coord = self.coordinates_list[selected_index]
            oval_id = coord[2]

            # Remove the oval from the canvas
            self.canvas.delete(oval_id)

            # Remove the coordinates from the list
            self.coordinates_list.pop(selected_index)

            # Update the coordinates listbox
            self.update_coordinates_listbox()

    def reset_coordinates(self):
        # Clear the coordinates list
        self.coordinates_list = []
        self.origin_oval_id = None
        self.target_oval_id = None
        self.external_moment = None
        self.f_magnitude = None
        self.f_angle = None
        self.perp_distance = None
        # Update the coordinates listbox
        self.update_coordinates_listbox()

    def set_origin(self):
        # Get the selected index from the listbox
        selected_index = self.coordinates_listbox.curselection()

        if selected_index:
            # Retrieve the corresponding oval ID
            selected_index = selected_index[0]
            oval_id = self.coordinates_list[selected_index][2]

            # Remove the highlight from the previous origin
            if self.origin_oval_id:
                self.canvas.itemconfig(self.origin_oval_id, fill="red")

            # Update the origin oval ID and change its color to blue
            if self.origin_oval_id != oval_id:
                # Change the color of the newly selected origin oval to blue
                self.canvas.itemconfig(oval_id, fill="blue")
                self.origin_oval_id = oval_id
                self.update_calculate_button_state()  # Update the Calculate button state

            else:
                # If the same origin is selected, reset the origin ID
                self.origin_oval_id = None
            self.update_coordinates_listbox()

    def set_target(self):
        # Get the selected index from the listbox
        selected_index = self.coordinates_listbox.curselection()

        if selected_index:
            # Retrieve the corresponding oval ID
            selected_index = selected_index[0]
            oval_id = self.coordinates_list[selected_index][2]

            # Remove the highlight from the previous origin
            if self.target_oval_id:
                self.canvas.itemconfig(self.target_oval_id, fill="red")

            # Update the origin oval ID and change its color to green
            if self.target_oval_id != oval_id:
                # Change the color of the newly selected target oval to green
                self.canvas.itemconfig(oval_id, fill="green")
                self.target_oval_id = oval_id
                self.update_calculate_button_state()  # Update the Calculate button state
            else:
                # If the same target is selected, reset the origin ID
                self.target_oval_id = None
            self.update_coordinates_listbox()

    def set_camera_view(self, option):
        self.camera_view.set(option)
        #print(self.camera_view.get())

        self.update_calculate_button_state()

    def update_calculate_button_state(self):
        # Enable the Calculate button if an origin and target oval are selected and the video is paused
        if self.origin_oval_id and self.target_oval_id and self.paused and self.camera_view.get() != 0 and self.video_path and self.txt_file_path:
            self.calculate_button.config(state=tk.NORMAL)
        else:
           self.calculate_button.config(state=tk.DISABLED)

    def update_frame_forwards_backwards_button_states(self):
        if self.paused == True:
            self.forward_button.config(state=tk.NORMAL)
            self.backward_button.config(state=tk.NORMAL)
        else:
            self.forward_button.config(state=tk.DISABLED)
            self.backward_button.config(state=tk.DISABLED)

    def toggle_pause(self):
        self.paused = not self.paused
        # Update the Pause button text
        if self.paused:
            self.pause_button.config(text="Play")
            self.update_frame_forwards_backwards_button_states()
        else:
            self.pause_button.config(text="Pause")
            self.update_frame_forwards_backwards_button_states()
            self.play_video()

        self.update_calculate_button_state()  # Update the Calculate button state

    def calculate(self):
        da = fda.ForcePlateDataAnalyser(self.txt_file_path, self.timestamp, self.camera_view.get(),
                                        self.origin_coordinate, self.target_coordinate)
        
        self.f_magnitude, self.f_angle, force_vector_tip_coorindate = da.get_force_vector_information()
        self.canvas.create_line(self.origin_coordinate[0], self.origin_coordinate[1],
                                force_vector_tip_coorindate[0], force_vector_tip_coorindate[1], 
                                smooth=True, width=3, fill='yellow')

        #work out the perpendicular distance from target to line
        #calculate external moment
        self.external_moment, target_to_vector_tip_coordinate, self.perp_distance = da.get_external_moment_information() #x_distance, y_distance, angle)
        self.update_coordinates_listbox()
        self.canvas.create_line(self.target_coordinate[0], self.target_coordinate[1],
                                target_to_vector_tip_coordinate[0], target_to_vector_tip_coordinate[1], 
                                smooth=True, width=2, fill='white')

    def handle_enter(self, event):
        event.widget.configure(cursor='hand2')

    def handle_leave(self, event):
        event.widget.configure(cursor='')

    def run(self):
        self.root.mainloop()


################################## Calibration Window #########################################

    def open_calibration_window(self):
        # Create a new Toplevel window (secondary window)
        calibration_window = Toplevel(self.root)
        calibration_window.title("Calibration Window")

        # Add widgets to the secondary window
        label = tk.Label(calibration_window, text="This is the secondary window.")
        label.pack()

# Create the main Tkinter window
root = tk.Tk()

# Set the window title
root.title("Video Player GUI")
root.configure(bg='#2d2d2d')

# Create an instance of the VideoPlayerGUI class
gui = VideoPlayerGUI(root)

# Run the GUI
gui.run()
