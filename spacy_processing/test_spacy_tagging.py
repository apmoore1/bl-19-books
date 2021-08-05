import tempfile
from pathlib import Path
import filecmp

import pytest

from spacy_tagging import process_text, ComponentNames

def compare_files(file_1: Path, file_2: Path) -> None:
    '''
    If this fails so will `filecmp.cmpfiles`. The only difference is that this 
    provides more detailed analysis of what is the difference between the files.
    '''
    with file_1.open('r') as fp_1:
        with file_2.open('r') as fp_2:
            lines_1 = fp_1.readlines()
            lines_2 = fp_2.readlines()
            for index, line_1 in enumerate(lines_1):
                assert line_1 == lines_2[index] 

@pytest.mark.parametrize("include_lemma", [False, True])
def test_process_text(include_lemma: bool) -> None:
    test_data_dir = Path(__file__, '..', 'test_data').resolve()
    book_folder = Path(test_data_dir, 'book_folder')
    expected_output_folder = Path(test_data_dir, 'expected_output_1')
    if include_lemma:
        expected_output_folder = Path(test_data_dir, 'expected_output')

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)
        
        if include_lemma:
            process_text(book_folder, tempdir_path, list(ComponentNames))
        else:
            process_text(book_folder, tempdir_path, [ComponentNames.POS, ComponentNames.NER])
        test_files = list(tempdir_path.iterdir())
        assert 2 == len(test_files)

        
        expected_files = list(expected_output_folder.iterdir())
        common_file_names = [file_name.name 
                             for file_name in expected_files]
        for common_file_name in common_file_names:
            expected_file = Path(expected_output_folder, common_file_name)
            test_file = Path(tempdir_path, common_file_name)
            compare_files(expected_file, test_file)
        
        
        file_difference_results = filecmp.cmpfiles(str(expected_output_folder), 
                                                   str(tempdir_path), 
                                                   common_file_names, shallow=False)
        matches, mis_matches, errors = file_difference_results
        assert 2 == len(matches)
        assert not mis_matches
        assert not errors

