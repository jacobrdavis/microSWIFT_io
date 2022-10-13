"""
Author: @jacobrdavis

A collection of python functions for reading microSWIFT short burst data (SBD) files.

Contents:
    - get_sensor_type()
    - unpack_SBD()
    - read_SBD()

Log:
    - 2022-09-06, J.Davis: created
    - 2022-09-12, J.Davis: updated doc strs

"""
import struct
import numpy as np
from datetime import datetime, timezone

"""
MicroSWIFT payload definitions. See https://github.com/alexdeklerk/microSWIFT
"""
payloadDef = {
    50 : '<sbbhfff42f42f42f42f42f42f42ffffffffiiiiii',
    51 : '<sbbhfff42fffffffffffiiiiii',
    52 : '<sbbheee42eee42b42b42b42b42Bffeeef',
}

"""
SWIFT variables to extract
"""
SWIFTvars = [
    'datetime', 'Hs', 'Tp', 'Dp',
    'E' ,'f' ,'a1', 'b1', 'a2', 'b2', 'check', 
    'u_mean', 'v_mean', 'z_mean', 'lat' , 'lon', 
    'temp', 'salinity', 'volt'
]

def get_sensor_type(fileContent: bytes) -> int:
    """
    Helper function to determine sensor type from an SBD message.

    Arguments:
        - fileContent (bytes), binary SBD message

    Raises:
        - ValueError, raise error if the sensor type is not one of the possible
          types defined in microSWIFT.py and configured to parsed on the sever.

    Returns:
        - (int), int corresponding to sensor type
    """
    payloadStartIdx = 0 # (no header) otherwise it is: = payload_data.index(b':') 
    sensorType = ord(fileContent[payloadStartIdx+1:payloadStartIdx+2]) # sensor type is stored 1 byte after the header
    if sensorType not in payloadDef.keys():
        raise ValueError(f"sensorType not defined - can only be value in: {list(payloadDef.keys())}")
    
    return sensorType

def unpack_SBD(fileContent: bytes) -> dict:
    """
    Unpack short burst data messages using formats defined in the sensor type
    payload definitions.

    Arguments:
        - fileContent (bytes), binary SBD message

    Returns:
        - (dict), microSWIFT variables stored in a temporary dictionary
    """
    sensorType = get_sensor_type(fileContent)

    payloadStruct = payloadDef[sensorType] #['struct']
   
    data = struct.unpack(payloadStruct, fileContent)

    SWIFT = {var : None for var in SWIFTvars}
    
    if sensorType == 50:
        #TODO:
        print('incomplete')
    elif sensorType == 51:
        #TODO:
        print('incomplete')

    elif sensorType == 52:
        payload_size = data[3]
        SWIFT['Hs'] = data[4]
        SWIFT['Tp'] = data[5]
        SWIFT['Dp'] = data[6]
        SWIFT['E']  = np.asarray(data[7:49])
        fmin = data[49]
        fmax = data[50]
        if fmin != 999 and fmax != 999:
            fstep = (fmax - fmin)/(len(SWIFT['E'])-1)
            SWIFT['f'] = np.arange(fmin, fmax + fstep, fstep)
        else:
            SWIFT['f'] = 999*np.ones(np.shape(SWIFT['E']))
        SWIFT['a1'] = np.asarray(data[51:93])/100
        SWIFT['b1'] = np.asarray(data[93:135])/100
        SWIFT['a2'] = np.asarray(data[135:177])/100
        SWIFT['b2'] = np.asarray(data[177:219])/100
        SWIFT['check'] = np.asarray(data[219:261])/10
        SWIFT['lat'] = data[261]
        SWIFT['lon'] = data[262]
        SWIFT['temp'] = data[263]
        SWIFT['salinity'] = data[264]
        SWIFT['volt'] = data[265]
        nowEpoch = data[266]
        SWIFT['datetime'] = datetime.fromtimestamp(nowEpoch, tz=timezone.utc)  

    #TODO: strip empty or Nones?

    return SWIFT

def read_SBD(SBDfile: str) -> dict: #, fromMemory: bool = False):
    """
    Read microSWIFT short burst data messages.

    Arguments:
        - SBDfile (str), path to .sbd file

    Returns:
        - (dict), microSWIFT variables stored in a temporary dictionary
    """

    fileContent = SBDfile.read()

    return unpack_SBD(fileContent)


