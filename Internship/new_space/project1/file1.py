import tkinter as tk
from tkinter import ttk
from tkinter import Menu, messagebox, filedialog
from PIL import Image, ImageTk
class CircuitDesignGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Circuit Design Interface")
        
        # Create a Navigation Bar with Search Bar
        self.create_menu_bar()
        self.top_left=[]
        self.bottom_right=[]
        # Create main frame with padding
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Create sliding menu frame (Navigator Drawer)
        self.menu_frame = tk.Frame(self.main_frame, width=200, bg='lightgray')
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.menu_frame.pack_propagate(False)

        # Create left frame for GUI
        self.left_frame = tk.Frame(self.main_frame, width=500, height=800)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create right frame for image display
        self.right_frame = tk.Frame(self.main_frame, width=500, height=800, bg='white')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # Create Canvas in left frame for Circuit Connections
        self.canvas = tk.Canvas(self.left_frame, width=500, height=800, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Components and connections
        self.components = []
        self.connections = []
        self.images = []  # List to store multiple images
        self.selected_image = None
        self.image_movement_enabled = False

        # LED indicator
        self.led = self.canvas.create_rectangle(450,700,460,710, fill="grey")  # Default to grey (off state)

        # Variable to store line and current connection
        self.current_line = None
        self.start_coords = None

        # Create right-click context menu for connections
        self.create_context_menu()

        # Add a label for displaying images in the right frame
        self.image_label = tk.Label(self.right_frame)
        self.image_label.pack(fill=tk.BOTH, expand=1)

        # Add "Import Image" and "Import Circuit" buttons
        self.import_button_image = tk.Button(self.right_frame, text="Import Image", command=self.import_image_right)
        self.import_button_image.pack(side=tk.BOTTOM, pady=10)

        self.import_button_circuit = tk.Button(self.menu_frame, text="Import Circuit", command=self.import_image_left)
        self.import_button_circuit.pack(pady=10, padx=10, fill=tk.X)
        
        # Create sliding menu (Navigator Drawer)
        self.create_sliding_menu()
        # Predefined Pin Coordinates
        self.predefined_pins = {
            'image1': {  # First image's pin coordinates
                'Vcc': [(80, 345), (95, 360)],
                'GND': [(200, 130), (410, 150)],
                'pins': [(85, 135), (115, 150), (135, 135), (180, 150)]
            },
            'image2': {  # Second image's pin coordinates
                'Vcc': [(750, 540), (788, 545)],
                'GND': [(750, 550), (788, 555)],
                'pins': [(750, 560), (788, 565)]
            }
        }
        self.start_image_id = None
        self.target_image_id = None
        self.root.bind("<Button-1>", self.print_coordinates)
    def print_coordinates(self,event):
        print(f"x: {event.x}, y: {event.y}")
    def create_menu_bar(self):
        # Create a menu bar
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        # Home Menu
        home_menu = Menu(menu_bar, tearoff=0)
        home_menu.add_command(label="Home", command=self.go_home)
        menu_bar.add_cascade(label="Home", menu=home_menu)

        # More features menu
        setting = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="setting", menu=setting)

    def create_context_menu(self):
        # Context menu for right-click
        self.context_menu = Menu(self.root, tearoff=0)
        
        # Add "Connect to" with a submenu
        connect_menu = Menu(self.context_menu, tearoff=0)
        connect_menu.add_command(label="OUT", command=lambda: self.make_connection("OUT"))
        connect_menu.add_command(label="Vcc", command=lambda: self.make_connection("Vcc"))
        connect_menu.add_command(label="GND", command=lambda: self.make_connection("GND"))
        
        movement_menu = Menu(self.context_menu, tearoff=0)
        movement_menu.add_command(label="Disable Movement", command=lambda: self.image_movement(0))
        movement_menu.add_command(label="Enable Movement", command=lambda: self.image_movement(1))
        
        # Adding options to the context menu
        self.context_menu.add_cascade(label="Connect to >>", menu=connect_menu)
        self.context_menu.add_cascade(label="Movements", menu=movement_menu)
        self.context_menu.add_command(label="Remove Connection", command=self.remove_recent_connection)

        # Bind right-click event to show the context menu
        self.canvas.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        # Display the context menu at the mouse position
        self.context_menu.post(event.x_root, event.y_root)
    
    def image_movement(self, enable):
        self.image_movement_enabled = bool(enable)
        if enable:
            messagebox.showinfo("Movement Enabled", "Image movement has been enabled")
        else:
            messagebox.showinfo("Movement Disabled", "Image movement has been disabled")

    def import_image_right(self):
        # Import and display image on the right frame
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
        if file_path:
            image = Image.open(file_path)
            resized_image = image.resize((250, 250))
            self.current_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.current_image)
            self.image_label.image = self.current_image

    def import_image_left(self):
        # Import and display image on the left frame (circuit)
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])
        if file_path:
            image = Image.open(file_path)
            resized_image = image.resize((350, 250))
            resized_width, resized_height = resized_image.size
            print(f"Resized image size: {resized_width}x{resized_height}")
            circuit_image = ImageTk.PhotoImage(resized_image)
            if len(self.images)==0:
                x=250   
                y=250
            else:
            # Calculate position for the new image
                x = 450 + (len(self.images) * 220) % 400  # Adjust for your canvas size
                y = 550 + (len(self.images) // 2) * 220   # Adjust for your canvas size
            image_id = self.canvas.create_image(x, y, image=circuit_image)
            image_coords = self.canvas.coords(image_id)
            print(f"Image imported at coordinates: {image_coords}")

            self.canvas.image = circuit_image  # Keep a reference
            
            # Store the image information
            self.images.append({
                'id': image_id,
                'image': circuit_image,
                'file_path': file_path,
                'can_move': False
            })

            # Bind movement functionality to the image
            self.canvas.tag_bind(image_id, "<B1-Motion>", lambda event, id=image_id: self.move_image(event, id))
            self.canvas.tag_bind(image_id, "<Button-1>", lambda event, id=image_id: self.select_image(event, id))
            

    def select_image(self, event, image_id):
        # Mark this image as the currently selected image for movement
        self.selected_image = image_id

        # Enable movement only for this selected image
        for image in self.images:
            if image['id'] == image_id:
                image['can_move'] = True
            else:
                image['can_move'] = False

        print(f"Image selected for movement: {self.selected_image}")

    def move_image(self, event, image_id):
        for image in self.images:
            if image['id'] == image_id and image['can_move'] and self.image_movement_enabled:
                self.canvas.coords(image_id, event.x, event.y)  # Move the image to the new coordinates
                self.new_coords = self.canvas.coords(image_id)       # Get new coordinates
                self.x1,self.y1=self.new_coords
                self.top_left.append([self.x1 - (350 // 2), self.y1 - (250 // 2)])
                self.bottom_right.append([self.x1 + (350 // 2), self.y1 + (250 // 2)])
                print(f"Image {image_id} moved to: ({event.x}, {event.y})")
                break

    def create_sliding_menu(self):
        # Add buttons to the sliding menu 
        tk.Button(self.menu_frame, text="Reset Connections", command=self.reset_all_connections).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(self.menu_frame,text="delete image",command=self.delete_image).pack(pady=10,padx=10,fill=tk.X)
        tk.Button(self.menu_frame, text="Remove Last Connection", command=self.remove_recent_connection).pack(pady=10, padx=10, fill=tk.X)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12))

    #     # Define the categories
    #     categories = [
    #         ("Breadboards", ["Option 1", "Option 2"]),
    #         ("Basic", ["Option 1", "Option 2", "Option 3"]),
    #         ("Input", ["Option 3", "Option 4"]),
    #         ("Output", ["Option 5", "Option 6"]),
    #         ("Microcontroller", ["Option 7"]),
    #         ("Internet of Things", ["Option 8"]),
    #         ("Power", ["Option 9"]),
    #         ("Integrated Circuit", ["Option 10"]),
    #         ("Adafruit", ["Option 11"])
    #     ]

    #     # Create collapsible sections for each category
    #     for category_name, options in categories:
    #         # Create a button for the category (collapsible section)
    #         category_button = ttk.Button(self.menu_frame, text=category_name, command=lambda c=category_name: self.toggle_category(c))
    #         category_button.pack(fill=tk.X, padx=10, pady=(5, 0))

    #         # Create a frame to hold the options within the category
    #         option_frame = tk.Frame(self.menu_frame)
    #         option_frame.pack(fill=tk.X, padx=10)
    #         option_frame.pack_forget()  # Initially hide the options

    #         # Add buttons for each option within the category
    #         for option in options:
    #             tk.Button(option_frame, text=option, command=lambda o=option: self.option_selected(o)).pack(fill=tk.X, padx=20, pady=2)

    #         # Store references to the option frames for toggling visibility
    #         setattr(self, f"{category_name}_frame", option_frame)

    # def toggle_category(self, category_name):
    #     # Toggle the visibility of the category's options
    #     frame = getattr(self, f"{category_name}_frame")
    #     if frame.winfo_viewable():
    #         frame.pack_forget()
    #     else:
    #         frame.pack(fill=tk.X)

    def option_selected(self, option_name):
        # Placeholder function for when an option is selected
        print(f"Selected: {option_name}")
    def delete_image(self):
    # Check if an image is selected
        if self.selected_image:
        # Delete the image from the canvas
            self.canvas.delete(self.selected_image)
        
        # Remove the image from the images list
            self.images = [image for image in self.images if image['id'] != self.selected_image]
        
        # Reset the selected image
            self.selected_image = None
        
            messagebox.showinfo("Delete Image", "Selected image has been deleted.")
        else:
            messagebox.showwarning("Delete Image", "No image selected to delete.")
    def go_home(self):
        messagebox.showinfo("Home", "Returning to Home")

    def reset_all_connections(self):
        for connection in self.connections:
            self.canvas.delete(connection)
        self.connections.clear()
        messagebox.showinfo("Reset", "All connections reset")

    def remove_recent_connection(self):
        if self.connections:
            recent_connection = self.connections.pop()
            self.canvas.delete(recent_connection)
            print("Most recent connection removed")
        else:
            messagebox.showinfo("No Connections", "No connections to remove")

    def make_connection(self, pin_type):
        # Automated connection when pin_type is clicked
        if self.image_movement_enabled:
            return 
        self.pin_type = pin_type
        if self.pin_type=="GND":
            self.canvas.bind("<Button-1>", self.start_connection)
            self.canvas.bind("<B1-Motion>", self.update_connection)
            self.canvas.bind("<ButtonRelease-1>", self.end_connection)
        elif self.pin_type=="Vcc":
            self.canvas.bind("<Button-1>", self.start_connection)
            self.canvas.bind("<B1-Motion>", self.update_connection)
            self.canvas.bind("<ButtonRelease-1>", self.end_connection)
        else:
            self.canvas.bind("<Button-1>", self.start_connection)
            self.canvas.bind("<B1-Motion>", self.update_connection)
            self.canvas.bind("<ButtonRelease-1>", self.end_connection)
    
    def start_connection(self, event):
        """Start connection by identifying the pin and image."""
        self.start_coords = (event.x, event.y)
        for image_data in self.images:
            if self.is_within_pin(event.x, event.y, image_data, 'Vcc', 'GND'):
                self.start_image_id = image_data['id']
                self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="black", width=2)
                break
        else:
            messagebox.showwarning("Warning", "Not a valid starting point for connection")

    def update_connection(self, event):
        """Update the connection line while dragging."""
        if self.current_line:
            self.canvas.coords(self.current_line, self.start_coords[0], self.start_coords[1], event.x, event.y)

    def end_connection(self, event):
        """End the connection and check if it's a valid one."""
        if not self.current_line:
            return

        for image_data in self.images:
            if self.is_within_pin(event.x, event.y, image_data, 'Vcc', 'GND'):
                self.target_image_id = image_data['id']
                if self.start_image_id != self.target_image_id:
                    self.connections.append(self.current_line)
                    self.canvas.itemconfig(self.led, fill="green")  # Correct connection
                    messagebox.showinfo("Success", "Connection successfully made!")
                else:
                    self.canvas.delete(self.current_line)
                    self.canvas.itemconfig(self.led, fill="red")  # Same image
                    messagebox.showwarning("Invalid", "Can't connect to the same image")
                break
        else:
            self.canvas.delete(self.current_line)
            self.canvas.itemconfig(self.led, fill="red")
            messagebox.showwarning("Warning", "No valid endpoint for connection")
        self.current_line = None
        self.start_coords = None

    def is_within_pin(self, x, y, image_data, vcc_key, gnd_key):
        """Check if the given coordinates (x, y) fall within a pin's area for a specific image."""
        image_id = image_data['id']
        image_name = 'image1' if image_id == self.images[0]['id'] else 'image2'
        
        vcc_region = self.predefined_pins[image_name][vcc_key]
        gnd_region = self.predefined_pins[image_name][gnd_key]

        if (vcc_region[0][0] <= x <= vcc_region[1][0] and vcc_region[0][1] <= y <= vcc_region[1][1]) or \
           (gnd_region[0][0] <= x <= gnd_region[1][0] and gnd_region[0][1] <= y <= gnd_region[1][1]):
            return True
        return False
if __name__ == "__main__":
    root = tk.Tk()
    app = CircuitDesignGUI(root)
    root.mainloop()