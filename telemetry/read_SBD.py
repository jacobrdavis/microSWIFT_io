import struct
import numpy as np
from datetime import datetime, timezone

"""
microSWIFT payload definitions
"""
payloadDef = {
    50 : '<sbbhfff42f42f42f42f42f42f42ffffffffiiiiii',
    51 : '<sbbhfff42fffffffffffiiiiii',
    52 : '<sbbheee42eee42b42b42b42b42Bffeeef',
}

"""
SWIFT variables
"""
SWIFTvars = ['datetime', 'Hs', 'Tp', 'Dp',
             'E' ,'f' ,'a1', 'b1', 'a2', 'b2', 'check', 
             'u_mean', 'v_mean', 'z_mean', 'lat' , 'lon', 
             'temp', 'salinity', 'volt']

def get_sensor_type(fileContent):
    #TODO: docstr
    payloadStartIdx = 0 # (no header) otherwise it is: = payload_data.index(b':') 
    sensorType = ord(fileContent[payloadStartIdx+1:payloadStartIdx+2]) # sensor type is stored 1 byte after the header
    if sensorType not in payloadDef.keys():
        raise ValueError(f"sensorType not defined - can only be value in: {list(payloadDef.keys())}")
    
    return sensorType

def unpack_SBD(fileContent):

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

def read_SBD(SBDfile: str): #, fromMemory: bool = False):
    #TODO: docstr
    
    # if fromMemory is True:
    #     fileContent = SBDfile.read()
        
    # else:
    #     with open(SBDfile, mode='rb') as file: # b is important -> binary
    #         fileContent = file.read()

    fileContent = SBDfile.read()

    return unpack_SBD(fileContent)




	# 				if sensor_type0 not in [50,51,52]:
	# 					logger.info(f'Failed to read sensor type properly; read sensor type as: {sensor_type0}')
	# 					logger.info(f'Trying to send as configured sensor type instead ({sensor_type})')
	# 					send_sensor_type = sensor_type
    # return data

    # SWIFT = {'datetime' : None,
    #          'Hs'       : None,
    #          'Tp'       : None,
    #          'Dp'       : None, 
    #          'E'        : None,
    #          'f'        : None, 
    #          'a1'       : None,
    #          'b1'       : None, 
    #          'a2'       : None,
    #          'b2'       : None,
    #          'check'    : None,
    #          'u_mean'   : None,
    #          'v_mean'   : None,
    #          'z_mean'   : None,
    #          'lat'      : None,
    #          'lon'      : None,
    #          'temp'     : None,
    #          'salinity' : None,
    #          'volt'     : None,
    # }

# s = slice

# payloadDef = {
#     50 : {
#         'struct' : '<sbbhfff42f42f42f42f42f42f42ffffffffiiiiii',
#         'params' :  [
#             ('Hs' ,4) , 
#             ('Tp', 5), 
#             ('E', s(6,42))
#         ]
#         # 'indices' : [ 4, 5, s(2,42), s(42,49), 
#     },

#     51 : {
#         'struct'  : '<sbbhfff42fffffffffffiiiiii',
#         'vars'    : [],
#         'indices' : [],
#     },

#     52 : {
#         'struct'  : '<sbbheee42eee42b42b42b42b42Bffeeef',
#         'vars'    : [],
#         'indices' : [],
#     },   
# }
# for key, idx in payloadDef[50]['params']:
#     data52[key] = data[idx]
