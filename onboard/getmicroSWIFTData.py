# getData.py
'''
@edwinrainville

# Description: Goal is to query the network to see which microSWIFTS are available then access each one of them 
# and use rsync to sync the data that is on the microSWIFT to a buffer on the local machine 
# INPUTS:
# lowest microSWIFT ID number
# highest microSWIFT ID number
# OUTPUT: transfers all data from each microSWIFT into a directory in the local machine in the main directory

'''

# Import Statements
import subprocess # Subprocess example: subprocess.run(["ls", "-l"])
import pandas as pd
import datetime
import logging

#---INPUTS
IP              = "192.168.0."                          # base microSWIFT IP address
PASSWORD        = "1013ne40th"                          # microSWIFT password
project_dir     = './'                                  # project directory
microSWIFT_IDs  = [17,34,54,57,61]                      # IDs to offload
start_time      = datetime.datetime(2022,8,23,19,0,0)   # start_time
end_time        = datetime.datetime(2022,8,24,0,0,0)    # end_time
# record_window_length = datetime.timedelta(minutes=20) # record Window Length 

#--Functions

# Function to convert microSWIFT file name to datetime
def get_microSWIFT_file_time(fname):
    import datetime

    if '_2' in fname[-6:]:
        fname = fname[:-6] + fname[-4:]

    # Convert Month string to month num
    month_str = fname[-21:-18]
    
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
    date_str = '{0}-{1}-{2}T{3}:{4}:{5}'.format(fname[-18:-14], month_num, fname[-23:-21], fname[-13:-11], fname[-11:-9], fname[-9:-7])
    microSWIFT_file_time = datetime.datetime.fromisoformat(date_str)
    return microSWIFT_file_time

#---start of scripting

# User input for mission number 
mission_num = int(input('Enter Mission Number: '))

# Create Data Directory for Mission
mission_dir_str =  project_dir + "/microSWIFT_data/mission_{}".format(mission_num)
subprocess.run(["mkdir", "-p", mission_dir_str])

# Set up Data Offload Logging file
log_name = mission_dir_str + '/data_offload.log'
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.DEBUG)
logging.info('------------ Mission {} Data Offload ------------'.format(mission_num))

# Read in Start Time and convert to datetime
logging.info('Mission Start Time is: {}'.format(start_time))

# Read in End Time and convert to datetime
logging.info('Mission End Time is: {}'.format(end_time))

# Loop through each microSWIFT on the network to offload data
time_to_offload_list = []
num_offloaded = 0
microSWIFTs_not_offloaded = []
num_not_offloaded = 0

logging.info('------------ Data Offload ------------')
for microSWIFT in microSWIFT_IDs:

    # Offload time
    start_offload_time = datetime.datetime.utcnow()

    # Ping microSWIFT to see if it is on the network
    microSWIFT_ip_address = IP + str(microSWIFT)
    ping = subprocess.run(['ping', '-c', '2', microSWIFT_ip_address])
    ping_val = ping.returncode

    # If microSWIFT is on network (return code from process is zero)
    if ping_val == 0:
        logging.info('microSWIFT {} is online'.format(microSWIFT))

        # Make Directory for this microSWIFT
        microSWIFT_dir_str =  mission_dir_str + '/microSWIFT_{}'.format(microSWIFT)
        subprocess.run(["mkdir", "-p", microSWIFT_dir_str])

        # Copy microSWIFT log into the microSWIFT directory
        # To download on mac OS use the command: brew install hudochenkov/sshpass/sshpass
        log_offload_process = subprocess.run(['sshpass', '-p', PASSWORD, 'scp', 'pi@{}:/home/pi/microSWIFT/logs/microSWIFT.log'.format(microSWIFT_ip_address), microSWIFT_dir_str ]) 
        log_offload_process_rc = log_offload_process.returncode
        if log_offload_process_rc == 0:
            logging.info('--- microSWIFT.log offloaded')
        else:
            logging.info('--- microSWIFT.log could not be offloaded')

        # Get list of all data files on microSWIFT
        list_of_data_files = subprocess.run(['sshpass', '-p', PASSWORD, 'ssh', 'pi@{}'.format(microSWIFT_ip_address), 'ls ~/microSWIFT/data'], stdout=subprocess.PIPE, text=True).stdout.splitlines()

        # Sort through each file to see if it is within the mission (within 1 record window)
        for file_name in list_of_data_files:
            # Get aware time object of when file was created
            print(file_name)
            file_time = get_microSWIFT_file_time(file_name)

            # Compare to see if it was within the mission time frame or within one burst length of the mission start time 
            if (file_time >= start_time  and file_time <= end_time): #(start_time - record_window_length) 
                subprocess.run(['sshpass', '-p', PASSWORD, 'scp', 'pi@{0}:/home/pi/microSWIFT/data/{1}'.format(microSWIFT_ip_address, file_name), microSWIFT_dir_str])
                logging.info('--- {0} was copied to microSWIFT {1} data directory'.format(file_name, microSWIFT))

            else:
                continue
        
        # End Offload time 
        num_offloaded += 1
        time_to_offload_datetime = datetime.datetime.utcnow() - start_offload_time
        time_to_offload_float = time_to_offload_datetime.total_seconds()
        time_to_offload_list.append(time_to_offload_float)

    else:
        logging.info('microSWIFT {} is offline'.format(microSWIFT))
        microSWIFTs_not_offloaded.append(microSWIFT)
        num_not_offloaded += 1

# End of Data Offloading - Log offload statistics
# microSWIFTs that were not offloaded
if num_not_offloaded == 0:
    logging.info('All microSWIFTs on mission were offloaded')
else:
    logging.info('{0} microSWIFTs that were not offloaded were {1}'.format(num_not_offloaded, microSWIFTs_not_offloaded))

# Offload times
time_to_offload_avg = sum(time_to_offload_list)/num_offloaded
logging.info('The average offload time was {}'.format(time_to_offload_avg))

