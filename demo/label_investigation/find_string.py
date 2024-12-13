import os
# This program can be used to verify that the log message containing 
# "Going to preempt 1 due to lack of space for maps" is not part of normal runs
# and, in fact, only appears in these two runs: 1445182159119_0013 and 
# 1445182159119_0011, indicating they are disk full anomalies.
# We can also verify that "Could not delete hdfs:"
# also exists in the normal runs. Thus, the existence of these log lines in runs
# 1445182159119_0017 and 1445062781478_0020 does not prevent them from being normal runs.


def find_folders_with_string(base_directory, file_suffix, search_string):
    for root, dirs, files in os.walk(base_directory):
        # Skip folders that don't start with "PageRank"
        if not os.path.basename(root).startswith("PageRank"):
            continue
        
        for file in files:
            if file.endswith(file_suffix):
                file_path = os.path.join(root, file)
                #print(f"Checking file: {file_path}")  # Debugging line
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            if search_string in line:
                                print(f"Found in folder: {root}")
                                print(f"Line: {line.strip()}")
                                break
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Variables
base_directory = "Hadoop"  # Update this if needed
file_suffix = "_01_000001.log"
#search_string = "Could not delete hdfs:"
search_string = "Going to preempt 1 due to lack of space for maps"
find_folders_with_string(base_directory, file_suffix, search_string)
