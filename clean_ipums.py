import os
import requests
import re
from ipumspy import IpumsApiClient, MicrodataExtract
import numpy as np
import pandas as pd

sampleID_CPS = 'https://cps.ipums.org/cps-action/samples/sample_ids' # url to CPS sample id's
content_CPS = requests.get(sampleID_CPS).text

sample_ID_CPS_list = re.findall(r"cps\d{4}_\d{2}[a-z]?", content_CPS) # list of CPS IDs

def get_CPS(years=(2000,2023)):
    '''collects IPUMS CPS data and returns dataframe
    
    ## **Args**:
    
    ***years***:
    a tuple of years to include

    &nbsp;ex. years = (2000,2023)
    '''
    
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
    
    client_API.submit_extract(extract=extract) 

    client_API.wait_for_extract(extract)

    client_API.download_extract(extract, download_dir='datasets') # download extract to 'datasets' folder




if __name__ == '__main__':
    a = get_CPS(years=(2022,2023))
    print(a)
    import glob 
    #fp = glob.glob('datasets/*.csv.gz')
    #d = pd.read_csv(fp[0])
    #print(d['AGE'].head())
    #print(np.max(d['AGE']))
    #print(mean, np.mean(d['SEX']))