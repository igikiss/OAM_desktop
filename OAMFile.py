import pandas as pd
from PyQt5.QtWidgets import QFileDialog


class LoadFile:
    def __init__(self):
        self.df = None
        
    def get_file(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file', '\home', "CSV files (*.csv)")
        if fname[0]:
            self.df = pd.read_csv(fname[0], encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
            self.df['DateTime'] = pd.to_datetime(self.df['DateTime'])
            #set DateTime as index
            self.df.set_index('DateTime', inplace=True)
            self.df.columns = self.df.columns.str.replace(' ', '_')
            modes = self.df['O2_Mode'].unique()

