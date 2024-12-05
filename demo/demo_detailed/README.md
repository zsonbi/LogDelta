# LogDelta
LogDelta - Hadoop demo detailed. 

Text work in progress...


## Setup
- `wget -O Hadoop.zip https://zenodo.org/records/8196385/files/Hadoop.zip?download=1`
- `unzip Hadoop.zip -d Hadoop`
- `python rename_hadoop.py`

## Demo 1 - Visualization

1. VIZ: App_vs_App - Application difference. App_4 antaa eron Application välillä. 
2. VIZ: Ano vs non-ano. Voidaan löytää ero isolle osalle anomalioita mutta osa edelleen jää. 
3. Anodetect_3. K-means erottaa normaalit anomaliasta Kun katsotaan container filuja 2-5 container__01_000005.log. 
Pahus taitaakin olla kyse siitä että Kmeans scoret kasvaa kun treeni-aineisto saa yhden uuden treeni filen. 