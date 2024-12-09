import os
# Ensure this always gets executed in the same location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# There are some labels that very likely incorrect. They have NOT been fixed for this original file.  
# All 3 are for PageRank application 
# Old label Normal: application_1445144423722_0024 -> New label: DiskFull: application_1445144423722_0024
# Old label MachineDown: application_1445182159119_0017 ja application_1445062781478_0020 -> New label: Normal: application_1445182159119_0017 application_1445062781478_0020
# Mapping of application IDs to their respective test case (WordCount or PageRank) and status
mapping = {
    'WordCount': {
        'Normal': [
            'application_1445087491445_0005', 'application_1445087491445_0007', 'application_1445175094696_0005'
        ],
        'MachineDown': [
            'application_1445087491445_0001', 'application_1445087491445_0002', 'application_1445087491445_0003',
            'application_1445087491445_0004', 'application_1445087491445_0006', 'application_1445087491445_0008',
            'application_1445087491445_0009', 'application_1445087491445_0010', 'application_1445094324383_0001',
            'application_1445094324383_0002', 'application_1445094324383_0003', 'application_1445094324383_0004',
            'application_1445094324383_0005'
        ],
        'NetworkDisconnection': [
            'application_1445175094696_0001', 'application_1445175094696_0002', 'application_1445175094696_0003',
            'application_1445175094696_0004'
        ],
        'DiskFull': [
            'application_1445182159119_0001', 'application_1445182159119_0002', 'application_1445182159119_0003',
            'application_1445182159119_0004', 'application_1445182159119_0005'
        ]
    },
    'PageRank': {
        'Normal': [
            'application_1445062781478_0011', 'application_1445062781478_0016', 'application_1445062781478_0019',
            'application_1445076437777_0002', 'application_1445076437777_0005', 'application_1445144423722_0021',
            'application_1445182159119_0012', 'application_1445144423722_0024' 
            
        ],
        'MachineDown': [
            'application_1445062781478_0012', 'application_1445062781478_0013', 'application_1445062781478_0014',
            'application_1445062781478_0015', 'application_1445062781478_0017', 'application_1445062781478_0018',
            'application_1445076437777_0001', 'application_1445076437777_0003', 'application_1445182159119_0017',
            'application_1445076437777_0004', 'application_1445182159119_0016', 'application_1445062781478_0020',
            'application_1445182159119_0018', 'application_1445182159119_0019', 'application_1445182159119_0020'
        ],
        'NetworkDisconnection': [
            'application_1445144423722_0020', 'application_1445144423722_0022', 'application_1445144423722_0023'
        ],
        'DiskFull': [
            'application_1445182159119_0011', 'application_1445182159119_0013', 'application_1445182159119_0014',
            'application_1445182159119_0015'
        ]
    }
}

def rename_folders(base_path, mapping):
    for application_type, failures in mapping.items():
        for failure_type, applications in failures.items():
            for app in applications:
                old_folder_name = os.path.join(base_path, app)
                new_folder_name = os.path.join(base_path, f"{application_type}_{failure_type}_{app}")
                
                # Renaming the folder
                if os.path.exists(old_folder_name):
                    os.rename(old_folder_name, new_folder_name)
                    print(f"Renamed {old_folder_name} to {new_folder_name}")
                else:
                    print(f"Folder {old_folder_name} does not exist.")

# Base path where your application folders are located
base_path = 'Hadoop'

# Call the function to rename folders
rename_folders(base_path, mapping)
