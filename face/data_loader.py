"""This file contains the functions used to load the data.
Author : Ying Sun"""

import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from sklearn.preprocessing import StandardScaler


def load_data():
    """This function loads the data from the csv files."""
    #We load the train, validation and test data
    df_train = pd.read_csv('splits/train.csv')
    df_val = pd.read_csv('splits/val.csv')
    df_test = pd.read_csv('splits/test.csv')

    #We convert the 'eye_gazing_features' column from string to list
    df_train['face_features'] = df_train['face_features'].apply(eval)
    df_val['face_features'] = df_val['face_features'].apply(eval)
    df_test['face_features'] = df_test['face_features'].apply(eval)

    X_train = np.array(df_train['face_features'].to_list(), dtype=object)
    y_train = np.array(df_train['ASD'])

    X_val = np.array(df_val['face_features'].to_list(), dtype=object)
    y_val = np.array(df_val['ASD'])

    X_test = np.array(df_test['face_features'].to_list(), dtype=object)
    y_test = np.array(df_test['ASD'])
    
    return X_train, y_train, X_val, y_val, X_test, y_test

class FaceDataset(Dataset):
    def __init__(self, X, y, normalize=False):
        self.y = torch.from_numpy(y).long()
        if normalize:
            self.X = [normalize_with_padding(torch.from_numpy(np.array(x)).float()) for x in X]
        else:
            self.X = [torch.from_numpy(np.array(x)).float() for x in X]

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return self.X[index], self.y[index]


def collate_fn(batch):
    X, y = zip(*batch)
    # Assuming X is a list of tensors and y is a list of labels.
    # Pad sequences to the longest in the batch.
    X_padded = pad_sequence(X, batch_first=True, padding_value=0.0)
    y = torch.tensor(y).long()
    # X_lengths could be used if your model needs to know the original lengths.
    X_lengths = torch.tensor([len(x) for x in X])
    return X_padded, y, X_lengths

def get_loader(batch_size=32, normalize=True):
    """This function returns the dataloaders for the train, validation and test data."""
    # Load the data
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    train_dataset = FaceDataset(X_train, y_train)
    test_dataset = FaceDataset(X_test, y_test)
    val_dataset = FaceDataset(X_val, y_val)

    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, collate_fn=collate_fn)

    return train_loader, test_loader, val_loader


def class_weights(train_loader, num_classes=2):
    """This function computes the class weights for the training data to feed into the loss function."""
    # Assume train_loader is your DataLoader
    class_counts = torch.zeros(num_classes)
    # Count the occurrences of each class in the DataLoader
    for _, labels, _ in train_loader:
        class_counts += torch.bincount(labels, minlength=num_classes)
    # Compute the class frequencies and class weights
    class_frequencies = class_counts / class_counts.sum()
    class_weights = 1.0 / (num_classes * class_frequencies)
    # Normalize the class weights
    class_weights /= class_weights.sum()
    return class_weights


def normalize_with_padding(data, padding_value=0):
    """
    Normalizes data considering padding values.
    Args:
        data (torch.Tensor): tensor with the shape (batch_size, seq_length, num_features)
        padding_value (float): the padding value in the data
    Returns:
        torch.Tensor: normalized data
    """
    # Create a mask for non-padded data
    mask = data != padding_value
    # StandardScaler expects a 2D array, reshape your data
    reshaped_data = data[mask].reshape(-1, 1)
    # Fit and transform the data
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(reshaped_data)
    # Reshape the normalized_data to match the shape of data[mask]
    normalized_data = normalized_data.reshape(-1)
    # Replace the non-padded values with the normalized values
    data[mask] = torch.Tensor(normalized_data).to(data.device)
    return data


if __name__ == '__main__':
    train_loader, test_loader, val_loader = get_loader()   
    class_weights = class_weights(train_loader)
    print(class_weights) 

    for X, y, X_lengths in train_loader:
        print(X.shape)
        print(y.shape)
        break