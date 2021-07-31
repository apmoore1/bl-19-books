#$ -S /bin/bash

#$ -q serial
#$ -N language-id
#$ -t 1-48

source /etc/profile
module add anaconda3/wmlce
conda_save_location=$global_storage/conda_environments/py3.8-bl-language-id

source activate $conda_save_location

batch_folder_number=$(expr $SGE_TASK_ID - 1)
echo Job task $SGE_TASK_ID 
echo Running on batch folder $batch_folder_number

bl_books_model_dir=$global_storage/bl-books-models
language_id_model_path=$bl_books_model_dir/large-language-id.bin
top_level_batch_folder=$global_storage/1890_books
batch_folder=$top_level_batch_folder/$batch_folder_number
results_file=$top_level_batch_folder/language_id_results/${batch_folder_number}.json

for FILE in $batch_folder/*
do
    python ./language_id.py $language_id_model_path $FILE $results_file false
done



