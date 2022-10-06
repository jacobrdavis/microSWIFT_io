#!/bin/bash

## Change git branch for each microSWIFT
# Description: This script goes through each microSWIFT and changes its git branch 
# to desired git branch that you enter as a user input. 

# User input on microSWIFT Range
read -p "Enter Lowest microSWIFT ID: " min
read -p "Enter Highest microSWIFT ID: " max
read -p "Enter git branch name you want to switch to: " branch
read -s -p "Enter Password: " password

printf "\n"

# Define SWIFT Range
NUMSWIFTSMIN=$min
NUMSWIFTSMAX=$max

# Define microSWIFT IP address 
IP="192.168.0."
PASSWORD=$password

# Loop through each microSWIFT possible and see who is online
for MSNUM in $(seq $NUMSWIFTSMIN $NUMSWIFTSMAX)
do
    # Ping the microSWIFT
    # Note it must be two pings to send and receive otherwise it wont be reached
    ping -c 2  $IP$MSNUM 2>&1 >/dev/null; PINGVAL=$?
    # If microSWIFT is online
    if [[ $PINGVAL -eq 0 ]]
    then
        echo "microSWIFT $MSNUM is online"
        # Pull from current branch to update before changing
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git pull"

        # Switch git branch to desired branch 
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git checkout -f $branch"

        # Pull from branch that it is switched to to update
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git pull"

         # Check Current Git branch and print to log
        echo "Current Git Branch:"
        sshpass -p $PASSWORD ssh pi@192.168.0.$MSNUM "cd ./microSWIFT; git branch | grep '*'"
        #revise-processing-start-condition - test branch name


    else
        echo "microSWIFT $MSNUM is offline"
    fi
done