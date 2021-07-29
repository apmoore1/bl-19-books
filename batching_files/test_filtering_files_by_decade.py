from pathlib import Path
import tempfile
from typing import List

from filtering_files_by_decade import filter_by_decade

cwd = Path(__file__, '..').resolve()
meta_data_file = Path(cwd, 'id_date_meta_data.json')
input_folder = Path(cwd, 'test_data', 'book_folder')


def test_filter_by_decade() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        def test_decade(decade: int, expected_file_names: List[str]):
            output_file = Path(temp_dir, 'output.txt')
            filter_by_decade(decade, meta_data_file, input_folder, output_file)
            file_names: List[str] = []
            with output_file.open('r') as output_fp:
                for line in output_fp:
                    line = line.strip()
                    if line:
                        file_names.append(line) 
            assert len(expected_file_names) == len(file_names)
            for file_name in expected_file_names:
                assert file_name in file_names
        
        test_decade(1880, ["0118/011833856_01_text.json", "0118/011834197_01_text.json", 
                           "0118/011834197_02_text.json"])
        test_decade(1840, ["0000/000057124_01_text.json"])

        