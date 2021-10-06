class Interval:
    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end
        self.count = 0
        # p as probability
        self.p = 0

    def increase(self):
        self.count += 1

    def set_probability(self, m: float):
        self.p = self.count / m

    def in_interval(self, x: float):
        return self.start <= x < self.end

    def middle(self) -> float:
        return (self.end + self.start) / 2
