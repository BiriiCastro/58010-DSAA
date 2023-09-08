# Node class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def printlist(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next

if __name__ == '__main__':
    llist = LinkedList()

    llist.head = Node("X")
    second = Node("Y")
    third = Node("Z")


    llist.head.next = second;

    second.next = third;
    #To make this a Dopbly
    third.next = llist.head;



print(llist.printlist())
