# LogDelta
LogDelta - Hadoop demo detailed. 



## Setup
- `wget -O Hadoop.zip https://zenodo.org/records/8196385/files/Hadoop.zip?download=1`
- `unzip Hadoop.zip -d Hadoop`
- `python label_hadoop_runs_fixed.py`

The .yml files in this directory are demonstration configurations for various stages of log analysis, anomaly detection, distance measurement, and visualization using LogDelta. Each file focuses on a specific use case or part of the pipeline:

Visualization of Applications (demo_viz_app_X.yml): PageRank and WordCount. These configurations focus on visualizing application-specific data patterns.

Visualization of Anomalies (demo_viz_ano_X.yml).These files provide settings for visualizing detected anomalies.

Distance Measurement (demo_dist_X.yml). These files demonstrate configurations for measuring distances between log sequences.

Anomaly Detection (demo_anodetect_X.yml). These files define configurations for running anomaly detection and also visualizing anomalies on line level. 

