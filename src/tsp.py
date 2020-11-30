#!/usr/bin/python
from fastkml import kml
from tsp_solver.greedy import solve_tsp
import geopy.distance

default_altitude = 5


answer1 = input('Enter the altitude at which pictures will be taken: ')


if not answer1:
    # In that case, use the default value
    altitude = default_altitude
else:
    altitude = float(answer1)
    if altitude < 1:
        altitude = 1
    elif altitude > 100:
        altitude = 100


# Define Hoverspeed parameter

default_HoverSpeed = 5

answer2 = 1

# Check if user pressed an empty character
if not answer2:
    # In that case, use the default value
    HoverSpeed = default_HoverSpeed
else:
    HoverSpeed = float(answer2)
    if HoverSpeed < 1:
        HoverSpeed = 1
    elif HoverSpeed > 5:
        HoverSpeed = 5


# Define hold parameter

default_hold = 2

answer3 = 1

# Check if user pressed an empty character
if not answer3:
    # In that case, use the default value
    hold = default_hold
else:
    hold = float(answer3)
    if hold < 0:
        hold = 0
    elif hold > 60:
        hold = 60


path = "../files/kml/"
filename = raw_input('Enter the name of the input kml: ')
file = filename
filename = path+filename+'.kml'


try:
    if ".kml" not in filename:
        raise ImportError
except ImportError:
    raise Exception("Kml file wasn't imported correctly")


with open(filename, 'rt', 8) as kmlFile:
    tmpKml = kmlFile.read().encode()

importedKml = kml.KML()
importedKml.from_string(tmpKml)
kmlFeatures = list(importedKml.features())

features = []

features = list(kmlFeatures[0].features())

try:
    if len(features) == 0:
        raise EOFError
except EOFError:
    raise Exception('End of file without reading any features')


coordinates = []


for i in range(len(features)):
    temp_tuple = tuple([features[i].geometry.x, features[i].geometry.y])
    coordinates.append(temp_tuple)


start_point = 0
initial_point = (coordinates[0][0], coordinates[0][1])
print initial_point
end_point = len(coordinates) - 1


def TSP(coords, start, end):

    ##########Calculate points' distances using geodesic function  FOR TSP_SOLVER #################

    distances_matrix = []

    for i in range(len(coords)):

        temp_list = []

        for j in range(i+1):

            distance = (geopy.distance.geodesic(coords[i], coords[j]).km)

            temp_list.append(distance)

        distances_matrix.append(temp_list)

    path = solve_tsp(distances_matrix, endpoints=(start, end))

    # Returns indices of points in the right order
    return path


##########Create dictionary of points based on the calculated route via TSP function #################
# Initialise dictionary
flight_points = {}


# Take_off point is assigned as the first dictionary point

flight_points[0] = coordinates[0]


# Initial Point is assigned as the second dictionary point

flight_points[len(coordinates)] = initial_point


#   Call TSP function only if the number of Sampling points is less than max_sampling_points00

max_sampling_points = 5000

if len(coordinates) < max_sampling_points:

    # Create new list ommitting first two points(Take-off and Initial points)
    #sampling_list = coordinates[2:]

    # Call TSP function passing the new list
    print("Applying greedy tsp solver")

    points_indices = TSP(coordinates, start_point, end_point)

    print("tsp completed")

    # Append the rest of the points to the dictionary
    for i, el in enumerate(points_indices):
        if i >= 1:
            flight_points[el] = coordinates[el]
else:
    # Just pass all points to the dictionary as they were imported from the kml
    for i, point in enumerate(coordinates):

        if i > 1:
            flight_points[i] = point


export_path = '../files/new/' + file + ".txt"


file = open(export_path, 'w')


for i in range(len(coordinates)):
    file.write(str(coordinates[points_indices[i]][0]))
    file.write(',')
    file.write(str(coordinates[points_indices[i]][1]))
    file.write(',')
    file.write(str(answer1))
    file.write('\n')
