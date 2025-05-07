print(""" 

#dc3 combined_mapper.py
      
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()

    # Character counting
    for char in line:
        print(f"CHAR_{char}\t1")

    # Word counting
    words = line.split()
    for word in words:
        print(f"WORD_{word}\t1")


#dc3 combined_reducer.py
      

#!/usr/bin/env python3
import sys; from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    key, value = line.strip().split('\t', 1)
    counts[key] += int(value)

# Output characters and words separately
print("=== Character Counts ===")
for key in sorted(counts):
    if key.startswith("CHAR_"):
        print(f"{key[5:]}\t{counts[key]}")

print("\n=== Word Counts ===")
for key in sorted(counts):
    if key.startswith("WORD_"):
        print(f"{key[5:]}\t{counts[key]}")

      
#dc 3 run command
      
type words.txt | python3 combined_mapper.py | sort | python3 combined_reducer.py  for cmd 
Get-Content words.txt | python combined_mapper.py | sort | python combined_reducer.py for powershell


    





""")