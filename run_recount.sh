# Snakefile 1
snakemake --snakefile Snake_partA --cores "$1"

while read line; do
    echo ${line}
    if [ -f "fastq/${line}_1.fastq" ]; then
        echo "${line}_1.fastq exists"
    else
        echo "${line}_1.fastq needs to be made"
        mv fastq/${line}.fastq fastq/${line}_1.fastq
    fi
done < $2

# Now need to use a python script
# goal is to line up the sample names, paired-end status, and successful download
python collect_SRA_essentials.py projectA_list.txt

while read line; do
    echo ${line}
    rm fastq/${line}_*.fastq
done < output/SRA_excludefiles.txt

# Subset the files
# while read line; do 
#     echo ${line}
#     if [ -f "fastq/${line}_1.fastq" ]; then
#         echo "downsampling ${line}_1.fastq"
#         seqtk sample -s100 fastq/${line}_1.fastq 500000 > fastq/${line}_1_sub.fastq
#         mv fastq/${line}_1_sub.fastq fastq/${line}_1.fastq
#     fi
#     if [ -f "fastq/${line}_2.fastq" ]; then
#         echo "downsampling ${line}_2.fastq"
#         seqtk sample -s100 fastq/${line}_2.fastq 500000 > fastq/${line}_2_sub.fastq
#         mv fastq/${line}_2_sub.fastq fastq/${line}_2.fastq
#     fi
# done < output/SRA_includefiles.txt

snakemake --snakefile Snake_partB --cores "$1"