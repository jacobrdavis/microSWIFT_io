#TODO: docstr header
#TODO: create fun to save to ncf and csv

from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
from io import BytesIO
from zipfile import ZipFile
import json
from datetime import datetime
from typing import Union, List, BinaryIO, TextIO
from pandas import DataFrame
from xarray import DataArray
from compile_SBD import compile_SBD

def create_request(buoyID: str, startDate: datetime, endDate: datetime, formatOut: str) -> dict:
    #TODO: docstr
    """
    _summary_

    Arguments:
        - buoyID (str), _description_
        - startDate (datetime), _description_
        - endDate (datetime), _description_
        - formatOut (str), _description_

    Returns:
        - (dict), _description_
    """
    # Convert dates to strings:
    startDateStr  = startDate.strftime('%Y-%m-%dT%H:%M:%S')
    endDateStr = endDate.strftime('%Y-%m-%dT%H:%M:%S')

    # Pack into a payload dictionary:
    payload = {'buoy_name' : f'microSWIFT {buoyID}'.encode('utf8'),
               'start' : startDateStr.encode('utf8'),
               'end' : endDateStr.encode('utf8'),
               'format' : formatOut.encode('utf8')}

    return urlencode(payload, quote_via=quote_plus)

def pull_telemetry_as_json(
    buoyID: str,
    startDate: datetime,
    endDate: datetime = datetime.utcnow(),
    ) -> dict:
    #TODO: docstr
    """
    _summary_

    Arguments:
        - buoyID (str), _description_
        - startDate (datetime), _description_
        - endDate (datetime, optional), _description_; defaults to datetime.utcnow().

    Returns:
        - (dict), _description_
    """
    # Create the payload request:
    formatOut = 'json'
    request = create_request(buoyID, startDate, endDate, formatOut)

    # Define the base URL:
    baseURL = 'http://swiftserver.apl.washington.edu/kml?action=kml&'   

    # Get the response:
    response = urlopen(baseURL + request)

    # Return as json
    jsonData = response.read()
    response.close()

    return json.loads(jsonData)

def pull_telemetry_as_var(
    buoyID: str,
    startDate: datetime,
    endDate: datetime = datetime.utcnow(),
    structType: str = dict,
    ) -> Union[List[dict], DataFrame, DataArray]:
    """
    Query the SWIFT server for microSWIFT data over a specified date range and 
    return an object in memory. Note the .zip file of short burst data (SBD) messages
    is handled in memory and not saved to the local machine. Use pull_telemetry_as_zip
    for this purpose.

    Arguments:
        - buoyID (str), microSWIFT ID including leading zero (e.g. '043')
        - startDate (datetime), query start date in UTC (e.g. datetime(2022,9,26,0,0,0))
        - endDate (datetime, optional), query end date in UTC; defaults to datetime.utcnow().
        - structType (str, optional), data structure to be returned; defaults to 'dict'
            Possible values include:
            * 'dict', returns a list of dictionaries with self-consistent keys
            * 'pandas', returns a pandas DataFrame object
            * 'xarray', returns an xarray DataArray object

    Returns:
        - (List[dict]), if structType == 'dict' 
        - (DataFrame), if structType == 'pandas' 
        - (DataArray), if structType == 'xarray' 

    Example:

    Return SWIFT as a pandas dataframe; by leaving the endDate empty, the 
    function will default to the present time (in UTC):

        >>> from datetime import datetime
        >>> import pandas
        >>> SWIFT_df = pull_telemetry_as_var('019', datetime(2022,9,26), structType = 'pandas')
    """
    # Create the payload request:
    formatOut = 'zip'
    request = create_request(buoyID, startDate, endDate, formatOut)

    # Define the base URL:
    baseURL = 'http://swiftserver.apl.washington.edu/services/buoy?action=get_data&'

    # Get the response:
    response = urlopen(baseURL + request)

    # Read the response into memory as a virtual zip file:
    zippedFile = ZipFile(BytesIO(response.read())) # virtual zip file
    response.close()

    # Compile SBD messages into specified variable and return:
    return compile_SBD(zippedFile, structType, fromMemory = True)

def pull_telemetry_as_zip(
    buoyID: str,
    startDate: datetime,
    endDate: datetime = datetime.utcnow(),
    localPath: str = None,
    ) -> BinaryIO:
    """
    Query the SWIFT server for microSWIFT data over a specified date range and 
    download a .zip file of individual short burst data (SBD) messages.

    Arguments:
        - buoyID (str), microSWIFT ID including leading zero (e.g. '043')
        - startDate (datetime), query start date in UTC (e.g. datetime(2022,9,26,0,0,0))
        - endDate (datetime, optional), query end date in UTC; defaults to datetime.utcnow().
        - localPath (str, optional), path to local file destination including folder 
            and filename; defaults to the current directory as './microSWIFT{buoyID}.zip'

    Returns:
        - (BinaryIO), compressed .zip file at localPath

    Example:

    Download zipped file of SBD messages; by leaving the endDate empty, the 
    function will default to the present time (in UTC):

        >>> from datetime import datetime
        >>> pull_telemetry_as_zip(buoyID = '019', startDate = datetime(2022,9,26))
    """
    # Create the payload request:
    formatOut = 'zip'
    request = create_request(buoyID, startDate, endDate, formatOut)

    # Define the base URL:
    baseURL = 'http://swiftserver.apl.washington.edu/services/buoy?action=get_data&'

    # Get the response:
    response = urlopen(baseURL + request)

    # Write the response to a local .zip file:
    zippedFile = response.read()
    response.close() 
    
    if localPath is None:
        localPath = f'./microSWIFT{buoyID}.zip'

    with open(localPath, 'wb') as local:
        local.write(zippedFile)
        local.close()  
    return


def pull_telemetry_as_kml(
    buoyID: str,
    startDate: datetime,
    endDate: datetime = datetime.utcnow(),
    localPath: str = None,
    ) -> TextIO:
    #TODO: docstr
    """
    _summary_

    Arguments:
        - buoyID (str), _description_
        - startDate (datetime), _description_
        - endDate (datetime, optional), _description_; defaults to datetime.utcnow().
        - localPath (str, optional), _description_; defaults to None.

    Returns:
        - (TextIO), _description_
    """
    # Create the payload request:
    formatOut = 'kml'
    request = create_request(buoyID, startDate, endDate, formatOut)

    # Define the base URL:
    baseURL = 'http://swiftserver.apl.washington.edu/kml?action=kml&'

    # Get the response:
    response = urlopen(baseURL + request)

    # Write the response to a local .kml geographic file:
    kmlFile = response.read()
    response.close()
    if localPath is None:
        startDateStr  = startDate.strftime('%Y-%m-%dT%H%M%S')
        endDateStr = endDate.strftime('%Y-%m-%dT%H%M%S')
        localPath = f'./microSWIFT{buoyID}_{startDateStr}_to_{endDateStr}.kml'

    with open(localPath, 'wb') as local:
            local.write(kmlFile)
    return


if __name__ == "__main__":
    start = datetime(2022,9,26,0,0,0)
    end = datetime.utcnow()
    
    # SWIFT_json = pull_telemetry_as_json(buoyID = '019', startDate = start, endDate= end)
    # print(SWIFT_json)

    # SWIFT_dict = pull_telemetry_as_var(buoyID = '019', startDate = start, endDate= end, structType = 'dict')
    # print(SWIFT_dict)

    SWIFT_df = pull_telemetry_as_var('019', datetime(2022,9,26), structType = 'pandas')

    # SWIFT_df = pull_telemetry_as_var(buoyID = '019', startDate = start, endDate= end, structType = 'pandas')
    print(SWIFT_df.info())

    #TODO:
    # SWIFT_ds = pull_telemetry_as_var(buoyID = '019', startDate = start, endDate= end, structType = 'xarray')
    # print(SWIFT_ds)

    # pull_telemetry_as_zip(buoyID = '019', startDate = start, endDate= end)

    # pull_telemetry_as_kml(buoyID = '019', startDate = start, endDate= end)
