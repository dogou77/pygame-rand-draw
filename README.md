# pygame-rand-draw
Author: Brayden Olsen

Date Modified: 1/13/2022

Version: 1.1.0


A Python script that draws randomly using different methods using pygame

Run draw.py with Python 3 installed

EPILEPSY WARNING

NOTE: This program is resource intensive

NOTE: Requires a 1080p or above monitor to view correctly



Method 1 - Draw Point

  This method involves having a pointer that tells the program where to draw pixels, this pointer is then randomly moved in
  1 of 9 possible directions (it can move diagonally).
  

  There are several different options for this drawing method.

    Option 1 - X-Axis Symmetry: Enables symmetry over the X-Axis, can be used with Y-Axis Symmetry

    Option 2 - Y-Axis Symmetry: Enables symmetry over the Y-Axis, can be used with X-Axis Symmetry

    Option 3 - Color Mode A:    Enables color for the pointer, each movement a random RGB value will be incremented or decremented

    Option 4 - Color Mode B:    Enables color for the pointer, each movement a random color value will be chosen

    Option 5 - Overwrite:       Makes it so that if the pointer is over an already existing pixel, it turns it white

    Option 6 - Borders:         Constrains the pointer to the pygame window so it always stays in view

    Option 7 - Import Image:    Enables you to input the filename of an image and sets the background of the drawing to that image

  
  There are also keyboard commands while you are in the drawing screen

    Escape: Returns to Main Menu

    Space:  Toggles rendering, when not being rendered the drawing process speeds up

    F12:    Captures an image named image.png to the script directory. Overwrites the previous image.png



Method 2 - Draw Circular Lines

  This method of drawing draws out lines from a central point to a ring
  

  Options

    Option 1 - Radius:       A text input that changes the radius of the ring that the lines are going to

    Option 2 - From X/Y:     Determines where the origin of the lines is

    Option 3 - To X/Y:       Determines where the center of the ring that the lines are going to is

    Option 4 - Color Mode A: Enables color for the lines, each new line a random RGB value will be incremented or decremented

    Option 5 - Color Mode B: Enables color for the lines, each new line a random color value will be chosen

    
  Keyboard Commands

    There are also keyboard commands while you are in the drawing screen

    Escape: Returns to Main Menu

    Space:  Toggles rendering, when not being rendered the drawing process speeds up

    F12:    Captures an image named image.png to the script directory. Overwrites the previous image.png



Method 3 - Draw Lines

  This method of drawing draws out lines from a random point to another random point
  

  Options

    Option 1 - Color Mode A: Enables color for the lines, each new line a random RGB value will be incremented or decremented

    Option 2 - Color Mode B: Enables color for the lines, each new line a random color value will be chosen

    
  Keyboard Commands

    There are also keyboard commands while you are in the drawing screen

    Escape: Returns to Main Menu

    Space:  Toggles rendering, when not being rendered the drawing process speeds up

    F12:    Captures an image named image.png to the script directory. Overwrites the previous image.png



Method 4 - Draw Rectangles

  This method of drawing draws out lines from a central point to a ring
  

  Options

    Option 1 - Color Mode A: Enables color for the rectangles, each new rectangle a random RGB value will be incremented or decremented

    Option 2 - Color Mode B: Enables color for the rectangles, each new rectangle a random color value will be chosen

    
  Keyboard Commands

    There are also keyboard commands while you are in the drawing screen

    Escape: Returns to Main Menu

    Space:  Toggles rendering, when not being rendered the drawing process speeds up

    F12:    Captures an image named image.png to the script directory. Overwrites the previous image.png