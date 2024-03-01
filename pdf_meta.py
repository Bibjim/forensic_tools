#!/usr/bin/env python3
# coding:utf8

import PyPDF2
import argparse
import re
import exifread


def get_pdf_meta(file_name):
    pdf_file = PyPDF2.PdfFileReader(open(file_name, "rb"))
    doc_info = pdf_file.getDocumentInfo()
    for info in doc_info:
        print("[+] " + info + " " + doc_info[info])


def get_strings(file_name):
    with open(file_name, "rb") as file:
        content = file.read()
    _re = re.compile("[\S\s]{4,}")
    for match in _re.finditer(content.decode("utf8", "backslashreplace")):
        print(match.group())


def _convert_to_degress(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def get_exif_gps_data(file_name):
    with open(file_name, "rb") as file:
        exif = exifread.process_file(file)
    if not exif:
        print("Aucune métadonnée EXIF")
    else:
        latitude = exif.get("GPS GPSLatitude")
        latitude_ref = exif.get("GPS GPSLatitudeRef")
        longitude = exif.get("GPS GPSLongitude")
        longitude_ref = exif.get("GPS GPSLongitudeRef")
        if latitude and longitude and latitude_ref and longitude_ref:
            lat = _convert_to_degress(latitude)
            long = _convert_to_degress(longitude)
            if str(latitude_ref) != "N":
                lat = 0 - lat
            if str(longitude_ref) != "E":
                long = 0 - long
            print("Latitude: " + str(latitude_ref) + " " + str(lat))
            print("Longitude: " + str(longitude_ref) + " " + str(long))
            print("http://maps.google.com/maps?q=loc:%s,%s" % (str(lat), str(long)))


def get_exif(file_name):
    with open(file_name, "rb") as file:
        exif = exifread.process_file(file)
    if not exif:
        print("Aucune métadonnée EXIF")
    else:
        for tag in exif.keys():
            print(tag + " " + str(exif[tag]))


parser = argparse.ArgumentParser(description="Forensic tool PDF")
parser.add_argument("-pdf", dest="pdf", help="FilePath PDF", required=False)
parser.add_argument("-str", dest="str", help="FilePath strings contents", required=False)
parser.add_argument("-exif", dest="exif", help="FilePath images for exif métadata", required=False)
parser.add_argument("-gps", dest="gps", help="FilePath images for gps data", required=False)
args = parser.parse_args()

if args.pdf:
    get_pdf_meta(args.pdf)

if args.str:
    get_strings(args.str)

if args.exif:
    get_exif(args.exif)

if args.gps:
    get_exif_gps_data(args.gps)
