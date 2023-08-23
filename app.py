import tkinter as tk
import scrpts.video_player_gui as vpg

def run():
    # Create the main Tkinter window
    root = tk.Tk()

    # Set the window title
    root.title("Video Player GUI")
    root.configure(bg='#2d2d2d')

    # Create an instance of the VideoPlayerGUI class
    gui = vpg.VideoPlayerGUI(root)

    # Run the GUI
    gui.run()

if __name__ == '__main__':

    exit(run())