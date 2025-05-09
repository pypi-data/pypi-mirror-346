print('''

A : 

Input to Mapper:
hello hadoop
hadoop program
hadoop world
hello world

su hduser
cd
nano word_count.txt(Paste input to mapper here then ctrl o + enter +ctrl x)

start-dfs.sh
start-yarn.sh
jps
hdfs dfs -ls /
#Delete any previous input or output files if present using: hdfs dfs -rm -r /input /output
hdfs dfs -mkdir -p /input
hdfs dfs -ls /
hdfs dfs -put word_count.txt /input/
hdfs dfs -ls /input/
whereis hadoop
hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.4.jar wordcount /input /output
hdfs dfs -ls /
hdfs dfs -ls /output/
hdfs dfs -cat /output/part-r-00000
stop-dfs.sh
stop-yarn.sh


----------------------------------------------------------------------------------------------------------------------------

B :

#mapper.py

#!/usr/bin/env python3
import sys
for line in sys.stdin:
    for char in line.strip():
        print(f"{char}\t1")
'''

#reducer.py
'''
#!/usr/bin/env python3
import sys
from collections import defaultdict
counts = defaultdict(int)
for line in sys.stdin:
    key, val = line.strip().split("\t")
    counts[key] += int(val)
for key in sorted(counts):
    print(f"{key}\t{counts[key]}")

'''

#hadoop commands
'''
su hduser
cd
start-dfs.sh
start-yarn.sh
jps
hdfs dfs -ls /
#Delete any previous input or output files if present using: hdfs dfs -rm -r /input /output
hdfs dfs -mkdir -p /input
nano character_count.txt
(type text or chars)
#Add your text in this file
#Press Ctrl + X
#Press Y
#Press Enter key

hdfs dfs -put character_count.txt /input/
nano mapper.py
#This will open the mapper.py file in nano editor; write the Mapper python code here
nano reducer.py
#Write the Reducer python code
chmod +x mapper.py
chmod +x reducer.py
whereis hadoop
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -input /input/character_count.txt -output /output/character_output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py

hdfs dfs -ls /output/character_output/
hdfs dfs -cat /output/character_output/part-00000
stop-dfs.sh
stop-yarn.sh




	''')