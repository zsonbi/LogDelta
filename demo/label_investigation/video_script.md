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


#### Visualization based on textual content.
##### Simple plot
Previously, we focused solely on investigating log file names. Now, we’ll analyze the actual textual content within the runs. This analysis is specified in the file `2_viz_run_content.yml`. To generate the results, execute the command: `python -m logdelta.config_runner -c 2_viz_run_content.yml`
The output will be saved in the `out_2` folder. 

We’ll continue by examining the output, starting once again with the Simple Plot. This plot shows the runs with two axes: the number of log lines on the Y-axis and the number of unique terms on the X-axis. When we refer to terms, we mean words or tokens. LogDelta provides several methods for splitting text into terms.

Since the Y-axis remains the same as in the previous analysis, we can reuse the boundary of 3,000 log lines to classify a run as anomalous. On the X-axis, we observe that a reasonable boundary for unique terms could be set at 3,400 terms.

When we zoom inside the box defined by these boundaries—3,000 log lines and 3,400 terms—we find all 8 normal cases and only 3 anomalies. In other words, this approach performs slightly better than the previous one, as it can now correctly classify approximately 86% of anomalies, successfully identifying 18 out of 21.

##### U-MAP
Now, we turn our attention to the U-MAP plot, which is also produced in the previous run. U-MAP operates on the Document-Term Matrix, where log files are treated as documents, and terms are derived based on the word splitting applied during preprocessing.
For example, the Document-Term Matrix includes the following details:
- Log-file1: Contains the term "IP" 2 times, the term "address" 4 times, and the term "is" 3 times.
- Log-file2: Does not contain the term "IP," but the term "address" appears 3 times, and the term "is" appears 5 times.
- Log-file3: Contains the term "IP" once, does not include the term "address," and has the term "is" 9 times.

On the screen, we have three different U-MAP visualizations, generated by executing the script three times. U-MAP visualizations will vary between executions because compressing multidimensional space into two-dimensional space depends on a random seed that changes with each run. This variability makes it important to perform multiple runs and compare the outputs to evaluate how consistent and repeatable the observed patterns are.

We can also apply the boxing strategy here, where we use the boundaries on the Y and X axes of the normal cases to draw a box. Everything inside the box is classified as normal, while anything outside is considered anomalous. 

On the first U-MAP, we can see the drawn box on the screen. Within this box, there are 10 items, of which only two are anomalies. Moving on to the second U-MAP, applying the boxing strategy shows three anomalies inside the box, which still manages to cover all eight normal cases. This result is consistent with the previous result we got using simple map. Finally, in the third U-MAP, the box again captures all the normal cases and includes only two anomalies.

As shown on screen, it appears that the boxing strategy applied to U-MAP is slightly better than using boxing strategy on simple maps. 

However, at this point, I’m starting to grow suspicious of the run `Machine_Down_application_1445062781478_0020`.  In U-Map 1, it appears inside the box of normal points. Note that on the screen, I’ve zoomed into the boxes for better visibility. In U-Map 2, we see that this run is just outside the box boundary. Meanwhile, in U-Map 3, it is back inside the box.

Looking at the previous plots, we notice some inconsistency as well. In the Simple Plot with textual content, the run is inside the box. However, in the Simple Plot with file names, it is outside the box.

To summarize, the high-level visualization approach using boxes seems to yield fairly good results. However, we have some questions regarding the correctness of the labels. That said, we cannot make such decisions solely based on these high-level plots. We will proceed with more detailed analysis in the next videos to investigate further.

### Anomaly Detection

#### AD with run content
We now move on to building an anomaly detection model using the textual content of the runs. To train the model, we use only the normal runs. Once the model is trained, we test it against all runs, including the normal ones.When testing a normal run, LogDelta automatically excludes that specific run from the training data. This ensures that the same run is not used for both training and testing, preventing biased results.

This analysis is specified in the file `3_ano_run_content.yml`. To generate the results, execute the following command: `python -m logdelta.config_runner -c 3_ano_run_content.yml`. The output will be saved in the `out_3` folder. 

The output of this process is a Microsoft Excel spreadsheet. If you prefer, you can generate a CSV output instead by modifying the YAML configuration file. The Excel output includes scores from multiple anomaly detection methods. These include two well-known general-purpose anomaly detection methods K-Means and Isolation Forest, as well as two custom algorithms we’ve developed: the Out-of-Vocabulary Detector and the Rarity Model.

For more details about these custom models and their evaluation against the established general-purpose anomaly detection methods, refer to our paper titled "Speed and Performance of Parserless and Unsupervised Anomaly Detection Methods on Software Logs."

For summarization, we provide two scores. Z-score that scales each anomaly score and offers a combined metric. However, we recommend using the rank sum for sorting, as some metrics can be highly distorted and may disproportionately influence the z-score. The rank sum is simply the sum of the ranks across all metrics for each run. With four metrics, the lowest possible rank sum is 4, indicating that the run has the lowest rank in all anomaly metrics. Lower scores always indicate less anomalous behavior.

If we sort the runs by rank sum, we identify three suspicious cases. Ideally, we would expect the top of the rank sum list to be dominated by normal runs. However, we notice two machine-down runs among the lowest-ranking runs. One of these is `PageRank_MachineDown_application_1445062781478_0020`, which we previously flagged as suspicious. The other case is `PageRank_MachineDown_application_1445182159119_0017`, which seems even more similar to normal runs than the first. 

These are the first two cases of suspected incorrect labels. Additionally, we identify a third suspicious case: `PageRank_Normal_application_1445144423722_0024`. When sorted by rank sum score, this run should be grouped with the other normal runs, but it is not. This suggests that it behaves anomalously compared to the actual normal runs, raising questions about the correctness of its label.

In this video, we demonstrated how to develop an unsupervised anomaly detection model using normal runs data. When sorting by anomaly scores, most of the least anomalous cases were normal runs. However, three suspicious cases were identified: two where an anomalous label is suspected to be normal, and one normal case that is suspected to be anomalous.

#### AD with line level model
Next, we analyze each log line in isolation and assign an anomaly score to each line. LogDelta provides these line-level anomaly scores as Excel or CSV-files. However, a practical starting point is to use visualizations. These visualizations create a unique "fingerprint" for each run, making it easier to identify deviations. On the screen, you can see both a spreadsheet of log lines and a visualization of log lines.

It is important to highlight the distinction from the previous video. In that approach, we evaluated the entire textual content of a run and assigned an anomaly score to the run as a whole. In contrast, this line-by-line approach focuses on individual log lines. The difference is notable: the previous model answers the question, "Is this entire run anomalous?" whereas this model answers, "Is this specific log line anomalous?" 

The advantage of the line-by-line approach is its ability to pinpoint exactly which lines are anomalous, providing more detailed insights into the data.
--
This model is specified in file `4_ano_line_content.yml`. For line level prediction we have to select a particular file. Hadoop log data is organized in away that one log is kind of like the main log while other logs are like sub-processes or containers. For this analysis we build and test models at the main log file called `container__01_000001.log` in all runs. To get results execute `python -m logdelta.config_runner -c 4_ano_line_content.yml`. Output is in `out_4` folder.
--
Now we have the results. Lets open one run line-by-line visualization log labeled as Normal, namely `PageRank_Normal_application_1445182159119_0012`,  to explain what is visualized. First, X-axis corresponds to the line number while Y-axis shows the anomaly scores. Anomalies are scored with the four anomaly detection models Kmeans, Isolation Forrest, Rarity Model, and Out Of Vocabulury Detector. We have also added their moving averages over 10 and 100 log lines. All anomaly scores have been normalized from 0 to 1. Otherwise reading this would be impossible as each anomaly detection method score anomalies differently. 
--
It is good to check each anomaly models scores first. We can see that Isolation Forrest and K-means have more fluctation compared to Rarity Model. We also notive that  Out Of Vocabulury Detector detects no out of vocabulary terms in this file as it scores every line as zero. 
--
We can checkout some indivual points. Moving mouse over the point brings up tool tip that shows the log line in more detail. Checking few points shows that the higher scoring log lines do not appear to particularly alarming. 
--
By clicking on and off different anomaly scores, we can also see that the anomaly scores of different models are not very clustered. We do not see points where all models would score high values.  If look into moving averages we can see that the 3 models  Isolation Forrest and K-means and Rarity Model give this run very similar looking pattern while Out Of Vocabulury Detector is always zero. 

### Comparing Line-by-Line Finger Prints

#### Investigating all Normal runs
Now, we can use 100 elements moving average as our pattern and checkout if the other normal runs look anything similar. In total we have 8 runs labeled as normal other runs to check lets see. 

Did you notice any of the normal runs looking different from each other?
It might be difficult to formulate a pattern without looking at them side-by-side. Here is an image. Now it is very easy to spot which one of the pattern does not belong or just looks too different. Yes. The one on the bottom right. In addition to shape being different the X-axis label also tells us that this log-file is far longer than any of the other ones extending way past 2,000 lines while the second longest log only gets past the 1,400 log lines. The log-file standing out also belongs to the run we previously identified as suspiscious. That is the run `PageRank_Normal_application_1445144423722_0024`

We can have another finger print or pattern comparison if we select all the raw values. If we put again 8 side-by-side it looks like... TODO

Now lets look into more detail to this highly suspcious normal execution. First we clear out the moving averages and just look at individual line by line scores.  Hovering mouse over the most anomalous points show that there seems to be lack of disk space this is indicated with log message stating " Going to preempt 1 due to lack of space for maps". This suggest that this run is suffering from Disk Full anomaly. 

#### Investigate all DiskFulls

% COMMENTED OUT Now we compare the suspcious normal runs log line finger print against other Disk Full anomaly finger prints. This comparison still makes our suspect log quite different from other Disk Full anomalies. 

We can also see that Disk Full anomalies are not internally very consistent. The only pair that looks similar to each other are one in the center middel and the other one in lower left. 

We can have another finger print or pattern comparison if we select all the raw values. 

% COMMENTED OUT No we do start to see similarities. The suspect file has plenty of vertical lines caused by repeated rare log message. Also the disk full anomalies that are on the second row have similar vertical lines. 

#### Investigate all Machine Down anomalies

#### Investigate all Network anomalies. 

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


ATTIC

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
