from dataclasses import dataclass
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5.QtWidgets import QFileDialog
import sys

@dataclass
class CSV_Load:
    file_path: str
    
    def load_file(self):
        df = pd.read_csv(self.file_path, encoding='unicode_escape', skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13]).dropna()
        df['DateTime'] = pd.to_datetime(df['DateTime'])
        df.set_index('DateTime', inplace=True)
        df.columns = df.columns.str.replace(' ', '_')
        modes = df['O2_Mode'].unique()

        return df




