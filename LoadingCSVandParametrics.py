import csv
# from datetime import datetime

# from matplotlib import pyplot as plt

filename = 'VariablesCSV.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    NumOfColumns = len(header_row)
    NumOfTests = int(NumOfColumns-1)
    # print(NumOfTests)

for i in range(1,NumOfTests+1):
    print("\nData column = %d" % i)
    with open(filename) as f:
        reader = csv.reader(f)
        variables, values = [], []
        for row in reader:
            # print(row)
            
            current_var = row[0]
            print(current_var)
            # variables.append(current_var)
            
            test_val = row[i]
            print(test_val)
            if len(test_val) > 0:
                if isinstance(test_val, float):
                    current_value = float(test_val)
                    exec("%s = %f" % (current_var,current_value))
                elif isinstance(test_val, str):
                    current_value = test_val
                    exec("%s = %s" % (current_var,current_value))
                    # values.append(current_value)
                elif isinstance(test_val, int):
                    current_value = test_val
                    exec("%s = %d" % (current_var,current_value))                    
            else:
                exec("%s = %s" % (current_var,''))
                
        
    
        
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