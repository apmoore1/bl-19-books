from pathlib import Path
import tempfile
from typing import List

from filtering_files import filter_files

cwd = Path(__file__, '..').resolve()
meta_data_file = Path(cwd, 'test_data', 'meta_data.json')
input_folder = Path(cwd, 'test_data', 'book_folder')


def test_filter_files() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        def test_filters(expected_file_names: List[str], **kwargs):
            output_file = Path(temp_dir, 'output.txt')
            filter_files(meta_data_file, input_folder, output_file, **kwargs)
            file_names: List[str] = []
            with output_file.open('r') as output_fp:
                for line in output_fp:
                    line = line.strip()
                    if line:
                        file_names.append(line) 
            assert len(expected_file_names) == len(file_names)
            for file_name in expected_file_names:
                assert file_name in file_names
        
        test_filters(["0118/011833856_01_text.json", "0118/011834197_01_text.json", 
                      "0118/011834197_02_text.json"], decade=1880)
        test_filters(["0000/000057124_01_text.json"], decade=1840)

        test_filters([], decade=1840, language="English")
        test_filters([], decade=1830)
        test_filters(["0000/000057123_01_text.json"], language="German")
        test_filters(["0118/011834197_01_text.json", "0118/011834197_02_text.json"], 
                     decade=1880, language="French")

        test_filters(["0118/011833856_01_text.json", "0118/011834197_01_text.json", 
                      "0118/011834197_02_text.json",
                      "0000/000057124_01_text.json", "0000/000057123_01_text.json"])

        