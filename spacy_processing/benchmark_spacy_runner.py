import json
from pathlib import Path
import subprocess
from itertools import combinations

from benchmark_spacy_tagging import ComponentNames

# components to include
all_components = list(ComponentNames)
all_combinations_of_components = []
for i in range(len(all_components)):
    for combination in combinations(all_components, i + 1):
        combination_names = [value.value for value in combination]
        all_combinations_of_components.append(combination_names)

run_file = str((Path.cwd() / 'benchmark_spacy_tagging.py'))


results = []
for component_list in all_combinations_of_components:
    params = ["python", f"{run_file}"]   
    for component in component_list:
        params.append("-i")
        params.append(f"{component}")
    result = subprocess.run(params, universal_newlines=True, capture_output=True)
    results.append(json.loads(result.stdout))

with Path(".", "benchmark_results.json").open("w") as result_fp:
    json.dump(results, result_fp)