class Plover(object):
    week = 0 #week the plover hatched
    habituation = 0.0 #some sort of quantifier for the plover's tolerance for humans, probably ~N(,)
    flush = 0.0 #some sort of quantifier for the flush distance of the plover
    #firstThreshold = false
    #secondThreshold = false
    #some sort of thing to say which nest it belongs to. otherwise we could just put a reference to the object in the nest instead

    def __init__(self, week, habituation, flush):
        self.week = week
        self.habituation = habituation
        self.flush = flush

    def printMembers(self):
        print(self.week)
