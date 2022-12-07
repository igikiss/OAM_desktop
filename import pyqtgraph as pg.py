import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pandas as pd

# Create a QApplication object to handle the main event loop
app = QtGui.QApplication([])

# Load some data from a CSV file
df = pd.read_csv("")

# Convert the "date" column to a datetime index
df.index = pd.to_datetime(df["date"])

# Create a window and set its title
win = pg.GraphicsWindow(title="Date and Time Plot")

# Add a plot to the window and set its title and labels
plot = win.addPlot(title="My Plot")
plot.setLabel("left", "Y")
plot.setLabel("bottom", "X")

# Set the minimum and maximum values for the x-axis as QDateTime objects
date_min = QtCore.QDateTime.fromString("2022-12-01 00:00:00", "yyyy-MM-dd hh:mm:ss")
date_max = QtCore.QDateTime.fromString("2022-12-31 23:59:59", "yyyy-MM-dd hh:mm:ss")
plot.setXRange(date_min, date_max)

# Add the data to the plot
plot.plot(x=df.index, y=df["value"], pen=pg.mkPen(color=(255, 0, 0), width=2))

# Show the window and run the main event loop
win.show()
app.exec_()
