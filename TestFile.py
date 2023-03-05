import pandas as pd
import TestUI

def signal_filter(df, min_signal, min_spo2):
    """Filter DataFrame by signal strength and SpO2"""
    return df[(df['Signal_I/Q'] >= min_signal) & (df['SpO2'] >= min_spo2)]

df = pd.DataFrame()
df_filter = signal_filter(df, 80, 50)
if __name__ == '__main__':
    from TestUI import MainWindow
    window = MainWindow()
    df = window.get_dataframe()
    

   


