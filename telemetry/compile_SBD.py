"""
Author: @jacobrdavis

A collection of python functions for compiling microSWIFT short burst data (SBD) files.

Contents:
    - to_pandas_datetime_index()
    - compile_SBD()

Log:
    - 2022-09-06, J.Davis: created
    - 2022-09-12, J.Davis: updated doc strs, convert dataframe index to datetime index

"""
from pandas import DataFrame, to_datetime
from read_SBD import read_SBD
from typing import Any

def to_pandas_datetime_index(
    df: DataFrame,
    datetimeColumnName: str = 'datetime',
) -> DataFrame:
    """
    Convert a pandas.DataFrame integer index to a pandas.DatetimeIndex (in place)

    Arguments:
        - df (DataFrame), DataFrame with integer index
        - datetimeColumnName (str, optional), column name containing datetime 
          objects to be converted to datetime index; defaults to 'datetime'.

    Returns:
        - (DataFrame), DataFrame with datetime index
    """
    df[datetimeColumnName] = to_datetime(df['datetime'], utc=True) # format="%Y-%m-%d %H:%M:%S",errors='coerce'
    df.set_index('datetime', inplace=True)
    df.sort_index(inplace=True)
    # df.drop(['datetime'], axis=1, inplace=True)
    return


def compile_SBD(
    SBDfolder: str, 
    varType: str, 
    fromMemory: bool = False
) -> Any:
    """
    Compile contents of short burst data files into the specified variable 
    type or output.

    Arguments:
        - SBDfolder (str), _description_
        - varType (str), _description_
        - fromMemory (bool, optional), _description_; defaults to False.

    Raises:
        - Exception, _description_
        - ValueError, _description_

    Returns:
        - (dict), if varType == 'dict'
        - (DataFrame), if varType == 'pandas'
        See pull_telemetry_as_var() for definitions

    """
    SWIFT = []

    if fromMemory == True:
        for file in SBDfolder.namelist():
            SWIFT.append(read_SBD(SBDfolder.open(file)))

    else: #TODO: support reading from a folder of SBDs?
        for SBDfile in SBDfolder: 
            with open(SBDfile, mode='rb') as file: # b is important -> binary
                # fileContent = file.read()
                SWIFT.append(read_SBD(file))

    if varType == 'dict':
        return {k: [d.get(k) for d in SWIFT] for k in set().union(*SWIFT)}
    
    elif varType == 'pandas':
        import pandas
        df = pandas.DataFrame(SWIFT)
        if not df.empty:
            to_pandas_datetime_index(df)
        return df

    elif varType == 'xarray':
        import xarray
        raise Exception('incomplete') #TODO:
    else:
        raise ValueError("varType can only be 'dict', 'pandas', or 'xarray'")
