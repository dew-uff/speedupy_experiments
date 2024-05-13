import sqlite3
import datetime
import matplotlib.pyplot as plt
from pandas import Series


fig = plt.figure(figsize=(9, 6))



siteID = '3'
siteName = 'Logan River at Main Street (Highway 89/91) Bridge'
variableID1 = '9'
variableID2 = '15'
startDateTime = "'2016-01-01'"
endDateTime = "'2016-12-31'"



conn = sqlite3.connect('cee6440_ex3_loganriver.sqlite')
sql_statement1 = 'SELECT LocalDateTime, DataValue ' \
                'FROM DataValues ' \
                'WHERE SiteID = ' + siteID + ' AND VariableID = ' + variableID1 + \
                ' AND LocalDateTime >= ' + startDateTime + ' AND LocalDateTime < ' + endDateTime + \
                ' AND QualityControlLevelID = 1 ' \
                'AND DataValue <> -9999 ' \
                'ORDER BY LocalDateTime'
cursor = conn.cursor()
cursor.execute(sql_statement1)
rows = cursor.fetchall()
localDateTimes1, dataValues1 = zip(*rows)



plotDates1 = []
for x in localDateTimes1:
    plotDates1.append(datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))



ts = Series(dataValues1, index=plotDates1)

####### Alteracao feita com base nesta resposta do StackOverflow https://stackoverflow.com/questions/23162472/python-pandas-daily-average
#######dailyAvg = ts.resample(rule='1D', base=0).mean() 
dailyAvg = ts.resample(rule='1D').agg("mean")

# Add the first subplot to the figure
ax = fig.add_subplot(1, 1, 1)  # (rows, columns, specific subplot assigned to ax)


# Plot the timeseries data
dailyAvg.plot(color='red')


# Set properties of the first subplot
plt.ylabel("Turbidity (NTU)", color='red')
plt.xlabel("Date")
plt.yticks(color='red')
plt.grid(axis='y')
plt.title("Average Daily Turbidity on the Logan River at Mendon Rd in 2016")


# Rotate the x-axis labels so they don't overlap and use matplotlib's
# automated tight layout function to arrange layout
plt.xticks(rotation=30)
fig.tight_layout()

# Display Plot
plt.savefig("out.png")
