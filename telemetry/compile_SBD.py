from pandas import DataFrame, to_datetime
from read_SBD import read_SBD

def to_pandas_datetime_index(
    df: DataFrame,
    datetimeColumnName: str = 'datetime',
    ) -> DataFrame:
    #TODO: docstr

    df[datetimeColumnName] = to_datetime(df['datetime'], utc=True) # format="%Y-%m-%d %H:%M:%S",errors='coerce'
    df.set_index('datetime',inplace=True)
    # df.drop(['datetime'], axis=1, inplace=True)
    return


def compile_SBD(SBDfolder: str, structType: str, fromMemory: bool = False):
    #TODO: docstr
    #     
    SWIFT = []

    if fromMemory is True:
        for file in SBDfolder.namelist():
            SWIFT.append(read_SBD(SBDfolder.open(file)))

    else: #TODO: support reading from a folder of SBDs
        for SBDfile in SBDfolder: 
            with open(SBDfile, mode='rb') as file: # b is important -> binary
                # fileContent = file.read()
                SWIFT.append(read_SBD(file))

    if structType == 'dict':
        return {k: [d.get(k) for d in SWIFT] for k in set().union(*SWIFT)}
    
    elif structType == 'pandas':
        import pandas
        return pandas.DataFrame(SWIFT)

    elif structType == 'xarray':
        import xarray
        raise Exception('incomplete') #TODO:
    else:
        raise ValueError("structType can only be 'dict', 'pandas', or 'xarray'")
