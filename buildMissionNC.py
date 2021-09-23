# Build microSWIFT netCDF data structure from raw text data files
'''
@edwinrainville

'''
# Import statements
from netCDF4 import Dataset
import datetime
import glob

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
imu_time_dim = imugrp.createDimension('time', len(imu_time))
imu_times = imugrp.createVariable('time', 'f8', ('time',))
imu_times[:] = imu_time

# ------ GPS Data Read-in ------
# Create GPS sub group
gpsgrp = microSWIFTgroup.createGroup('GPS')







