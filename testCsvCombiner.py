import pandas as pd
import sys
import generatefixtures
import unittest
import os
from csvCombiner import combineCSV
from io import StringIO
import os.path as path


class TestMethods(unittest.TestCase):
    # declaring all paths
    testOutput = "./test_output.csv"
    combinerPath = "./csvCombiner.py"
    accessoriesPath = "./fixtures/accessories.csv"
    clothingPath = "./fixtures/clothing.csv"
    householdPath = "./fixtures/household_cleaners.csv"
    emptyPath = "./fixtures/empty_file.csv"

    # declaring the test output
    backup = sys.stdout
    test_output = open(testOutput, 'w+')


    @classmethod
    # creating the empty file for testing
    def setUpClass(cls):
        DIR = path.abspath(path.dirname(__file__))
        with open(path.join(DIR, 'fixtures', 'empty_file.csv'), 'w', encoding='utf-8') as fh:
            pass

        # redirect the output to ./test_output.csv
        sys.stdout = cls.test_output

    @classmethod
    def tearDownClass(cls):

        cls.test_output.close()

        if os.path.exists(cls.emptyPath):
            os.remove(cls.emptyPath)
        if os.path.exists(cls.testOutput):
            os.remove(cls.testOutput)

    def setUp(self):
        # setup
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.testOutput, 'w+')

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.testOutput, 'w+')
        sys.stdout = self.backup
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    # 1st Unit Test - Checking a command with no arguments
    def testNoFiles(self):
        # given
        combiner = combineCSV([])
        # when
        output = combiner.check_path()
        # then
        self.assertFalse(output)
        self.assertEqual("Error: No input. Please verify.", self.output.getvalue().strip())

    # 2nd Unit Test - Checking if given input file is empty
    def testEmptyFile(self):
        # given
        combiner = combineCSV([self.clothingPath, self.emptyPath])
        # when
        output = combiner.check_path()
        # then
        self.assertFalse(output)
        self.assertEqual("Error: File Empty. Please verify your input - " + self.emptyPath,
                         self.output.getvalue().strip())

    # 3rd Unit Test - Checking if the given file path doesnt exist
    def testWrongPathHandling(self):

        combiner = combineCSV(["fake.csv"])

        output = combiner.check_path()

        self.assertFalse(output)
        self.assertEqual("Error: Directory invalid. Please verify your input - fake.csv",
                         self.output.getvalue().strip())

    # 4th Unit Test - Checking if the given file path exists
    def testCorrectFilePaths(self):

        combiner = combineCSV([self.clothingPath, self.accessoriesPath, self.householdPath])

        output = combiner.check_path()

        self.assertTrue(output)

    # 5th Unit Test - get chunks - checks if the reading in the form of chunks are fine and the colomn filename is getting added
    def testGetChunksCorrectly(self):
        # given
        chunk_len = 5
        chunk_list = []
        append_file_name = True
        df, chunk_list_len = self.createDataframeWithFileName(self.clothingPath, 'clothing.csv', chunk_len)

        # when
        combineCSV.get_chunks(self.clothingPath, chunk_len, chunk_list, append_file_name)
        # then
        self.assertEqual(len(chunk_list), chunk_list_len)
        self.assertIn('filename', df.columns.values)

    # 6th Unit Test - get chunks but without the header
    def testGetChunksCorrectlyWithoutHeader(self):
        # given
        chunk_len = 5
        chunk_list = []
        append_file_name = False
        df, chunk_list_len = self.createDataframeWithFileName(self.clothingPath, '', chunk_len)

        # when
        combineCSV.get_chunks(self.clothingPath, chunk_len, chunk_list, append_file_name)
        # then
        self.assertEqual(len(chunk_list), chunk_list_len)
        self.assertNotIn('filename', df.columns.values)

    # 7th Unit Test - get chunks function when the chunk length is zero
    def testGetChunksWithZeroChunkLen(self):
        # given
        chunk_len = 0
        chunk_list = []
        append_file_name = True
        # when
        combineCSV.get_chunks(self.clothingPath, chunk_len, chunk_list, append_file_name)
        # then
        self.assertEqual("Error: Chunk size should be >=1", self.output.getvalue().strip())

    # 8th Unit test - checking if the merge function is happening properly
    def testMergeFiles(self):
        # given
        combiner = combineCSV([self.clothingPath, self.accessoriesPath])
        chunk_len = 5
        df1, _ = self.createDataframeWithFileName(self.clothingPath, 'clothing.csv', chunk_len)
        df2, _ = self.createDataframeWithFileName(self.accessoriesPath, 'accessories.csv', chunk_len)

        # when
        combiner.merge_files(chunk_len)
        # then
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        with open(self.testOutput) as f:
            df = pd.read_csv(f)
        self.assertIn('filename', df.columns.values)
        self.assertEqual(len(df.values), len(df1.values)+ len(df2.values))

    @staticmethod
    def createDataframeWithFileName(file_path, file_name, chunk_len):
        with open(file_path) as f:
            df = pd.read_csv(f)
        if file_name != '':
            df['filename'] = file_name
        if len(df.values) % chunk_len == 0:
            chunk_list_len = len(df.values) / chunk_len
        else:
            chunk_list_len = int(len(df.values) / chunk_len) + 1
        return df, chunk_list_len
