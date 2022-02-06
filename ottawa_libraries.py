"""Pulls in XML file containing Ottawa library data and returns parsed dictionary.
"""
import urllib
import xmltodict

def get_ottawa_locations():
    """The ottawa library system provides a well structure data set with
    various library info. The following code works to pull and format it
    as of February 2022.
    
    Returns:
        dict: dictionary of Ottawa library names and their lat/long
    """
    ottawa_url = 'https://biblioottawalibrary.ca/branches.xml'
    ottawa_data = urllib.request.urlopen(url).read()
    ottawa_libs = {}
    for library in xml_parsed['Branches']['BranchInfo']:
        ottawa_libs[library['Name']] = library['Coordinates']
    return ottawa_libs
