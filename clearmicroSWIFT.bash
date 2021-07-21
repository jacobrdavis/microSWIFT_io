#!/bin/bash

## Clear microSWIFT data
# Description: This script will got through each buoy that is online - check that all data that is on each buoy 
# has been archived in the local directory - if all data has been archived then it will delete the data off of the microSWIFT 
# Deleting data from microSWIFT is irreversible! Be careful with this script!

# To-do items: 
# 1. Go through each microSWIFT
# 2. Check that all data has been locally archived 
# 3. print out that all files have been archived and if they have been ask if you want to delete
# 4. Delete files from microSWIFT - put this into daily log