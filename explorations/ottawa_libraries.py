"""Pulls in XML file containing Ottawa library data and returns parsed dictionary.
"""
import urllib
import xmltodict
import ssl

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
