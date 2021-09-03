#$ -S /bin/bash

#$ -q serial
#$ -l h_vmem=4G
#$ -N conda-install

source /etc/profile
module add anaconda3/wmlce

export CONDA_ENVS_PATH=$global_storage/conda/envs
export CONDA_PKGS_DIRS=$global_storage/conda/pkgs
export PIP_CACHE_DIR=$global_storage/conda/pip

conda_save_location=$global_storage/conda_environments/py3.8-bl-spacy-processing

conda-env create -p $conda_save_location --file ./environment.yml


if source activate $conda_save_location; then
	pip install -r conda_requirements.txt
else
    echo "Could not activate the conda environment at $conda_save_location"
fi

# Create a directory to store the language identification results
mkdir -p $global_storage/1890_english_books_spacy_output