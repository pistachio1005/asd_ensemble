"""This file contains functions to preprocess the videos.
Author : Marie Huynh"""

import cv2
from loading_s3_data import *
import requests
import os

def video_to_image(signed_url, video_key, path_to_save='../data/frames_data/', fps=1):
    """This function converts a video into a sequence of images and saves it locally.
    Args:
        signed_url (str): Signed URL for the video.
        video_key (str): Key for the video.
        path_to_save (str): Path to save the folder of images.
        fps (int): Frames per second to capture.
    Returns:
        None"""
    # Create the folder to save the images
    modified_video_key = video_key.split('/')[0] + '_' + video_key.split('/')[1]
    final_saving_path = os.path.join(path_to_save, modified_video_key)
    os.makedirs(final_saving_path, exist_ok=True)

    # Download the video file from the signed URL
    response = requests.get(signed_url)
    file_bytes = response.content
    with open('temp_video.mp4', 'wb') as f:
        f.write(file_bytes)

    # Open the downloaded video file
    cap = cv2.VideoCapture('temp_video.mp4')

    # Check if the video opened successfully
    if (cap.isOpened() == False): 
        print("Error opening video file.")

    # Set the video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS) * fps

    # Read until the end of the video file
    i = 0
    count = 0
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        count += 1
        #The function captures a frame every int(cap.get(cv2.CAP_PROP_FPS) / fps) frames 
        # to achieve the desired fps of the output images
        if ret == True and count % int(cap.get(cv2.CAP_PROP_FPS) / fps) == 0:
            # Save the image
            cv2.imwrite(os.path.join(final_saving_path, f'frame{i:04d}.jpg'), frame)
            i += 1
        # Break the loop if the end of the video file is reached
        elif not ret:
            break

    # Release the video capture object and delete the downloaded video file
    cap.release()
    os.remove('temp_video.mp4')

    # Close all windows
    cv2.destroyAllWindows()


def check_rotation(signed_url):
    """This function checks if a video is rotated.
    Args:
        signed_url (str): Signed URL for the video.
    Returns:
        bool: True if the video is rotated, False otherwise."""
    # Load the video using OpenCV
    cap = cv2.VideoCapture(signed_url)
    # Read the first frame
    ret, frame = cap.read()
    # Check if the frame is valid
    if not ret:
        print("Error reading video frame.")
        return False
    # Check if the video is rotated
    if frame.shape[0] > frame.shape[1]:
        # Video is vertically oriented (rotated)
        return True
    else:
        # Video is horizontally oriented (not rotated)
        return False


def split(signed_url, video_key, upload_bucket, fps, upload_folder=''):
    """This function splits a video into frames at a specified frames-per-second rate and uploads them to S3.
    Args:
        signed_url (str): Signed URL for the video.
        video_key (str): Key for the video.
        upload_bucket (str): Name of the bucket where the frames will be uploaded.
        fps (int): Frames per second to capture.
    Returns:
        None"""

    # Create the folder to save the images    
    flipFlag = 0
    if check_rotation(signed_url):
        flipFlag = 1
        print("Video is rotated.")
    
    vidcap = cv2.VideoCapture(signed_url)
    success, image = vidcap.read()

    count = 1  # Start the count at 1
    framerate = int(vidcap.get(cv2.CAP_PROP_FPS))
    frame_interval = round(framerate/fps)  # Calculate frame interval based on desired fps
    print("The framerate is :", framerate)
    print("The frame interval is :", frame_interval)
    temp_file_path = 'data/frames_' + str(video_key)
    os.makedirs(temp_file_path, exist_ok=True)

    while success:
        if count % frame_interval == 0:
            cv2.imwrite(f"{temp_file_path}/frame{count//frame_interval:04d}.jpg", image)  # save frame as JPEG file
            #We add the folder to the key if we want to upload the frames in a specific folder
            if upload_folder != '':
                k = f"{upload_folder}/frames/{video_key}/frame{count//frame_interval:04d}.jpg"
            else:
                k = f"frames/{video_key}/frame{count//frame_interval:04d}.jpg"
            filename = f"{temp_file_path}/frame{count//frame_interval:04d}.jpg"

            upload_bucket.upload_file(filename, k)
            os.remove(filename)

        success, image = vidcap.read()
        if flipFlag:
            image = cv2.flip(image, 0)

        count += 1

    vidcap.release()
    cv2.destroyAllWindows()


def splitallFrames(signed_urls, allFilenames, upload_bucket, fps, upload_folder=''):
    """This function splits the videos into frames and stores them in the S3 bucket 'bmi212marie'.
    Args: 
        signed_urls (list): List of signed urls for the videos.
        allFilenames (list): List of video keys.
        framerates (list): List of frame rates for the videos.
        upload_bucket (str): Name of the bucket where the frames will be uploaded.
        fps (int): Frames per second to capture.
        upload_folder (str): Name of the folder where the frames will be uploaded.
    Returns:
        None"""
    
    for i in range(len(signed_urls)):
        #We get the signed url for the video
        signed_url = signed_urls[i]
        #We get the video key
        file_id = allFilenames[i]
        print(file_id)
        # #We get the frame rate for the video
        # framerate = framerates[i]
        #We split the video into frames and store them in the S3 bucket 'bmi212marie'
        split(signed_url, file_id, upload_bucket, fps, upload_folder)
        print("Video {} uploaded".format(i))



if __name__ == "__main__":
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = loading_credentials()
    client = boto3.client('s3', 
                        aws_access_key_id=AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    resource = boto3.resource('s3', 
                            aws_access_key_id=AWS_ACCESS_KEY_ID, 
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    bucket_name = 'headsup-du1r3b78fy'
    upload_bucket = 'bmi212marie'
    #We get all the signed urls from the csv file
    df_signed = get_signed_urls('headsup-du1r3b78fy', 'starting_dataset_rekognition.csv', time_limit=200000000)
    #df_signed = df_signed[:1]
    print(df_signed)
    #We want to split the videos into frames and store them in the S3 bucket 'bmi212marie'
    #We use multiprocessing to speed up the process
    bucket_name = 'headsup-du1r3b78fy'
    upload_bucket = 'bmi212marie'
    allFilenames = df_signed['video_key'].tolist()
    signed_urls = df_signed['signed_url'].tolist()
    upload_bucket = resource.Bucket(upload_bucket)
    splitallFrames(signed_urls, allFilenames, upload_bucket, 10, upload_folder='Downsampling')


    