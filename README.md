# pcapAnalyze
python scripts to analyze pcap files with the support of command tools of Wireshark

This repo collects python scripts to process pcap files for iTrafficMonitor system.

**Materials:**  

1. a pcap file  
2. log file of that pcap file, which contains packet logs for some packets in pcap file, like `{  "length" : 976,  "protocol" : "TCP",  "time" : "2018-12-27 23:48:45.861",  "dstIP" : "msga.cupid.iqiyi.com",  "dstPort" : "80",  "srcPort" : "0",  "srcIP" : "36.*.*.*"}`

## environment
OS version: macOS Mojave 10.14.2  
python version: Python 2.7.14  
Wireshark version: Wireshark 2.4.2 (v2.4.2-0-gb6c63ae)  

## How to use

### start with `extract.py`

put `extract.py` in the same directory with your pcapfile

`logfile`: path of log file  
`dnsile`: my `F` key doesn't work well so... this file is a output file, which contains some of dns records appeared in pcap file.  
`savefile`: another output file, which outputs hosts appeared in pcap file, except internal net address.  
`pcapfile`: that pcap file going to be processed.  

**used commands:**  

`tshark -r pcapfile -q -z "hosts"`: reads dns records in pcapfile  

### second step with `extract_flows.py`

put `extract_flows.py` with the same directory with your pcapfile

`extracted_flows_dir`: directory extracted pcaps with be put in.  
`targets_path`: which is the `savefile` in former step.
`pcapfile`: that pcap file going to be processed.

**used commands:**  

`"tshark -r %s -2 -R \"%s\" -w %s"%(pcap_path, rule, save_file)`: this cmd saves filtered packets in a new pcapfile

### last step with `extract_features.py`

put `extract_features.py` in `extracted_flows_dir` of second step.

`feature_file`: file that saves output features.  
`app`: app name  
`protocol`: protocol number  

**used commands:**  

`tshark -r pcapfile -q -z conv,tcp|wc -l`: use this to count the number of tcp flows in pcapfile(need to be minused by 6)  
`tshark -r %s -q -z follow,tcp,hex,%d"%(pcap,i)`: use this to get detailed information of a tcp stream. 
 

