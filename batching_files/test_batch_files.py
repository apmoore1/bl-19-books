import tempfile
from pathlib import Path

from batch_files import batch

def test_batch() -> None:
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        
        test_data_dir = Path(__file__, '..', 'test_data').resolve()
        extracted_files_path = Path(test_data_dir, 'extracted_files.txt')
        book_folder = Path(test_data_dir, 'book_folder')
        batch(2, book_folder, extracted_files_path, temp_dir_path)
        
        # Expect 2 folders in temp_dir which are called 0 and 1
        
        sub_folders = list(temp_dir_path.iterdir())
        sub_folder_0 = Path(temp_dir_path, '0')
        sub_folder_1 = Path(temp_dir_path, '1')
        assert 2 == len(sub_folders)
        assert sub_folder_0 in sub_folders
        assert sub_folder_1 in sub_folders

        # Expect folder 0 to contain files 011833856_01_text.json, 
        # 011834197_01_text.json
        # Expect folder 1 to contain file 011834197_02_text.json
        print(list(sub_folder_0.iterdir()))
        print(list(sub_folder_1.iterdir()))
        assert 2 == len(list(sub_folder_0.iterdir()))
        assert 1 == len(list(sub_folder_1.iterdir()))

        assert Path(sub_folder_0, '011833856_01_text.json').exists()
        assert Path(sub_folder_0, '011834197_01_text.json').exists()
        assert Path(sub_folder_1, '011834197_02_text.json').exists()
