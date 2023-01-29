import pandas as pd
import OAMFile

class DataAnalysis:
    def __init__(self):
        #load_file = OAMFile.LoadFile()
        #self.df = load_file.get_file()
        self.df = pd.read_csv('/Users/igorkiss/Documents/Igor Personal/Data/VAP2.csv', encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
        self.df['DateTime'] = pd.to_datetime(self.df['DateTime'])
        self.df.set_index('DateTime', inplace=True)
        self.df.columns = self.df.columns.str.replace(' ', '_')
        self.modes = self.df['O2_Mode'].unique()
        
        
        
    def signal_filter(self, min_signal, min_spo2):
        """Filter DataFrame by signal strength and SpO2"""
        return self.df[(self.df['Signal_I/Q'] >= min_signal) & (self.df['SpO2'] >= min_spo2)]

    def filter_o2_mode(self, mode):
        """Filter DataFrame by O2 mode"""
        return self.df[self.df['O2_Mode'] == mode] 

    def percentage(self, column):
        """Calculate percentage of unique values in a column"""
        return self.df[column].value_counts(normalize=True) * 100

    def get_ticks(self, column):
        df_p = pd.DataFrame(self.percentage(column))
        df_p.columns = ['Percentage']
        df_p.index.name = column
        xval = list(range(1, len(df_p['Percentage']) + 1))
        ticks = []
        for i, item in enumerate(df_p.index):
            ticks.append((xval[i], item))
        return [ticks]
   

analysis = DataAnalysis()
df_f = analysis.signal_filter(80, 40)
df_m = analysis.filter_o2_mode('Manual')
df_a = analysis.filter_o2_mode('Auto')
df_p = pd.DataFrame(analysis.percentage('O2_Mode'))
df_p.columns = ['Percentage']
df_p.index.name = 'O2_Mode'

print(df_p)






    
    
      
    

    



