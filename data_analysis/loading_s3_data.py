"""This file contains utils functions to load data from the S3 bucket.
Author : Marie Huynh"""
import os
import boto3
from boto3 import session
import configparser
import pandas as pd


def loading_credentials():
    """This function loads the credentials from the config file.
    Args:
        None
    Returns:
        AWS_ACCESS_KEY_ID (str): AWS access key id.
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key."""
    #We load the information from the config file
    #Define your crendentials
    config_path = os.path.abspath('../AWS/config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    AWS_ACCESS_KEY_ID = config['AWS']['ACCESS_KEY']
    AWS_SECRET_ACCESS_KEY = config['AWS']['SECRET_KEY']
    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

def connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    """This function define the client session and the client connection.
    Args:
        AWS_ACCESS_KEY_ID (str): AWS access key id.
        AWS_SECRET_ACCESS_KEY (str): AWS secret access key.    
    Returns:
        session (boto3.session.Session): Client session.
        s3_client (boto3.client): Client connection."""
    #Define the client session
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    #Define the client connection
    s3 = 's3'
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    return session, s3_client

def download_s3_data(bucket_name, file_name, new_file_name):
    """This function loads the data from the S3 bucket.
    Args:
        bucket_name (str): Name of the bucket where the data is stored.
        file_name (str): Name of the file to download.
        new_file_name (str): Name of the file once downloaded.
    Returns:
        None"""
    #We load the information from the config file
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = loading_credentials()

    #Define the client session and the client connection
    session, s3_client = connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    # Download the file from S3 and save it locally
    s3_client.download_file(bucket_name, file_name, new_file_name)


def get_signed_urls(s3_bucket_name, dataset_path, time_limit = 600):
    """This functions gets the signed urls from the s3 bucket for all videos in a given dataset path.
    Args:
        s3_bucket_name (str): Name of the s3 bucket.
        dataset_path (str): Path to the dataset.
        time_limit (int): Time limit for the signed url."""
    #Load the information from the config file
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = loading_credentials()

    #Define the client session and the client connection
    session, s3_client = connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    #Read the dataset form the dataset path
    df = pd.read_csv(dataset_path)

    #Get the list of all videos keys in the dataset
    videos_keys = df["video_key"].tolist()

    #Generate the signed url for each video key
    for key in videos_keys:
        url = s3_client.generate_presigned_url('get_object', 
                                       Params = {'Bucket': s3_bucket_name, 'Key': key}, 
                                       ExpiresIn = time_limit) #this url will be available for time_limit seconds
        df.loc[df['video_key'] == key, 'signed_url'] = url

    return df

if __name__ == "__main__":
    #Define the bucket name and the dataset path
    bucket_name = 'headsup-du1r3b78fy'
    dataset_path = "dataset_1.csv"

    #Get the signed urls for all videos in the dataset
    df_signed_urls = get_signed_urls(bucket_name, dataset_path)

    print(df_signed_urls.head())
    
