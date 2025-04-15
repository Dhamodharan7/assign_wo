import json
import geopy
import random
import piexif
import datetime
import piexif.helper
import geopy.distance
from datetime import date

addressList = [{"address": "4823 Oak Meadow Dr, Houston, TX 77018",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/houston.png"},
               {"address": "7831 Sunset Trail, Austin, TX 78745",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/austin.png"},
               {"address": "6245 Bluebonnet Ln, Dallas, TX 75209",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/dallas.png"},
               {"address": "3902 Lone Star Pkwy, San Antonio, TX 78253",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/san-antonio.png"},
               {"address": "2184 Prairie Rose St, El Paso, TX 79938",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/el-paso.png"},
               {"address": "1109 Brady Ridge Dr, Round Rock, TX 78681",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/round-rock.png"},
               {"address": "3571 Silver Creek Dr, Arlington, TX 76016",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/arlington.png"},
               {"address": "9214 Pecan Grove Ln, Corpus Christi, TX 78410",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/corpus-christi.png"},
               {"address": "7401 Westwind Blvd, Lubbock, TX 79424",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/lubbock.png"},
               {"address": "4501 Tejas Trail, Austin, TX 78745",
                "map": "https://feldtchaspstg01.blob.core.windows.net/fta-images/maps/austin1.png"}]

gt_coordinate = (33.01691819998306, -96.69424252820593)
order_start_time = ["8:00", "10:00", "11:30", "13:00", "14:30", "16:30"]
order_due_time = ["9:00", "10:30", "12:00", "13:30", "15:30", "17:00"]
order_timeslots = [list(item) for item in zip(order_start_time, order_due_time)]

def fetch_metadata(filename) :
    exif_dict = piexif.load(filename)
    user_comment = piexif.helper.UserComment.load(exif_dict["Exif"][piexif.ExifIFD.UserComment])
    metadata = json.loads(user_comment)
    return metadata

def modify_valid_metadata(imagePath) :    
    order_timeslot_selected = order_timeslots[0] # random.choice(order_timeslots)
    start_time = order_timeslot_selected[0]
    end_time = order_timeslot_selected[1]
    start = datetime.timedelta(hours = int(start_time.split(':')[0]), minutes = int(start_time.split(':')[1]))
    end = datetime.timedelta(hours = int(end_time.split(':')[0]), minutes = int(end_time.split(':')[1]))
    
    random_seconds=random.randint(start.total_seconds(),end.total_seconds())
    random_time=datetime.timedelta(seconds=random_seconds)
    order_time = str(random_time).replace(':' + str(random_time).split(':')[-1], '')
    order_date = str(date.today())
    
    generated_coordinates_1 = random.uniform(33.0155, 33.0175)
    generated_coordinates_2 = random.uniform(-96.6955, -96.6935)
    generated_coordinates = [generated_coordinates_1, generated_coordinates_2]
    order_distance = geopy.distance.geodesic(gt_coordinate, generated_coordinates).m
    order_address = random.choice(addressList)
    
    metadataToInsert = {
        'order_date': order_date,
        'order_time': order_time,
        'order_timeslot' : order_timeslot_selected,
        'order_coordinate': generated_coordinates, 
        'order_distance' : order_distance, 
        'order_address' : order_address['address'],
        'order_map' : order_address['map'],
    }

    try : existant_metadata = fetch_metadata(imagePath)
    except : existant_metadata = {}

    response = {}
    try :
        exif_dict = piexif.load(imagePath)
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(json.dumps(metadataToInsert), encoding="unicode")
        piexif.insert(piexif.dump(exif_dict), imagePath)
        response['status'] = 'Metadata successfully modified.'
        response['existant metadata'] = existant_metadata
        response['updated metadata'] = metadataToInsert
    except Exception as err:
        response['status'] = 'Metadata not modified.'
        response['error occured'] = err
    return response

def modify_invalid_metadata(imagePath) :   
    
    order_timeslot_selected = random.choice(order_timeslots)
    start_time = order_timeslot_selected[0]
    end_time = order_timeslot_selected[1]
    start = datetime.timedelta(hours = int(start_time.split(':')[0]), minutes = int(start_time.split(':')[1]))
    end = datetime.timedelta(hours = int(end_time.split(':')[0]), minutes = int(end_time.split(':')[1]))
    
    random_seconds=random.randint(start.total_seconds(),end.total_seconds())
    random_time=datetime.timedelta(seconds=random_seconds)
    order_time = str(random_time).replace(':' + str(random_time).split(':')[-1], '')
    order_date = str(date.today())
    
    generated_coordinates_1 = random.uniform(33.0155, 33.0175)
    generated_coordinates_2 = random.uniform(-96.6955, -96.6935)
    generated_coordinates = [generated_coordinates_1, generated_coordinates_2]
    order_distance = geopy.distance.geodesic(gt_coordinate, generated_coordinates).m
    order_address = random.choice(addressList)

    invalid_slot = random.choice(['date', 'time', 'location'])
    if invalid_slot == 'date' :  
        if int(order_date.split('-')[-1]) == 1 : order_date = '-'.join([str(int(order_date.split('-')[0])-1)] + order_date.split('-')[1:])
        else : order_date = '-'.join(order_date.split('-')[:-1] + [str(int(order_date.split('-')[-1])-1)])
    if invalid_slot == 'time' : 
        order_hour = random.randint(0, 7)
        order_minute = random.randint(10, 59)
        order_time = '{}:{}'.format(order_hour, order_minute)
    if invalid_slot == 'location' : 
        generated_coordinates_1 = random.uniform(33, 33.015)
        generated_coordinates_2 = random.uniform(-96.69, -96.68)
        generated_coordinates = [generated_coordinates_1, generated_coordinates_2]
        order_distance = geopy.distance.geodesic(gt_coordinate, generated_coordinates).m
        
    metadataToInsert = {
        'order_date': order_date,
        'order_time': order_time,
        'order_timeslot' : order_timeslot_selected,
        'order_coordinate': generated_coordinates, 
        'order_distance' : order_distance, 
        'order_address' : order_address['address'],
        'order_map' : order_address['map'],
    }

    try : existant_metadata = fetch_metadata(imagePath)
    except : existant_metadata = {}

    response = {}
    try :
        exif_dict = piexif.load(imagePath)
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = piexif.helper.UserComment.dump(json.dumps(metadataToInsert), encoding="unicode")
        piexif.insert(piexif.dump(exif_dict), imagePath)
        response['status'] = 'Metadata successfully modified. Metadata validity issue at {}.'.format(invalid_slot)
        response['existant metadata'] = existant_metadata
        response['updated metadata'] = metadataToInsert
    except Exception as err:
        response['status'] = 'Metadata not modified.'
        response['error occured'] = err
    return response