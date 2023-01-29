import pandas as pd


class DataAnalysis:
    def __init__(self, df):
        self.df = df
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