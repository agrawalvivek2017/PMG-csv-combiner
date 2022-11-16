import sys
import os
import pandas as pd
from pandas import read_csv


class combineCSV:
    #intialzizing the class using a constructor and passing the input paths as parameter
    def __init__(self, files_list: list):
        self.__files_path = files_list

    # function to check if the parameters are correct
    # parameter -> path arguments
    # return Type -> boolean
    def check_path(self):
        if len(self.__files_path) < 1:
            print("Error: No input. Please verify.")
            return False
        for filePath in self.__files_path:
            # checking if the directory exists
            if not os.path.exists(filePath):
                print("Error: Directory invalid. Please verify your input - " + filePath)
                return False
            # checking if file is empty
            if os.stat(filePath).st_size == 0:
                print("Error: File Empty. Please verify your input - " + filePath)
                return False
        return True

    #function to read the file in chunks
    #parameters -> file path, chunk length, list to store the results, and a boolean var to toogle filename
    #return type -> list with the results
    @staticmethod
    def get_chunks(file_path, chunk_length, chunk_list=[], append_filename= True):
        if chunk_length <= 0:
            print('Error: Chunk size should be >=1')
            return None
        file_name = os.path.basename(file_path)
        for chunk in read_csv(file_path, chunksize=chunk_length):
            if append_filename:
                chunk['filename'] = file_name
            chunk_list.append(chunk)
        return chunk_list



    # function to merge all the csv files and print them
    # parameter -> chunk size
    # chunk size = chunks to break file into while reading
    # return type -> void, prints on stdOut
    def merge_files(self, chunk_size = 10 ** 4):
        # we will read the data as chunks to deal with huge data
        chunk_list = []

        if self.check_path():
            for filePath in self.__files_path:
                self.get_chunks(filePath, chunk_size, chunk_list)
            # flag to indicate if a header should be added
            head_flag = True

            # combine all chunks
            for chunk in chunk_list:
                print(chunk.to_csv(index=False, header=head_flag, line_terminator='\n', chunksize=chunk_size), end='')
                head_flag = False

if __name__ == '__main__':
    args = sys.argv
    file_paths = []
    #reading the input file path from the input paramteres
    if len(sys.argv) > 1:
        file_paths = args[1:]
    combiner = combineCSV(file_paths)
    combiner.merge_files()

