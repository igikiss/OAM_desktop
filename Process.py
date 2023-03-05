from dataclasses import dataclass
import pandas as pd
from datetime import timedelta


@dataclass
class DataProcessor:
    df: pd.DataFrame
    
    def signal_filter(self, min_signal, min_spo2):
        """Filter DataFrame by signal strength and SpO2"""
        return self.df[(self.df['Signal_I/Q'] >= min_signal) & (self.df['SpO2'] >= min_spo2)]
    
    #vectorized function
    def signal_filter_v(self, min_signal, min_spo2):
        """Filter DataFrame by signal strength and SpO2"""
        return self.df[(self.df[['Signal_I/Q', 'SpO2']] >= [min_signal, min_spo2]).all(axis=1)]

    def filter_o2_mode(self, mode):
        """Filter DataFrame by O2 mode"""
        return self.df[self.df['O2_Mode'] == mode] 
    #vectorized function
    def filter_o2_mode_v(self, mode):
        """Filter DataFrame by O2 mode"""
        return self.df.loc[self.df['O2_Mode'].eq(mode)]


    def percentage(self, column):
        """Calculate percentage of unique values in a column"""
        return self.df[column].value_counts(normalize=True) * 100

    def o2_distribution(self):
        """Calculate O2 distribution from filtered data frame"""
        df_d = pd.DataFrame(self.percentage('O2')).round(0)
        df_d = df_d[df_d['O2'] >= 1]
        df_d.index.name = 'O2'
        df_d.columns = ['Percentage']
        return df_d
    
    def o2_distribution_v(self):
        """Calculate O2 distribution from filtered data frame"""
        df = self.filtered_df[['O2']]
        df = df[df['O2'] >= 1].round(0).value_counts().sort_index().reset_index()
        df.columns = ['O2', 'Count']
        df['Percentage'] = df['Count'] / df['Count'].sum() * 100
        return df.set_index('O2')[['Percentage']]
    

    def calculate_table(self):
        """Calculate table values"""
        df_filter = self.filter_o2_mode('Auto')
        df_e = df_filter['O2'].quantile(0.75)
        df_f = df_filter['O2'].mean().round(0)
        df_g = df_filter['O2'].quantile(0.25)
        df_h = df_filter['PI'].quantile(0.25)
        df_i = df_filter['PI'].quantile(0.75)
        table_val = pd.DataFrame({'Parameter': ['Last 25% of O2', 'Average O2', 'First 75% of O2', 'Temperature(°C)'], 
                                'Value': [df_filter['O2'].quantile(0.75), df_f, df_filter['O2'].quantile(0.25), df_filter['Temp_(°C)'].mean()]})
        return table_val

    def elapsed_time(self):
        """Calculate elapsed time in seconds"""
        count = int(self.df['O2'].count())
        return timedelta(seconds=count)

    def rolling_mean(self, column, window, mean_value):
        """Calculate rolling mean"""
        return self.df[column].rolling(window).mean().fillna(mean_value).round(0)

    def flow_o2_distribution(self):
        """Calculate O2 value distribution for each flow value"""
        df_filter = self.filter_o2_mode('Auto')
        df_j = df_filter.groupby('Flow_(L/min)').agg({'O2': ['count', 'mean', 'median', 'min', 'max']})
        df_j.columns = ['Count', 'Mean', 'Median', 'Min', 'Max']
        df_j = df_j.round(0)
        df_j = df_j[df_j['Count'] >= 1]
        return df_j

