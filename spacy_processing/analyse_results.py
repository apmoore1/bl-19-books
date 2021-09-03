from pathlib import Path


import numpy as np
import pandas as pd
import typer

app = typer.Typer()

@app.command()
def display_results(result_file: Path = Path('.', 'benchmark_results.json')) -> None:
    component_rank_order = {'tagger': 1, 'lemmatizer': 2, 'ner': 3, 'tagger,lemmatizer': 4,
                            'ner,tagger': 5, 'ner,lemmatizer': 6, 
                            'ner,tagger,lemmatizer': 7}
    component_rank_order_rev = {v: k for k, v in component_rank_order.items()}

    def re_index_model(table: pd.DataFrame) -> pd.DataFrame:
        new_index = [component_rank_order_rev[model] for model in table.index] 
        new_index = pd.Index(new_index, name="components")
        table.index = new_index
        return table

    with result_file.open("r") as results_fp:
        result_df = pd.read_json(results_fp)
        result_df['components'] = result_df['compoenets'].apply(','.join)
        result_df['components_order'] = result_df['components'].map(component_rank_order)
        number_pages_in_whole_corpus = 325 * 63984
        result_df['Whole Corpus Processing Time (Hours)'] = (result_df['time'] / 10) * number_pages_in_whole_corpus
        result_df['Whole Corpus Processing Time (Hours)'] = result_df['Whole Corpus Processing Time (Hours)'] / 3600
        result_df['time (S)'] = result_df['time']
        result_df['total memory (MB)'] = result_df['total_memory']
        
        pivot_results = result_df.pivot_table(index='components_order',  
                                              values=["time (S)", "total memory (MB)", "Whole Corpus Processing Time (Hours)"])
        pivot_results = re_index_model(pivot_results).round(3)
        typer.echo(pivot_results.to_html())

if __name__ == "__main__":
    app()