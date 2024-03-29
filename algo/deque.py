# coding=utf-8


class Deque(object):

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self,item):
        self.items.append(item)

    def addRear(self,item):
        self.items.insert(0, item)

    def removeFront(self):
        return self.items.pop()

    def removeRear(self):
        return self.items.pop(0)

    def size(self):
        return len(self.items)


q = Deque()
q.addFront("3")
q.addFront("4")
q.addRear("5")
q.addRear("6")
print(q.size())
print(q.items)