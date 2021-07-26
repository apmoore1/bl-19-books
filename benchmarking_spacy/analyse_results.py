from pathlib import Path


import numpy as np
import pandas as pd
import typer

app = typer.Typer()

@app.command()
def display_results(result_file: Path = Path('.', 'results.json')) -> None:
    model_rank_order = {'sm': 1, 'md': 2, 'lg': 3, 'trf': 4}
    model_rank_order_rev = {v: k for k, v in model_rank_order.items()}

    def re_index_model(table: pd.DataFrame) -> pd.DataFrame:
        new_index = [model_rank_order_rev[model] for model in table.index] 
        new_index = pd.Index(new_index, name="model")
        table.index = new_index
        return table

    with result_file.open("r") as results_fp:
        result_df = pd.read_json(results_fp)
        result_df['included'] = result_df['included'].apply(','.join)
        result_df['model'] = result_df['model'].map(model_rank_order)
        
        # Time results
        time_pivot_results = result_df.pivot_table(index='model', 
                                                columns=["included", "batch_size"], 
                                                values="time")
        time_pivot_results = re_index_model(time_pivot_results).round(3)
        typer.echo("Time results:\n")
        typer.echo(time_pivot_results.to_html())

        # Total memory results
        t_memory_pivot_results = result_df.pivot_table(index='model', 
                                                    columns=["included", "batch_size"], 
                                                    values="total_memory")
        t_memory_pivot_results = re_index_model(t_memory_pivot_results).round(1)
        typer.echo("Toal memory results:\n")
        typer.echo(t_memory_pivot_results.to_html())


        # Load memory results
        l_memory_pivot_results = result_df.pivot_table(index='model', 
                                                    columns="included", 
                                                    values="model_load_memory",
                                                    aggfunc=np.mean)
        l_memory_pivot_results = re_index_model(l_memory_pivot_results).round(1)
        typer.echo("\nLoad model memory results:\n")
        typer.echo(l_memory_pivot_results.to_html())


if __name__ == "__main__":
    app()