class Person:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.votes = {}

    def include_vote(self, bill_id: int, vote_id: int, result: int) -> None:
        if bill_id in self.votes.keys():
            self.votes[bill_id][vote_id] = result
        else:
            self.votes[bill_id] = {vote_id: result}

    def get_vote_count(self) -> tuple[int, int]:
        yea = 0
        nay = 0
        for vote in self.votes.values():
            for value in vote.values():
                if value == 1:
                    yea += 1
                else:
                    nay += 1

        return yea, nay
