import turtle
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, EpsImagePlugin

# ========== Config ========== #
EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"  # Locate ghostscript execute
COLORS = ["Black", "Red", "Green", "Yellow", "White", "Magenta", "Cyan", "Blue"]
PADDING = 50
DOT_SIZE = 15

FONT = ("Arial", 12, "normal")
FONT_OUTLINE = ("Arial", 12, "bold")
FONT_OUTLINE_COLOR = "black"

PLAYER_SHAPE = "arrow"
PLAYER_COLOR = "white"

COORD_MIN, COORD_MAX = -160, 160
PEARL_MENU_SCREEN_SIZE = "400x300"
PLAYER_MENU_SCREEN_SIZE = "300x200"
MAIN_MENU_SCREEN_SIZE = "400x300"
# ========== Setup Turtle Screen ========== #
screen = turtle.Screen()
screen.setup(width=800 + PADDING, height=800 + PADDING)
screen.title("Roblox Mapping Tool")
screen.bgpic('map.png')

# ========== Turtle Pens ========== #
pen = turtle.Turtle()  # For drawing pearl location
pen.hideturtle()
pen.speed(0)
pen.penup()

arrow = turtle.Turtle()  # For showing player location
arrow.hideturtle()
arrow.shape(PLAYER_SHAPE)
arrow.color(PLAYER_COLOR)
arrow.penup()


# ========== Pearl Mapping ========== #
def draw_pearl(x, y, color, note):
    pen.goto(x * 2.5, -y * 2.5)  # Multiple with 2.5, change from in-game coordination to Image coordination 160 -> 400
    pen.dot(DOT_SIZE, color)
    pen.pencolor(FONT_OUTLINE_COLOR)
    pen.write(note, False, align="center", font=FONT_OUTLINE)
    pen.pencolor(color)
    pen.write(note, False, align="center", font=FONT)


def pearl_mapping():
    root = tk.Tk()
    root.title("Pearl Mapping")
    root.geometry(PEARL_MENU_SCREEN_SIZE)

    def submit():
        try:
            #   Receive input from textbox
            x = int(x_entry.get())
            y = int(y_entry.get())
            color = color_entry.get().capitalize()
            note = note_entry.get()

            if color not in COLORS:
                messagebox.showerror(f"Invalid Color", f"Choose from: {COLORS}")
                return

            #   Set boundary for mapping
            if not (COORD_MIN <= x <= COORD_MAX and COORD_MIN <= y <= COORD_MAX):
                messagebox.showerror(f"Out of Range", f"Coordinates must be between {COORD_MIN} and {COORD_MAX}")
                return

            #   If note is empty, set default to display the coordinate
            if not note:
                note = f"({x}, {y})"

            draw_pearl(x, y, color, note)
            root.destroy()

        except ValueError:
            messagebox.showerror("Input Error, please enter valid numbers.")

    #   Pearl mapping menu
    tk.Label(root, text='Color (e.g. Red, Green, Blue)').pack(pady=5)
    color_entry = tk.Entry(root)
    color_entry.pack()

    tk.Label(root, text='X Coordinate').pack(pady=5)
    x_entry = tk.Entry(root)
    x_entry.pack()

    tk.Label(root, text='Y Coordinate').pack(pady=5)
    y_entry = tk.Entry(root)
    y_entry.pack()

    tk.Label(root, text='Note (optional)').pack(pady=5)
    note_entry = tk.Entry(root)
    note_entry.pack()

    tk.Button(root, text="Submit", command=submit).pack(pady=10)

    root.mainloop()


# ========== Player Location Finder ========== #
def player_location_finder():
    root = tk.Tk()
    root.title("Player Location Finder")
    root.geometry(PLAYER_MENU_SCREEN_SIZE)

    def show_arrow():
        try:
            x = int(x_entry.get())
            y = int(y_entry.get())
            #   Set boundary, if exceed return error and wait for new respond.
            if not (COORD_MIN <= x <= COORD_MAX and COORD_MIN <= y <= COORD_MAX):
                messagebox.showerror("Out of Range", f"Coordinates must be between {COORD_MIN} and {COORD_MAX}")
                return
            arrow.goto(x * 2.5, -y * 2.5)
            arrow.setheading(90)
            arrow.showturtle()
        #   If input coordination is not number
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid coordinates.")

    def exit_and_hide():
        arrow.hideturtle()
        root.destroy()

    tk.Label(root, text="X Coordinate").pack(pady=5)
    x_entry = tk.Entry(root)
    x_entry.pack()

    tk.Label(root, text="Y Coordinate").pack(pady=5)
    y_entry = tk.Entry(root)
    y_entry.pack()

    tk.Button(root, text="Show Player", command=show_arrow).pack(pady=10)

    tk.Button(root, text="Exit", command=exit_and_hide).pack(pady=5)

    root.mainloop()


# ========== Save Map as PNG ========== #
def save_canvas():
    filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")],
                                            title="Save Map As")

    #   If user close the save map menu, exit the menu (Return nothing)
    if not filepath:
        return
    #   Save current map as eps file for converting
    canvas = screen.getcanvas()
    canvas.postscript(file="temp_output.eps")

    try:
        img = Image.open("temp_output.eps")
        img.save(filepath, "png")
        messagebox.showinfo(f"Success, map saved as {filepath}")
    except Exception as e:
        messagebox.showerror(f"Error, failed to convert: {e}")


# ========== Main Menu on Click ========== #
def on_click(x, y):  # Input x,y parameter for receiving onclick x-axis,y-axis from turtle
    root = tk.Tk()
    root.title("Mapping Options")
    root.geometry(MAIN_MENU_SCREEN_SIZE)
    tk.Label(root, text="Choose an Option", pady=10).pack()
    tk.Button(root, text="Player Location Finder", width=40, height=2,  # Lambda for multiple command
              command=lambda: [root.destroy(), player_location_finder()]).pack(pady=5)
    tk.Button(root, text="Pearl Mapping", width=40, height=2,
              command=lambda: [root.destroy(), pearl_mapping()]).pack(pady=5)
    tk.Button(root, text="Save Map as PNG", width=40, height=2,
              command=lambda: [root.destroy(), save_canvas()]).pack(pady=5)
    root.mainloop()


screen.onclick(on_click)
screen.mainloop()
