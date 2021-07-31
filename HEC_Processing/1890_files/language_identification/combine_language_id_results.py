import json
from pathlib import Path

import typer


app = typer.Typer()

@app.command()
def combine_results(results_directory: Path = typer.Argument(..., exists=True, dir_okay=True, file_okay=False, help="Directory that contains a list of files, whereby each file contains a JSON string on each new line."),
                    combined_results_file: Path = typer.Argument(..., help="A file to write each JSON string from each file in the `results_directory` too, whereby each JSON string will be on a new line.")) -> None:
    with combined_results_file.open('w') as combined_fp:
        for result_file in results_directory.iterdir():
            with result_file.open('r') as result_fp:
                for line in result_fp:
                    line = line.strip()
                    if line:
                        result = json.loads(line)
                        combined_fp.write(f'{json.dumps(result)}\n')

if __name__ == "__main__":
    app()