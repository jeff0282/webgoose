
import os

def pytest_configure(config):

    """
    Initialise Testing-Environment 

    1. Point To Test Data Directory
    """

    TEST_DATA_DIR = "./test/test_files"
    os.chdir(TEST_DATA_DIR)