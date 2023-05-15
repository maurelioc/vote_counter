from .bill import Bill
from .person import Person


class Counter:
    def __init__(self, bills, people, votes, vote_results) -> None:
        self.bills = {}
        self.people = {}
        self.vote_bill = {}
        self.bill_vote_count = {}
        self.legislator_vote_count = {}

        for row in people:
            self.people[int(row['id'])] = Person(int(row['id']), row['name'])

        for row in bills:
            self.bills[int(row['id'])] = Bill(
                int(row['id']), row['title'], int(row['sponsor_id'])
            )

        for row in votes:
            self.vote_bill[int(row['id'])] = int(row['bill_id'])

        for row in vote_results:
            person = self.people[int(row['legislator_id'])]
            bill_id = self.vote_bill[int(row['vote_id'])]
            bill = self.bills[bill_id]

            person.include_vote(bill_id, int(row['vote_id']), int(row['vote_type']))
            bill.include_vote(person.id, int(row['vote_id']), int(row['vote_type']))

    def count_bill_votes(self):
        for bill in self.bills.values():
            for vote_id in bill.votes.keys():
                if bill.id in self.bill_vote_count.keys():
                    self.bill_vote_count[bill.id][vote_id] = bill.get_vote_count(
                        vote_id
                    )
                else:
                    self.bill_vote_count[bill.id] = {
                        vote_id: bill.get_vote_count(vote_id)
                    }

        return self.bill_vote_count

    def count_legislator_votes(self):
        for legislator in self.people.values():
            self.legislator_vote_count[legislator.id] = legislator.get_vote_count()

        return self.legislator_vote_count
