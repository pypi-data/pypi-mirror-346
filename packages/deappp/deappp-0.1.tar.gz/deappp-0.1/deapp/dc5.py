print(""" 

#dc5 mapper.py 
      
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
      

      

#dc5 reducer.py

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

#dc5 runcommand
      
type input.txt | python3 mapper.py | sort | python3 reducer.py
Get-Content input.txt | python3 mapper.py | sort | python3 reducer.py


""")