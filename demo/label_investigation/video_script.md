# LogDelta
Hello, and welcome to this video! Today, we’ll explore how to analyze logs using the LogDelta tool. For this demonstration, we’re using data derived from two notable papers.

The original dataset comes from the 2016 paper "Log Clustering-Based Problem Identification for Online Service Systems", published in ICSE [^1]. This data has since been republished as part of the Log Hub Log Data Collection Set [^2], making it widely accessible for research and experimentation.

In this video, we’ll focus exclusively on the PageRank application from the dataset. While the dataset also includes a separate application—WordCount—that could be analyzed in a similar manner, we will leave that for a potential future investigation.


[^1]: Qingwei Lin, Hongyu Zhang, Jian-Guang Lou, Yu Zhang, Xuewei Chen. *Log Clustering Based Problem Identification for Online Service Systems*. International Conference on Software Engineering (ICSE), 2016.

[^2]: Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R. Lyu. *Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics*. IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

## Setup
To get started, we’ll begin by setting up LogDelta for our analysis. First, install LogDelta using pip.
Next, clone the LogDelta repository from GitHub.
After cloning the repository, navigate to the logdelta demo label-investigation folder.
Finally, download the Hadoop dataset and extract its contents into the working folder.
With these steps completed, we’re ready to dive into the analysis.

The Hadoop dataset includes labels in a separate file for the different runs we plan to analyze. To make this analysis compatible with LogDelta’s philosophy, it’s a good idea to rename the existing runs or folders using these label names. To assist with this, we provide a script that automates the renaming process, ensuring the labels are clearly associated with each run. This makes the analysis phase much more easier to follow.

- `pip install logdelta`
- `git clone https://github.com/EvoTestOps/LogDelta.git`
- `cd LogDelta/demo/label_investigation`
- `wget -O Hadoop.zip https://zenodo.org/records/8196385/files/Hadoop.zip?download=1`
- `unzip Hadoop.zip -d Hadoop`
- `python label_hadoop_runs_orig.py`


## Investigation

### Visualization 

#### Visualization based file names level. 
This is the most top level analysis. It is specified in file `1_viz_file_names.yml`. To get results execute `python -m logdelta.config_runner -c 1_viz_file_names.yml`. Output is in `out_1` folder.

Simple plot show runs with two axis the number of log lines in Y-axis the runs and number of unique file names in X-axis. 
Number of loglines in runs can be usefull as anomolous runs are often smaller or larger than normal run. 

For example paper by Landauer et al[^3] showed that one third of anomaly seqeuences in HDFS data set can be recognized by the fact that they shorter than any of the normal runs. 

[^3]: Landauer M, Skopik F, Wurzenberger M. A critical review of common log data sets used for evaluation of sequence-based anomaly detection techniques. Proceedings of the ACM on Software Engineering. 2024 Jul 12;1(FSE):1354-75.

For our Hadoop dataset, we can observe on the Y-axis that normal executions have a maximum of roughly 3,000 log lines. Additionally, the number of unique log file names, shown on the X-axis, can be particularly useful for analyzing large applications that produce multiple log files. Anomalous conditions might exhibit a larger or smaller number of unique log files compared to normal runs. In our case, normal executions have a maximum of about 15 unique log files.

Based on this straightforward analysis, we can define boundaries to classify anomalies. Specifically, any run with more than 15 files or more than 3,000 log lines would be considered anomalous. From the dataset, we have 29 runs in total, 8 of which are labeled as normal. When we zoom into the defined boundaries, we find 13 runs within the box—5 labeled as anomalies and the remaining 8 as normal. This simple approach achieves a roughly 76% accuracy in identifying anomalies, successfully detecting 16 out of 21 anomalies.

Lastly, we skip the UMAP plot for this analysis, as the input consists only of file names, which do not provide enough richness for such dimensionality reduction techniques.

TODO from here onwards

#### Visualization based on textual content.
##### Simple plot
Visualization on runs textual content on simple plot. This looks at beyond file names and analysis the actual textual content inside the runs. It is specified in file `2_viz_run_content.yml`. To get results execute `python -m logdelta.config_runner -c 2_viz_run_content.yml`. Output is in `out_2` folder.

In this case, simple plot show runs with two axis the number of log lines in Y-axis the runs and number of unique terms in X-axis. When we say terms we could also say words tokens. LogDelta offers different ways to split text to terms. Here we use word splitting that tries to split based on white spaces.

As we have the same Y-axis as in previous we can establish the previous boundary of 3000 log lines after which we can call a run an anomaly. Looking into X-axis we can see that bound for unique terms could be set to 3,400 terms. Zooming insize the box with boundies at 3,000 log lines and 3,400 terms, we can see that we have all of the 8 normal cases and only 3 anomalies. In otherwords, this approach was slight better than previous as now our boundaries might can correctly classify 86% of anomalies (18/21)

##### UMAP
Now we turn our attention to UMAP-plot. It is produced by the previous run. 
It should be noted that as UMAP results will be different between runs as compressing multidimensional space to two dimensional space is not exact science. So you may need to do multiple runs and check how repeatable the patterns are. 

Determinin a box around two U-Map dimensions gives us a similar result at last time meaning that using the bow we correctly classify over 90% of anomalies 19/21. 

However, at this point point run ending `Machine_Down_application_1445062781478_0020` start to look suspicious as it is completly surrenounded by normal points. If we look at the previous plots we can see the same. We also notice that `Normal_application_1445144423722_0024` always seems to be on the outer boundary of the normal cases.  

So the visualization approach with box seems to produce quite good results but we are left with suspicioun on two data points. 

### Anomaly Detection

#### AD with run content
We continue by forming an anomaly detection model on run content. We use the Normal runs without the one normal we were suspicious about to develop the model. Then we test all runs against the model. We also test the normal runs but for each normal run test the model excludes the normal run in question. This way we do not use the same run on both sides train and test. 

It is specified in file `3_ano_run_content.yml`. To get results execute `python -m logdelta.config_runner -c 3_ano_run_content.yml`. Output is in `out_3` folder.

This the output is Microsoft Excel speadsheet. You can also get CSV output if you like. 

The out has scores from multiple anomaly detection methods. Kmeans, Isolation Forrest are well know one. We have also developed to custom algorithms called Out Of Vocabulury Detector and Rarity Model. You can read more about from this paper.  

For summarization we offer z-score that scales each anomaly score and tries to offer combined metric. We however recommend using rank sum for sorting as the some metrics can be quite dissorted and can get too much weight in the Z-score. Rank sum is simply sum of ranks for each run. As we have 4 runs lowest possible score is 4 meaning that run has lowest rank in anomaly metrics. So again lower is less anomalous. 

If we sort by rank sum we can see that we have three abonormal cases. First we would expect the top end of rank sum list be filled with Normal runs. However, we see two machine down runs among the lowest ranking runs. One is the `PageRank_MachineDown_application_1445062781478_0020` that we already idenfied as suspicous. We also have another one `PageRank_MachineDown_application_1445182159119_0017`

So those are abnormalities one and two. The third abnormality is that the previously identified suspect run `PageRank_Normal_application_1445144423722_0024` should be among the top in rank sum score but it is not. Indicating it is anomalous combared to actual Normal runs

#### AD with line level model
Next, we move on to looking individual patterns by developing a line level anomaly detection models. These models look at each log line in isolation and give it anomaly score while the previous looked at the entire textual content of the run gave the whole run an anomaly score. The benefit of line-by-line model is that it can potentially point out which lines are anomalous and the visualations can illustrates how a typical normal runs looks. This gives each run like a visual finger print. 

This model is specified in file `4_ano_line_content.yml`. To get results execute `python -m logdelta.config_runner -c 4_ano_line_content.yml`. Output is in `out_4` folder.

For line level prediction we have to select a particular file. Hadoop log data is organized in away that one log is kind of like the main log while other logs are like sub-processes or containers. For this analysis we build and test models at the main log file called `container__01_000001.log` in all runs.  

Now we have the results. Lets open one run line-by-line visualization log labeled as Normal, namely `PageRank_Normal_application_1445182159119_0012`,  to explain what is visualized. First, X-axis corresponds to the line number while Y-axis shows the anomaly scores. Anomalies are scored with the four anomaly detection models Kmeans, Isolation Forrest, Rarity Model, and Out Of Vocabulury Detector. We have also added their moving averages over 10 and 100 log lines. All anomaly scores have been normalized from 0 to 1. Otherwise reading this would be impossible as each anomaly detection method score anomalies differently. 

It is good to check each score no normal values first. We can see that Isolation Forrest and K-means have more fluctation compared to Rarity Model. We also notive that  Out Of Vocabulury Detector detects no out of vocabulary terms in this file as it scores every line as zero. 

We can checkout some indivual points. Moving mouse over the point brings up tool tip that shows the log line in more detail. Checking few points shows that the higher scoring log lines do not appear to particularly alarming. PAUSE By clicking on and off different anomaly scores, we can also see that the anomaly scores of different models are not very clustered. We do not see points where all models would score high values.  

If look into moving averages we can see that the 3 models  Isolation Forrest and K-means and Rarity Model give this run very similar looking pattern while Out Of Vocabulury Detector is always zero. Now, we can use 100 elements moving average as our pattern and checkout if the other normal runs look anything similar. In total we have 8 runs labeled as normal other runs to check lets see. 

Did you notice any of the normal runs looking different from each other?
It might be difficult to formulate a pattern without looking at them side-by-side. Here is an image. Now it is very easy to spot which one of the pattern does not belong or just looks too different. Yes. The one on the bottom right. In addition to shape being different the X-axis label also tells us that this log-file is far longer than any of the other ones extending way past 2,000 lines while the second longest log only gets past the 1,400 log lines. The log-file standing out also belongs to the run we previously identified as suspiscious. That is the run `PageRank_Normal_application_1445144423722_0024`

Now lets look into more detail to this highly suspcious normal execution. First we clear out the moving averages and just look at individual line by line scores.  Hovering mouse over the most anomalous points show that there seems to be lack of disk space this is indicated with log message stating " Going to preempt 1 due to lack of space for maps". This suggest that this run might suffer from Disk Full anomaly. 

Now we compare the suspcious normal runs log line finger print against other Disk Full anomaly finger prints. This comparison still makes our suspect log quite different from other Disk Full anomalies. We can also see that Disk Full anomalies are not internally very consistent. The only pair that looks similar to each other are one in the center middel and the other one in lower left. 

We can have another finger print or pattern comparison if we select all the raw values. No we do start to see similarities. The suspect file has plenty of vertical lines caused by repeated rare log message. Also the disk full anomalies that are on the second row have similar vertical lines. 

Normal->DF
We conclude that our suspect normal run `PageRank_Normal_application_1445144423722_0024` is actually a Diskfull anomaly.


MD -> Normal
What about the other suspect cases. We had two machine down anomalies that looked like Normal runs. 
`PageRank_MachineDown_application_1445182159119_0017` Fingerprint super normal. Put on next to normals

MD -> MD
`PageRank_MachineDown_application_1445062781478_0020` Not normal enough too much Yellow OOVD raw

MD -> Disk full 
looks like Diskfull as well. 
`PageRank_MachineDown_application_1445182151478_0015` has lack of space for maps
Java.io. There is not enough space. 

DF -> MD
119_0013
119_0011

Summary
DF +1 +1 -2 = +0
Normal -1 +1 = 0
MD -1 -1 +2 = +0 

### Summary
Below we present fixed labels. The cases for turning IDs ending 0024 0015 to disk full is straight forward as we are able to find messages in the logs indicating disk is full or lack of disk space. The cases for  turning IDs ending 0013 0011 from Disk full to machine down is based on the oppostite. We did not find any log messages indicating lack of disk space. And their profiles or finger prints are similar to machine down runs. Finally changing ID ending 119_0017 from Machine Down to Normal is based on the runs profile being as similar to other Normals as possible.  


| ID                 | Orig Label    | Fixed Label    |
|--------------------|---------------|----------------|
| 1445144423722_0024 | Normal        | Disk Full      |
| 1445182159119_0017 | Machine Down  | Normal         |
| 1445182151478_0015 | Machine Down  | Disk Full      |
| 1445182159119_0013 | Disk Full     | Machine Down   |
| 1445182159119_0011 | Disk Full     | Machine Down   |


There were two in below table that are suspicous with their possible new labels. However, in the end there was not enough evidence to state that labels are incorrect. We follow the principle that changing a label requires more evidence than retaining current label. What this means in practice is that we keep the labels as they are. However, shall I had seen the two runs without any knowledge their orignal labels I would classify them under the possible label. All in all, it seems that there are runs that are on the borderline between Normal and Machine Down and the line between them is not clear. 


| ID                 | Orig Label    | Possible Label |
|--------------------|---------------|----------------|
| 1445062781478_0020 | Machine Down  | Normal         |
| 1445076437777_0005 | Normal        | Machine Down   |



### Dead Ends

From this video, we have left out analysis that did not yield clear results. Those were inparticular analysis of run distances measured with pair-wise distances like Jaccard distance, Cosine distance and Compression Distance. In principle, those analysis should yield similar results as the anomaly detection based and visualization based analysis. However, it seemed that distances between log files were too small that made the distance based analysis inconclusive. You should checkout distance based demostrations in the other demo folders as it can provide meaningfull results in other contexts. 

Other analysis that we excluded was visualization at log file level textual contents as each log file can be visualized against the same log in other runs. We only did run level textual content visualization that considers all logs from the runs. Similarly we could have log file level anomaly detection. Now we only did run level and jumped directly to line level. In Hadoop data file by file comparisons did not yield results that would have broguht further insight so they were left out. However, in some other context analysing different log files only against each other might reveal intresting details if the differences between logs are very focused on a single file. In Hadoop the main log file name `container__01_000001.log` was the largest and dominated the results while sub-process log analysis.

Finally, we did not investigate effect of different log enhancements like log parsing or using different tokiniers or vectorizers. 


## Conclusion
The purpose of this demo is to demonstarte the process that discovering the incorrent labels. We are highly confident that 