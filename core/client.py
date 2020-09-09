from github import Github


class Client(Github):

    current_rate_limiting = [0, 0]

    def rate_limiting_initialization(self):
        self.current_rate_limiting = [self.rate_limiting[0], self.rate_limiting[1]]

    def count_rate_limit(self, requests_count: int):
        if self.current_rate_limiting[0] >= requests_count:
            self.current_rate_limiting[0] -= requests_count
        else:
            self.current_rate_limiting[0] = 0
