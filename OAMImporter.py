import pandas as pd
from PyQt5.QtWidgets import QFileDialog



def load_file():
    fname = QFileDialog.getOpenFileName(None, 'Open file', '\home', "CSV files (*.csv)")
    if fname[0]:
        df = pd.read_csv(fname[0], encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        #set DateTime as index
        df.set_index('DateTime', inplace=True)
        df.columns = df.columns.str.replace(' ', '_')
        modes = df['O2_Mode'].unique()
        print(modes)
        print(df.columns)

        def signal_filter(df, min_signal, min_spo2):
            """Filter DataFrame by signal strength and SpO2"""
            return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

        df_f = signal_filter(df, 80, 40)
        df_f.info()

   
        def filter_o2_mode(df, mode):
            """Filter DataFrame by O2 mode"""
            return df[df['O2_Mode'] == mode] 

        df_m = filter_o2_mode(df, 'Manual')
        df_a = filter_o2_mode(df, 'Auto')
        
        def percentage(df, column):
            """Calculate percentage of unique values in a column"""
            return df[column].value_counts(normalize=True) * 100
        
        
        df_p = pd.DataFrame(percentage(df, 'O2_Mode'))
        df_p.columns = ['Percentage']
        df_p.index.name = 'O2_Mode'
       
        xval = list(range(1,len(df_p['Percentage'])+1))
        ticks=[]
        for i, item in enumerate(df_p.index):
            ticks.append( (xval[i], item) )
        ticks = [ticks]
