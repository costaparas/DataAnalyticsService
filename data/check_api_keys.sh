#!/bin/sh
#Written by Costa Paraskevopoulos in October 2018
#Check that OMDb API keys are active

while read -r key
do
	printf "%s\n" "$key"
	wget -qO- "http://www.omdbapi.com?i=tt0114709&apikey=$key"
	printf "\n\n"
done < .api_keys.txt
