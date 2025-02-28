import numpy as np

def binary(image, threshold):
    height, width = image.shape
    binary_image = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):

            if image[y, x] > threshold:
                binary_image[y, x] = 255
            else:
                binary_image[y, x] = 0

    return binary_image