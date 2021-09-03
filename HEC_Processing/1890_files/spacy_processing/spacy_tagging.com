#$ -S /bin/bash

#$ -q serial
#$ -l h_vmem=1G
#$ -N spacy-tagging-1890
#$ -t 1-39

source /etc/profile
module add anaconda3/wmlce

conda_save_location=$global_storage/conda_environments/py3.8-bl-spacy-processing
source activate $conda_save_location


batch_folder_number=$(expr $SGE_TASK_ID - 1)
echo Job task $SGE_TASK_ID 
echo Running on batch folder $batch_folder_number

results_folder=$global_storage/1890_english_books_spacy_output
top_level_batch_folder=$global_storage/1890_english_books
batch_folder=$top_level_batch_folder/$batch_folder_number

python spacy_tagging.py $batch_folder $results_folder -i tagger