import json
from pathlib import Path

import typer

app = typer.Typer()

@app.command()
def analyse_results(character_count_file: Path = typer.Argument(Path('.', 'character_count_results.json'),
                                                                exists=True, dir_okay=False, file_okay=True,
                                                                help="File that contains the output/result from `character_range.py`"),
                    number_character_per_word: int = typer.Argument(4, help="Number of characters in a word.")) -> None:

    max_words = 0
    max_characters = 0
    with character_count_file.open('r') as character_count_fp:
        character_data = json.load(character_count_fp)
        max_characters = max(character_data['max_page_characters'])
        max_words = int(max_characters / number_character_per_word)
    typer.echo(f"Longest page from all of the books contains:\n{max_words} "
               f"words\n{max_characters} characters\nBased on "
               f"{number_character_per_word} per word.")


if __name__ == "__main__":
    app()