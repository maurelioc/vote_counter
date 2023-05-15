import argparse
import csv
import logging
import os

from classes.counter import Counter

logger = logging.Logger(__name__)
logger.addHandler(logging.StreamHandler())


def read_csvs(args):
    bills = []
    with open(args.bills_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            bills.append(row)

    people = []
    with open(args.legislators_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            people.append(row)

    votes = []
    with open(args.votes_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            votes.append(row)

    vote_results = []
    with open(args.vote_results_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vote_results.append(row)

    return bills, people, votes, vote_results


def write_csvs(folder, counter):
    if not os.path.exists(folder):
        os.makedirs(folder)

    legislator_results_path = os.path.join(
        folder, 'legislators-support-oppose-count.csv'
    )
    bill_results_path = os.path.join(folder, 'bills.csv')

    with open(legislator_results_path, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=['id', 'name', 'num_supported_bills', 'num_opposed_bills'],
        )
        writer.writeheader()
        for legislator_id in counter.legislator_vote_count.keys():
            writer.writerow(
                {
                    'id': legislator_id,
                    'name': counter.people[legislator_id].name,
                    'num_supported_bills': counter.legislator_vote_count[legislator_id][
                        0
                    ],
                    'num_opposed_bills': counter.legislator_vote_count[legislator_id][
                        1
                    ],
                }
            )

    with open(bill_results_path, 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                'id',
                'title',
                'supporter_count',
                'opposer_count',
                'primary_sponsor',
            ],
        )
        writer.writeheader()
        for bill_id in counter.bill_vote_count.keys():
            try:
                sponsor_name = counter.people[counter.bills[bill_id].sponsor_id].name
            except KeyError:
                sponsor_name = 'Unknown'
            if len(counter.bill_vote_count[bill_id].keys()) == 1:
                vote_id = list(counter.bill_vote_count[bill_id].keys())[0]
                writer.writerow(
                    {
                        'id': bill_id,
                        'title': counter.bills[bill_id].title,
                        'supporter_count': counter.bill_vote_count[bill_id][vote_id][0],
                        'opposer_count': counter.bill_vote_count[bill_id][vote_id][1],
                        'primary_sponsor': sponsor_name,
                    }
                )
            else:
                for vote_id in counter.bill_vote_count[bill_id].keys():
                    writer.writerow(
                        {
                            'id': bill_id,
                            'title': counter.bills[bill_id].title,
                            'supporter_count': counter.bill_vote_count[bill_id][
                                vote_id
                            ][0],
                            'opposer_count': counter.bill_vote_count[bill_id][vote_id][
                                1
                            ],
                            'primary_sponsor': sponsor_name,
                            'vote_id': vote_id,
                        }
                    )


def main():
    parser = argparse.ArgumentParser(description='Script to count votes from csv files')
    parser.add_argument('bills_csv', help='csv file containing bill data')
    parser.add_argument('legislators_csv', help='csv file containing legislators data')
    parser.add_argument('votes_csv', help='csv file containing vote data')
    parser.add_argument('vote_results_csv', help='csv file containing vote results')
    parser.add_argument(
        'results_folder',
        help='path to folder where will be written result csvs',
    )

    logger.info('Starting script')
    logger.info('Parsing arguments')
    args = parser.parse_args()

    logger.info('Loading csv files')
    bills, people, votes, vote_results = read_csvs(args)

    logger.info('Counting votes')
    counter = Counter(bills, people, votes, vote_results)
    counter.count_bill_votes()
    counter.count_legislator_votes()

    logger.info('Writing results to csv file')
    write_csvs(args.results_folder, counter)

    logger.info('Script finished')


if __name__ == '__main__':
    main()
