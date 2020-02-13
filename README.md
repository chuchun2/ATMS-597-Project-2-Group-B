# ATMS-597-Project-2-Group-B

Project 2 for ATMS 597 SP 2020.

## Description 
This project uses pandas to organize and view climate data and an API call to a data server at the National Centers for Environmental Information (NCEI) to produce a visualization of climate stripes, created by Ed Hawkins at the University of Reading. Using the daily maximum and minimum temperature, a daily average temperature is calculated. Pandas is then used to resample the daily average temperature to yearly, monthly, and weekly means. Then the standard deviations of either the weekly, monthly, or yearly mean temperature is calculated. Each climate stripe can represent the normalized anomalies of either the annual, monthly, or weekly mean temperature of a specific site called using a GHCN ID. In addition, a time series of the mean temperature can be plotted over the stripes as another means of viewing the temperature trend.

## Usage
The user can enter a GHCN site ID and a date range of their choice, while noting that the date range may be dependent on the site chosen. Then, the data is called from the NCEI API V2 for each year. Next, the user is asked to choose the frequency for plotting the stripes. Lastly, the user is asker whether or not they would like to plot a time series of the mean temeperature over the climate stripes.

## Authors and acknowledgment
Group B: Piyush Garg, Chu-Chun Chen, Michael Sessa
* Credit to Ed Hawkins for the Climate Stripes visualization, https://showyourstripes.info/
* NCEI CDO data: doi:10.7289/V5D21VHZ, doi:10.1175/JTECH-D-11-00103.1

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
