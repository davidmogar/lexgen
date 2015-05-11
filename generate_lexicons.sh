#! /bin/bash
#
# Script to generate multiple datasets while I'm sleeping ;)

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.75 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --surnames --confidence 0.9 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --faces  --confidence 0.9 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces  --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --faces --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.5 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.25 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.75 --lexicon-percentage 0.05 --remove-outliers

python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers
python3 -m lexgen geolocated-asturias.json --surnames --confidence 0.9 --lexicon-percentage 0.05 --remove-outliers