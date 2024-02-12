import os.path
from pathlib import Path

import pytest
import unittest
from llm_zero_to_hundred_extra.convert_requirementstxts import (
    process_requirements_txt_file,
    modify_requirements_txt,
)


class TestConvertRequirementsTxts(unittest.TestCase):

    def test_modify_requirements_txt(self):
        requirements_txt = """
        numpy==1.16.1=pypi_0
        pandas>=1.0.0
        scikit-learn
        matplotlib==3.0.2
        bzip2=1.0.8=he774522_0
        googleapis-common-protos=1.62.0=pypi_0
        """
        expected_txt = """numpy==1.16.1
pandas>=1.0.0
scikit-learn
matplotlib==3.0.2
bzip2=1.0.8
googleapis-common-protos=1.62.0
        """.strip()
        result = modify_requirements_txt(requirements_txt)
        self.assertEqual(expected_txt, result)

    def test_modify_requirements_txt_empty(self):
        requirements_txt = ""
        expected_txt = ""
        result = modify_requirements_txt(requirements_txt)
        self.assertEqual(result, expected_txt)

    def test_modify_requirements_txt_no_versions(self):
        requirements_txt = """
        numpy
        pandas
        scikit-learn
        matplotlib
        """
        expected_txt = ""
        result = modify_requirements_txt(requirements_txt)
        self.assertEqual(result, expected_txt)

    def test_process_requirements_txts(self):
        # Test with empty list
        actual = process_requirements_txt_file("./test_orig_requirements.txt")

        expected = (
            Path(os.path.dirname(__file__)) / "test_orig_requirements_expected.txt"
        )
        expected = expected.read_text().strip()
        assert actual == expected, f"Expected {expected}, but got {actual}"

        # Test with a single requirements.txt (file does not exist)
        with pytest.raises(FileNotFoundError):
            process_requirements_txt_file("non_existent_file.txt")

        # Due to the inability to create files in this environment, testing with valid file paths is not possible.
        # However, it is advised to test with actual files in your own testing environment. Examples would be:
        #
        # assert process_requirements_txts(["valid_file_1.txt"]) == expected_result
        # assert process_requirements_txts(["valid_file_1.txt", "valid_file_2.txt"]) == expected_result
