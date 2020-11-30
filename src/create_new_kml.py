#!/usr/bin/python
import os


lat = []
lon = []
alt = []
file_name = raw_input("Name of file")
path = '../files/new/' + file_name + '.txt'
file = open(path, 'r')


kmlfile = "../files/new/"+file_name + '.kml'
kmltemp = '../files/kml/template.kml'

for lines in file:
    lati = lines.split(',')[1]
    loni = lines.split(',')[0]
    alti = lines.split(',')[2]
    lat.append(lati)
    lon.append(loni)
    alt.append(alti)
file.close()


with open(kmltemp, mode="r+", buffering=-1) as kml:
    new_path = open(kmlfile, "w")

    for kmlline in kml.readlines():
        line = kmlline.strip()
        new_path.write(line)
        new_path.write("\n")

        if line == "<!--pathCoords-->":
            for i in range(len(lat)):
                new_path.write(lon[i]+","+lat[i]+","+alt[i])
        if line == "<!--startCoords-->":
            new_path.write(lon[len(lat)-1]+"," +
                           lat[len(lat)-1]+"," + alt[len(lat)-1])

        if line == "<!--endCoords-->":
            new_path.write(lon[0]+","+lat[0]+","+alt[0])
