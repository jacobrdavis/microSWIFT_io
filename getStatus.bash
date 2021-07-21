#!/bin/bash

## microSWIFT Status check
# Description: This script goes through each microSWIFT that you want to deploy and checks the current status of it,
# checking the current status includes a git pull to update each microSWIFT to the current version of the git repo, then
# print the branch information, test GPS sensor status, test IMU sensor status and check telemetry status.

# To-do list
# Test GPS sensor status
# test IMU sensor status
# Test Telemetry status

# User input on microSWIFT Range
read -p "Enter Lowest microSWIFT ID: " min
read -p "Enter Highest microSWIFT ID: " max
read -p "Enter UTC Date(DDMMMYYYY): " date
read -s -p "Enter Password: " password
printf "\n"

# Make Directory in current directory for this data that all data will be saved in 
mkdir -p ../$date

# Make Status log in the directory
status_log=../$date/status-$date.log
echo -e "Status file for $date \n" > $status_log
echo Status log created

# Define SWIFT Range
NUMSWIFTSMIN=$min
NUMSWIFTSMAX=$max

# Define microSWIFT IP address 
IP="192.168.0."
PASSWORD=$password

# Make empty array to be filled with microSWIFTS that are good to deploy
goodmicros=()

# Loop through each microSWIFT possible and see who is online
for MSNUM in $(seq $NUMSWIFTSMIN $NUMSWIFTSMAX)
do
    # Ping the microSWIFT
    # Note it must be two pings to send and receive otherwise it wont be reached
    ping -c 2  $IP$MSNUM 2>&1 >/dev/null; PINGVAL=$?
    # If microSWIFT is online, sync if not skip
    if [[ $PINGVAL -eq 0 ]]
    then
        echo "microSWIFT $MSNUM is online"
        echo "Checking Status now..."
        # To download on mac OS use the command: brew install hudochenkov/sshpass/sshpass
        echo "microSWIFT $MSNUM Information" >> $status_log
        echo "microSWIFT $MSNUM is online" >> $status_log

       
        # Check Current Git branch and print to log
        echo "Current Git Branch:" >> $status_log
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git branch | grep '*'" >> $status_log

        # Pull from remote to make sure microSWIFT is updated
        echo "Results from git pull:" >> $status_log
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git pull" >> $status_log
        
        # Add empty line before next status check
        echo -e "\n" >> $status_log


        # Add to list of good microSWIFTs if all tests are passed 
        goodmicros[${#goodmicros[@]}]="microSWIFT $MSNUM"

        # End status check
        echo "Status Check Complete for microSWIFT $MSNUM"
        echo -e "\n"
    else
        echo "microSWIFT $MSNUM Information" >> $status_log
        echo "microSWIFT $MSNUM is offline"
        echo -e "\n"
        echo "microSWIFT $MSNUM is offline" >> $status_log
        echo -e "\n" >> $status_log
    fi
done

# Print list of microSWIFTs that are ready to be deployed 
echo -e "\n" >> $status_log
echo "The microSWIFTs to be deployed on $date are:" >> $status_log
printf "%s\n" "${goodmicros[@]}" >> $status_log