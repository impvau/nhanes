
import requests
import os
import pdfkit

base_url = "https://wwwn.cdc.gov/Nchs/Nhanes"                   # Base URL for BMX data
base_url_dxa = "https://wwwn.cdc.gov/nchs/data/nhanes/dxa"      # Base URL for DXA data

# Get structure for remote and local data
def get_map(dir):

    # Dictionary to map each year and the datasources on CDC's website
    return {
        
        "1999-2000": [ 
            [
                f"{base_url}/1999-2000/BMX.XPT",    # Source on website
                f"{dir}/1999-2000/BMX.XPT",         # Destination on disk
                f"{base_url}/1999-2000/BMX.htm"     # Documentation on website
            ],
            [
                f"{base_url_dxa}/DXX.XPT", 
                f"{dir}/1999-2000/DXX.XPT", 
                f"{base_url_dxa}/DXX.pdf" 
            ],
            [
                f"{base_url}/1999-2000/DEMO.XPT",
                f"{dir}/1999-2000/DEMO.XPT",   
                f"{base_url}/1999-2000/DEMO.htm"
            ]
        ],
        "2001-2002": [
            [
                f"{base_url}/2001-2002/BMX_B.XPT", 
                f"{dir}/2001-2002/BMX_B.XPT", 
                f"{base_url}/2001-2002/BMX_B.htm" 
            ],
            [
                f"{base_url_dxa}/DXX_B.XPT", 
                f"{dir}/2001-2002/DXX_B.XPT", 
                f"{base_url_dxa}/DXX_B.pdf"
            ],
            [
                f"{base_url}/2001-2002/DEMO_B.XPT", 
                f"{dir}/2001-2002/DEMO_B.XPT", 
                f"{base_url}/2001-2002/DEMO_B.htm" 
            ]
        ],
        "2003-2004": [
            [
                f"{base_url}/2003-2004/BMX_C.XPT", 
                f"{dir}/2003-2004/BMX_C.XPT", 
                f"{base_url}/2003-2004/BMX_C.htm" 
            ],
            [
                f"{base_url_dxa}/DXX_C.XPT", 
                f"{dir}/2003-2004/DXX_C.XPT", 
                f"{base_url_dxa}/DXX_C.pdf" 
            ],
            [
                f"{base_url}/2003-2004/DEMO_C.XPT", 
                f"{dir}/2003-2004/DEMO_C.XPT", 
                f"{base_url}/2003-2004/DEMO_C.htm" 
            ]
        ],
        "2005-2006": [
            [
                f"{base_url}/2005-2006/BMX_D.XPT", 
                f"{dir}/2005-2006/BMX_D.XPT", 
                f"{base_url}/2005-2006/BMX_D.htm" 
            ],
            [
                f"{base_url_dxa}/DXX_D.XPT", 
                f"{dir}/2005-2006/DXX_D.XPT", 
                f"{base_url_dxa}/DXX_D.htm" 
            ],
            [
                f"{base_url}/2005-2006/DEMO_D.XPT", 
                f"{dir}/2005-2006/DEMO_D.XPT", 
                f"{base_url}/2005-2006/DEMO_D.htm"
            ]
        ],
        #"2017-2018": [
        #    [
        #        f"{base_url}/2017-2018/BMX_J.XPT", 
        #        f"{dir}/2017-2018/BMX_J.XPT",
        #        f"{base_url}/2017-2018/BMX_J.htm" 
        #    ],
        #    [
        #        f"{base_url}/2017-2018/DXX_J.XPT", 
        #        f"{dir}/2017-2018/DXX_J.XPT",
        #        f"{base_url}/2017-2018/DXX_J.htm"
        #    ],
        #    [
        #        f"{base_url}/2017-2018/DEMO_J.XPT", 
        #        f"{dir}/2017-2018/DEMO_J.XPT", 
        #        f"{base_url}/2017-2018/DEMO_J.htm"
        #    ]
        #]
        
        #"2007-2008": ["2007-2008/BMX_E"],
        #"2009-2010": ["2009-2010/BMX_F"],
        #"2011-2012": ["2011-2012/BMX_G"],
        #"2013-2014": ["2013-2014/BMX_H"],
        #"2015-2016": ["2015-2016/BMX_I"],
        #"2017-2018": ["2017-2018/BMX_J"]
    }

# Process for downloading non-existant data into data/ in the format data/<year>/<dataset>.XPT
def download(dir): 

    data_map = get_map(dir)

    for year, datasets in data_map.items():
        for dataset in datasets:
            
            ## Process File
            url = f"{dataset[0]}"           # Source on website
            fileName = f"{dataset[1]}"      # Destination on disk

            # Ensure directory structure exists
            directory = os.path.dirname(fileName)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Don't process if the file already exists
            if not os.path.exists(fileName):
                
                # Else download the file
                print(f"Downloading from: {url} ... to {fileName}")

                response = requests.get(url, stream=True)
                with open(fileName, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)

            ## Process Doco
            url = dataset[2]
            fileName = dataset[1].replace(".XPT",".pdf")

            if ".htm" in url:
                if not os.path.exists(fileName):

                    # Else download the file
                    print(f"Downloading from: {url} ... to {fileName}")

                    response = requests.get(url)
                    response.raise_for_status()  # Ensure we got a valid response
                    html_content = response.text

                    # Convert to PDF
                    pdfkit.from_string(html_content, fileName)
            
            elif ".pdf" in url:

                if not os.path.exists(fileName):
                    # Else download the file
                    print(f"Downloading from: {url} ... to {fileName}")

                    response = requests.get(url, stream=True)
                    with open(fileName, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
