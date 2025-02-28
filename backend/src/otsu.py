import numpy as np
from src.binary_thresholding import binary

def otsu(image):
    """
    -- Compute the intensity histogram of the image
    -- Compute the probability distribution using the histogram
    -- Cmpute global mean intensity
    -- Compute class probabilities (Wb, Wf, mu_b, and mu_f)
    -- Iterate through all the available pixel value as threshold
    """

    # Compute intensity and probability distibution
    total_pixel = image.shape[0] * image.shape[1] # H * W
    histogram, bins = np.histogram(image.flatten(), bins = 256,  range = [0, 256])
    probability_distribution = histogram / total_pixel

    # Compute global mean intensity
    intensity_level = np.arange(256) # Create an array of 0-255
    mu_T = np.sum(intensity_level * probability_distribution)

    # Iterate through all possible threshold value to maximize between-class variance
    best_threshold = 0
    max_between_class_variance = 0
    wb, mu_b = 0, 0

    for threshold in range(256):
        wb += probability_distribution[threshold] 

        if wb == 0:
            continue

        wf = 1 - wb
        if wf == 0:
            break

        mu_b += threshold * probability_distribution[threshold]
        mean_intensity_background = mu_b / wb

        mean_intensity_foreground = (mu_T - mu_b) / wf

        between_class_variance = wb * wf * (mean_intensity_background - mean_intensity_foreground)**2


        if between_class_variance > max_between_class_variance:
            max_between_class_variance = between_class_variance
            best_threshold = threshold
    
    binarized_image = binary(image, best_threshold)

    return binarized_image

