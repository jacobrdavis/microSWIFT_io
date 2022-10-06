import string
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
from io import BytesIO
from zipfile import ZipFile
import json
import datetime
from compile_SBD import compile_SBD

def pull_telemetry(
    buoyID: str,
    startDate: datetime.datetime,
    endDate = datetime.datetime.utcnow(),
    formatOut: str = 'var',
    structType: str = None,
    inMemory: bool = False
    ) -> :

    #TODO: docstr

    # Convert dates to strings:
    startDateStr  = startDate.strftime('%Y-%m-%dT%H:%M:%S')
    endDateStr = endDate.strftime('%Y-%m-%dT%H:%M:%S')

    # Define the payload and encode it as a request:
    payload = {'buoy_name' : f'microSWIFT {buoyID}'.encode('utf8'),
               'start' : startDateStr.encode('utf8'),
               'end' : endDateStr.encode('utf8'),
               'format' : formatOut.encode('utf8')}
    request = urlencode(payload, quote_via=quote_plus)

    # Define the base URL based on output format:
    if formatOut == 'json' or formatOut == 'kml':
        baseURL = 'http://swiftserver.apl.washington.edu/kml?action=kml&'
    elif formatOut == 'zip' or formatOut == 'var':
        baseURL = 'http://swiftserver.apl.washington.edu/services/buoy?action=get_data&'
    else:
        raise ValueError("formatOut can only be 'kml', 'json', 'zip', or 'var'")

    # Get the response:
    response = urlopen(baseURL + request)

    # Handle the response:
    if formatOut == 'json': # read and return json formatted text
        return json.loads(response.read())

    elif formatOut == 'var': # read contents of the response into memory and return as a variable
        zippedFile = ZipFile(BytesIO(response.read())) # virtual zip file
        response.close()
        return compile_SBD(zippedFile, structType, fromMemory = True)
    
    elif formatOut == 'zip': # save local copy of the zipped SBD messages
        zippedFile = response.read()
        response.close()  
        with open(f'microSWIFT{buoyID}.zip', 'wb') as local:
            local.write(zippedFile)
            local.close()  
        #TODO: if structType     
        return

    elif formatOut == 'kml': # save local copy of the KML file
        kmlFile = response.read()
        response.close()
        with open(f'microSWIFT{buoyID}_{startDateStr.replace(":","")}_to_{endDateStr.replace(":","")}.kml', 'wb') as local:
                local.write(kmlFile)
        return

#%%
if __name__ == "__main__":
    #%%
    buoyID = '019'
    startDate = datetime.datetime(2022,9,26,0,0,0)
    endDate = datetime.datetime.utcnow() #TODO: if none entered use UTC now
    formatOut = 'kml' # 'zip'
    structType = 'pandas'
    inMemory = False
    #%%
    pull_telemetry(buoyID, 
                   startDate,
                   formatOut = formatOut
                   inMemory = inMemory)
#%%

#%%

    # for file in [myzip.namelist()[0]]:
    #     data = compile_SBD(myzip.open(file),inMemory)


    # elif formatOut == 'kml':
    #     with open("10MB", "wb") as handle:
    #         for data in tqdm(response.iter_content()):
    #             handle.write(data)

    #TODO: if in memory:
    # https://stackoverflow.com/questions/5710867/downloading-and-unzipping-a-zip-file-without-writing-to-disk


    
        #     with open(TX_fname, mode='rb') as file: # b is important -> binary
        # fileContent = file.read()
    
    # data = struct.unpack('<sbbheee42eee42b42b42b42b42Bffeeef', fileContent)

        # i=0
        # for line in myzip.open(file).readlines():
        #     print(line)
        #     print(i)
        #     i+=1
        #     # print(line.decode('utf-8'))            
    #%%
    

    #%%
    # with urllib.request.urlopen('http://www.example.com/') as f:
    #     data_json = json.loads(f.read())
    #     print(data_json)