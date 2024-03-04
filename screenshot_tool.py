from PIL import ImageGrab, Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import keyboard

class ScreenshotTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.4)  # Set transparency for selection box
        self.root.attributes('-fullscreen', True)
        self.root.withdraw()  # Hide the window initially
        self.root.bind("<ButtonPress-1>", self.on_button_press)
        self.root.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<ButtonRelease-1>", self.on_button_release)
        self.rect_id = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.capture_key = 's'  # Shortcut key to trigger capture
        self.exit_key = 'q'  # Shortcut key to exit

    def take_screenshot(self):
        # Check if coordinates are properly set
        if None in [self.start_x, self.start_y, self.end_x, self.end_y]:
            self.root.deiconify()
            messagebox.showerror("Error", "Please select an area to capture.")
            self.root.withdraw()
            return

        # Take screenshot of the selected region
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Create a preview window
        self.show_preview(screenshot)

    def show_preview(self, screenshot):
        # Create a preview window
        preview_window = tk.Toplevel()
        preview_window.title("Screenshot Preview")

        # Calculate the size of the preview image
        width, height = screenshot.size
        if width > 800 or height > 600:
            screenshot.thumbnail((800, 600))

        # Convert PIL image to Tkinter PhotoImage
        photo = ImageTk.PhotoImage(screenshot)

        # Display the screenshot in the preview window
        canvas = tk.Canvas(preview_window, width=width, height=height)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.pack()

        # Callback function for save button
        def save_screenshot():
            # Prompt user for save location
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                      filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

            if save_path:
                screenshot.save(save_path)
                messagebox.showinfo("Screenshot", f"Screenshot saved as: {save_path}")
                preview_window.destroy()
                self.root.withdraw()

        # Save button to save the screenshot
        save_button = tk.Button(preview_window, text="Save", command=save_screenshot)
        save_button.pack()

        # Callback function for discard button
        def discard_screenshot():
            preview_window.destroy()
            self.root.withdraw()

        # Discard button to discard the screenshot
        discard_button = tk.Button(preview_window, text="Discard", command=discard_screenshot)
        discard_button.pack()

        # Run the Tkinter event loop
        preview_window.mainloop()

    def on_button_press(self, event):
        # Save starting coordinates
        self.start_x = event.x
        self.start_y = event.y

        # Create rectangle
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        # Update rectangle as mouse is dragged
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        # Take screenshot and show prompt
        self.take_screenshot()

    def run(self):
        keyboard.add_hotkey(self.capture_key, self.show_window)
        keyboard.add_hotkey(self.exit_key, self.exit_app)
        self.root.mainloop()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)

    def exit_app(self):
        self.root.withdraw()

if __name__ == "__main__":
    screenshot_tool = ScreenshotTool()
    
    # Define the shortcut key for capturing ('s' by default)
    capture_key = screenshot_tool.capture_key
    print(f"Press '{capture_key}' to capture a screenshot.")
    
    # Define the shortcut key for exiting ('q' by default)
    exit_key = screenshot_tool.exit_key
    print(f"Press '{exit_key}' to exit the application.")
    
    screenshot_tool.run()
