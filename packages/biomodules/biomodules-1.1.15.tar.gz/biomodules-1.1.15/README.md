# biomodules: 生物信息模块

## 基础模块（base）

1. `MergeDir`，给定一个输入文件夹和一个输出文件，把该文件夹下的所有文件合并到该文件中；
2. `CountLines`，给定一个文件计算其行数；
3. `MergeZipFile`，给定一个zip文件，将该zip文件下的所有文件合并为一个文件

## 序列相关（seq）

1. `Fastq2Fasta`，fastq转fasta；
2. `SubSeq`，从fasta文件中提取部分序列；

## 预处理模块（preprocessing）

1. `Fastqc`，使用fastqc进行质量控制；
2. `Filtlong`，使用Filtlong过滤reads；

## 序列比对（align）

1. `Blastn`，使用blastn进行序列比对；
2. `Minimap2`，使用minimap2进行序列比对；
3. `Samtools`，使用samtools处理比对结果；
4. `LowDepth`，提取samtools depth中低深度位点；
5. `Muscle`，muscle多序列比对；

## 变异检测（variant）

1. `Bgzip`，bgzip压缩；
2. `Bcftools`，bcftools相关功能；

## Oxford Nanopore（ont）

注意，使用该功能需要安装额外的包：

```shell
pip install biomodules[ont]
```

1. `medaka`，使用medaka call突变；

## 系统发育

1. `IQTree`，使用iqtree构建进化树