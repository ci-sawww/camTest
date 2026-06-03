import sys
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
#comment for test push

class CameraApp:
    def __init__(self, root):
        # Set up the tkinter window
        self.root = root
        self.root.title("Camera App with Controls")
        self.root.geometry("700x650")
        
        # Flag to control the camera loop
        self.running = True
        self.cam = None
        self.current_frame = None
        
        # Create a frame for the video display
        self.video_label = tk.Label(root, bg="black")
        self.video_label.pack(pady=10)
        
        # Create a frame for buttons at the bottom
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Create a "Capture Frame" button that saves the current frame
        self.button_capture = tk.Button(
            button_frame, 
            text="Capture Frame", 
            command=self.capture_frame, 
            width=15, 
            height=2
        )
        self.button_capture.pack(side=tk.LEFT, padx=5)
        
        # Create a "Cycle Mode" button for custom functionality
        self.button_cycle = tk.Button(
            button_frame, 
            text="Cycle Mode", 
            command=self.cycle_mode, 
            width=15, 
            height=2
        )
        self.button_cycle.pack(side=tk.LEFT, padx=5)
        
        # Create an "Exit" button to close the application
        self.button_exit = tk.Button(
            button_frame, 
            text="Exit", 
            command=self.exit_app, 
            width=15, 
            height=2
        )
        self.button_exit.pack(side=tk.LEFT, padx=5)
        
        # Create a status label to show current status
        self.status_label = tk.Label(root, text="Camera: Starting...", fg="blue")
        self.status_label.pack(pady=5)
        
        # Start the camera in a separate thread so the UI remains responsive
        self.camera_thread = threading.Thread(target=self.run_camera, daemon=True)
        self.camera_thread.start()
        
        # Handle window close button (X)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def run_camera(self):
        """
        Run the OpenCV camera feed and update the tkinter window.
        This runs in a separate thread to keep the UI responsive.
        """
        # Open the default webcam (device 0)
        self.cam = cv2.VideoCapture(0)
        
        # Check if the camera opened successfully
        if not self.cam.isOpened():
            messagebox.showerror("Error", "Cannot open camera. Make sure your webcam is connected.")
            self.running = False
            self.root.quit()
            return
        
        # Update the status label
        self.status_label.config(text="Camera: Running", fg="green")
        
        # Main camera loop - runs until user clicks exit or closes window
        while self.running:
            # Read a frame from the webcam
            ret, frame = self.cam.read()
            if not ret or frame is None:
                print("Failed to capture frame from camera.")
                break
            
            # Store the current frame for the capture button
            self.current_frame = frame
            
            # Resize frame to fit nicely in the window
            frame_resized = cv2.resize(frame, (640, 480))
            
            # Convert BGR (OpenCV format) to RGB (PIL format)
            rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to a PIL Image
            pil_image = Image.fromarray(rgb_frame)
            
            # Convert PIL Image to tkinter PhotoImage
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Update the label with the new frame
            self.video_label.config(image=tk_image)
            self.video_label.image = tk_image  # Keep a reference to prevent garbage collection
            
            # Allow the tkinter event loop to process events (button clicks, etc.)
            self.root.update()
        
        # Clean up camera resources
        if self.cam:
            self.cam.release()

    def capture_frame(self):
        """
        Capture and save the current frame from the camera.
        This is called when the "Capture Frame" button is clicked.
        """
        if self.current_frame is not None:
            # Save the frame as a PNG image
            cv2.imwrite("captured_image.png", self.current_frame)
            messagebox.showinfo("Success", "Frame saved as captured_image.png")
            self.status_label.config(text="Status: Frame captured", fg="green")
        else:
            messagebox.showerror("Error", "No frame available to capture")

    def cycle_mode(self):
        """
        Handle the "Cycle Mode" button press.
        This is called when the "Cycle Mode" button is clicked.
        """
        messagebox.showinfo("Cycle Mode", "Cycle button pressed. You can add custom functionality here.")
        self.status_label.config(text="Status: Cycle mode activated", fg="blue")

    def exit_app(self):
        """
        Exit the application cleanly.
        Stops the camera loop and closes all windows.
        """
        self.running = False
        self.root.quit()


def main():
    """
    Main function that sets up the application.
    Creates a single tkinter window with camera feed and buttons.
    """
    # Create the main tkinter window
    root = tk.Tk()
    
    # Create the application instance
    app = CameraApp(root)
    
    # Run the tkinter event loop (keeps the window responsive)
    root.mainloop()


if __name__ == "__main__":
    main()