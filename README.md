# PMG-csv-combiner
# PMG Graduate Leadership Program Coding Assessment


A solution to PMG's csv-combiner challenge. a command line program that takes several CSV files as arguments. Each CSV file (found in the fixtures directory of this repo) will have the same columns. The script outputs a new CSV file to stdout that contains the rows from each of the inputs along with an additional column that has the filename from which the row came (only the file's basename, not the entire path). The script uses 'filename' as the header for the additional column.

## Language and Third-party Library

- Python 3.9.1
- pandas

## csvCombiner.py Usage

Through command line:
```
$ python ./csvCombiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv
```

## testCsvCombiner.py Usage

Through command line: 
```
$ python -m unittest -v testCsvCombiner.py
```

## Added Unit Testcases
- 1st Unit Test - Checking a command with no arguments
- 2nd Unit Test - Checking if given input file is empty
- 3rd Unit Test - Checking if the given file path doesnt exist
- 4th Unit Test - Checking if the given file path exists
- 5th Unit Test - get chunks - checks if the reading in the form of chunks are fine and the colomn filename is getting added
- 6th Unit Test - get chunks but without the header
- 7th Unit Test - get chunks function when the chunk length is zero
- 8th Unit test - checking if the merge function is happening properly


## Example Output of csvCombiner.py

Given two input files named `clothing.csv` and `accessories.csv`.

|email_hash|category|
|----------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|

|email_hash|category|
|----------|--------|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|

The script would output

|email_hash|category|filename|
|----------|--------|--------|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Shirts|clothing.csv|
|21d56b6a011f91f4163fcb13d416aa4e1a2c7d82115b3fd3d831241fd63|Pants|clothing.csv|
|166ca9b3a59edaf774d107533fba2c70ed309516376ce2693e92c777dd971c4b|Cardigans|clothing.csv|
|176146e4ae48e70df2e628b45dccfd53405c73f951c003fb8c9c09b3207e7aab|Wallets|accessories.csv|
|63d42170fa2d706101ab713de2313ad3f9a05aa0b1c875a56545cfd69f7101fe|Purses|accessories.csv|
