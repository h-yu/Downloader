
class MockConnection:
    def __init__(self, response_data, fail_on=-1):
        self.response_data = response_data
        self.cursor = 0
        self.readcount = 0
        self.fail_on = fail_on

    # For iterables
    def iter_content(self, chunk_size):
        iterable_response = [self.response_data[i:i+chunk_size] for i in range(0, len(self.response_data), chunk_size)]
        for i in iterable_response:
            if self.fail_on == self.readcount:
                raise Exception
            self.readcount += 1
            yield i.encode()

    # For successive calls
    def read(self, chunk_size):
        if self.fail_on == self.readcount:
            raise Exception
        self.readcount += 1
        if self.cursor >= len(self.response_data):
            return None
        else:
            read_end = min(self.cursor + chunk_size, len(self.response_data))
            res = self.response_data[self.cursor: read_end]
            self.cursor = read_end
            return res.encode()
