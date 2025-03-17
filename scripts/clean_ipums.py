import os
import requests
import re
import glob
from pathlib import Path
from ipumspy import IpumsApiClient, MicrodataExtract, readers
import numpy as np
import pandas as pd


def get_CPS(years, vars = ['AGE'], filename='', filepath=''):
    """collects IPUMS CPS data and downloads extract
    
    ## Args:
    
    #### years:
    a tuple of years, or single integer year to include

    &nbsp;ex. years = (2000,2023)

    #### vars:
    list of variables to include

    &nbsp;ex. vars = ['AGE', 'SEX', 'EMPSTAT']

    #### filename:
    string of desired file name 

    &nbsp;ex. filename = 'cps_16to24_2023'

    #### filepath:
    string of directory where files should go

    &nbsp;ex. filename = 'datasets'

    """
    
    
    sampleID_CPS = 'https://cps.ipums.org/cps-action/samples/sample_ids' # url to CPS sample id's
    content_CPS = requests.get(sampleID_CPS).text
    sample_ID_CPS_list = re.findall(r"cps\d{4}_\d{2}[a-z]?", content_CPS) # list of CPS IDs

    
    IPUMS_API_KEY = os.environ.get("IPUMS_API_KEY") # get API environmental variable
    
    client_API = IpumsApiClient(IPUMS_API_KEY)

    if isinstance(years, int): # if only one year is supplied
        start = end = years
    else:
        start, end = years # get start and end range for years to include
    
    samples_list = [] # list of IPUMS CPS API samples
    
    for i in range(start, end + 1):
        for j in ['s','b']:
            for k in range(1, 13):
                if k < 10:
                    samples_list.append('cps' + str(i) + '_0' + str(k) + j) # all possible IDs, the 's' and 'b' vary randomly by year
                else:
                    samples_list.append('cps' + str(i) + '_' + str(k) + j)
    
    cleaned_samples_list = [i for i in samples_list if i in sample_ID_CPS_list] # only existing sample IDs
    
    extract = MicrodataExtract(
        collection='cps',
        samples=cleaned_samples_list,
        description='CPS Extract for NEETs',
        variables=vars
    )
    
    # submit, wait, download extract
    client_API.submit_extract(extract=extract) 

    client_API.wait_for_extract(extract)

    client_API.download_extract(extract, download_dir=filepath + '/') # download extract 

    # rename files from cps_0000[X].csv.gz to our filename parameter
    default_data_files = Path(glob.glob(filepath + '/' 'cps_0*.dat.gz')[0])
    default_ddi_files = Path(glob.glob(filepath + '/' 'cps_0*.xml')[0])

    renamed_data_files = filepath + '/' + filename + '.dat.gz'
    renamed_ddi_files = filepath + '/' + filename + '.xml'

    default_data_files.rename(renamed_data_files)
    default_ddi_files.rename(renamed_ddi_files)




if __name__ == '__main__':
    get_CPS(years=(2022,2023), vars=['AGE', 'SEX'], filename='test_cps', filepath='datasets/') # test if I can pull data from IPUMS API, and rename file

    ddi = readers.read_ipums_ddi('datasets/test_cps.xml')
    dff = readers.read_microdata(ddi=ddi, filename='datasets/test_cps.dat.gz')

    print(dff.head())
    print('mean age in data:', np.mean(dff['AGE']))
    print('share of men in sample:', (dff['SEX'] == 1).mean())
    