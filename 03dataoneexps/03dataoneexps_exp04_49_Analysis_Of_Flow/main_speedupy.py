from suds.client import Client
from pandas import Series
import matplotlib.pyplot as plt
import matplotlib.ticker

from speedupy.speedupy import initialize_speedupy, deterministic

def get_input():
    dados = None
    with open("main_speedupy.bin", "rb") as f:
        import pickle
        dados = pickle.load(f)
    return dados

@deterministic
def cell_1(dados):
    # Get the site's name from the response
    siteName = dados["siteName"]
    # Create some blank lists in which to put the values and their dates
    a = dados["a"]
    b = dados["b"]

    # Create a Pandas Series object from the lists
    # Set the index of the Series object to the dates
    ts = Series(a, index=b)
    return ts, siteName

@deterministic
def cell_2(ts):
    temp1 = ts.resample(rule='1D')
    tsAvg = temp1.agg('mean')#############ts.resample(rule='1D', base=0).mean()   # The daily average value for the 15 minute values
    
    temp2 = ts.resample(rule='1D')
    tsMin = temp2.agg('min')#############ts.resample(rule='1D', base=0).min()    # The minimum value for that day
    
    temp3 = ts.resample(rule='1D')
    tsMax = temp3.agg('max')#############ts.resample(rule='1D', base=0).max()    # The maximum value for that day
    
    return tsAvg, tsMin, tsMax

def cell_3(ts, tsAvg, tsMin, tsMax, siteName):
    # Generate a plot of the data subsets
    fig = plt.figure(figsize=(6.5,7)) # figsize(width,height)
    ax = fig.add_subplot(1, 1, 1)
    # Add data sets to the plot
    ts.plot(ax=ax, use_index=True, style='-', label='15-minute flow', color='lightgrey')
    tsAvg.plot(ax=ax, kind='line', use_index=True, style='-',
            marker='^', label='Average Daily Flow', color='blue')
    tsMax.plot(ax=ax, kind='line', use_index=True, style='-',
            marker='.', label='Maximum Daily Flow', color='red')
    tsMin.plot(ax=ax, kind='line', use_index=True, style='-',
            marker='.', label='Minimum Daily Flow', color='black')

    # Add commas to the values in the y-axis
    temp4 = ax.get_yaxis()
    temp4.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda y, p: format(int(y), 'n')))
    # Add labels to the plot
    ax.set_ylabel('Discharge, cubic feet per second')
    ax.set_xlabel('Date')
    # Add a grid
    ax.grid(True)
    # Add a legend
    legend = ax.legend(loc='upper left', shadow=True)
    # Add a title
    plt.title('Flow at %s' % (siteName))
    fig.tight_layout()
    # Make sure the plot displays
    plt.savefig("out.png")

@initialize_speedupy
def main():
    dados = get_input()
    ts, siteName = cell_1(dados)
    tsAvg, tsMin, tsMax = cell_2(ts)
    cell_3(ts, tsAvg, tsMin, tsMax, siteName)

main()