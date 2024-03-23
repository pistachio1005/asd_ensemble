"""This file contains the functions used to engineer the eye gazing features 
Author : Marie Huynh"""

import pandas as pd
import numpy as np

def truncate_confidence(sequence):
    """This function truncates a sequence that has None at the beginning or at the end."""
    #We get the index of the first non None value
    first_non_none_index = sequence.index(next(x for x in sequence if x is not None))
    #We get the index of the last non None value
    last_non_none_index = len(sequence) - sequence[::-1].index(next(x for x in sequence[::-1] if x is not None)) - 1
    #We truncate the sequence
    sequence = sequence[first_non_none_index:last_non_none_index+1]
    return sequence

def truncate_eye_directions(sequence):
    """This function truncates a sequence of eye directions that has [None, None] at the beginning or at the end."""
    #We get the index of the first non [None, None] value
    first_non_none_index = sequence.index(next(x for x in sequence if x != [None, None]))
    #We get the index of the last non [None, None] value
    last_non_none_index = len(sequence) - sequence[::-1].index(next(x for x in sequence[::-1] if x != [None, None])) - 1
    #We truncate the sequence
    sequence = sequence[first_non_none_index:last_non_none_index+1]
    return sequence

def cut_into_windows(row, s):
    """This function cuts the eye_directions and confidences lists into windows of continuous time series with no more than s seconds of
    missing data in between. It returns a list of windows in the column Windows. Each window is a dictionary with the following keys:"""
    
    eye_directions = row['eye_directions']
    confidences = row['confidences']

    eye_directions_windows = []
    confidences_windows = []
    total_confidence_windows = []
    number_of_frames_with_face_windows = []
   
    #We initialize the number of frames with face in the window to 0
    number_of_frames_with_face = 0
    #We initialize the total confidence in the window to 0
    total_confidence = 0
    #We initialize the number of None values in the window to 0
    number_of_consecutive_none = 0
    #We initialize the list of eye directions in the window to []
    eye_directions_window = []
    #We initialize the list of confidences in the window to []
    confidences_window = []
    
    i = 0
    #We iterate through the eye_directions and confidences lists
    while i < len(eye_directions):
        eye_directions_window.append(eye_directions[i])
        confidences_window.append(confidences[i])
        # print(confidences_window)
        #If the eye_directions[i] is not [None, None]
        if eye_directions[i] != [None, None]:
            #We set the number_of_consecutive_none to 0
            number_of_consecutive_none = 0
    
        #If the eye_directions[i] is None
        else:
            #We increment the number of None values in the window
            number_of_consecutive_none += 1
    

        #If the number of None values in the window is greater than s*10
        if number_of_consecutive_none > s*5:

            confidences_window_without_none = [x for x in confidences_window if x is not None]

            #We only append the window if there is at least one non None value in the window
            if len(confidences_window_without_none) != 0:
                #We compute the total confidence in the window
                total_confidence = sum([x for x in confidences_window if x is not None])
                total_confidence = total_confidence/len([x for x in confidences_window if x is not None])
                
                #We compute the number of frames with face in the window
                number_of_frames_with_face = len([x for x in confidences_window if x is not None])

                #We delete truncate the window from the beginning None values and the end None values
                eye_directions_window = truncate_eye_directions(eye_directions_window)
                confidences_window = truncate_confidence(confidences_window)
                
                eye_directions_windows.append(eye_directions_window)
                confidences_windows.append(confidences_window)
                total_confidence_windows.append(total_confidence)
                number_of_frames_with_face_windows.append(number_of_frames_with_face)

            #We reset everything
            number_of_consecutive_none = 0
            eye_directions_window = []
            confidences_window = []
            total_confidence = 0
            number_of_frames_with_face = 0
        
        #If we are at the end of the list, we append the last window
        if i == len(eye_directions) - 1:
            confidences_window_without_none = [x for x in confidences_window if x is not None]

            #We only append the window if there is at least one non None value in the window
            if len(confidences_window_without_none) != 0:
                #We compute the total confidence in the window
                total_confidence = sum([x for x in confidences_window if x is not None])
                total_confidence = total_confidence/len([x for x in confidences_window if x is not None])
                
                #We compute the number of frames with face in the window
                number_of_frames_with_face = len([x for x in confidences_window if x is not None])
                
                #We delete truncate the window from the beginning None values and the end None values
                eye_directions_window = truncate_eye_directions(eye_directions_window)
                confidences_window = truncate_confidence(confidences_window)

                eye_directions_windows.append(eye_directions_window)
                confidences_windows.append(confidences_window)
                total_confidence_windows.append(total_confidence)
                number_of_frames_with_face_windows.append(number_of_frames_with_face)

        i += 1

    #We set the new columns
    row['eye_directions_windows'] = eye_directions_windows
    row['confidences_windows'] = confidences_windows
    row['total_confidence_windows'] = total_confidence_windows
    row['number_of_frames_with_face_windows'] = number_of_frames_with_face_windows

    return row

def select_max_window_size(row):
    """This function selects the max window size for a given video. 
    It returns the updated row."""
    eye_directions_windows = row['eye_directions_windows']
    confidences_windows = row['confidences_windows']
    total_confidence_windows = row['total_confidence_windows']
    number_of_frames_with_face_windows = row['number_of_frames_with_face_windows']

    #We get the index of the max window size
    index_max_window_size = np.argmax(number_of_frames_with_face_windows)
    #We get the max window size
    max_window_size = number_of_frames_with_face_windows[index_max_window_size]
    #We get the eye_directions of the max window size
    eye_directions_max_window_size = eye_directions_windows[index_max_window_size]
    #We get the confidences of the max window size
    confidences_max_window_size = confidences_windows[index_max_window_size]
    #We get the total confidence of the max window size
    total_confidence_max_window_size = total_confidence_windows[index_max_window_size]
    #We get the number of frames with face of the max window size
    number_of_frames_with_face_max_window_size = number_of_frames_with_face_windows[index_max_window_size]

    #We set the new columns
    row['max_window_size'] = max_window_size
    row['eye_directions_max_window_size'] = eye_directions_max_window_size
    row['confidences_max_window_size'] = confidences_max_window_size
    row['total_confidence_max_window_size'] = total_confidence_max_window_size
    row['number_of_frames_with_face_max_window_size'] = number_of_frames_with_face_max_window_size

    return row


def add_NT_rows(df):
    """This function creates a final dataset with more rows for NT children."""
    df_final = pd.DataFrame(columns=df.columns)
    #We only keep the columns that we need
    df_final = df_final[['video_key', 'ASD', 'child_id', 'age', 'gender', 'eye_directions', 'confidences', 'total_confidence', 'number_of_frames_with_face']]

    for i in range(len(df)):
        label = df.iloc[i]['ASD']
        #If the label is 0 (NT)
        if (label == 0) :
            #For each window of more than 20 seconds of eye direction data, we create a new row
            eye_directions_windows = df['eye_directions_windows'][i] 
            confidences_windows = df['confidences_windows'][i]
            total_confidence_windows = df['total_confidence_windows'][i]
            number_of_frames_with_face_windows = df['number_of_frames_with_face_windows'][i]

            for eye_dir, conf, total_conf, nb_frames_face in zip(eye_directions_windows, confidences_windows, total_confidence_windows, number_of_frames_with_face_windows):
                #If the window is more than 20 seconds of eye direction data
                if nb_frames_face > 20*5:
                    #We create a new row
                    # Create a new row as a dictionary
                    new_row = {
                        'video_key': [df.at[i, 'video_key']],
                        'ASD': [df.at[i, 'ASD']],
                        'child_id': [df.at[i, 'child_id']],
                        'age': [df.at[i, 'age']],
                        'gender': [df.at[i, 'gender']],
                        'eye_directions': [eye_dir],
                        'confidences': [conf],
                        'total_confidence': [total_conf],
                        'number_of_frames_with_face': [nb_frames_face]
                    }
                    new_df = pd.DataFrame(new_row, index=[0])
                    
                    #We append the new row to the dataframe
                    df_final = pd.concat([df_final, new_df], ignore_index=True)

        #If the label is 1 (ASD)
        else:
            #We append the row with the max window size to the dataframe
            new_row = pd.DataFrame({
                'video_key': [df.at[i, 'video_key']],
                'ASD': [df.at[i, 'ASD']],
                'child_id': [df.at[i, 'child_id']],
                'age': [df.at[i, 'age']],
                'gender': [df.at[i, 'gender']],
                'eye_directions': [df.at[i, 'eye_directions_max_window_size']],
                'confidences': [df.at[i, 'confidences_max_window_size']],
                'total_confidence': [df.at[i, 'total_confidence_max_window_size']],
                'number_of_frames_with_face': [df.at[i, 'number_of_frames_with_face_max_window_size']]
            })
            new_df = pd.DataFrame(new_row, index=[0])
            #We concatenate the new row to the dataframe
            df_final = pd.concat([df_final, new_df], ignore_index=True)
    return df_final

