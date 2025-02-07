import tkinter as tk
from tkinter import filedialog, ttk
import svgwrite
import xml.etree.ElementTree as ET

class SVGEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("SVG Polygon Editor")
        
        # Configure the root window
        self.root.configure(bg='#f0f0f0')  # Light gray background
        self.root.geometry('500x600')  # Set initial window size
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize variables
        self.points = []  # Store polygon points
        self.viewBox = "-60 -50 120 120"
        self.fill = "#185452"
        self.stroke = "black"
        self.stroke_width = 1
        self.drag_data = {'index': None, 'x': 0, 'y': 0}
        
        # Create and style the canvas
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=400,
            height=400,
            bg='white',
            relief='ridge',
            bd=2
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Style the buttons
        style = ttk.Style()
        style.configure('Action.TButton', padding=5)
        
        # Create and pack buttons with improved styling
        btn_load = ttk.Button(
            button_frame,
            text="Load SVG",
            command=self.load_svg,
            style='Action.TButton'
        )
        btn_load.pack(side=tk.LEFT, padx=5)
        
        btn_save = ttk.Button(
            button_frame,
            text="Save SVG",
            command=self.save_svg,
            style='Action.TButton'
        )
        btn_save.pack(side=tk.LEFT, padx=5)
        
        # Add clear button
        btn_clear = ttk.Button(
            button_frame,
            text="Clear Points",
            command=self.clear_points,
            style='Action.TButton'
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Create color selection frame
        color_frame = ttk.LabelFrame(main_frame, text="Style Settings", padding="5")
        color_frame.pack(fill=tk.X, pady=10)
        
        # Add color selection buttons
        ttk.Label(color_frame, text="Fill Color:").grid(row=0, column=0, padx=5, pady=5)
        self.fill_entry = ttk.Entry(color_frame, width=10)
        self.fill_entry.insert(0, self.fill)
        self.fill_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(color_frame, text="Stroke Color:").grid(row=1, column=0, padx=5, pady=5)
        self.stroke_entry = ttk.Entry(color_frame, width=10)
        self.stroke_entry.insert(0, self.stroke)
        self.stroke_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Add apply button
        ttk.Button(
            color_frame,
            text="Apply Colors",
            command=self.update_colors,
            style='Action.TButton'
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Bind canvas events
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)  # Add double-click binding
        
        # Add help text
        help_text = ttk.Label(
            main_frame,
            text="Double-click to add points • Click and drag to move points",
            font=('Arial', 9)
        )
        help_text.pack(pady=(0, 5))
        
        # Add status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Double-click to add points")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, pady=(5, 0))

    def clear_points(self):
        """Clear all points from the polygon"""
        self.points = []
        self.render_polygon()
        self.status_var.set("All points cleared")

    def on_double_click(self, event):
        """Handle double-click event to add new points"""
        # Convert canvas coordinates to polygon coordinates
        new_x = event.x - 200
        new_y = event.y - 200
        
        # Find the best position to insert the new point
        if len(self.points) < 2:
            # If we have less than 2 points, simply append
            self.points.append((new_x, new_y))
        else:
            # Find the closest line segment to insert the point
            min_dist = float('inf')
            insert_index = len(self.points)
            
            for i in range(len(self.points)):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % len(self.points)]
                
                # Calculate distance from point to line segment
                dist = point_to_line_distance((new_x, new_y), p1, p2)
                
                if dist < min_dist:
                    min_dist = dist
                    insert_index = i + 1
            
            self.points.insert(insert_index, (new_x, new_y))
        
        self.render_polygon()
        self.status_var.set(f"Added new point at ({new_x}, {new_y})")

    def update_colors(self):
        """Update polygon colors based on entry fields"""
        self.fill = self.fill_entry.get()
        self.stroke = self.stroke_entry.get()
        self.render_polygon()
        self.status_var.set("Colors updated")

    def render_polygon(self):
        """Render the polygon and control points on the canvas"""
        self.canvas.delete("all")
        
        # Scale points to canvas coordinates
        self.scaled_points = [(x + 200, y + 200) for x, y in self.points]
        
        # Draw polygon if points exist
        if self.scaled_points:
            self.canvas.create_polygon(
                self.scaled_points,
                fill=self.fill,
                outline=self.stroke
            )
            
            # Draw control points
            for i, (x, y) in enumerate(self.scaled_points):
                self.canvas.create_oval(
                    x-5, y-5, x+5, y+5,
                    fill='red',
                    tags=("point", str(i))
                )

    def on_press(self, event):
        """Handle mouse press event to start dragging points"""
        for i, (x, y) in enumerate(self.scaled_points):
            if (x-5 <= event.x <= x+5) and (y-5 <= event.y <= y+5):
                self.drag_data['index'] = i
                self.drag_data['x'] = event.x
                self.drag_data['y'] = event.y
                self.status_var.set(f"Dragging point {i}")
                break

    def on_drag(self, event):
        """Handle mouse drag event to move points"""
        index = self.drag_data['index']
        if index is not None:
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            px, py = self.points[index]
            self.points[index] = (px + dx, py + dy)
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y
            self.render_polygon()

    def save_svg(self):
        """Save the polygon as an SVG file"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")]
        )
        if not filepath:
            return
            
        dwg = svgwrite.Drawing(filepath, viewBox=self.viewBox)
        dwg.add(dwg.polygon(
            points=self.points,
            fill=self.fill,
            stroke=self.stroke,
            stroke_width=self.stroke_width
        ))
        dwg.save()
        self.status_var.set(f"Saved SVG to {filepath}")

    def load_svg(self):
        """Load an SVG file and extract polygon data"""
        filepath = filedialog.askopenfilename(
            filetypes=[("SVG files", "*.svg")]
        )
        if not filepath:
            return
            
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        
        polygon = root.find('.//svg:polygon', ns)
        if polygon is not None:
            self.points = [tuple(map(float, p.split(',')))
                         for p in polygon.get('points', '').split()]
            self.fill = polygon.get('fill', self.fill)
            self.stroke = polygon.get('stroke', self.stroke)
            self.stroke_width = float(polygon.get('stroke-width', self.stroke_width))
            self.viewBox = root.get('viewBox', self.viewBox)
            
            # Update color entries
            self.fill_entry.delete(0, tk.END)
            self.fill_entry.insert(0, self.fill)
            self.stroke_entry.delete(0, tk.END)
            self.stroke_entry.insert(0, self.stroke)
            
            self.render_polygon()
            self.status_var.set(f"Loaded SVG from {filepath}")

def point_to_line_distance(point, line_start, line_end):
    """Calculate the distance from a point to a line segment"""
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # Calculate the distance from point to line
    numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
    denominator = ((y2-y1)**2 + (x2-x1)**2)**0.5
    
    return numerator/denominator if denominator != 0 else 0

if __name__ == "__main__":
    root = tk.Tk()
    app = SVGEditor(root)
    root.mainloop()