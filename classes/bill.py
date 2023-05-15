class Bill:
    def __init__(self, id, title, sponsor_id) -> None:
        self.id = id
        self.title = title
        self.sponsor_id = sponsor_id
        self.votes = {}

    def include_vote(self, person_id, vote_id: int, result: int) -> None:
        if vote_id in self.votes.keys():
            self.votes[vote_id][person_id] = result
        else:
            self.votes[vote_id] = {person_id: result}

    def get_vote_count(self, vote_id: int) -> tuple[int, int]:
        yea = 0
        nay = 0
        for value in self.votes[vote_id].values():
            if value == 1:
                yea += 1
            else:
                nay += 1

        return yea, nay
