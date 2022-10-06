#!/bin/bash

# Description: Goal is to query the network to see which microSWIFTS are available then access each one of them 
# and use rsync to sync the data that is on the microSWIFT to a buffer on the local machine 
# INPUTS:
# lowest microSWIFT ID number
# highest microSWIFT ID number
# OUTPUT:
# transfers all data from each microSWIFT into a directory in the local machine in the main directory
# 

# User input on microSWIFT Range
read -p "Enter Lowest microSWIFT ID: " min
read -p "Enter Highest microSWIFT ID: " max
# read -p "Enter Mission Number: " mission_num
read -p "Enter Start Time (UTC) (DDMMMYYYY_HHMMSS): " start
read -p "Enter End Time (UTC) (DDMMMYYYY_HHMMSS): " end 
# read -s -p "Enter Password: " password
printf "\n"

# # Make Directory in current directory for this data that all data will be saved in 
# mkdir -p ../Data/Mission$mission_num

# # Define SWIFT Range
# NUMSWIFTSMIN=$min
# NUMSWIFTSMAX=$max

# Define dates and times
start_date=${start:0:9}
start_time=${start:10:16}
end_date=${end:0:9}
end_time=${end:10:16}

# Find Files in date range
printf "start date: $start_date\n"
printf "start time: $start_time\n"
printf "end date: $end_date\n"
printf "end time: $end_date\n"

# Define microSWIFT IP address 
IP="192.168.0."
PASSWORD=$password

# Loop through each microSWIFT possible and see who is online
for MSNUM in $(seq $min $max)
do
    # # Ping the microSWIFT
    # # Note it must be two pings to send and receive otherwise it wont be reached
    # ping -c 2  $IP$MSNUM 2>&1 >/dev/null; PINGVAL=$?
    # # If microSWIFT is online, sync if not skip
    # if [[ $PINGVAL -eq 0 ]]
    # then
        echo "microSWIFT $MSNUM is online"
        
        if [ $start_date = $end_date ]
        then
            echo "they are equal"Piee123451
            
        else
            echo "not equal"
        fi

        # # rsync locates data on microSWIFT and puts it in the local buffer
        # # Potential Flags for rsync -avzh
        # # To download on mac OS use the command: brew install hudochenkov/sshpass/sshpass
        # # rsync the data directory
        # sshpass -p $PASSWORD rsync -av --include "*/" --include="*$date*" --exclude="*" pi@$IP$MSNUM:/home/pi/microSWIFT/data ../Data/Mission$mission_num/$MSNUM --log-file=../Data/Mission$mission_num/dataoffload.log
        # # rsync the logs directory
        # sshpass -p $PASSWORD rsync -av --include "*/" --include="*$date*" --exclude="*" pi@$IP$MSNUM:/home/pi/microSWIFT/logs ../Data/Mission$mission_num/$MSNUM --log-file=../Data/Mission$mission_num/logoffload.log
    # else
    #     echo "microSWIFT $MSNUM is offline"
    # fi
done







