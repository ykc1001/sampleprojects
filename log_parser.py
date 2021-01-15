import csv
import pandas as pd
import math
import numpy as np
import os
import time

start_time = time.time()

# to parse specific logs, parse whole log then do stuff on it?

# parsing whole log
temp_filename = os.listdir('C:/Users/yk1001.choi/Desktop/parser test')[0]
filename = os.path.splitext(temp_filename)[0]

print('This program gives both all logs and specific logs you want to parse')

output = open(f'C:/Users/yk1001.choi/Desktop/parser test/{filename}_All_logs.csv', 'w')
with open('C:/Users/yk1001.choi/Desktop/parser test/test.txt', 'r', encoding='UTF-8-sig') as input_file:
    for line in input_file:
        if 'D/MACS_LOG > ,' in line:
            output.write(line) # when D/MACS_LOG>, is found, this is starting line and write it into output
            for line in input_file:
                output.write(line) # write the remaining lines under it
        
# parsing specific logs with pandas
    # input file
with open(f'C:/Users/yk1001.choi/Desktop/parser test/{filename}_All_logs.csv', 'r', encoding='UTF-8-sig') as temp:
    col_count = [len(l.split(',')) for l in temp.readlines()]
column_names = [i for i in range(max(col_count))]
csv_input = pd.read_csv(f'C:/Users/yk1001.choi/Desktop/parser test/{filename}_All_logs.csv', encoding= 'UTF-8-sig', header = None, delimiter = ',', names = column_names)

# change name for default columns and set timestamp column as index column for indexing
csv_input.rename(columns = {0 : 'Timestamp', 1 : 'Log', 2 : 'Systime'}, inplace = True)
csv_input.set_index('Timestamp', inplace = True)

# Select A6 or B6
scs = input('A6 or B6?: ')

# create SFN, SN 
if scs == 'B6':
    # csv_input['SFN'] = (np.floor(csv_input['Systime'] / 20)) % 1024
    csv_input['SFN'] = (csv_input['Systime'] // 20) % 1024
    csv_input['slot'] = csv_input['Systime'] % 20
elif scs == 'A6':
    # csv_input['SFN'] = (np.floor(csv_input['Systime'] / 80)) % 1024
    csv_input['SFN'] = (csv_input['Systime'] // 80) % 1024
    csv_input['slot'] = csv_input['Systime'] % 80

# mSystime
multiplier = 0
length = len(csv_input['Systime'].values)
list1 =[]
for i in range(length-1):
    if csv_input.iat[i,1] - csv_input.iat[i+1,1] < 20 :
        list1.append(multiplier)
    else:
        multiplier += 1
        list1.append(multiplier)
list1.insert(0,0)

# create new multiplier column in csv_input dataframe
csv_input['Multiplier'] = list1

# create m_systime columns
if scs == 'B6':
    csv_input['Multiplier'] = csv_input['Multiplier'] * 81920
    csv_input['M_systime'] = csv_input['Systime'] + csv_input['Multiplier']
elif scs == 'A6':
    csv_input['Multiplier'] = csv_input['Multiplier'] * 81920 * 4
    csv_input['M_systime'] = csv_input['Systime'] + csv_input['Multiplier']

# Delete multiplier column as it is not required in the final result
csv_input.drop('Multiplier', inplace = True, axis = 1)

print(' %s seconds ' % (time.time() - start_time))

# Get user input to choose which log user wants to parse
# If user enters non exisiting log -> print according log is not in log -> Raise error?????
print('Enter stop to start parsing')
list_logs = []
i = 0
while i <= 1:    
    log_name = input('Log: ')
    list_logs.append(log_name)
    if log_name == 'stop':
        break
new_list_logs = list_logs[:-1]

for log in new_list_logs:
    if log in csv_input['Log'].values:
        pass
    else:
        print(f'{log} is not in your log! Check again')

#parsing logs based on new_list_logs
temp = csv_input.loc[csv_input['Log'].isin(new_list_logs)]   #df.loc[] for selecting rows, df[] for selecting columns

# reindexing columns
cols = list(temp.columns)
new_cols = cols[:2] + cols[-3:] + cols[2:-3]
new_temp = temp.reindex(columns = new_cols)
# new_temp = temp[new_cols]

# output
new_temp.to_csv(f'C:/Users/yk1001.choi/Desktop/parser test/{filename}_logs.csv', index = True)





