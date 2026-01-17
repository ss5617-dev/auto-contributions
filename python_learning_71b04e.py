# Learning Objective: Visualize the Mandelbrot Set

# This tutorial will guide you through creating a visual representation
# of the Mandelbrot set using Python and the NumPy library.
# We'll learn how to:
# 1. Define a complex plane region.
# 2. Implement the core Mandelbrot iteration algorithm.
# 3. Map iteration counts to colors to reveal the fractal pattern.

import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iterations):
    """
    Performs the Mandelbrot iteration for a single complex number 'c'.

    The Mandelbrot set is defined by the recurrence relation:
    z_(n+1) = z_n^2 + c
    starting with z_0 = 0.

    If the magnitude of z_n stays bounded (doesn't go to infinity)
    as n increases, then 'c' belongs to the Mandelbrot set.

    Args:
        c (complex): The complex number to test.
        max_iterations (int): The maximum number of iterations to perform.

    Returns:
        int: The number of iterations it took for the magnitude of z to
             exceed 2 (divergence), or max_iterations if it remained bounded.
    """
    z = 0  # Initialize z to 0, as per the Mandelbrot definition.
    for i in range(max_iterations):
        # The core Mandelbrot iteration: z = z^2 + c
        z = z*z + c

        # Check for divergence: if the magnitude of z becomes greater than 2,
        # it will continue to grow towards infinity. We can stop iterating.
        if abs(z) > 2:
            return i  # Return the number of iterations it took to diverge.

    # If the loop completes without divergence, the point is likely in the set.
    # We return max_iterations to indicate it stayed bounded.
    return max_iterations

def create_mandelbrot_image(width, height, x_min, x_max, y_min, y_max, max_iterations):
    """
    Generates a 2D NumPy array representing the Mandelbrot fractal.

    This function maps each pixel in the desired image to a point in the
    complex plane and calculates its Mandelbrot iteration count.

    Args:
        width (int): The width of the output image in pixels.
        height (int): The height of the output image in pixels.
        x_min (float): The minimum real value (x-axis) of the complex plane.
        x_max (float): The maximum real value (x-axis) of the complex plane.
        y_min (float): The minimum imaginary value (y-axis) of the complex plane.
        y_max (float): The maximum imaginary value (y-axis) of the complex plane.
        max_iterations (int): The maximum number of iterations for the Mandelbrot algorithm.

    Returns:
        np.ndarray: A 2D NumPy array where each element represents the
                    iteration count for the corresponding point in the complex plane.
    """
    # Create arrays of real and imaginary parts for the complex plane.
    # np.linspace creates evenly spaced numbers over a specified interval.
    # We want 'width' points for the real axis and 'height' for the imaginary axis.
    real_axis = np.linspace(x_min, x_max, width)
    imaginary_axis = np.linspace(y_min, y_max, height)

    # Initialize an empty array to store the iteration counts for each pixel.
    # The shape will be (height, width) because we usually think of images
    # with rows (height) and columns (width).
    mandelbrot_image = np.zeros((height, width), dtype=int)

    # Iterate over each pixel in the image.
    # We use nested loops for clarity, though more advanced NumPy
    # operations could vectorize this further.
    for i in range(height):  # Corresponds to the imaginary part (y-axis)
        for j in range(width):  # Corresponds to the real part (x-axis)

            # Construct the complex number 'c' for the current pixel.
            # The real part is from the real_axis array, and the imaginary part
            # is from the imaginary_axis array.
            c = complex(real_axis[j], imaginary_axis[i])

            # Calculate the Mandelbrot iteration count for this complex number.
            iterations = mandelbrot(c, max_iterations)

            # Store the result in our image array.
            mandelbrot_image[i, j] = iterations

    return mandelbrot_image

# --- Example Usage ---

# Define the parameters for our Mandelbrot set visualization.
# Image resolution (pixels)
image_width = 800
image_height = 800

# Region of the complex plane to explore.
# The default view of the Mandelbrot set is often centered around (-0.75, 0)
# with a real range of about -2 to 1, and an imaginary range of -1.5 to 1.5.
x_min_val = -2.0
x_max_val = 1.0
y_min_val = -1.5
y_max_val = 1.5

# Maximum number of iterations per point.
# A higher number of iterations reveals more detail, especially in areas
# close to the boundary of the set.
max_iter = 100

print("Generating Mandelbrot set image...")

# Create the Mandelbrot set image data.
# This will be a 2D array of iteration counts.
mandelbrot_data = create_mandelbrot_image(
    image_width, image_height,
    x_min_val, x_max_val,
    y_min_val, y_max_val,
    max_iter
)

print("Image data generated. Plotting...")

# Use matplotlib to visualize the generated data.
plt.figure(figsize=(10, 10))  # Set the figure size for better viewing.

# imshow displays the image.
# The 'cmap' argument specifies the colormap. 'hot' is a good choice for
# showing the transition from bounded to unbounded areas. Other options: 'viridis', 'plasma', 'inferno', 'magma'.
# 'origin="lower"' ensures that the y-axis starts from the bottom, matching
# our complex plane definition where y_min is at the bottom.
plt.imshow(mandelbrot_data, cmap='hot', extent=(x_min_val, x_max_val, y_min_val, y_max_val), origin='lower')

# Add titles and labels for clarity.
plt.title("Mandelbrot Set")
plt.xlabel("Real Part")
plt.ylabel("Imaginary Part")

# Display the plot.
plt.show()

print("Done!")