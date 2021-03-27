from tweetcollector.db import Database

class StateService:
    def __init__(self):
        self.db = Database()

    def get_states(self):
        return self.db.get_all_states()

    def get_state_info(self, state):
        return self.db.get_state_info(state)