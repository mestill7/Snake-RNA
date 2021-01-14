import sys
import os
import subprocess
import pandas as pd

def collect_info(project_samples):
    dl_status={}
    pe_status={}
    read_status={}
    proj_samples=[line.rstrip() for line in open(project_samples)]
    for mysample in proj_samples:
        r1="fastq/" + mysample + "_1.fastq"
        r2="fastq/" + mysample + "_2.fastq"
        if os.path.isfile(r1) and os.path.isfile(r2):
            pe_status[mysample]="pair"
        else:
            pe_status[mysample]="single"
        dl_file="output/temp/" + mysample + "_SRAdownload.txt"
        if os.path.isfile(dl_file) :
            dl_status[mysample]="pass"
        else:
            dl_status[mysample]="fail"
        if pe_status[mysample]=="pair":
            r1_line_command="wc -l " + r1
            r1_lines=subprocess.check_output(r1_line_command, shell=True,stderr=subprocess.STDOUT)
            r1_lines=int(r1_lines.split()[0])
            r2_line_command="wc -l " + r2
            r2_lines=subprocess.check_output(r2_line_command, shell=True,stderr=subprocess.STDOUT)
            r2_lines=int(r2_lines.split()[0])
            if r1_lines==r2_lines:
                read_status[mysample]="equal"
            elif r1_lines!=r2_lines:
                read_status[mysample]="notequal"
        else:
            read_status[mysample]="equal"
    fin=pd.DataFrame({'dl_result':pd.Series(dl_status),'PE': pd.Series(pe_status),"read_pairing":pd.Series(read_status)})
    fin["use"] = "Yes"
    fin[(fin["PE"]=="pair") & (fin["read_pairing"]!="equal")] = "No"
    fin[fin["dl_result"]=="fail"] = "No"
    return(fin)

# a = collect_info("projectA_list.txt")
a = collect_info(sys.argv[1])
# now save the results in a csv in output
a.to_csv("output/SRA_full_result.csv")
with open("output/SRA_excludefiles.txt", 'w') as output:
    for row in list(a[a["use"]!="Yes"].index):
        output.write(str(row) + '\n')

with open("output/SRA_includefiles.txt", 'w') as output:
    for row in list(a[a["use"]=="Yes"].index):
        output.write(str(row) + '\n')