"""
Author: @jacobrdavis
#TODO:
A collection of python functions for accessing data from the UW-APL SWIFT server:
http://swiftserver.apl.washington.edu/ (base URL)
http://faculty.washington.edu/jmt3rd/SWIFTdata/DynamicDataLinks.html (HTML page)

See pull_telemetry_example.ipynb for a complete tutorial.


Contents:
    - create_request()
    - pull_telemetry_as_var()
    - pull_telemetry_as_zip()
    - pull_telemetry_as_json()
    - pull_telemetry_as_kml()

Log:
    - 2022-09-06, J.Davis: created
    - 2022-09-12, J.Davis: updated doc strs, added datetime indexing to dataframes, requirements.txt

"""
from typing import Iterable
from pull_telemetry import pull_telemetry_as_json, pull_telemetry_as_var
from datetime import datetime, timezone, timedelta, tzinfo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
#%%
#TODO:
# - pull config from branch?
# -  
def find_full_range(
    X1: np.array,
    X2: np.array,
)-> tuple:
    #TODO: doctstr
    x_min = min([X1.min(), X2.min()])
    x_max = max([X1.max(), X2.max()])
    return (x_min, x_max)

def date_range(
    start: datetime,
    end: datetime, 
    msgPerHr: float,
)-> pd.DatetimeIndex:
    #TODO:
    dateRange = pd.date_range(
        start, 
        end, 
        freq = f'{msgPerHr}H', 
        tz = timezone.utc
    ) 
    return dateRange

def create_telemetry_report(
    buoyID: str, 
    startDate: datetime, 
    endDate: datetime, 
    burstInterval: int = None,
)-> dict:



    print('')


def create_telemetry_report_figure(
    serverTimestamps, 
    onboardTimestamps,
    allCallWindows,
):

    fig,ax = plt.subplots(figsize = (8, 3))

    ax.hist(
        serverTimestamps,
        bins= allCallWindows,
        color='red',
        edgecolor='red',
        alpha=0.5,
        label='received'
    )

    ax.hist(
        onboardTimestamps,
        bins= allCallWindows,
        color='royalblue',
        edgecolor='royalblue',
        alpha=0.5,
        label='recorded'
    )

    ax.axvline(
        start,
        color='darkorange',
        alpha=0.75,
        linewidth = 1.5,
        label = 'query start',
        clip_on = False,
    )

    ax.axvline(
        end, 
        color='darkorange',
        alpha=0.75,
        linewidth = 1.5,
        label = 'query end',
        clip_on = False,
    )

    dtFmt = mpl.dates.DateFormatter('%d%b %H:%M') # define the formatting
    plt.gca().xaxis.set_major_formatter(dtFmt) 
    plt.xticks(rotation = 90)

    ylims = np.round(ax.get_ylim()) #+ np.array([0,1])
    yticks = ax.get_yticks()
    ax.set_yticks(np.unique(np.round(yticks,0)))
    yminor_ticks = np.arange(0, ylims[1], 1)

    ax.set_xticks(fullRange, minor=True)
    ax.set_yticks(yminor_ticks, minor=True)

    # grid settings:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.2)

    ax.set_xlim([minDate, maxDate])
    ax.set_ylim(ylims)
    ax.legend(loc='upper right')
    ax.set_ylabel('messages per burst window')

#%%
# start = datetime(2022,9,26,0,0,0)
# end   = datetime(2022,9,30,0,0,0)
# buoyID = '019'
# buoyID = '057'

start = datetime(2022,10,13,0,0,0)
end   = datetime(2022,10,15,0,0,0)
buoyID = '062'


# start = datetime(2022,10,15,12,0,0)
# buoyID = '005'
# buoyID = '068'

SWIFT_pd = pull_telemetry_as_var(buoyID = buoyID, startDate = start, endDate = end, varType = 'pandas')


burstInterval = None
SWIFT_json = pull_telemetry_as_json(buoyID = buoyID, startDate = start)


serverTimes = [msg['timestamp'] for msg in SWIFT_json['buoys'][0]['data']]

serverTimes = pd.to_datetime(serverTimes, format='%Y-%m-%dT%H:%M:%S%Z') # datetime.strptime(serverTimes[0], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)


SWIFT_dict = pull_telemetry_as_var(buoyID = buoyID, startDate = start, endDate = end, varType = 'dict')
#%%
if burstInterval is None:
    msgRate = np.diff(SWIFT_dict['datetime'])
    msgPerHr = np.round(np.mean(msgRate[msgRate > timedelta(0)]).total_seconds() / 3600)
    print(f'Inferred burst rate of {msgPerHr} messages per hour.')
else:
    msgPerHr = burstInterval/60

# end = datetime.utcnow().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)#TODO: make fun arg default

startRange = SWIFT_dict['datetime'].min().replace(minute=0, second=0)
endRange = SWIFT_dict['datetime'].max().replace(minute=0, second=0)

dateRange = date_range(startRange, endRange, msgPerHr)
dateRangeQuery = date_range(start, end, msgPerHr)
minDate, maxDate = find_full_range(dateRange, dateRangeQuery)
fullRange = date_range(minDate, maxDate, msgPerHr)

# inTimes = np.searchsorted(dateRange.tolist(), SWIFT_dict['datetime'], side='left')

# [dateRange[i] for i in inTimes]
# inTimesServer = np.searchsorted(dateRange.tolist(), serverTimes, side='left')

#%%
create_telemetry_report_figure(serverTimes, SWIFT_dict['datetime'], dateRange)


#%%
