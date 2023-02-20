import pandas as pd
import OAMFile
from datetime import timedelta


def dat_verify():
        #load_file = OAMFile.LoadFile()
        #self.df = load_file.get_file()
        #self.df = pd.read_csv('/Users/igorkiss/Documents/Igor Personal/Data/VAP2.csv', encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
        #self.df['DateTime'] = pd.to_datetime(self.df['DateTime'])
        #self.df.set_index('DateTime', inplace=True)
        #self.df.columns = self.df.columns.str.replace(' ', '_')
        #self.modes = self.df['O2_Mode'].unique()
        loader = OAMFile.CSV_Load(file_path='/Users/igorkiss/Documents/Igor Personal/Data/VAP2.csv')
        df = loader.load_file()

        # raise Exception if DataFrame is empty or None
        if df is None or df.empty:
            raise Exception('DataFrame is empty or None')
        # raise Exception if DataFrame does not contain the required columns
        if not all(col in df.columns for col in ['Signal_I/Q', 'SpO2', 'O2_Mode']):
            raise Exception('DataFrame does not contain the required columns')
        
        return df

df = dat_verify()
        
def signal_filter(df, min_signal, min_spo2):

    """Filter DataFrame by signal strength and SpO2"""
    return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

df_filter = signal_filter(df, 80, 50)

def filter_o2_mode(df, mode):
    """Filter DataFrame by O2 mode"""
    return df[df['O2_Mode'] == mode] 

df_filter_a = filter_o2_mode(df_filter, 'Auto')
print(df_filter_a)

# create function to calculate rolling average from filtered data frame and replace NaN values with 0
def rolling_avg(df, column, window):
    """Calculate rolling average"""
    return df[column].rolling(window).mean().fillna(0)

roll = rolling_avg(df_filter_a, 'SpO2', 10)
print(roll)




def percentage(df, column):
    """Calculate percentage of unique values in a column"""
    return df[column].value_counts(normalize=True) * 100
df_c = percentage(df, 'O2_Mode')
print(df_c)

# calculating O2 distribution from filtered data frame, rounding to 0 decimal places and removing values less than 1%
df_d = pd.DataFrame(percentage(df_filter, 'O2').round(0))
df_d = df_d[df_d['O2'] >= 1]
df_d.index.name = 'O2'
df_d.columns = ['Percentage']
print(df_d)
#TABLE
# claculate last 25% of O2 values from filtered data frame
df_e = df_filter['O2'].quantile(0.75)
# calculate avarage O2 value from filtered data frame
df_f = df_filter['O2'].mean()
# calculate first 75% of O2 values from filtered data frame
df_g = df_filter['O2'].quantile(0.25)
# creates a data frame with the calculated values
table_val = pd.DataFrame({'Parameter': ['Last 25% of O2', 'Average O2', 'First 75% of O2'], 'Value': [df_e, df_f, df_g]})
print(table_val)


def elapsed_time(dff):
    """Calculate elapsed time in seconds"""
    count = int(dff['O2'].count())
    return timedelta(seconds=count)

print(df_filter_a.columns)












