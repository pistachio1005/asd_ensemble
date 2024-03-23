"""This file contains code to analyze the dataset. It is not used in the training or evaluation of the model."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def asd_children_statistics(df):
    """This file returns the number of children with ASD and the number of children without ASD in a dataset.
    Args:
        df (pandas.DataFrame): Dataframe containing the data.
    Returns:
        dict: Dictionary containing the number of children and the number of videos with ASD and 
        the number of children and the number of videos without ASD and the ratios of ASD vs Non-ASD."""
    # Get the number of children with ASD
    asd_children = df[df['ASD'] == 1]['child_id'].unique()
    # Get the number of children without ASD
    non_asd_children = df[df['ASD'] == 0]['child_id'].unique()
    # Get the number of videos with ASD
    asd_videos = df[df['ASD'] == 1]['video_key']
    # Get the number of videos without ASD
    non_asd_videos = df[df['ASD'] == 0]['video_key']
    #Get the ratio of videos with ASD/videos without ASD
    #ratio_children = len(asd_children)/len(non_asd_children)
    ratio_videos = len(asd_videos)/len(non_asd_videos)
    return {'Number of children with ASD': len(asd_children), 'Number of videos with ASD': len(asd_videos),
            'Number of children without ASD': len(non_asd_children), 'Number of videos without ASD': len(non_asd_videos), 
            'Ratio of videos with ASD/children without ASD': ratio_videos}



def get_graph_asd_children(df_train, df_val, df_test):
    """This function generates two bar plots : one of the number of children across the datasets and one
    of the number of videos across the datasets.
    Args:
        df_train (pandas.DataFrame): Dataframe containing the train data.
        df_val (pandas.DataFrame): Dataframe containing the validation data.
        df_test (pandas.DataFrame): Dataframe containing the test data.
    Returns:
        None"""
    
    #We create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    #We create two pie plots
    train_stats = asd_children_statistics(df_train)
    val_stats = asd_children_statistics(df_val)
    test_stats = asd_children_statistics(df_test)
    children_ASD_train = train_stats['Number of children with ASD']
    children_non_ASD_train = train_stats['Number of children without ASD']
    children_ASD_val = val_stats['Number of children with ASD']
    children_non_ASD_val = val_stats['Number of children without ASD']
    children_ASD_test = test_stats['Number of children with ASD']
    children_non_ASD_test = test_stats['Number of children without ASD']
    #We create a bar plot for the number of children
    ax1.bar(['Train', 'Val', 'Test'], [children_ASD_train, children_ASD_val, children_ASD_test], color='blue')
    ax1.bar(['Train', 'Val', 'Test'], [children_non_ASD_train, children_non_ASD_val, children_non_ASD_test], bottom=[children_ASD_train, children_ASD_val, children_ASD_test], color='orange')
    ax1.set_title('Number of children')
    ax1.legend(['ASD', 'Non ASD'])
    #We create a bar plot for the number of videos
    videos_ASD_train = train_stats['Number of videos with ASD']
    videos_non_ASD_train = train_stats['Number of videos without ASD']
    videos_ASD_val = val_stats['Number of videos with ASD']
    videos_non_ASD_val = val_stats['Number of videos without ASD']
    videos_ASD_test = test_stats['Number of videos with ASD']
    videos_non_ASD_test = test_stats['Number of videos without ASD']
    ax2.bar(['Train', 'Val', 'Test'], [videos_ASD_train, videos_ASD_val, videos_ASD_test], color='blue')
    ax2.bar(['Train', 'Val', 'Test'], [videos_non_ASD_train, videos_non_ASD_val, videos_non_ASD_test], bottom=[videos_ASD_train, videos_ASD_val, videos_ASD_test], color='orange')
    ax2.set_title('Number of videos')
    ax2.legend(['ASD', 'Non ASD'])
    plt.show()



def get_graph_asd_children_without_val(df_train, df_test):
    """This function generates two bar plots : one of the number of children across the datasets and one
    of the number of videos across the datasets.
    Args:
        df_train (pandas.DataFrame): Dataframe containing the train data.
        df_val (pandas.DataFrame): Dataframe containing the validation data.
        df_test (pandas.DataFrame): Dataframe containing the test data.
    Returns:
        None"""
    
    #We create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    #We create two pie plots
    train_stats = asd_children_statistics(df_train)
    test_stats = asd_children_statistics(df_test)
    children_ASD_train = train_stats['Number of children with ASD']
    children_non_ASD_train = train_stats['Number of children without ASD']
    children_ASD_test = test_stats['Number of children with ASD']
    children_non_ASD_test = test_stats['Number of children without ASD']
    #We create a bar plot for the number of children
    ax1.bar(['Train', 'Test'], [children_ASD_train, children_ASD_test], color='blue')
    ax1.bar(['Train', 'Test'], [children_non_ASD_train, children_non_ASD_test], bottom=[children_ASD_train, children_ASD_test], color='orange')
    ax1.set_title('Number of children')
    ax1.legend(['ASD', 'Non ASD'])
    #We create a bar plot for the number of videos
    videos_ASD_train = train_stats['Number of videos with ASD']
    videos_non_ASD_train = train_stats['Number of videos without ASD']
    videos_ASD_test = test_stats['Number of videos with ASD']
    videos_non_ASD_test = test_stats['Number of videos without ASD']
    ax2.bar(['Train', 'Test'], [videos_ASD_train, videos_ASD_test], color='blue')
    ax2.bar(['Train', 'Test'], [videos_non_ASD_train, videos_non_ASD_test], bottom=[videos_ASD_train, videos_ASD_test], color='orange')
    ax2.set_title('Number of videos')
    ax2.legend(['ASD', 'Non ASD'])
    plt.show()