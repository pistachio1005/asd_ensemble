"""This file contains the functions used to split the data into training, validation and testing sets.
Author: Marie Huynh"""

import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold


def split_train_val_test(df, random_state=42):
    """Splits the data into training, validation and testing sets.
    :return: the training, validation and testing sets
    """
    # Get unique IDs and split them
    unique_ids = df['child_id'].unique()
    train_ids, test_ids = train_test_split(unique_ids, test_size=0.2, random_state=random_state)
    train_ids, val_ids = train_test_split(train_ids, test_size=0.2, random_state=random_state)

    # Split the dataframe based on IDs
    train_df = df[df['child_id'].isin(train_ids)]
    test_df = df[df['child_id'].isin(test_ids)]
    val_df = df[df['child_id'].isin(val_ids)]

    return train_df, val_df, test_df


def split_train_test(df, test_size, random_state=42):
    """Splits the data into training and testing sets.
    :return: the training and testing sets
    """
    # Get unique IDs and split them
    unique_ids = df['child_id'].unique()
    train_ids, test_ids = train_test_split(unique_ids, test_size=test_size, random_state=random_state)

    # Split the dataframe based on IDs
    train_df = df[df['child_id'].isin(train_ids)]
    test_df = df[df['child_id'].isin(test_ids)]

    return train_df, test_df


def create_custom_folds(df, n_splits=5, random_state=None):
    """
    Create folds for cross-validation on the dataframe ensuring no leakage of the specified child_id.

    Parameters:
    df (DataFrame): The dataframe to create folds from.
    n_splits (int): Number of folds for cross-validation.
    random_state (int): Controls the shuffling applied to the data before applying the split.

    Returns:
    list: A list of tuples, where each tuple contains the training set and the validation set DataFrames for each fold.
    """

    # Get unique IDs and create KFold object
    unique_ids = df['child_id'].unique()
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    # Initialize list to store the folds
    folds = []

    # Create folds
    for train_index, val_index in kf.split(unique_ids):
        # Split the IDs into training and validation sets
        train_ids, val_ids = unique_ids[train_index], unique_ids[val_index]

        # Create training and validation data based on IDs
        train_df = df[df['child_id'].isin(train_ids)]
        val_df = df[df['child_id'].isin(val_ids)]

        folds.append((train_df, val_df))

    return folds

 

