# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 15:10:44 2022

@author: rgilland
"""

import os
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

filepath = os.environ['USERPROFILE'] + "/Dropbox (Harvard University)/econ_api/"

def read_url(url, ftype=".zip"):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    files = []
    for i in x:
        file_name = i.extract().get_text()
        if ftype in file_name:
            files.append(i.extract().get_text())
    return files

state_abbrev = [
    "al",
    "ak",
    "az",
    "ar",
    "ca",
    "co",
    "ct",
    "de",
    "dc",
    "fl",
    "ga",
    "hi",
    "id",
    "il",
    "in",
    "ia",
    "ks",
    "ky",
    "la",
    "me",
    "md",
    "ma",
    "mi",
    "mn",
    "ms",
    "mo",
    "mt",
    "ne",
    "nv",
    "nh",
    "nj",
    "nm",
    "ny",
    "nc",
    "nd",
    "oh",
    "ok",
    "or",
    "pa",
    "pr",
    "ri",
    "sc",
    "sd",
    "tn",
    "tx",
    "ut",
    "vt",
    # "vi",
    "va",
    "wa",
    "wv",
    "wi",
    "wy"
]

download = {
    'dl_csub_2010': 0,
    'dl_csub_2019': 0,
    'dl_block_2019': 0,
    'dl_od_pri_pri_10': 0,
    'dl_od_10': 0,
    'dl_od_primary_10': 0,
    'dl_od_20': 0,
    'dl_od_primary_20': 0,
    'dl_wac_10': 0,
    'dl_wac_20': 1,
    'dl_rac_10': 0,
    'dl_rac_20': 0,
    'dl_xwalk_st': 0,
    'dl_xwalk': 0,
    'dl_csub_shp_21': 0,
    'dl_csub_shp_22': 0,
    'dl_tract_shp_21': 0
}

if download['dl_csub_2010'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2010/COUSUB/2010/"
    files = read_url(url)
    for file in files:
        if len(file) > 23:
            continue
        else:
            with open(filepath + "shapefiles/county_subdivision/" + file, 'wb') as out_file:
                content = requests.get(url + file, stream=True).content
                out_file.write(content)

if download['dl_csub_2019'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2019/COUSUB/"
    files = read_url(url)
    for file in files:
        with open(filepath + "shapefiles/county_subdivision/" + file, 'wb') as out_file:
            content = requests.get(url + file, stream=True).content
            out_file.write(content)

if download['dl_block_2019'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2019/TABBLOCK/"
    files = read_url(url)
    for file in files:
        with open(filepath + "shapefiles/block/" + file, 'wb') as out_file:
            content = requests.get(url + file, stream=True).content
            out_file.write(content)

if download['dl_od_10'] == 1:
    existing_files = os.listdir(filepath + "lodes/od/2010/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES7/" + state + "/od/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            print("Downloading", file + ".")
            with open(filepath + "lodes/od/2010/" + file, 'wb') as out_file:
                content = requests.get(url + file, stream=True).content
                out_file.write(content)

if download['dl_od_pri_pri_10'] == 1:
    existing_files = os.listdir(filepath + "lodes/od/2010/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES7/" + state + "/od/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            if "JT01" in file:
                print("Downloading", file + ".")
                with open(filepath + "lodes/od/2010/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_od_primary_10'] == 1:
    existing_files = os.listdir(filepath + "lodes/od/2010/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES7/" + state + "/od/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            if "JT01" in file or "JT03" in file or "JT05" in file:
                print("Downloading", file + ".")
                with open(filepath + "lodes/od/2010/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_od_20'] == 1:
    existing_files = os.listdir(filepath + "lodes/od/2020/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES8/" + state + "/od/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            print("Downloading", file + ".")
            with open(filepath + "lodes/od/2020/" + file, 'wb') as out_file:
                content = requests.get(url + file, stream=True).content
                out_file.write(content)

if download['dl_od_primary_20'] == 1:
    existing_files = os.listdir(filepath + "lodes/od/2020/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES8/" + state + "/od/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            if "JT01" in file or "JT03" in file or "JT05" in file:
                print("Downloading", file + ".")
                with open(filepath + "lodes/od/2020/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_wac_10'] == 1:
    existing_files = os.listdir(filepath + "lodes/wac/2010/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES7/" + state + "/wac/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            print("Downloading", file + ".")
            with open(filepath + "lodes/wac/2010/" + file, 'wb') as out_file:
                content = requests.get(url + file, stream=True).content
                out_file.write(content)

if download['dl_wac_20'] == 1:
    existing_files = os.listdir(filepath + "lodes/wac/2020/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES8/" + state + "/wac/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            if "S000_JT01" in file and "2019" in file:
                print("Downloading", file + ".")
                with open(filepath + "lodes/wac/2020/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_rac_10'] == 1:
    existing_files = os.listdir(filepath + "lodes/rac/2010/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES7/" + state + "/rac/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            print("Downloading", file + ".")
            if "S000" in file and ("JT01" in file or "JT03" in file or "JT05" in file):
                with open(filepath + "lodes/rac/2010/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_rac_20'] == 1:
    existing_files = os.listdir(filepath + "lodes/rac/2020/")
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES8/" + state + "/rac/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            if file in existing_files:
                print(file, "already present.")
                continue
            print("Downloading", file + ".")
            # if "S000" in file and ("JT01" in file or "JT03" in file or "JT05" in file):
            if "S000" in file and "JT01" in file and "2019" in file:
                with open(filepath + "lodes/rac/2020/" + file, 'wb') as out_file:
                    content = requests.get(url + file, stream=True).content
                    out_file.write(content)

if download['dl_xwalk_st'] == 1:
    for state in state_abbrev:
        url = "https://lehd.ces.census.gov/data/lodes/LODES8/" + state + "/"
        files = read_url(url, "csv.gz")
        
        for file in files:
            with open(filepath + "lodes/xwalk/" + file, 'wb') as out_file:
                content = requests.get(url + file, stream=True).content
                out_file.write(content)

if download['dl_xwalk'] == 1:
    url = "https://lehd.ces.census.gov/data/lodes/LODES8/us/us_xwalk.csv.gz"
    with open(filepath + "lodes/xwalk/us_xwalk.csv.gz", 'wb') as out_file:
        content = requests.get(url, stream=True).content
        out_file.write(content)

if download['dl_csub_shp_21'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2021/COUSUB/"
    files = read_url(url, "zip")
    
    for file in files:
        with open(filepath + "shapefiles/" + file, 'wb') as out_file:
            content = requests.get(url + file, stream=True).content
            out_file.write(content)

if download['dl_csub_shp_22'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2022/COUSUB/"
    files = read_url(url, "zip")
    
    for file in files:
        with open(filepath + "shapefiles/" + file, 'wb') as out_file:
            content = requests.get(url + file, stream=True).content
            out_file.write(content)

if download['dl_tract_shp_21'] == 1:
    url = "https://www2.census.gov/geo/tiger/TIGER2021/TRACT/"
    files = read_url(url, "zip")
    
    for file in files:
        with open(filepath + "shapefiles/" + file, 'wb') as out_file:
            content = requests.get(url + file, stream=True).content
            out_file.write(content)

try:
    del content, out_file
    print("Done downloading.")
except:
    print("No downloads selected.")
