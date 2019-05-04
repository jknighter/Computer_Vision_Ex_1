# -*- coding: utf-8 -*-
"""05_hough_transform.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nAy9fuzdXIUwocLqCf4qwGGWqKjpjStm

# 2D Structure Extraction (Hough Transform)
In this exercise, we will implement a Hough transform in order to detect parametric curves, such as lines or circles.
In the following, we shortly review the motivation for this technique.

Consider the point $p=(\mathtt{x},\mathtt{y})$ and the equation for a line $y = mx+c$. What are the lines that could pass through $p$?
The answer is simple: all the lines for which $m$ and $c$ satisfy $\mathtt{y} = m\mathtt{x}+c$.
Regarding $(\mathtt{x},\mathtt{y})$ as fixed, the last equation is that of a line in $(m,c)$-space.
Repeating this reasoning, a second point $p'=(\mathtt{x}',\mathtt{y}')$ will also have an associated line in parameter space, and the two lines will intersect at the point $(\tilde{m},\tilde{c})$, which corresponds to the line connecting $p$ and $p'$.

In order to find lines in the input image, we can thus pursue the following approach.
We start with an empty accumulator array quantizing the parameter space for $m$ and $c$.
For each edge pixel in the input image, we then draw a line in the accumulator array and increment the corresponding cells.
Edge pixels on the same line in the input image will produce intersecting lines in $(m,c)$-space and will thus reinforce the intersection point.
Maxima in this array thus correspond to lines in the input image that many edge pixels agree on.

In practice, the parametrization in terms of $m$ and $c$ is problematic, since the slope $m$ may become infinite.
Instead, we use the following parametrization in polar coordinates:
\begin{equation}
	\mathtt{x}\cos\theta + \mathtt{y}\sin\theta = \rho \label{eq:hough_line}
\end{equation}
This produces a sinusoidal curve in $(\rho,\theta)$-space, but otherwise the procedure is unchanged.

The following sub-questions will guide you through the steps of building a Hough transform.
"""

# %matplotlib notebook
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

"""## Some convenience functions"""

def imread_gray(filename):
    """Read grayscale image from our data directory."""
    return cv2.imread(f'../data/{filename}', cv2.IMREAD_GRAYSCALE)

def imread_rgb(filename):
    """Read a color image from our data directory."""
    im = cv2.imread(f'../data/{filename}', cv2.IMREAD_COLOR)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

def plot_hough(image, edges, hough_space):
    fig, axes = plt.subplots(1, 3, figsize=(3 * 4, 4))
    axes = axes.flat

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Image')
    
    axes[1].imshow(edges, cmap='gray')
    axes[1].set_title('Edges')
    
    axes[2].imshow(hough_space, cmap='hot')
    axes[2].set_title('Hough space')
    axes[2].set_xlabel('theta (index)')
    axes[2].set_ylabel('rho (index)')
    fig.tight_layout()
    
def plot_with_hough_lines(image_rgb, rhos, thetas):
    """Plot an image with lines drawn over it.
    The lines are specified as an array of rho values and
    and array of theta values.
    """
    
    rhos = np.asarray(rhos)
    thetas = np.asarray(thetas)

    # compute start and ending point of the line x*cos(theta)+y*sin(theta)=rho
    x0, x1 = 0, image.shape[1] - 1  # Draw line across image  
    y0 = rhos / np.sin(thetas)
    y1 = (rhos - x1 * np.cos(thetas)) / np.sin(thetas)

    # Check out this page for more drawing function in OpenCV:
    # https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html
    for yy0, yy1 in zip(y0, y1):
        cv2.line(image_rgb, (x0, int(yy0)), (x1, int(yy1)), color=(255, 0, 0))

    return image_rgb

"""## Part a
Build up an accumulator array ``votes_acc`` for votes in the parameter space $(\rho, \theta)$. $\theta$ ranges from $-\pi/2$ to $\pi/2$, and $\rho$ ranges from $-D$ to $D$, where $D$ denotes the length of the image diagonal.
Use ``n_bins_rho`` and ``n_bins_theta`` as the number of bins in each direction.
Initially, the array should be filled with zeros.

For each edge pixel in the input image, create the corresponding curve in $(\rho, \theta)$ space by evaluating above line equation for all values of $\theta$ and increment the corresponding cells of the accumulator array.
"""

def hough_transform(edge_image, n_bins_rho, n_bins_theta):
    # Vote accumulator
    votes_acc = np.zeros((n_bins_rho, n_bins_theta), dtype=np.int)  
    
    # Create bins
    diag = np.linalg.norm(edge_image.shape)  # Length of image diagonal
    theta_bins = np.linspace(-np.pi / 2, np.pi / 2, n_bins_theta)
    rho_bins = np.linspace(-diag, diag, n_bins_rho) 
    
    # Implement Hough transform here
    im_h, im_w = edge_image.shape
    for i in range(im_h):
        for j in range(im_w):
            if edge_image[i,j] == 255 :
                for theta in theta_bins:
                    rho = j * np.sin(theta) + i * np.cos(theta)
                    rho_idx = int(np.floor((n_bins_rho) * (rho+diag) / (2*diag)))
                    votes_acc[rho_idx, np.where(theta_bins == theta)] += 1
    return votes_acc, rho_bins, theta_bins

"""Test the implementation on an example image. Visualize the resulting Hough space by displaying it as a 2D image."""

image = imread_gray('gantrycrane.png')

# Get edges using Canny
sigma = 2
kernel_size = 2 * int(3 * sigma) + 1
blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
edges = cv2.Canny(blurred, threshold1=30, threshold2=90)  # 30, 90 are manually tuned

n_bins_rho, n_bins_theta = 300, 300
hough_space, rho_bins, theta_bins = hough_transform(edges, n_bins_rho, n_bins_theta)
plot_hough(image, edges, hough_space)
plt.show()
"""## Part b
Write a function ``nms2d`` which suppresses all points in the Hough space that are not local maxima.
This can be achieved by looking at the 8 direct neighbors of each pixel and keeping only pixels whose value is greater than all its neighbors.
This function is simpler than the non-maximum suppression from the Canny Edge Detector since it does not take into account local gradients.
"""

def nms2d(image):
    image_out = np.zeros_like(image)
    offsets_x = [-1, -1, 0, 1, 1, 1, 0, -1]
    offsets_y = [0, -1, -1, -1, 0, 1, 1, 1]
    # Your code here
    im_h, im_w = image.shape
    for i in range(im_h):
        for j in range(im_w):
            for ox, oy in zip(offsets_x, offsets_y):
                if image[i,j] >= image[i + ox, j + oy]:
                    image_out[i,j] = image[i,j]
    return image_out

"""Write a function ``find_hough_peaks`` that takes the result of ``hough_transform`` as an argument, finds the extrema in Hough space using ``nms2d`` and returns the index of all points $(\rho_i, \theta_i)$ for which the corresponding Hough value is greater than ``threshold``."""

def find_hough_peaks(hough_space, threshold):
    rho_max_index = []
    theta_max_index = []
    im_h, im_w = hough_space.shape
    for i in range(im_h):
        for j in range(im_w):
            if hough_space[i,j] > threshold:
                rho_max_index.append(i)
                theta_max_index.append(j)
    return rho_max_index, theta_max_index

"""Try your implementation on the images ``gantrycrane.png`` and ``circuit.png``.
Do you find all the lines?
"""

# Find maximum
rho_max_idx, theta_max_idx = find_hough_peaks(hough_space, 250)
print(f'gantrycrane.png: found {len(rho_max_idx)} lines in the image.')
rho_max, theta_max = rho_bins[rho_max_idx], theta_bins[theta_max_idx]

color_image = imread_rgb('gantrycrane.png')
image_with_lines = plot_with_hough_lines(color_image, rho_max, theta_max)

# Plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.imshow(image_with_lines)
plt.show()
# Try another image
image = imread_gray('circuit.png')

sigma = 2
kernel_size = 2 * int(3 * sigma) + 1
blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
edge = cv2.Canny(blurred, threshold1=30, threshold2=90)
hough_space, rho_bins, theta_bins = hough_transform(edge, n_bins_rho, n_bins_theta)

# Find maximum
rho_max_idx, theta_max_idx = find_hough_peaks(hough_space, 130)
print('circuit.png: found {} lines in the image.'.format(len(rho_max_idx)))
rho_max, theta_max = rho_bins[rho_max_idx], theta_bins[theta_max_idx]
color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
image_with_lines = plot_with_hough_lines(color_image, rho_max, theta_max)

# Plot
fig, ax = plt.subplots(figsize=(8, 4))
ax.imshow(image_with_lines)
plt.show()
"""**Do you find all the lines? Type your answer here:**
    
----

## Part c (bonus)

The Hough transform is a general technique that can not only be applied to lines, but also to other parametric curves, such as circles.
In the following, we will show how the implementation can be extended to finding circles.

A circle can be parameterized by the following equation:
$$	
    (\mathtt{x}-a)^2 + (\mathtt{y}-b)^2 = r^2. \label{eq:hough_circle}
$$

Unfortunately, the computation and memory requirements for the Hough transform increase exponentially with the number of parameters.
While a 3D search space is still just feasible, we can dramatically reduce the amount of computation by integrating the gradient direction in the algorithm.

Without gradient information, all values $a, b$ lying on the cone given by above equation are incremented.
With the gradient information, we only need to increment points on an arc centered at $(a, b)$:
$$
\begin{eqnarray}
	a &=& x + r\cos\phi\\
	b &=& y + r\sin\phi,
\end{eqnarray}
$$
where $\phi$ is the gradient angle returned by the edge operator.

Create a function ``hough_circle`` which implements the Hough transform for circles.
Try your implementation for a practical application of counting coins in an image.
You can use the images ``coins1.png`` and ``coins2.png`` for testing.

## Pard d (bonus)
The same trick (as in **Part c**) of using the image gradient can be used for lines.
Modify the code from **Part a** to only vote for one line per edge pixel, instead of all the lines running through this pixel.

## Part e (bonus)
Can you build an online coin classification and counting system?

You can take a look at the ``Haribo classification`` demo (MATLAB) in the Moodle for some ideas. Use the functions you wrote in the previous questions.
(Hint: you may need to include a reference shape in the picture in order to obtain the absolute scale).
"""