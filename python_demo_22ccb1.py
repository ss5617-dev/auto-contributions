# Learning Objective:
# This tutorial will teach you how to generate visually stunning fractal art
# using Python's Turtle graphics. We will focus on the concept of recursion
# to create self-similar patterns, exploring mathematical beauty.

# Import the turtle module, which provides a canvas and drawing tools.
import turtle

# --- Configuration ---
# You can adjust these values to change the appearance of your fractal.

# The initial length of the line segment.
INITIAL_LENGTH = 100

# The angle for branching.
BRANCH_ANGLE = 30

# How much shorter each subsequent branch should be.
# A value of 0.7 means each branch is 70% the length of the parent.
LENGTH_REDUCTION_FACTOR = 0.7

# The maximum depth of recursion. This prevents infinite loops and controls detail.
MAX_DEPTH = 7

# Set up the screen for drawing.
screen = turtle.Screen()
screen.setup(width=800, height=600) # Set the window size
screen.bgcolor("black")            # Set the background color to black for good contrast
screen.title("Fractal Tree Generator") # Set the window title

# Create a turtle object to do the drawing.
# We'll call it 'artist' for clarity.
artist = turtle.Turtle()
artist.speed(0) # Set the speed to the fastest (0) for quicker rendering.
artist.pensize(2) # Set the pen thickness for better visibility.
artist.color("green") # Set the initial color of the branches.

# --- Recursive Function Definition ---

def draw_fractal_tree(t, length, depth):
    """
    Recursively draws a fractal tree.

    Args:
        t (turtle.Turtle): The turtle object used for drawing.
        length (float): The current length of the branch to draw.
        depth (int): The current recursion depth.
    """

    # Base Case: If we've reached the maximum depth, stop drawing this branch.
    # This is crucial to prevent infinite recursion.
    if depth <= 0:
        return

    # --- Drawing the Current Branch ---
    # Move the turtle forward by the specified length. This draws a line.
    t.forward(length)

    # --- Branching Logic ---
    # Save the current position and heading of the turtle.
    # This is important because we'll need to return to this point
    # to draw the other branches.
    current_pos = t.position()
    current_heading = t.heading()

    # --- Draw the Left Branch ---
    # Turn the turtle left by the BRANCH_ANGLE.
    t.left(BRANCH_ANGLE)
    # Recursively call draw_fractal_tree for the left branch.
    # The new length is the current length multiplied by the reduction factor.
    # The depth is decreased by 1 for the next level of recursion.
    draw_fractal_tree(t, length * LENGTH_REDUCTION_FACTOR, depth - 1)

    # --- Return to the Parent Branch Point ---
    # Restore the turtle's position and heading to where it was before drawing the left branch.
    t.penup()     # Lift the pen so it doesn't draw while repositioning.
    t.goto(current_pos)
    t.setheading(current_heading)
    t.pendown()   # Put the pen back down to continue drawing.

    # --- Draw the Right Branch ---
    # Turn the turtle right by the BRANCH_ANGLE.
    t.right(BRANCH_ANGLE)
    # Recursively call draw_fractal_tree for the right branch.
    draw_fractal_tree(t, length * LENGTH_REDUCTION_FACTOR, depth - 1)

    # --- Return to the Parent Branch Point (again) ---
    # After drawing both branches, we need to return the turtle to its
    # original position and heading for the calling function.
    t.penup()
    t.goto(current_pos)
    t.setheading(current_heading)
    t.pendown()

# --- Setup for the Initial Call ---
# Move the turtle to the bottom center of the screen to start drawing the trunk.
artist.penup()         # Lift the pen
artist.goto(0, -200)   # Move to a starting position lower on the screen
artist.left(90)        # Point the turtle upwards, ready to draw the trunk
artist.pendown()       # Put the pen down

# --- Example Usage ---
# This is where we start the fractal generation process.
# We call the recursive function with the initial parameters.
print("Generating fractal tree...")
draw_fractal_tree(artist, INITIAL_LENGTH, MAX_DEPTH)
print("Fractal tree generation complete!")

# Hide the turtle icon after drawing is finished.
artist.hideturtle()

# Keep the window open until it's manually closed.
screen.mainloop()