import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import traceback

from PIL import Image, ImageGrab, ImageTk
from game_bot.picture import capture_screen, extract_text
import numpy as np
import yaml

class ScreenshotPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Picker")
        self.root.geometry("1200x1000")
        self.root.configure(bg='#1e1e1e')
        self.config_filename = os.path.expanduser("~/.picker.yml")
        self.load_config()
        
        # Modern font settings
        self.font_normal = ('Segoe UI', 9)
        self.font_bold = ('Segoe UI', 9, 'bold')
        
        # Current image and selection
        self.current_image = None
        self.selection_start = None
        self.selection_rect = None
        self.rect_id = None
        self.points = []
        self.ctrl_pressed = False
        
        # Create UI elements
        self.create_widgets()

        # Keyboard bindings
        self.root.bind("<Control_L>", lambda e: self.set_ctrl_pressed(True))
        self.root.bind("<KeyRelease-Control_L>", lambda e: self.set_ctrl_pressed(False))
    
    def load_config(self):
        if os.path.exists(self.config_filename):
            with open(self.config_filename, 'r') as f:
                self.config = yaml.load(f, Loader=yaml.Loader)
        else:
            self.config = {
                'last_save_path': os.path.expanduser(os.path.join("~","Downloads"))
            }
            self.save_config()

    def save_config(self):
        with open(self.config_filename, 'w') as f:
            yaml.dump(self.config, f, Dumper = yaml.Dumper)

    def set_ctrl_pressed(self, pressed):
        self.ctrl_pressed = pressed
        if pressed:
            self.greenlight.config(fg="green")
        else:
            self.greenlight.config(fg="red")

    def create_widgets(self):
        # Main control frame with modern styling
        control_frame = tk.Frame(self.root, bg='#2d2d2d', padx=5, pady=5)
        control_frame.pack(fill=tk.X)
        button_frame = tk.Frame(control_frame, bg='#2d2d2d')
        button_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Button styling
        button_style = {
            'font': self.font_bold,
            'bg': '#4a6baf',
            'fg': 'white',
            'activebackground': '#3a5a9f',
            'borderwidth': 0,
            'padx': 10,
            'pady': 5
        }
        
        self.capture_btn = tk.Button(button_frame, text="Capture Screenshot", 
                                   command=self.capture_screenshot, **button_style)
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        self.load_btn = tk.Button(button_frame, text="Load Image", command=self.load_image, **button_style)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = tk.Button(button_frame, text="Save Image", command=self.save_image, **button_style)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Save path entry with Browse button
        path_frame = tk.Frame(button_frame, bg='#2d2d2d')
        path_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        self.save_path = tk.Entry(path_frame, bg='#3d3d3d', fg='#e0e0e0', insertbackground='white')
        self.save_path.insert(0, self.config["last_save_path"])
        self.save_path.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        browse_btn = tk.Button(path_frame, text="Browse...", 
                             command=self.browse_save_path, **button_style)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Second row - pixel info        
        # Modern label styling
        label_style = {
            'font': self.font_normal,
            'bg': '#2d2d2d',
            'fg': '#e0e0e0'
        }
        
        # First row - pixel info
        self.pixel_info = tk.Label(control_frame, text="", anchor=tk.W, **label_style)
        self.pixel_info.pack(fill=tk.X, expand=True)
        self.selected_info = tk.Label(control_frame, text="", anchor=tk.W, **label_style)
        self.selected_info.pack(fill=tk.X, expand=True)
        
        # Second row - info frame
        info_frame = tk.Frame(control_frame, bg='#2d2d2d')
        info_frame.pack(fill=tk.X, pady=(5,0), anchor=tk.W)
        self.greenlight = tk.Label(info_frame, text="●", fg="red")
        self.greenlight.pack(side=tk.LEFT)
        self.points_info = tk.Label(info_frame, text="Points: 0", anchor=tk.W, **label_style)
        self.points_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Add format selection dropdown
        self.format_var = tk.StringVar(value="default")
        self.format_menu = tk.OptionMenu(info_frame, self.format_var, "default")
        self.format_menu.config(bg='#3d3d3d', fg='#e0e0e0', activebackground='#4a6baf', highlightthickness=0)
        self.format_menu['menu'].config(bg='#3d3d3d', fg='#e0e0e0')
        self.format_menu.pack(side=tk.LEFT, padx=5)
        
        self.clear_points_btn = tk.Button(info_frame, text="Clear Points", command=self.clear_points, **button_style)
        self.copy_points_btn = tk.Button(info_frame, text="Copy Points", command=self.copy_points_to_clipboard, **button_style)
        self.clear_points_btn.pack(side=tk.LEFT, padx=5)
        self.copy_points_btn.pack(side=tk.LEFT, padx=5)

        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.root, bg='#1e1e1e', width=800, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add scrollbars
        xscroll = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        yscroll = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        # Event bindings
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Add zoom controls at bottom center
        self.scale_frame = tk.Frame(self.root, bg='#1e1e1e')
        self.scale_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        # Container frame for centered controls
        center_frame = tk.Frame(self.scale_frame, bg='#2d2d2d')
        center_frame.pack(expand=True)
        self.image_info = tk.Label(center_frame, text="", anchor=tk.CENTER, **label_style)
        self.image_info.pack(fill=tk.X, padx=5, pady=5)
        
        # Add minus button (now changes by 1%)
        self.minus_btn = tk.Button(center_frame, text="-", width=2, 
                                  command=lambda: self.adjust_zoom(-1), **button_style)
        self.minus_btn.pack(side=tk.LEFT)
        
        # Add zoom slider
        self.scale_slider = tk.Scale(
            center_frame,
            from_=50,
            to=1000,
            orient=tk.HORIZONTAL,
            command=self.on_scale_change,
            length=int(self.root.winfo_width() * 0.8),
            bg='#2d2d2d',
            fg='#e0e0e0',
            highlightthickness=0,
            troughcolor='#3d3d3d',
            activebackground='#3a5a9f'
        )
        self.root.bind('<Configure>', self.on_window_resize)
        self.scale_slider.set(100)
        self.scale_slider.pack(side=tk.LEFT, padx=5)
        
        # Add plus button (now changes by 1%)
        self.plus_btn = tk.Button(center_frame, text="+", width=2,
                                 command=lambda: self.adjust_zoom(1), **button_style)
        self.plus_btn.pack(side=tk.LEFT)

    def adjust_zoom(self, delta):
        """Adjust zoom level by specified delta (now in 1% increments)"""
        current = self.scale_slider.get()
        new_value = max(10, min(200, current + delta))
        self.scale_slider.set(new_value)
        self.on_scale_change(new_value)
        
    def on_window_resize(self, event):
        """Handle window resize event to adjust slider length"""
        if hasattr(self, 'scale_slider'):
            self.scale_slider.config(length=int(self.root.winfo_width() * 0.8))

    def on_scale_change(self, value):
        if not self.current_image:
            return
            
        scale_factor = float(value) / 100.0
        self.display_image(scale_factor)

    def display_image(self, scale_factor=1.0):
        if not self.current_image:
            return
            
        # Calculate memory requirements (4 bytes per pixel for RGBA)
        scaled_width = int(self.current_image.width * scale_factor)
        scaled_height = int(self.current_image.height * scale_factor)
        estimated_memory = scaled_width * scaled_height * 4 / (1024 * 1024)  # MB
        
        # Show warning if memory usage would be too high
        if estimated_memory > 500:  # 500MB threshold
            if not messagebox.askyesno("Memory Warning", f"Zooming would require {estimated_memory:.1f}MB of memory (max 500MB recommended). Continue anyway?"):
                return
            
        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate scaled dimensions
        width = int(self.current_image.width * scale_factor)
        height = int(self.current_image.height * scale_factor)
        
        # Store scale factor for coordinate mapping
        self.scale_factor = scale_factor
        
        # Resize image
        img = self.current_image.resize((width, height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)
        
        # Create image at 0,0
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        # Configure scroll region
        self.canvas.config(scrollregion=(0, 0, width, height))
        
        # Reset view to top-left
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

    def crop_selected(self):
        if not self.current_image or not self.selection_rect:
            return
        try:
            # Get canvas scroll position
            x_scroll = self.canvas.xview()[0] * self.current_image.width * self.scale_factor
            y_scroll = self.canvas.yview()[0] * self.current_image.height * self.scale_factor
            
            # Calculate selection coordinates (accounting for scale)
            x1 = min(self.selection_rect[0], self.selection_rect[2]) + x_scroll
            y1 = min(self.selection_rect[1], self.selection_rect[3]) + y_scroll
            x2 = max(self.selection_rect[0], self.selection_rect[2]) + x_scroll
            y2 = max(self.selection_rect[1], self.selection_rect[3]) + y_scroll
            
            # Map back to original image coordinates
            x1 = int(x1 / self.scale_factor)
            y1 = int(y1 / self.scale_factor)
            x2 = int(x2 / self.scale_factor)
            y2 = int(y2 / self.scale_factor)
            
            # Ensure coordinates are within bounds
            x1 = max(0, min(x1, self.current_image.width - 1))
            y1 = max(0, min(y1, self.current_image.height - 1))
            x2 = max(0, min(x2, self.current_image.width - 1))
            y2 = max(0, min(y2, self.current_image.height - 1))
            
            # Crop and display
            original_width = self.current_image.width
            original_height = self.current_image.height
            
            cropped = self.current_image.crop((x1, y1, x2, y2))
            
            return cropped, original_width, original_height, (x1, y1, x2, y2)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", str(e))
            return None, None, None, None
    
    def view_selection(self):
        if not self.current_image or not self.selection_rect:
            return
        
        try:
            cropped, original_width, original_height, rect = self.crop_selected()
            if cropped is None: return
            x1, y1, x2, y2 = rect
            self.current_image = cropped
            self.display_image()
            # Add debug info to verify calculations
            debug_info = (
                f"Original: {original_width}x{original_height}\n"
                f"Cropped: {cropped.width}x{cropped.height}\n"
                f"Selection: (x1={x1},y1={y1},x2={x2},y2={y2})"
            )
            self.image_info.config(text=debug_info)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", str(e))
    
    def ocr_selection(self):
        cropped, original_width, original_height, rect = self.crop_selected()
        if cropped is None: return
        ocr_result = extract_text(cropped)
        if ocr_result:
            self.selected_info.config(text=self.selected_info.cget('text') + f"| OCR Result: {ocr_result}")

    def on_press(self, event):
        # Update ctrl indicator
        if self.ctrl_pressed:
            self.greenlight.config(fg="green")
        else:
            self.greenlight.config(fg="red")
            
        if self.ctrl_pressed:
            # Get pixel color and position
            x, y = event.x, event.y
            img_width = self.current_image.width
            img_height = self.current_image.height
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            scale_x = img_width / canvas_width
            scale_y = img_height / canvas_height
            
            img_x = int(x * scale_x)
            img_y = int(y * scale_y)
            
            if 0 <= img_x < img_width and 0 <= img_y < img_height:
                pixel = self.current_image.getpixel((img_x, img_y))
                hex_color = "#{:02x}{:02x}{:02x}".format(*pixel[:3])
                
                if not self.points:
                    # First point - record as (0,0)
                    self.points.append((0, 0, hex_color))
                else:
                    # Subsequent points - relative to first point
                    first_x, first_y = self.points[0][0], self.points[0][1]
                    dx = img_x - first_x
                    dy = img_y - first_y
                    self.points.append((dx, dy, hex_color))
            # points_text = ",".join([f"({point[0]},{point[1]},{point[2]})" for point in self.points])
            points_text = self.format_points(self.format_var.get())
            self.points_info.config(text=f"Points: {points_text}")
            return
            
        # Original selection rectangle code
        self.selection_start = (event.x, event.y)
        self.selection_rect = [event.x, event.y, event.x, event.y]
        
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            
        self.rect_id = self.canvas.create_rectangle(
            *self.selection_rect, 
            outline="red", 
            width=2
        )
        
        # Get pixel color
        if self.current_image:
            x, y = event.x, event.y
            # Get scroll position
            x_scroll = self.canvas.xview()[0] * self.current_image.width * self.scale_factor
            y_scroll = self.canvas.yview()[0] * self.current_image.height * self.scale_factor
            
            # Calculate absolute image coordinates
            img_x = int((x + x_scroll) / self.scale_factor)
            img_y = int((y + y_scroll) / self.scale_factor)
            
            if 0 <= img_x < self.current_image.width and 0 <= img_y < self.current_image.height:
                pixel = self.current_image.getpixel((img_x, img_y))
                self.pixel_info.config(text=f"Position: ({img_x}, {img_y}), Color: RGB{pixel[:3]}")
    
    def on_motion(self, event):
        if self.selection_start and self.rect_id:
            self.selection_rect[2] = event.x
            self.selection_rect[3] = event.y
            self.canvas.coords(self.rect_id, *self.selection_rect)
            self.selected_info.config(text=f"Selected: {self.selection_rect}")
    
    def on_release(self, event):
        if not self.selection_start or not self.current_image:
            return
            
        # Only show menu if we have a valid selection (not just a click)
        if (abs(self.selection_rect[0] - self.selection_rect[2]) > 5 and 
            abs(self.selection_rect[1] - self.selection_rect[3]) > 5):
            # Show context menu
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Save selected to...", command=self.save_selection)
            menu.add_command(label="View selected", command=self.view_selection)
            menu.add_command(label="OCR selected", command=self.ocr_selection)
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        # Clean up
        self.selection_start = None

    def clear_points(self):
        self.points = []
        self.points_info.config(text="Points: 0")
    
    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def format_points(self, format_name="default"):
        """Format points according to the selected format"""
        if not self.points:
            return ""
            
        if format_name == "default":
            return ",".join([f"({point[0]},{point[1]},{point[2]})" for point in self.points])
        # Add more formats here in the future
        return ""
        
    def copy_points_to_clipboard(self):
        if not self.points:
            return
            
        points_text = self.format_points(self.format_var.get())
        self.copy_to_clipboard(points_text)

    def capture_screenshot(self):
        """Capture a screenshot and display it in the viewer."""
        try:
            self.current_image = capture_screen()
            self.scale_slider.set(100)  # Reset zoom to 100%
            self.display_image()
            self.image_info.config(text=f"Size: {self.current_image.width}x{self.current_image.height}")
            filename = f"{self.config['last_save_path']}/{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
            print(f"Saving screenshot to {filename}")
            self.current_image.save(filename)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_image(self):
        """Load an image from file and display it in the viewer."""
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
        if filename:
            try:
                self.current_image = Image.open(filename)
                self.display_image()
                self.image_info.config(text=f"File: {filename}, Size: {self.current_image.width}x{self.current_image.height}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_image(self):
        """Save the current image to file"""
        if not self.current_image:
            messagebox.showwarning("Warning", "No image to save")
            return
            
        save_path = self.save_path.get().strip() or "./"
        filename = filedialog.asksaveasfilename(
            initialdir=save_path,
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")],
            defaultextension=".png"
        )
        
        if filename:
            try:
                self.current_image.save(filename)
                self.image_info.config(text=f"Saved image to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_selection(self):
        if not self.current_image or not self.selection_rect:
            return
            
        save_path = self.save_path.get().strip() or "./"
        filename = filedialog.asksaveasfilename(
            initialdir=save_path,
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")],
            defaultextension=".png"
        )
        
        if filename:
            try:
                # Get canvas scroll position
                x_scroll = self.canvas.xview()[0] * self.current_image.width * self.scale_factor
                y_scroll = self.canvas.yview()[0] * self.current_image.height * self.scale_factor
                
                # Calculate selection coordinates (accounting for scale and scroll)
                x1 = min(self.selection_rect[0], self.selection_rect[2]) + x_scroll
                y1 = min(self.selection_rect[1], self.selection_rect[3]) + y_scroll
                x2 = max(self.selection_rect[0], self.selection_rect[2]) + x_scroll
                y2 = max(self.selection_rect[1], self.selection_rect[3]) + y_scroll
                
                # Map back to original image coordinates
                x1 = int(x1 / self.scale_factor)
                y1 = int(y1 / self.scale_factor)
                x2 = int(x2 / self.scale_factor)
                y2 = int(y2 / self.scale_factor)
                
                # Ensure coordinates are within bounds
                x1 = max(0, min(x1, self.current_image.width - 1))
                y1 = max(0, min(y1, self.current_image.height - 1))
                x2 = max(0, min(x2, self.current_image.width - 1))
                y2 = max(0, min(y2, self.current_image.height - 1))
                
                cropped = self.current_image.crop((x1, y1, x2, y2))
                cropped.save(filename)
                self.image_info.config(text=f"Saved selection to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def browse_save_path(self):
        """Open directory dialog to select save location"""
        path = filedialog.askdirectory(initialdir=self.save_path.get())
        if path:
            self.save_path.delete(0, tk.END)
            self.save_path.insert(0, path)
            self.config['last_save_path'] = path
            self.save_config()

def main():
    root = tk.Tk()
    app = ScreenshotPicker(root)
    root.mainloop()

if __name__ == "__main__":
    main()