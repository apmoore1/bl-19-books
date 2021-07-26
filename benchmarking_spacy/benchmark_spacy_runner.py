import json
from pathlib import Path
import subprocess

from benchmark_spacy import SpacyVersion, ComponentNames

# models
model_names = [spacy_version.value for spacy_version in SpacyVersion]

# components to include
components_to_include = [[component_name.value] for component_name in ComponentNames]

batch_sizes = [1, 100, 200, 300]
text_size = 1000
run_file = str((Path.cwd() / 'benchmark_spacy.py'))


results = []
for model_name in model_names:
    for component_list in components_to_include:
        for batch_size in batch_sizes:
            params = ["python", f"{run_file}"]
            params.append(model_name)
            for component in component_list:
                params.append("-i")
                params.append(f"{component}")
            params.append("--text-size")
            params.append(f"{text_size}")
            params.append("--batch-size")
            params.append(f"{batch_size}")
            params.append("--json")
            result = subprocess.run(params, universal_newlines=True, capture_output=True)
            results.append(json.loads(result.stdout))

with Path(".", "results.json").open("w") as result_fp:
    json.dump(results, result_fp)