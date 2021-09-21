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
import netCDF4 as nc

# Define microSWIFT IP address and Password
IP="192.168.0."
PASSWORD="1013ne40th"

# User input for mission number 
mission_num = int(input('Enter Mission Number: '))

# Create Data Directory for Mission
mission_dir_str =  "../mission_{}".format(mission_num)
subprocess.run(["mkdir", "-p", mission_dir_str])

# Set up Data Offload Logging file
log_name = '../mission_{}/data_offload.log'.format(mission_num)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.DEBUG)
logging.info('------------ Mission {} Data Offload ------------'.format(mission_num))

# Create dataframe object from DUNEX MetaData SpreadSheet
dunex_xlsx = pd.read_excel('/Users/edwinrainville/Documents/UW/DUNEX/DUNEXMainExp_Oct2021/DUNEXMainExp_MetaData.xlsx')

# Read in Start Time and convert to datetime
start_time = datetime.datetime.fromisoformat(dunex_xlsx['Start Time'].iloc[mission_num])
logging.info('Mission Start Time is: {}'.format(start_time))

# Read in End Time and convert to datetime
end_time = datetime.datetime.fromisoformat(dunex_xlsx['End Time'].iloc[mission_num])
logging.info('Mission End Time is: {}'.format(end_time))

# Read in list of microSWIFTs Deployed during the mission
microSWIFTs_deployed = []
for microSWIFT in dunex_xlsx['microSWIFTs Deployed'].iloc[mission_num].split(','):
    microSWIFTs_deployed.append(int(microSWIFT))
logging.info('microSWIFTs Deployed on this mission were: {}'.format(microSWIFTs_deployed))

# Loop through each microSWIFT on the network to offload data
logging.info('------------ Data Offload ------------')
for microSWIFT in microSWIFTs_deployed:
    # Ping microSWIFT to see if it is on the network
    microSWIFT_ip_address = IP + str(microSWIFT)
    ping = subprocess.run(['ping', '-c', '2', microSWIFT_ip_address])
    ping_val = ping.returncode

    # If microSWIFT is on network (return code from process is zero)
    if ping_val == 0:
        logging.info('microSWIFT {} is online'.format(microSWIFT))

        # Make Directory for this microSWIFT
        microSWIFT_dir_str =  "../mission_{0}/microSWIFT_{1}".format(mission_num, microSWIFT)
        subprocess.run(["mkdir", "-p", microSWIFT_dir_str])

        # Copy microSWIFT log into the microSWIFT directory
        log_offload_process = subprocess.run(['sshpass', '-p', PASSWORD, 'scp', 'pi@{}:/home/pi/microSWIFT/logs/microSWIFT.log'.format(microSWIFT_ip_address), microSWIFT_dir_str ]) 
        log_offload_process_rc = log_offload_process.returncode
        if log_offload_process_rc == 0:
            logging.info('--- microSWIFT.log offloaded')
        else:
            logging.info('--- microSWIFT.log could not be offloaded')

        # Get list of all data files on microSWIFT
        list_of_data_files = subprocess.run(['sshpass', '-p', PASSWORD, 'ssh', 'pi@{}'.format(microSWIFT_ip_address), 'ls ~/microSWIFT/data'], stdout=PIPE).stdout.splitlines()
        print(type(list_of_data_files))
        # # Sort through each file to see if it is within the mission (within 1 record window)
        # for file_name in data_file_list:
        #     subprocess.run(['sshpass', '-p', PASSWORD, 'scp', 'pi@{0}:/home/pi/microSWIFT/data/{1}'.format(microSWIFT_ip_address, file_name), microSWIFT_dir_str])
        #     logging.info('{0} is copied to microSWIFT {1} data directory'.format(file_name, microSWIFT))

    else:
        logging.info('microSWIFT {} is offline'.format(microSWIFT))
