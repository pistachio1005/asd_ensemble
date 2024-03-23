"""This file contains the functions used to resample the videos."""

import random
import pandas as pd

def make_dict_child_videos(df):
    """This function creates a dictionary mapping a child id to all its video keys.
    Args:
        df (pandas DataFrame): The dataframe containing the videos.
    Returns:
        dict_child_videos (dictionary): The dictionary mapping a child id to its video keys."""
    # We create a dictionary mapping a child id to the number of videos
    dict_child_videos = {}
    # We iterate through the dataframe
    for index, row in df.iterrows():
        video_key = row['video_key']
        child_id = row['child_id']
        # If the child id is not in the dictionary, we add it
        if child_id not in dict_child_videos:
            dict_child_videos[child_id] = [video_key]
        # Otherwise, we append the video key to the list
        else:   
            dict_child_videos[child_id].append(video_key)
    return dict_child_videos


def upsample(df):
    """This function upsamples the minority class (NT). We follow Nick Deveau's algorithm.
    Args:
        df (pandas DataFrame): The dataframe containing the videos."""
    d = make_dict_child_videos(df)
    # We create a list of the child ids whose ASD label is 0
    list_child_id_0 = df[df['ASD'] == 0]['child_id'].unique()
    print(list_child_id_0)
    # For each child id in the list, we upsample the videos
    for child_id in list_child_id_0:
        # We get the number of videos for this child id
        num_videos = len(d[child_id])
        # If the number of videos is less than 10, we upsample the videos without replacement from V (i)
        if num_videos <= 10:
            # We get the video keys for this child id
            list_video_keys = d[child_id]
            # We upsample the videos without replacement from V(i)
            if len(list_video_keys) == 1:
                list_video_keys_upsampled = random.sample(list_video_keys, 1)
            else : 
                list_video_keys_upsampled = random.sample(list_video_keys, 2)
            # We append the upsampled videos to the dataframe
            for video_key in list_video_keys_upsampled:
                df = df.append(df[df['video_key'] == video_key], ignore_index=True)
        # Otherwise, we upsample the videos with replacement from V (i)
        else:
            # We get the video keys for this child id
            list_video_keys = d[child_id]
            # We upsample the videos with replacement from V (i)
            list_video_keys_upsampled = random.choices(list_video_keys, k=2)
            # We append the upsampled videos to the dataframe
            for video_key in list_video_keys_upsampled:
                df = df.append(df[df['video_key'] == video_key], ignore_index=True)
    return df


if __name__ == "__main__":
    # We read the dataframe
    df = pd.read_csv("../data/Constructed Dataset/constructed_dataset.csv")
    # We upsample the dataframe
    df_upsampled = upsample(df)
    # We save the dataframe
    print(df_upsampled)
    print("Done!")