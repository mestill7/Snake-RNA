# Snake-RNA:

This repository hosts an automated NGS data analysis pipeline to summarize expression data for batches of RNA-seq, emulating the functions of *recount2*. This Snakemake pipeline provides an alternative to the Rail-RNA pipeline described in "Reproducible RNA-seq analysis using recount2", doi: 10.1038/nbt.3838. 

## Dependency:
- [Anaconda](https://conda.io/docs/user-guide/install/linux.html) 
- [Samtools](https://github.com/samtools/samtools)

## Installation:
Clone this repository and change into the cloned Snake-RNA directory. 

To create an environment using the environment.yaml file, type the following:

`conda env create -f environment.yaml`

This will create a conda environment called recount.

## Usage note:

You must manually activate the conda environment prior to running the sh files. Type the following to activate the environment:

`conda activate recount`

The reason for this requirement is a failure of the conda environment to successfully activate from within a shell script.

## Overall description

This pipeline takes a list of SRA accession numbers for your desired RNA-seq samples, downloads the files from SRA, and performs quality checks on the files. All samples that pass the quality checks are then adaptor-trimmed, aligned to the genome, and expression matrices for both gene-level and exon-level counts are generated. To enable visualization, a bigwig is generated for each sample. This pipeline automatically detects for paired-end or single-end structure in the samples and treats each sample accordingly. This pipeline has been tested on murine samples, using the mm10 genome and the GENCODE(version M25) annotation. 

## Usage on an LSF cluster:

Copy the config.yaml, run\_recount\_cluster.sh, cluster.json, collect_SRA_essentials.py, Snakefile_partA and Snakefile_partB to your project directory. Also place the text file containing the SRA accession numbers for your desired RNA-seq samples in the project directory. Make sure the project directory structure is as follows:
```
.
├── cluster.json
├── config.yaml
├── Snake_partA
├── Snake_partB
├── collect_SRA_essentials.py
├── run_recount_cluster.sh
└── projectA_list.txt
```
Make any required changes to the config.yaml and cluster.json file.

collect_SRA_essentials.py

Next, type `nohup sh run_recount_cluster.sh 1 projectA_list.txt &` (to run in background).

## Usage on a local machine:

Copy the config.yaml, run\_recount.sh and Snakefile to your NGS project directory. Create a text file containing the SRA accession numbers for your desired RNA-seq samples. Make sure the project directory structure contains the following files:
```
.
├── config.yaml
├── Snake_partA
├── Snake_partB
├── collect_SRA_essentials.py
├── run_recount.sh
└── projectA_list.txt
```
Make the required changes to the config.yaml file.

Finally, type `sh run_recount.sh` followed by the maximum number of CPU cores to be used by snakemake and the name of the SRA accession list. For example, type `sh run_recount.sh 2 projectA_list.txt` for 2 CPU cores. You can also type `nohup sh run_recount.sh 2 projectA_list.txt &` to run the pipeline in background.

## Steps in RNA processing pipeline:

 ![ScreenShot](dag.png)

## Output directory structure:
```
.
├── cluster.json
├── config.yaml
├── fastq
│   ├── SampleA_1.fastq.gz
│   └── SampleA_2.fastq.gz
├── run_recount_cluster.sh
├── Snake_partA
├── Snake_partB
├── collect_SRA_essentials.py
└── output
    ├── counts_gene_matrix.txt
    ├── counts_exon_matrix.txt
    ├── multiqc_report.html
    ├── trim_fastq
    	├── SampleA_1.fastq.gz_trimming_report.txt
    	└── SampleA_2.fastq.gz_trimming_report.txt
    ├── logs
    ├── fastqc
    	├── SampleA_1_fastqc.html
    	├── SampleA_1_fastqc.zip
    	├── SampleA_2_fastqc.html
    	└── SampleA_2_fastqc.zip
    ├── bam
    	├── SampleA.bam
    	├── SampleA.bam.bai
    	├── SampleA.sorted.rmdup.bam
    	├── SampleA.sorted.rmdup.chr.bam
    	└── SampleA.sorted.rmdup.chr.bam.bai
    ├── bw
    	└── SampleA.sorted.rmdup.chr.bw
    └── counts
    	├── SRR11173864.exon.counts.txt
    	├── SRR11173864.exon.counts.txt.summary
    	├── SRR11173864.gene.counts.txt
    	├── SRR11173864.gene.counts.txt.summary
    	├── SRR11173864.junction.counts
    	├── SRR11173864.junction.counts.jcounts
    	└── SRR11173864.junction.counts.summary
```

## Additional Snakemake options:

You can also customize the run\_recount.sh and run\_recount_cluster.sh scripts according to your own needs. You might wish to change the number of cores snakemake uses. Or you might want to do a dryrun. To explore additional options available in snakemake, type:

`conda activate recount`

followed by 

`snakemake --help`
