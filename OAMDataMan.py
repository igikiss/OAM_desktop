import pandas as pd
import OAMFile
from PyQt5 import QtWidgets
import sys 

def dat_verify():
        #load_file = OAMFile.LoadFile()
        #self.df = load_file.get_file()
        #self.df = pd.read_csv('/Users/igorkiss/Documents/Igor Personal/Data/VAP2.csv', encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
        #self.df['DateTime'] = pd.to_datetime(self.df['DateTime'])
        #self.df.set_index('DateTime', inplace=True)
        #self.df.columns = self.df.columns.str.replace(' ', '_')
        #self.modes = self.df['O2_Mode'].unique()
        loader = OAMFile.DataFrameLoader(file_path='/Users/igorkiss/Documents/Igor Personal/Data/VAP2.csv')
        df = loader.load_file()

        # raise Exception if DataFrame is empty or None
        if df is None or df.empty:
            raise Exception('DataFrame is empty or None')
        # raise Exception if DataFrame does not contain the required columns
        if not all(col in df.columns for col in ['Signal_I/Q', 'SpO2', 'O2_Mode']):
            raise Exception('DataFrame does not contain the required columns')
        
        return df

df = dat_verify()
print(df)
        
def signal_filter(df, min_signal, min_spo2):

    """Filter DataFrame by signal strength and SpO2"""
    return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

df_a = signal_filter(df, 90, 90)
print(df_a)

def filter_o2_mode(df, mode):
    """Filter DataFrame by O2 mode"""
    return df[df['O2_Mode'] == mode] 

df_b = filter_o2_mode(df_a, 'Auto')
print(df_b)

def percentage(df, column):
    """Calculate percentage of unique values in a column"""
    return df[column].value_counts(normalize=True) * 100
df_c = percentage(df, 'O2_Mode')
print(df_c)

def get_ticks(df, column):
    df_p = pd.DataFrame(percentage(column))
    df_p.columns = ['Percentage']
    df_p.index.name = column
    xval = list(range(1, len(df_p['Percentage']) + 1))
    ticks = []
    for i, item in enumerate(df_p.index):
        ticks.append((xval[i], item))
    return [ticks]
