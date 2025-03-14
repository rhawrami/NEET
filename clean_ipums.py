import os
import requests
import re
import glob
from pathlib import Path
from ipumspy import IpumsApiClient, MicrodataExtract, readers
import numpy as np
import pandas as pd

sampleID_CPS = 'https://cps.ipums.org/cps-action/samples/sample_ids' # url to CPS sample id's
content_CPS = requests.get(sampleID_CPS).text

sample_ID_CPS_list = re.findall(r"cps\d{4}_\d{2}[a-z]?", content_CPS) # list of CPS IDs

def get_CPS(years=(2000,2023), filename=''):
    '''collects IPUMS CPS data and returns csv
    
    ## **Args**:
    
    ***years***:
    a tuple of years to include

    &nbsp;ex. years = (2000,2023)

    ***filename***:
    string of desired file name (all files will be placed in a 'datasets' folder)

    &nbsp;ex. filename = 'cps_16to24_2023'
    '''

    if Path('datasets/' + filename + '.csv.gz').exists():
        raise FileExistsError(f'File with that name already exists') # check if filename already exists
    
    IPUMS_API_KEY = os.environ.get("IPUMS_API_KEY") # get API environmental variable
    
    client_API = IpumsApiClient(IPUMS_API_KEY)

    start, end = years # get start and end range for years to include
    samples_list = [] # list of IPUMS CPS API samples
    
    for i in range(start, end + 1):
        for j in ['s','b']:
            for k in range(1, 13):
                samples_list.append('cps' + str(i) + '_0' + str(k) + j) # all possible IDs, the 's' and 'b' vary randomly by year
    
    cleaned_samples_list = [i for i in samples_list if i in sample_ID_CPS_list] # only existing sample IDs
    
    extract = MicrodataExtract(
        collection='cps',
        samples=cleaned_samples_list,
        description='CPS Extract for NEETs',
        variables=['AGE', 'SEX', 'RACE'],
        data_format='csv'
    )
    
    # submit, wait, download extract
    client_API.submit_extract(extract=extract) 

    client_API.wait_for_extract(extract)

    client_API.download_extract(extract, download_dir='datasets') # download extract to 'datasets' folder

    # rename files from cps_0000x.csv.gz to our filename parameter
    default_data_files = Path(glob.glob('datasets/cps_0*.csv.gz')[0])
    default_ddi_files = Path(glob.glob('datasets/cps_0*.xml')[0])

    renamed_data_files = 'datasets/' + filename + '.csv.gz'
    renamed_ddi_files = 'datasets/' + filename + '.xml'

    default_data_files.rename(renamed_data_files)
    default_ddi_files.rename(renamed_ddi_files)




if __name__ == '__main__':
    get_CPS(years=(2022,2023), filename='test_cps') # test if I can pull data from IPUMS API, and rename file

    ddi = readers.read_ipums_ddi('datasets/test_cps.xml')
    dff = readers.read_microdata(ddi=ddi, filename='datasets/test_cps.csv.gz')

    print(dff.head())
    print('mean age in data:', np.mean(dff['AGE']))
    print('share of men in sample:', (dff['SEX'] == 1).mean())
    