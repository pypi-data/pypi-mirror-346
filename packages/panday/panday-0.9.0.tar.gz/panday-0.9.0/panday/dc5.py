print('''
#mapper.py
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    if len(parts) == 3:
        date_str, min_temp, max_temp = parts
        if "-" in date_str:
            year = date_str.split("-")[0]
            print(f"{year} {min_temp} {max_temp}")

#reducer.py

#!/usr/bin/env python3
import sys
from collections import defaultdict

temps_by_year = defaultdict(list)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) != 3:
        continue
    year, min_temp, max_temp = parts
    try:
        temps_by_year[year].append((int(min_temp), int(max_temp)))
    except:
        continue

for year in sorted(temps_by_year.keys()):
    mins, maxs = zip(*temps_by_year[year])
    print(f"{year}\t{min(mins)}\t{max(maxs)}")

#hadoop commands

su hduser
cd
start-dfs.sh
start-yarn.sh
jps
#Delete any previous input or output files if present using: hdfs dfs -rm -r /input /output
hdfs dfs -mkdir -p /input
hdfs dfs -ls /
nano weather_data.txt
#weather_data.txt file will open in nano text editor
#Copy the text from the provided weather data text file and paste it here
#Press Ctrl + X
#Press Y
#Press Enter key
hdfs dfs -put weather_data.txt /input/
hdfs dfs -ls /input/
nano mapper.py
#This will open the mapper.py file in nano editor; write the Mapper python code here
#Here’s the code for mapper.py
nano reducer.py
chmod +x mapper.py
chmod +x reducer.py
whereis hadoop
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -input /input/weather_data.txt -output /output/weather_output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py
hdfs dfs -ls /output/weather_output/
hdfs dfs -cat /output/weather_output/part-00000
stop-dfs.sh
stop-yarn.sh
''')