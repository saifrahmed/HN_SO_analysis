# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:48:42 2018
"""

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def todays_date():
    
    """Returns today's date in 'YYYYMMDD' format"""
    
    todays_date = datetime.now()
    if todays_date.month <10:
        month = '0'+str(todays_date.month)
    else:
        month = str(todays_date.month)
    
    if todays_date.day <10:
        day = '0'+str(todays_date.day)
    else:
        day = str(todays_date.day)
    
    date = str(todays_date.year) + month + day
    return date

### hn_plots - function to plot 4 time series at once
###             for the needs of analysis of data from Hacker News (HN) and
###             Stack Overflow (SO)    

def hn_plots(data,
             freq = 'd',
             select_tech = ['d3js', 'javascript', 'tensorflow'],
             alpha = 0.7,
             after_date = '2017-01-01',
             output_date = todays_date(),
             common_var = 'hn_all_match_score',
             common_var2 = None,
             common_var3 = None,
             common_var4 = None,
             var1 = 'so_usage_cnt',
             var2 = 'so_score_sum',
             var3 = 'so_answers',
             var4 = 'so_views',
             subfolder = None):
    
    """
    PARAMETERS:
    1) data - input data
    2) freq - frequency of time series aggregation
    3) select_tech - technologies, for which data should be plotted
    4) alpha - transparency level
    5) after_date - date, from which time series should be plotted
    6) output_date - date of plot creation, goes to the name of outputted
        .png file
    7) common_var - ffirst time series which is used for all four plots
        (if not specified otherwise)
    8) common_var2, common_var3, common_var4 - first time series
        for the second, third and fourth plot (if not specified, `common_var`
        is used)
    9) var1, var2, var3, var4 - second time series used for consecutive
        plots (each has to be specified separately)
    """
    
    if(freq == 'w'):
        data = (data.groupby(['tech',
                       pd.Grouper(key = 'date', freq = 'W-MON')])
                .sum()
                .reset_index())
        freq_label = 'weekly'
    elif(freq == 'd'):
        freq_label = 'daily'
    elif(freq == 'M'):
        data = (data.groupby(['tech',
                       pd.Grouper(key = 'date', freq = freq)])
                .sum()
                .reset_index())
        freq_label = 'monthly'
     
    if common_var2 == None:
        common_var2 = common_var
    if common_var3 == None:
        common_var3 = common_var
    if common_var4 == None:
        common_var4 = common_var
        
    after_date_declared = after_date
    
    if subfolder == None:
        subfolder = ''
    else:
        subfolder = '.\\' + subfolder + '\\'
        
    for i in select_tech:#data.tech.unique():
        
        fig_daily = plt.figure(figsize = (16,10))
        fig_daily.subplots_adjust(hspace = 0.3)
        fig_daily.tight_layout()
        ax1 = plt.subplot(221)
        ax2 = ax1.twinx()
        ax3 = plt.subplot(222)
        ax4 = ax3.twinx()
        ax5 = plt.subplot(223)
        ax6 = ax5.twinx()
        ax7 = plt.subplot(224)
        ax8 = ax7.twinx()
        ax1.tick_params(axis='x', labelrotation =30)
        ax2.tick_params(axis='x', labelrotation =30)
        ax3.tick_params(axis='x', labelrotation =30)
        ax4.tick_params(axis='x', labelrotation =30)
        ax5.tick_params(axis='x', labelrotation =30)
        ax6.tick_params(axis='x', labelrotation =30)
        ax7.tick_params(axis='x', labelrotation =30)
        ax8.tick_params(axis='x', labelrotation =30)
        
        # First plot:
        after_date = (max(pd.to_datetime(after_date_declared),
                        data.loc[(data['tech'] == i) &
                                 ((data['hn_all_match_score'] > 0) | 
                                         (data['so_views']>0))]
            .date.min()).strftime('%Y-%m-%d'))
#        print(after_date)    
        data_plot = data.loc[(data['tech'] == i) & (data['date'] >= after_date)]
        ax1.plot(data_plot['date'], data_plot[common_var], 'g-', alpha = alpha)
        ax2.plot(data_plot['date'], data_plot[var1], 'b-', alpha = alpha)
    #    ax1.set_xlabel('Date')
        ax1.set_ylabel('HN', color = 'g')
        ax2.set_ylabel('SO', color = 'b')
        ax2.set_title(var1 + ' vs ' + common_var + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        
        # Second plot: 
        ax3.plot(data_plot['date'], data_plot[common_var2], 'g-', alpha = alpha)
        ax4.plot(data_plot['date'], data_plot[var2], 'b-', alpha = alpha)
    #    ax3.set_xlabel('Date')
    #    ax3.set_ylabel('Score HN', color = 'g')
#        ax3.tick_params(left='off', labelleft='off')
        ax3.set_ylabel('HN', color = 'g')
        ax4.set_ylabel('SO', color = 'b')
        ax4.set_title(var2 + ' vs ' + common_var2 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
    
        # Third plot: 
        ax5.plot(data_plot['date'], data_plot[common_var3], 'g-', alpha = alpha)
        ax6.plot(data_plot['date'], data_plot[var3], 'b-', alpha = alpha)
#        ax5.set_xlabel('Date')
        ax5.set_ylabel('HN', color = 'g')
        ax6.set_ylabel('SO', color = 'b')
        ax6.set_title(var3 + ' vs ' + common_var3 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        
        # Fourth plot: 
        ax7.plot(data_plot['date'], data_plot[common_var4], 'g-', alpha = alpha)
        ax8.plot(data_plot['date'], data_plot[var4], 'b-', alpha = alpha)
    #    ax7.set_xlabel('Date')
    #    ax7.set_ylabel('Score HN', color = 'g')
#        ax7.tick_params(left='off', labelleft='off')
        ax7.set_ylabel('HN', color = 'g')
        ax8.set_ylabel('SO', color = 'b')
        ax8.set_title(var4 + ' vs ' + common_var4 + ' for ' + i + ' since ' +
                      after_date + '; ' + freq_label)
        
#        fig_daily.autofmt_xdate()
        plt.xticks(rotation=90)
#        plt.setp(ax5.get_xticklabels(), visible=True)
        fig_daily.savefig(subfolder + output_date + '_' + i + '_' + common_var +
                          '_' +
                          common_var2 + '_' + common_var3 + '_' + common_var4 +
                          '_'+ freq + '_since' + after_date.replace('_', '')
                          + '.png'#, bbox_inches = 'tight'
                          )
        
### End of code