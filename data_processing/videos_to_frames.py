"""This file is used to convert videos to frames which will be used to test the AWS vision API.
Author: Marie Huynh"""
import cv2
from loading_s3_data import *
import requests
import os
from video_preprocessing import *
import concurrent.futures
import json
import boto3

def process_video(signed_url, filename, upload_bucket):
    """Process a single video."""
    splitallFrames([signed_url], [filename], upload_bucket, fps=10, upload_folder='Downsampling')
    print("Video uploaded: {}".format(filename))

def process_videos_in_thread(thread_id, signed_urls, filenames, upload_bucket):
    for i in range(thread_id, len(signed_urls), 5):
        signed_url = signed_urls[i]
        filename = filenames[i]
        process_video(signed_url, filename, upload_bucket)
        print(f"Thread {thread_id}: Video {filename} uploaded")

if __name__ == "__main__":
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = loading_credentials()
    client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket_name = 'headsup-du1r3b78fy'
    upload_bucket = 'bmi212marie'

    # We get all the signed URLs from the CSV file
    df_signed = get_signed_urls('headsup-du1r3b78fy', 'finish.csv', time_limit=200000000)

    # We want to split the videos into frames and store them in the S3 bucket 'bmi212marie'

    # We define the videos we want to split
    df_signed = df_signed
    video_keys = df_signed['video_key'].tolist()

    # We select the signed URLs for which the column 'video_key' is in video_keys
    allFilenames = df_signed[df_signed['video_key'].isin(video_keys)]['video_key'].tolist()
    signed_urls = df_signed[df_signed['video_key'].isin(video_keys)]['signed_url'].tolist()
    upload_bucket = resource.Bucket(upload_bucket)

    # Create a ThreadPoolExecutor with 5 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Launch threads to process videos
        futures = [executor.submit(process_videos_in_thread, thread_id, signed_urls, allFilenames, upload_bucket) for thread_id in range(5)]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

