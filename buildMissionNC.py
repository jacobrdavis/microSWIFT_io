# Build microSWIFT netCDF data structure from raw text data files
'''
@edwinrainville

'''
# Import statements
from netCDF4 import Dataset
import datetime
import glob
import numpy as np
import pynmea2
import cftime

# Define Project Directory 
project_dir = '/Volumes/DUNEXdata/DUNEXMainExp_Oct2021/'

# Define Data Directory
data_dir = 'microSWIFT_data/'

# Define Mission Number
mission_num = 0
mission_dir = 'mission_{}/'.format(mission_num)

# Define netCDF filename and path
ncfile_name = project_dir + data_dir + mission_dir + 'mission_{}.nc'.format(mission_num)

# Open netCDF dataset
rootgrp = Dataset(ncfile_name, 'w')

# Define microSWIFT num
microSWIFT_num = 11

# Define microSWIFT directory
microSWIFT_dir = 'microSWIFT_{}/'.format(microSWIFT_num)
microSWIFT_dir_path = project_dir + data_dir + mission_dir + microSWIFT_dir

# Create netcdf group for microSWIFT
microSWIFTgroup = rootgrp.createGroup('microSWIFT_{}'.format(microSWIFT_num))

# ------ IMU Data Read-in ------
# Create IMU sub group
imugrp = microSWIFTgroup.createGroup('IMU')

# Get list of all IMU files
imu_file_list = glob.glob(microSWIFT_dir_path + '*IMU*')

# Define lists for each variable
imu_time = []
accel_x = []
accel_y = []
accel_z = []
mag_x =[]
mag_y = []
mag_z = []
gyro_x = []
gyro_y = []
gyro_z = []

# Loop through each file and read in data from each line 
for file in imu_file_list:
    with open(file) as f:
        lines = f.readlines()
        # Line Structure: timestamp, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z
        for line in lines:
            values = line.split(',')
            imu_time.append(datetime.datetime.fromisoformat(values[0]))
            accel_x.append(float(values[1]))
            accel_y.append(float(values[2]))
            accel_z.append(float(values[3]))
            mag_x.append(float(values[4]))
            mag_y.append(float(values[5]))
            mag_z.append(float(values[6]))
            gyro_x.append(float(values[7]))
            gyro_y.append(float(values[8]))
            gyro_z.append(float(values[9]))

# Create IMU dimensions and write data to netCDF file
# Create imu time dimension
imu_time_dim = imugrp.createDimension('time', len(imu_time))

# IMU Time Variable
imu_time_nc = imugrp.createVariable('time', 'f8', ('time',))
imu_time_nc.units = "hours since 0001-01-01 00:00:00.0"
imu_time_nc.calendar = "gregorian"
imu_time_num = cftime.date2num(imu_time, units=imu_time_nc.units,calendar=imu_time_nc.calendar)
imu_time_nc[:] = imu_time_num

# Accelerations
accel_x_nc = imugrp.createVariable('accel_x', 'f8', ('time',))
accel_x_nc[:] = accel_x
accel_y_nc = imugrp.createVariable('accel_y', 'f8', ('time',))
accel_y_nc[:] = accel_y
accel_z_nc = imugrp.createVariable('accel_z', 'f8', ('time',))
accel_z_nc[:] = accel_z

# Magnetometer
mag_x_nc = imugrp.createVariable('mag_x', 'f8', ('time',))
mag_x_nc[:] = mag_x
mag_y_nc = imugrp.createVariable('mag_y', 'f8', ('time',))
mag_y_nc[:] = mag_y
mag_z_nc = imugrp.createVariable('mag_z', 'f8', ('time',))
mag_z_nc[:] = mag_z

# Gyroscope
gyro_x_nc = imugrp.createVariable('gyro_x', 'f8', ('time',))
gyro_x_nc[:] = gyro_x
gyro_y_nc = imugrp.createVariable('gyro_y', 'f8', ('time',))
gyro_y_nc[:] = gyro_y
gyro_z_nc = imugrp.createVariable('gyro_z', 'f8', ('time',))
gyro_z_nc[:] = gyro_z

# ------ GPS Data Read-in ------
# Create GPS sub group
gpsgrp = microSWIFTgroup.createGroup('GPS')

# Get list of all GPS files
gps_file_list = glob.glob(microSWIFT_dir_path + '*GPS*')

# Define lists for each variable
gps_time = []
lat = []
lon = []
u = []
v = []
z= []

# Read in GPS data from each file in the GPS list
for gps_file in gps_file_list:
    with open(gps_file, 'r') as file:
        
            for line in file:
                if "GPGGA" in line:
                    gpgga = pynmea2.parse(line,check=True)   #grab gpgga sentence and parse
                    #check to see if we have lost GPS fix
                    if gpgga.gps_qual < 1:
                        continue
                    
                    # Create datetime from timestamp and file name
                    # Convert Month string to month num
                    month_str = gps_file[-21:-18]
                    
                    # January
                    if month_str == 'Jan':
                        month_num = '01'
                    # February
                    if month_str == 'Feb':
                        month_num = '02'
                    # March
                    if month_str == 'Mar':
                        month_num = '03'
                    # April
                    if month_str == 'Apr':
                        month_num = '04'
                    # May
                    if month_str == 'May':
                        month_num = '05'
                    # June
                    if month_str == 'Jun':
                        month_num = '06'
                    # July
                    if month_str == 'Jul':
                        month_num = '07'
                    # August
                    if month_str == 'Aug':
                        month_num = '08'
                    # September
                    if month_str == 'Sep':
                        month_num = '09'
                    # October 
                    if month_str == 'Oct':
                        month_num = '10'
                    # November
                    if month_str == 'Nov':
                        month_num = '11'
                    # December
                    if month_str == 'Dec':
                        month_num = '12'

                    # Compute Datetime
                    date_str = '{0}-{1}-{2}'.format(gps_file[-18:-14], month_num, gps_file[-23:-21])
                    gps_date = datetime.date.fromisoformat(date_str)
                    gps_datetime = datetime.datetime.combine(gps_date, gpgga.timestamp)
                    gps_time.append(gps_datetime)

                    # Read in other attributes from the GPGGA sentence
                    z.append(gpgga.altitude)
                    lat.append(gpgga.latitude)
                    lon.append(gpgga.longitude)
                elif "GPVTG" in line:
                    if gpgga.gps_qual < 1:
                        continue
                    gpvtg = pynmea2.parse(line,check=True)   #grab gpvtg sentence
                    u.append(gpvtg.spd_over_grnd_kmph*np.cos(gpvtg.true_track)) #units are kmph
                    v.append(gpvtg.spd_over_grnd_kmph*np.sin(gpvtg.true_track)) #units are kmph
                else: #if not GPGGA or GPVTG, continue to start of loop
                    continue

# Save GPS data to netCDF file
# Create gps time dimension
gps_time_dim = gpsgrp.createDimension('time', len(gps_time))

# GPS Time Variable
gps_time_nc = gpsgrp.createVariable('time', 'f8', ('time',))
gps_time_nc.units = "hours since 0001-01-01 00:00:00.0"
gps_time_nc.calendar = "gregorian"
gps_time_num = cftime.date2num(gps_time, units=gps_time_nc.units,calendar=gps_time_nc.calendar)
gps_time_nc[:] = gps_time_num

# Locations
lat_nc = gpsgrp.createVariable('lat', 'f8', ('time',))
lat_nc[:] = lat
lon_nc = gpsgrp.createVariable('lon', 'f8', ('time',))
lon_nc[:] = lon
z_nc = gpsgrp.createVariable('z', 'f8', ('time',))
z_nc[:] = z

# GPS Velocity variable
gps_velocity = gpsgrp.createDimension('gps_velocity', len(u))
u_nc = gpsgrp.createVariable('u', 'f8', ('gps_velocity',))
u_nc[:] = u
v_nc = gpsgrp.createVariable('v', 'f8', ('gps_velocity',))
v_nc[:] = v







