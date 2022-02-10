"""Pulls in data containing library data and returns parsed dictionary.
"""
import urllib
import xmltodict
import ssl
import json
import re


def get_ottawa_locations():
    """The ottawa library system provides a well structure data set with
    various library info. The following code works to pull and format it
    as of February 2022.
    
    Returns:
        dict: dictionary of Ottawa library names and their lat/long
    """
    context = ssl._create_unverified_context()
    ottawa_url = 'https://biblioottawalibrary.ca/branches.xml'
    ottawa_data = urllib.request.urlopen(ottawa_url, context=context).read()
    libraries = xmltodict.parse(ottawa_data)
    ottawa_libraries = {}
    for library in libraries['Branches']['BranchInfo']:
        ottawa_libraries[library['Name']] = library['Coordinates']
    return ottawa_libraries


def get_calgary_locations():
    """The calgary library system provides a well structure data set with
    various library info. The following code works to pull and format it
    as of February 2022.
    
    Returns:
        dict: dictionary of Ottawa library names and their lat/long
    """
    url = "https://data.calgary.ca/resource/niu9-34wk.json"
    calgary_data = urllib.request.urlopen(url).read()
    data = json.loads(calgary_data)
    calgary_libraries = {}
    for lib in data:
        location = {}
        location['Latitude'] = lib['location']['latitude']
        location['Longitude'] = lib['location']['longitude']
        calgary_libraries[lib['library']] = location
    return calgary_libraries


def get_edmonton_locations():
    """The edmonton library system provides a well structure data set with
    various library info. The following code works to pull and format it
    as of February 2022.
    
    Returns:
        dict: dictionary of Ottawa library names and their lat/long
    """
    url = "https://data.edmonton.ca/resource/jn25-zspi.json"
    edmonton_data = urllib.request.urlopen(url).read()
    data = json.loads(edmonton_data)
    edmonton_libraries = {}
    for lib in data:
        # for some reason the location data for this library was not included so hard coding it here
        # raised the issue with city of Edmnton
        if lib['branch'] == "Shelley Milner Children's Library":
            location = {}
            location['Latitude'] = 53.543273
            location['Longitude'] = -113.490284
            edmonton_libraries[lib['branch']] = location
        else:
            location = {}
            location['Latitude'] = lib['latitude']
            location['Longitude'] = lib['longitude']
            edmonton_libraries[lib['branch']] = location
    return edmonton_libraries


def get_montreal_locations():
    """Had issues with the Montreal library system (see montreal_libraries.ipynb).
    Ended up scraping their webpage. The following code formats the scraped data.
    
    Returns:
        dict: dictionary of Ottawa library names and their lat/long
    """
    with open('montreal_scraped_text.txt') as file:
        scraped_text = file.read()
    montreal_libraries = {}
    for lib in scraped_text.split('}},{'):
        loc = re.findall(r'"coordinates":\[(.*?)\]}', lib)
        loc = loc[0].split(',')
        location = {}
        location['Latitude'] = loc[1]
        location['Longitude'] = loc[0]
        name = re.findall(r'<span class=\\"link-label\\">(.*)</span>', lib)[0]
        name = name.replace("&#x27;", "'")
        name = name.replace('Ã¨', 'è')
        montreal_libraries[name] = location
    return montreal_libraries


def get_toronto_locations():
    """The Toronto library system provides a well structure data set with
    various library info. The following code works to pull and format it
    as of February 2022.
    
    Returns:
        dict: dictionary of Toronto library names and their lat/long
    """
    url = 'https://www.torontopubliclibrary.ca/data/library-data.kml'
    toronto_data = urllib.request.urlopen(url).read()
    libraries = xmltodict.parse(toronto_data)
    libraries = libraries['kml']['Document']['Placemark']
    toronto_libraries = {}
    for library in libraries:
        loc = library['Point']['coordinates'].split(',')
        location = {}
        location['Latitude'] = loc[1]
        location['Longitude'] = loc[0]
        toronto_libraries[library['name']] = location
    return toronto_libraries


def main(city):
    if city == 'Ottawa':
        return get_ottawa_locations()
    elif city == "Calgary":
        return get_calgary_locations()
    elif city == 'Edmonton':
        return get_edmonton_locations()
    elif city == 'Toronto':
        return get_toronto_locations()
    elif city == 'Montreal':
        return get_montreal_locations()
    else: print(f'No data for {city}')