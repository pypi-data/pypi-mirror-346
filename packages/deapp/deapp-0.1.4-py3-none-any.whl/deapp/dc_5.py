print("""

# mapper.py


#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if line.startswith("Year"):  # skip header
        continue

    parts = line.split(",")
    if len(parts) < 5:
        continue

    year = parts[0]
    try:
        max_temp = int(parts[3])
        min_temp = int(parts[4])
        print(f"{year}\\t{min_temp} {max_temp}")
    except ValueError:
        continue



# reducer.py

#!/usr/bin/env python3
import sys
from collections import defaultdict

temps_by_year = defaultdict(list)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    try:
        year, temps = line.split("\\t")
        min_temp, max_temp = map(int, temps.split())
        temps_by_year[year].append((min_temp, max_temp))
    except:
        continue

for year in sorted(temps_by_year.keys()):
    mins, maxs = zip(*temps_by_year[year])
    print(f"{year}\\t{min(mins)}\\t{max(maxs)}")




# steps

su hduser

start-dfs.sh
start-yarn.sh
jps

hdfs dfs -mkdir -p /input
hdfs dfs -ls /

nano weather_data.txt

Year,Month,Day,Max Temp (°C),Min Temp (°C),Rainfall (mm)
1950,01,01,25,-18,43
1950,01,02,26,-17,44
1950,01,03,27,-12,32
1950,01,04,28,-20,41
1950,01,05,29,-13,40
1950,01,06,30,-16,45
1950,01,07,31,-14,33
1950,01,08,32,-19,38
1950,01,09,33,-20,28
1950,01,10,34,-19,40


hdfs dfs -put weather_data.txt /input
hdfs dfs -ls /input


nano mapper.py
nano reducer.py
chmod +x mapper.py
chmod +x reducer.py



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.*.jar -input /input/weather_data.txt -output /output -mapper mapper.py -reducer reducer.py


hdfs dfs -ls /output


hdfs dfs -cat /output/part-00000


------------------------- method 2 py --------------------------------

# mapper.py

import sys


for line in sys.stdin:
        line = line.strip()
        if line.startswith("Year"):
                continue
        parts = line.split(",")
        year = parts[0]
        temp = parts[1]
        print(f"{year}\\t{temp}")

# reducer.py

import sys

coolest_year = None
coolest_temp = float('inf')

hottest_year = None
hottest_temp = float('-inf')

for line in sys.stdin:
        line = line.strip()
        year,temp = line.split("\\t")

        temp = float(temp)
        if temp<coolest_temp:
                coolest_temp = temp
                coolest_year = year

        if temp>hottest_temp:
                hottest_temp = temp
                hottest_year = year

print(f"Hottest Year: {hottest_year} with {hottest_temp}°C")
print(f"Coolest Year: {coolest_year} with {coolest_temp}°C")


# nano weather_data.txt
Year,Temp
2010,11
2011,-2
2012,30


# command

cat weather_data.txt | python mapper.py | sort | python reducer.py



------------------------------ method 3 py ---------------------------------


# mapper

#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split()
    if len(parts) == 3:
        year, min_temp, max_temp = parts
        print(f"{year} {min_temp} {max_temp}")



# reducer

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
    # try:
    temps_by_year[year].append((int(min_temp), int(max_temp)))
    # except ValueError:
    #     continue  # skip if temperature can't be parsed

# Track year with lowest min and highest max
coolest_year = None
hottest_year = None
lowest_temp = float('inf')
highest_temp = float('-inf')

for year, temps in temps_by_year.items():
    min_temps, max_temps = zip(*temps)
    year_min = min(min_temps)
    year_max = max(max_temps)

    if year_min < lowest_temp:
        lowest_temp = year_min
        coolest_year = year

    if year_max > highest_temp:
        highest_temp = year_max
        hottest_year = year

# Output only the coolest and hottest years
if coolest_year is not None:
    print(f"Coolest Year: {coolest_year} with {lowest_temp}°C")

if hottest_year is not None:
    print(f"Hottest Year: {hottest_year} with {highest_temp}°C")



# input.txt

2012 -5 3
2012 -3 4
2013 -10 2
2013 5 12
2014 15 55
2014 -2 5
2012 -4 6
2013 0 9
1999 -20 40



# command

cat input.txt | python3 mapper.py | sort | python3 reducer.py







""")
