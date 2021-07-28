import json
from pathlib import Path
from typing import List
import tempfile

import pytest

from language_id import text_generator, process_file

TEST_DATA_DIR = Path(__file__, '..', 'test_data').resolve()
TEST_FILE_1 = Path(TEST_DATA_DIR, "test1.json")
TEST_FILE_2 = Path(TEST_DATA_DIR, "test2.json")
TEST_FILES = [TEST_FILE_1, TEST_FILE_2]

FASTTEXT_MODEL_PATH = Path(__file__, '..', 'large_model.bin').resolve()

def test_text_generator() -> None:
    test_file_1_page_numbers = [5,7,8]
    test_file_1_page5_text = "ASHE PYEE."
    page_numbers: List[int] = []
    for page_number, text in text_generator(TEST_FILE_1):
        if page_number == 5:
            assert test_file_1_page5_text == text
        page_numbers.append(page_number)
    assert test_file_1_page_numbers == page_numbers




@pytest.mark.parametrize("excl_filename", [True, False])
@pytest.mark.parametrize("high_threshold", [True, False])
def test_process_file(excl_filename: bool, high_threshold: bool) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = Path(temp_dir, "output.json")

        print(FASTTEXT_MODEL_PATH.resolve())

        if high_threshold:
            process_file(FASTTEXT_MODEL_PATH, TEST_FILE_1, output_file, excl_filename, 0.7)
            process_file(FASTTEXT_MODEL_PATH, TEST_FILE_2, output_file, excl_filename, 0.7)
        else:
            process_file(FASTTEXT_MODEL_PATH, TEST_FILE_1, output_file, excl_filename)
            process_file(FASTTEXT_MODEL_PATH, TEST_FILE_2, output_file, excl_filename)
        
        file_1_output = {'language': 'Spanish', 
                         'filename': 'test1',
                         'language_extras': {'Spanish': {'BCP 47 code': 'es', 'count': 2, 'proportion': 0.67}, 
                                             'English': {'BCP 47 code': 'en', 'count': 1, 'proportion': 0.33}}}
        if high_threshold:
            file_1_output = {'language': 'English', 
                             'filename': 'test1',
                             'language_extras': {'English': {'BCP 47 code': 'en', 'count': 1, 'proportion': 1.0}}}
        file_2_output = {'language': 'English', 
                         'filename': 'test2',
                         'language_extras': {'English': {'BCP 47 code': 'en', 'count': 3, 'proportion': 1.0}}}
        if excl_filename:
            del file_1_output['filename']
            del file_2_output['filename']
        file_outputs = [file_1_output, file_2_output]

        with output_file.open('r') as fp:
            lines = []
            for index, line in enumerate(fp):
                output = json.loads(line)
                expected_output = file_outputs[index]
                assert len(expected_output) == len(output)
                assert expected_output['language'] == output['language']
                if not excl_filename:
                    assert expected_output['filename'] == output['filename']
                assert len(expected_output['language_extras']) == len(output['language_extras'])
                for extra_language in output['language_extras']:
                    assert len(expected_output['language_extras'][extra_language]) == len(output['language_extras'][extra_language])
                    for key, value in output['language_extras'][extra_language].items():
                        if key == 'proportion':
                            value = round(value, 2)
                        assert value == expected_output['language_extras'][extra_language][key]
                
                lines.append(output)
            assert 2 == len(lines)
