## 📄 Complete Code

### image_editor.py
```python
"""
Image Filtering and Transformation Tool
A Python application for basic image processing operations
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
import os

class ImageEditor:
    """
    Main Image Editor Class with GUI and Processing Functions
    """
    
    def __init__(self, root):
        """
        Initialize the Image Editor Application
        """
        self.root = root
        self.root.title("🎨 Image Filtering and Transformation Tool")
        self.root.geometry("1100x650")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)
        
        # Image variables
        self.original_image = None      # Original image (OpenCV format)
        self.current_image = None       # Current working image (OpenCV format)
        self.display_image = None       # Image for Tkinter display
        self.image_path = None          # Path to loaded image
        
        # Create UI components
        self.create_menu_bar()
        self.create_main_layout()
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def create_menu_bar(self):
        """Create menu bar with File and Help menus"""
        menubar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="📂 Open Image", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="💾 Save Image", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="📖 About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
    
    def create_main_layout(self):
        """Create the main application layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Panel - Controls
        self.create_control_panel(main_frame)
        
        # Right Panel - Image Display
        self.create_display_panel(main_frame)
        
        # Status Bar
        self.create_status_bar()
    
    def create_control_panel(self, parent):
        """Create control panel with buttons and sliders"""
        control_frame = tk.Frame(parent, bg="#2d2d3d", width=280, relief="flat", bd=2)
        control_frame.pack(side="left", fill="y", padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            control_frame, 
            text="🎨 IMAGE CONTROLS", 
            font=("Arial", 14, "bold"),
            bg="#2d2d3d", 
            fg="#ffffff"
        )
        title_label.pack(pady=15)
        
        # Separator
        self.add_separator(control_frame)
        
        # File Operations Section
        file_section = tk.LabelFrame(
            control_frame, 
            text="📁 File Operations", 
            font=("Arial", 10, "bold"),
            bg="#2d2d3d", 
            fg="#a6e3a1",
            relief="flat"
        )
        file_section.pack(fill="x", padx=10, pady=10)
        
        self.create_button(file_section, "📂 Open Image", self.open_image, "#89b4fa")
        self.create_button(file_section, "💾 Save Image", self.save_image, "#a6e3a1")
        self.create_button(file_section, "🔄 Reset Image", self.reset_image, "#f9e2af")
        
        # Filter Operations Section
        filter_section = tk.LabelFrame(
            control_frame, 
            text="🔍 Image Filters", 
            font=("Arial", 10, "bold"),
            bg="#2d2d3d", 
            fg="#f38ba8",
            relief="flat"
        )
        filter_section.pack(fill="x", padx=10, pady=10)
        
        self.create_button(filter_section, "⚫ Grayscale", self.apply_grayscale, "#cba6f7")
        self.create_button(filter_section, "🌀 Gaussian Blur", self.apply_blur, "#89dceb")
        self.create_button(filter_section, "🔪 Edge Detection", self.apply_edges, "#f38ba8")
        self.create_button(filter_section, "✨ Sharpen", self.apply_sharpen, "#fab387")
        
        # Transformation Section
        transform_section = tk.LabelFrame(
            control_frame, 
            text="🔄 Transformations", 
            font=("Arial", 10, "bold"),
            bg="#2d2d3d", 
            fg="#89b4fa",
            relief="flat"
        )
        transform_section.pack(fill="x", padx=10, pady=10)
        
        self.create_button(transform_section, "🔄 Rotate 90°", self.apply_rotate, "#89dceb")
        self.create_button(transform_section, "🪞 Flip Horizontal", self.apply_flip, "#cba6f7")
        
        # Enhancement Section
        enhance_section = tk.LabelFrame(
            control_frame, 
            text="⭐ Image Enhancement", 
            font=("Arial", 10, "bold"),
            bg="#2d2d3d", 
            fg="#f9e2af",
            relief="flat"
        )
        enhance_section.pack(fill="x", padx=10, pady=10)
        
        # Brightness Slider
        tk.Label(
            enhance_section, 
            text="Brightness:", 
            bg="#2d2d3d", 
            fg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        
        self.brightness_slider = tk.Scale(
            enhance_section,
            from_=0.5, to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.update_brightness,
            bg="#2d2d3d",
            fg="#ffffff",
            highlightthickness=0
        )
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(fill="x", padx=10, pady=5)
        
        # Contrast Slider
        tk.Label(
            enhance_section, 
            text="Contrast:", 
            bg="#2d2d3d", 
            fg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))
        
        self.contrast_slider = tk.Scale(
            enhance_section,
            from_=0.5, to=2.0,
            resolution=0.1,
            orient="horizontal",
            command=self.update_contrast,
            bg="#2d2d3d",
            fg="#ffffff",
            highlightthickness=0
        )
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill="x", padx=10, pady=5)
        
        # Info Label
        self.info_label = tk.Label(
            control_frame,
            text="No image loaded",
            font=("Arial", 9),
            bg="#2d2d3d",
            fg="#6c7086",
            wraplength=250
        )
        self.info_label.pack(pady=20)
    
    def create_button(self, parent, text, command, color):
        """Helper function to create styled buttons"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#1e1e2e",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            pady=8
        )
        btn.pack(fill="x", padx=10, pady=5)
        
        # Hover effect
        def on_enter(e):
            btn.config(bg=self.lighten_color(color))
        
        def on_leave(e):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        """Lighten a color for hover effect"""
        colors = {
            "#89b4fa": "#a6c9ff",
            "#a6e3a1": "#c2ffbd",
            "#f9e2af": "#fff5d1",
            "#cba6f7": "#e2c8ff",
            "#89dceb": "#a5f0ff",
            "#f38ba8": "#ffa5c2",
            "#fab387": "#ffccaa"
        }
        return colors.get(color, color)
    
    def add_separator(self, parent):
        """Add a separator line"""
        separator = tk.Frame(parent, bg="#45475a", height=2)
        separator.pack(fill="x", padx=10, pady=5)
    
    def create_display_panel(self, parent):
        """Create image display panel"""
        display_frame = tk.Frame(parent, bg="#1e1e2e")
        display_frame.pack(side="right", fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            display_frame,
            text="🖼️ Image Preview",
            font=("Arial", 14, "bold"),
            bg="#1e1e2e",
            fg="#ffffff"
        )
        title_label.pack(pady=10)
        
        # Canvas for image display
        self.canvas = tk.Canvas(
            display_frame,
            bg="#181825",
            highlightthickness=0,
            relief="flat"
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg="#313244",
            fg="#a6e3a1",
            anchor="w",
            padx=10
        )
        self.status_bar.pack(side="bottom", fill="x")
    
    def update_status(self, message, is_error=False):
        """Update status bar message"""
        self.status_bar.config(text=message, fg="#f38ba8" if is_error else "#a6e3a1")
        self.root.after(3000, lambda: self.status_bar.config(text="Ready", fg="#a6e3a1"))
    
    def open_image(self):
        """Open and load an image file"""
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Read image using OpenCV
                self.original_image = cv2.imread(file_path)
                if self.original_image is None:
                    raise ValueError("Could not read image file")
                
                self.current_image = self.original_image.copy()
                self.image_path = file_path
                
                # Display image info
                height, width = self.original_image.shape[:2]
                self.info_label.config(text=f"Image: {os.path.basename(file_path)}\nSize: {width} x {height}")
                
                # Reset sliders
                self.brightness_slider.set(1.0)
                self.contrast_slider.set(1.0)
                
                # Display image
                self.display_image_on_canvas()
                self.update_status(f"Loaded: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.update_status("Failed to load image", True)
    
    def display_image_on_canvas(self):
        """Display current image on canvas"""
        if self.current_image is None:
            return
        
        # Convert OpenCV BGR to RGB
        img_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Get canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas not yet rendered
            canvas_width = 600
            canvas_height = 500
        
        # Resize image to fit canvas while maintaining aspect ratio
        img_pil.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.display_image = ImageTk.PhotoImage(img_pil)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        x = (canvas_width - img_pil.width) // 2
        y = (canvas_height - img_pil.height) // 2
        self.canvas.create_image(x, y, anchor="nw", image=self.display_image)
    
    def save_image(self):
        """Save current image to file"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.current_image)
                self.update_status(f"Saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                self.update_status("Failed to save image", True)
    
    def reset_image(self):
        """Reset to original image"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = self.original_image.copy()
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.display_image_on_canvas()
        self.update_status("Reset to original image")
    
    def apply_grayscale(self):
        """Convert image to grayscale"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.display_image_on_canvas()
        self.update_status("Applied: Grayscale filter")
    
    def apply_blur(self):
        """Apply Gaussian blur to image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = cv2.GaussianBlur(self.current_image, (15, 15), 0)
        self.display_image_on_canvas()
        self.update_status("Applied: Gaussian Blur")
    
    def apply_edges(self):
        """Apply Canny edge detection"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.display_image_on_canvas()
        self.update_status("Applied: Edge Detection")
    
    def apply_sharpen(self):
        """Apply sharpening kernel to image"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        kernel = np.array([[-1, -1, -1],
                           [-1,  9, -1],
                           [-1, -1, -1]])
        self.current_image = cv2.filter2D(self.current_image, -1, kernel)
        self.display_image_on_canvas()
        self.update_status("Applied: Sharpen filter")
    
    def apply_rotate(self):
        """Rotate image 90 degrees clockwise"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = cv2.rotate(self.current_image, cv2.ROTATE_90_CLOCKWISE)
        self.display_image_on_canvas()
        self.update_status("Applied: Rotate 90°")
    
    def apply_flip(self):
        """Flip image horizontally"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = cv2.flip(self.current_image, 1)
        self.display_image_on_canvas()
        self.update_status("Applied: Horizontal Flip")
    
    def update_brightness(self, value=None):
        """Update image brightness"""
        if self.original_image is None:
            return
        
        value = float(value)
        img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        enhancer = ImageEnhance.Brightness(img_pil)
        img_pil = enhancer.enhance(value)
        
        self.current_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        self.display_image_on_canvas()
    
    def update_contrast(self, value=None):
        """Update image contrast"""
        if self.original_image is None:
            return
        
        value = float(value)
        img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        enhancer = ImageEnhance.Contrast(img_pil)
        img_pil = enhancer.enhance(value)
        
        self.current_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        self.display_image_on_canvas()
    
    def show_about(self):
        """Show about dialog""
        about_text = """
        🎨 Image Filtering and Transformation Tool
        
        Version: 1.0
        Language: Python 3.8+
        
        Features:
        • Image filters (Grayscale, Blur, Edges, Sharpen)
        • Transformations (Rotate, Flip)
        • Brightness and Contrast adjustment
        • Open and save images
        
       
        
        messagebox.showinfo("About", about_text)


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
