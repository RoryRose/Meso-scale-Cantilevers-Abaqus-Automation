import csv
from datetime import datetime

# from matplotlib import pyplot as plt

filename = 'VariablesCSV.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)

    # Get dates and high temperatures from this file.
    variables, values = [], []
    for row in reader:
        print(row)
        
        current_var = row[0]
        # variables.append(current_var)
        
        try:
            current_value = float(row[1])
            exec("%s = %f" % (current_var,current_value))
        except ValueError:
            current_value = row[1]
            exec("%s = %s" % (current_var,current_value))
        # values.append(current_value)
        
        
# x='buffalo'    
# exec("%s = %d" % (x,2))

# filename = 'data/sitka_weather_2018_simple.csv'
# with open(filename) as f:
#     reader = csv.reader(f)
#     header_row = next(reader)
#     print(header_row)

#     # Get dates and high temperatures from this file.
#     dates, highs = [], []
#     for row in reader:
#         print(row)
#         current_date = datetime.strptime(row[2], '%Y-%m-%d')
#         dates.append(current_date)
#         high = int(row[5])
#         highs.append(high)

# # Plot the high temperatures.
# plt.style.use('seaborn')
# fig, ax = plt.subplots()
# ax.plot(dates, highs, c='red')

# # Format plot.
# ax.set_title("Daily high temperatures - 2018", fontsize=24)
# ax.set_xlabel('', fontsize=16)
# fig.autofmt_xdate()
# ax.set_ylabel("Temperature (F)", fontsize=16)
# ax.tick_params(axis='both', which='major', labelsize=16)

# plt.show()