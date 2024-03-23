"""This file is used to extract the characteristics of the videos.
Author : Mahdi Honarmand"""

import math


def get_no_face_proportion_1(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 1.00
    
    video_duration = video_data[0]['VideoMetadata']['DurationMillis']
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    timestamps.append(video_duration)

    no_face_duration = 0
    ts1 = 0
    for ts2 in timestamps:
        diff = ts2 - ts1
        if diff > 500:
            no_face_duration += diff - 500
        ts1 = ts2
        
    proportion = no_face_duration/video_duration
    
    return round(proportion, 2)

def get_no_face_proportion_2(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 1.00
        
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
        
    video_duration = video_data[0]['VideoMetadata']['DurationMillis']
 
    proportion = 1.00 - len(set(timestamps))/(math.ceil(video_duration/500)+1)
    
    return round(proportion, 2)

def get_multi_face_proportion_1(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 0.00
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    multi_face_timestamps = []
    for item in timestamps:
        if timestamps.count(item) != 1:
            multi_face_timestamps.append(item)
            
    video_duration = video_data[0]['VideoMetadata']['DurationMillis']
        
    proportion = len(set(multi_face_timestamps)) / (math.ceil(video_duration/500)+1)
    
    return round(proportion, 2)  

def get_multi_face_proportion_2(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
        
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    multi_face_timestamps = []
    for item in timestamps:
        if timestamps.count(item) != 1:
            multi_face_timestamps.append(item)
        
    proportion = len(set(multi_face_timestamps)) / len(set(timestamps))
    
    return round(proportion, 2)  

def get_eyes_closed_proportion(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    proportion = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            if item['Face']['EyesOpen']['Value'] == 'False':
                proportion += 1
            n += 1
            
    if n == 0:
        return 'n=0'        
    proportion /= n
    
    return round(proportion, 2)  

def get_eyes_closed_confidence(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['EyesOpen']['Confidence']
            n += 1
            
    if n == 0:
        return 'n=0'        
    average /= n
    
    return round(average, 1)

def get_average_confidence_1(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    average = 0
    for item in video_data[0]['Faces']:
        timestamp = item['Timestamp']
        if timestamp not in timestamps:
            average += item['Face']['Confidence']
            timestamps.append(timestamp)
            
    if len(timestamps) == 0:
        return 'len(timestamps)=0'
    average /= len(timestamps)
    
    return round(average, 1)

def get_average_confidence_2(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['Confidence']
            n += 1
        
    if n == 0:
        return 'n=0'
    average /= n
    
    return round(average, 1)

def get_average_quality(category, video_data):    # category = 'Sharpness' or 'Brightness'
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    average = 0
    for item in video_data[0]['Faces']:
        timestamp = item['Timestamp']
        if timestamp not in timestamps:
            average += item['Face']['Quality'][category]
            timestamps.append(timestamp)
            
    if len(timestamps) == 0:
        return 'len(timestamps)=0'        
    average /= len(timestamps)
    
    return round(average, 1)

def get_average_pose_1(category, video_data):    # category = 'Pitch', 'Roll', 'Yaw'
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    average = 0
    for item in video_data[0]['Faces']:
        average += item['Face']['Pose'][category]
        
    average /= len(video_data[0]['Faces'])
    
    return round(average, 1)

def get_average_pose_2(category, video_data):    # category = 'Pitch', 'Roll', 'Yaw'
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['Pose'][category]
            n += 1
        
    if n == 0:
        return 'n=0'
    average /= n
    
    return round(average, 1)

def get_age_low(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['AgeRange']['Low']
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return round(average, 1)

def get_age_high(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['AgeRange']['High']
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return round(average, 1)

def get_gender(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            gender = item['Face']['Gender']['Value']
            if gender == 'Male':
                average += 1
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    if average > 0.5:
        return 'Male'
    return 'Female'

def get_gender_confidence(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['Gender']['Confidence']
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return round(average, 1)

def get_eyeglasses(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            eyeglasses = item['Face']['Eyeglasses']['Value']
            if eyeglasses == 'True':
                average += 1
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    if average > 0.5:
        return 'True'
    return 'False'

def get_eyeglasses_confidence(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['Eyeglasses']['Confidence']
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return round(average, 1)

def get_sunglasses(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            sunglasses = item['Face']['Sunglasses']['Value']
            if sunglasses == 'True':
                average += 1
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    if average > 0.5:
        return 'True'
    return 'False'

def get_sunglasses_confidence(video_data):    
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            average += item['Face']['Sunglasses']['Confidence']
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return round(average, 1)

def get_average_size(video_data):
    if len(video_data[0]['Faces']) == 0:
        return 'NA'
    
    timestamps = []
    for item in video_data[0]['Faces']:
        timestamps.append(item['Timestamp'])
    
    average = 0
    n = 0
    for item in video_data[0]['Faces']:
        if timestamps.count(item['Timestamp']) == 1:
            height = item['Face']['BoundingBox']['Height']
            width = item['Face']['BoundingBox']['Width']
            average += height*width
            n += 1
            
    if n == 0:
        return 'n=0'         
    average /= n
    
    return average 