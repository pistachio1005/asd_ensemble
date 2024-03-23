"""This file contains the functions for the analysis of the eye gaze data.
Author : Marie Huynh"""

#We import the libraries we need
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_yaw_pitch(eye_directions_features, confidences, output_file):
    """This function plots a figure of the evolution of yaw and pitch over time for a given video. 
    Each dot represents a frame. The color of the dot is the confidence of the eye direction estimation.
    The figure contains two subplots, one above the other. The first subplot is the evolution of yaw over time.
    The second subplot is the evolution of pitch over time. """

    #We replace all the None values by -30 and 0 for confidence
    eye_directions_features = [[-50, -50] if element is None else element for element in eye_directions_features]
    confidences = [0 if element is None else element for element in confidences]

    # We get the yaw and pitch values for the video
    yaw = np.array([element[0] for element in eye_directions_features])
    pitch = np.array([element[1] for element in eye_directions_features])

    # We get the confidence values for the video
    confidence = np.array(confidences)

    # We create a figure
    plt.figure(figsize=(10, 10))

    # We create the first subplot
    plt.subplot(2, 1, 1)
    #We want the dots to be a bit smaller and want to see the multiple dots
    sc = plt.scatter(range(len(yaw)), yaw, c=confidence, cmap='RdYlGn', s=1)
    plt.title('Yaw')
    plt.xlabel('Frame')
    plt.ylabel('Yaw')
    # We add the colorbar on the right of the whole figure
    cbar = plt.colorbar(sc, orientation='vertical')
    cbar.set_label('Confidence')
    # We create the second subplot
    plt.subplot(2, 1, 2)
    sc = plt.scatter(range(len(pitch)), pitch, c=confidence, cmap='RdYlGn')
    plt.title('Pitch')
    plt.xlabel('Frame')
    plt.ylabel('Pitch')

    # We add the colorbar on the right of the whole figure
    cbar = plt.colorbar(sc, orientation='vertical')
    cbar.set_label('Confidence')

    plt.show()

    if output_file is not None:
        # Save the figure to the specified PDF file
        plt.savefig(output_file, format='pdf')
        plt.close()


def get_yaw(eye_directions_features):
    """This function returns the yaw values for a given video. """

    # We get the yaw values for the video
    yaw = np.array([element[0] for element in eye_directions_features])

    return yaw

def get_pitch(eye_directions_features):
    """This function returns the pitch values for a given video. """

    # We get the pitch values for the video
    pitch = np.array([element[1] for element in eye_directions_features])

    return pitch

def get_yaw_pitch_statistics(eye_directions_features, confidences):
    """This function returns the statistics of the yaw and pitch values for a given video. 
    The statistics are the mean, standard deviation, minimum and maximum values. """

    # We replace all the None values by -30 and 0 for confidence
    eye_directions_features = [[-50, -50] if element is None else element for element in eye_directions_features]
    confidences = [0 if element is None else element for element in confidences]

    # We get the yaw and pitch values for the video
    yaw = np.array([element[0] for element in eye_directions_features])
    pitch = np.array([element[1] for element in eye_directions_features])

    # We get the statistics for yaw
    yaw_mean = np.mean(yaw)
    yaw_std = np.std(yaw)
    yaw_min = np.min(yaw)
    yaw_max = np.max(yaw)

    # We get the statistics for pitch
    pitch_mean = np.mean(pitch)
    pitch_std = np.std(pitch)
    pitch_min = np.min(pitch)
    pitch_max = np.max(pitch)

    print("Yaw mean: ", yaw_mean)
    print("Yaw standard deviation: ", yaw_std)
    print("Yaw minimum: ", yaw_min)
    print("Yaw maximum: ", yaw_max)
    print("Pitch mean: ", pitch_mean)
    print("Pitch standard deviation: ", pitch_std)
    print("Pitch minimum: ", pitch_min)
    print("Pitch maximum: ", pitch_max)

    return yaw_mean, yaw_std, yaw_min, yaw_max, pitch_mean, pitch_std, pitch_min, pitch_max
