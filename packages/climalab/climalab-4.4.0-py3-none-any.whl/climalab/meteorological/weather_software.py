#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

import numpy as np
import pandas as pd

#------------------------#
# Import project modules #
#------------------------#

from pygenutils.arrays_and_lists.patterns import approach_value
from pygenutils.time_handling.calendar_utils import week_range

#-------------------------#
# Define custom functions #
#-------------------------#

def temperature_typical_extreme_period(hdy_df_t2m):
    
    """
    Function that calculates the typical and extreme periods
    concerning the 2 metre temperature, required for E+ software
    as the third part of the header.
    Only temperature is needed to work with, 
    together with a date and time column.    
    """
    
    # HDY winter #
    #------------#
    
    hdy_df_t2m_dec = hdy_df_t2m[(hdy_df_t2m.date.dt.month == 12)]
    hdy_df_t2m_jan_feb = hdy_df_t2m[(hdy_df_t2m.date.dt.month >= 1) & 
                                    (hdy_df_t2m.date.dt.month <= 2)]
    hdy_df_t2m_winter = pd.concat([hdy_df_t2m_dec,hdy_df_t2m_jan_feb], axis = 0).reset_index()
    
    # Mininum temperature #
    HDY_winter_min = np.min(hdy_df_t2m_winter.t2m)
    iaprox_winter_min = np.where(hdy_df_t2m_winter == HDY_winter_min)[0][0]
    
    winter_date_min = hdy_df_t2m_winter.date.loc[iaprox_winter_min]
    winter_week_range_min = week_range(winter_date_min)
    
    winter_start_month_week_range_min = winter_week_range_min[0].month
    winter_end_month_week_range_min = winter_week_range_min[1].month
    
    winter_start_day_week_range_min = winter_week_range_min[0].day
    winter_end_day_week_range_min = winter_week_range_min[1].day
    
    winter_week_range_min_epw\
    = f"{winter_start_month_week_range_min:d}/"\
      f"{winter_start_day_week_range_min:2d},"\
      f"{winter_end_month_week_range_min:d}/"\
      f"{winter_end_day_week_range_min:2d}"
    
    # Average temperature #
    HDY_winter_avg = np.mean(hdy_df_t2m_winter.t2m)
    iaprox_winter_avg = approach_value(hdy_df_t2m_winter.t2m, HDY_winter_avg)[1]
    
    winter_date_aprox_avg = hdy_df_t2m_winter.date.loc[iaprox_winter_avg]
    winter_week_range_avg = week_range(winter_date_aprox_avg)
    
    winter_start_month_week_range_avg = winter_week_range_avg[0].month
    winter_end_month_week_range_avg = winter_week_range_avg[1].month
    
    winter_start_day_week_range_avg = winter_week_range_avg[0].day
    winter_end_day_week_range_avg = winter_week_range_avg[1].day
    
    winter_week_range_avg_epw\
    = f"{winter_start_month_week_range_avg:d}/"\
      f"{winter_start_day_week_range_avg:2d},"\
      f"{winter_end_month_week_range_avg:d}/"\
      f"{winter_end_day_week_range_avg:2d}"
    
    # HDY spring #
    #------------#
    
    hdy_df_t2m_spring = hdy_df_t2m[(hdy_df_t2m.date.dt.month >= 3)
                             & (hdy_df_t2m.date.dt.month <= 5)].reset_index() 
    
    # Average temperature only #
    HDY_spring_avg = np.mean(hdy_df_t2m_spring.t2m)
    iaprox_spring_avg = approach_value(hdy_df_t2m_spring.t2m, HDY_spring_avg)[1]
    
    spring_date_aprox_avg = hdy_df_t2m_spring.date.loc[iaprox_spring_avg]
    spring_week_range_avg = week_range(spring_date_aprox_avg)
    
    spring_start_month_week_range_avg = spring_week_range_avg[0].month
    spring_end_month_week_range_avg = spring_week_range_avg[1].month
    
    spring_start_day_week_range_avg = spring_week_range_avg[0].day
    spring_end_day_week_range_avg = spring_week_range_avg[1].day
    
    spring_week_range_avg_epw\
    = f"{spring_start_month_week_range_avg:d}/"\
      f"{spring_start_day_week_range_avg:2d},"\
      f"{spring_end_month_week_range_avg:d}/"\
      f"{spring_end_day_week_range_avg:2d}"
    
    # HDY summer #
    #------------#
    
    hdy_df_t2m_summer = hdy_df_t2m[(hdy_df_t2m.date.dt.month >= 6)
                             &(hdy_df_t2m.date.dt.month <= 8)].reset_index() 
    
    # Maximum temperature #
    HDY_summer_max = np.max(hdy_df_t2m_summer.t2m)
    iaprox_summer_max = np.where(hdy_df_t2m_summer == HDY_summer_max)[0][0]
    
    summer_date_max = hdy_df_t2m_summer.date.loc[iaprox_summer_max]
    summer_week_range_max = week_range(summer_date_max)
    
    summer_start_month_week_range_max = summer_week_range_max[0].month
    summer_end_month_week_range_max = summer_week_range_max[1].month
    
    summer_start_day_week_range_max = summer_week_range_max[0].day
    summer_end_day_week_range_max = summer_week_range_max[1].day
    
    summer_week_range_max_epw\
    = f"{summer_start_month_week_range_max:d}/"\
      f"{summer_start_day_week_range_max:2d},"\
      f"{summer_end_month_week_range_max:d}/"\
      f"{summer_end_day_week_range_max:2d}"
    
    # Average temperature #
    HDY_summer_avg = np.mean(hdy_df_t2m_summer.t2m)
    iaprox_summer_avg = approach_value(hdy_df_t2m_summer.t2m, HDY_summer_avg)[1]
    
    summer_date_aprox_avg = hdy_df_t2m_summer.date.loc[iaprox_summer_avg]
    summer_week_range_avg = week_range(summer_date_aprox_avg)
    
    summer_start_month_week_range_avg = summer_week_range_avg[0].month
    summer_end_month_week_range_avg = summer_week_range_avg[1].month
    
    summer_start_day_week_range_avg = summer_week_range_avg[0].day
    summer_end_day_week_range_avg = summer_week_range_avg[1].day
    
    summer_week_range_avg_epw\
    = f"{summer_start_month_week_range_avg:d}/"\
      f"{summer_start_day_week_range_avg:2d},"\
      f"{summer_end_month_week_range_avg:d}/"\
      f"{summer_end_day_week_range_avg:2d}"
    
    # HDY fall #
    #----------#
    
    hdy_df_t2m_fall = hdy_df_t2m[(hdy_df_t2m.date.dt.month >= 9)
                           &(hdy_df_t2m.date.dt.month <= 11)].reset_index() 
      
    # Average temperature only #
    HDY_fall_avg = np.mean(hdy_df_t2m_fall.t2m)
    iaprox_fall_avg = approach_value(hdy_df_t2m_fall.t2m, HDY_fall_avg)[1]
    
    fall_date_aprox_avg = hdy_df_t2m_fall.date.loc[iaprox_fall_avg]
    fall_week_range_avg = week_range(fall_date_aprox_avg)
    
    fall_start_month_week_range_avg = fall_week_range_avg[0].month
    fall_end_month_week_range_avg = fall_week_range_avg[1].month
    
    fall_start_day_week_range_avg = fall_week_range_avg[0].day
    fall_end_day_week_range_avg = fall_week_range_avg[1].day
    
    fall_week_range_avg_epw\
    = f"{fall_start_month_week_range_avg:d}/"\
      f"{fall_start_day_week_range_avg:2d},"\
      f"{fall_end_month_week_range_avg:d}/"\
      f"{fall_end_day_week_range_avg:2d}"
    
    # Define the third header #
    #-------------------------#
    
    header_3 = "TYPICAL/EXTREME PERIODS,6,Summer - Week Nearest Max Temperature For Period,Extreme,"\
               f"{summer_week_range_max_epw},Summer - Week Nearest Average Temperature For Period,Typical,"\
               f"{summer_week_range_avg_epw},Winter - Week Nearest Min Temperature For Period,Extreme,"\
               f"{winter_week_range_min_epw},Winter - Week Nearest Average Temperature For Period,Typical,"\
               f"{winter_week_range_avg_epw},Autumn - Week Nearest Average Temperature For Period,Typical,"\
               f"{fall_week_range_avg_epw},Spring - Week Nearest Average Temperature For Period,Typical,"\
               f"{spring_week_range_avg_epw}"
               
    return header_3
    

def epw_creator(HDY_df_epw,
                header_list,
                file_name_noext):
        
    # Open the writable file #
    epw_file_name = f"{file_name_noext}.epw"
    epw_file_obj = open(epw_file_name, "w")
    
    # Write the hearders down #
    for header in header_list:
        epw_file_obj.write(f"{header} \n")
    
    # Append HDY values to the headers # 
    HDY_df_epw_vals = HDY_df_epw.values
    HDY_ncols = HDY_df_epw_vals.shape[1]
    
    lhdy = len(HDY_df_epw)
       
    for t in range(lhdy):
        for ivar in range(HDY_ncols):
            epw_file_obj.write(f"{HDY_df_epw_vals[t,ivar]},")
            
            if ivar == HDY_ncols-1:
                epw_file_obj.write(f"{HDY_df_epw_vals[t,ivar]}\n" )
    
    # Close the file #
    epw_file_obj.close()
