# Vote Counter
A vote-counting python script

# How to run
This script needs no external libraries to run.
It needs 5 mandatory parameters:
    - bills_csv means the path to a CSV file containing bills data;
    - legislators_csv means the path to a CSV file containing legislators data;
    - votes_csv means the path to a CSV file containing votes data;
    - vote_results_csv means the path to a CSV file containing vote results data;
    - results_folder means the path to a folder where will be written the results.

The command, inside the project folder, must be like this example:
python3 main.py <bills_csv> <legislators_csv> <votes_csv> <vote_results_csv> <results_folder>

Inside results folder there will be two new CSV files: legislators-support-oppose-count.csv and bills.csv,
each containing the vote count for both classes.
