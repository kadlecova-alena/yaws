# yaws
Yet another worm scanner

## Introduction
This is a first version of a software for automatic analysis of survival of Caenorhabditis elegans. The idea is to take two pictures of a plate with the worm population on a flatbed scanner and identify living individuals based on their movement (= change of their position between the two images). Our method is inspired by WormScan (<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3311640/>) and Lifespan Machine (<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3865717/>).

## Description of the scripts
*scanner.py - Starts the scanning and takes two pictures of each plate placed on a scanner. The current setup allows to place 18 plates on each scanner. Script scans the plates in 9 rows, cuts the picture and covers the corners of the picture to hide the parts of neighbouring plates. The frequency and exact times of scanning can be set in crontab.
*fiji_macro.py - Runs the image analysis basic principle of which is to take the two pictures, subtract them and count the number of objects on a difference picture.
*counter.py - Runs the script fiji_macro for all of the pictures in a folder and generates a table with results for further analysis.
*blink.py - An aid for a user to find out which scanner has which ID.

## Authors
Jan Michelfeit & Alena Kadlecova

Developed in Laboratory of Growth Regulators, Palacký University & Institute of Experimental Botany AS CR (<http://www.rustreg.upol.cz/en/>)

## Acknowledgements
This work was supported by the Ministry of Education, Youth and Sports of the Czech Republic: INTER-COST (LTC17), project code LTC17072.

