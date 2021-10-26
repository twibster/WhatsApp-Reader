class Conversation():
    def __init__(self,title=None,type="private",session=None,msgs=None,id=0):
        self.next = None
        self.title=title
        self.type=type
        self.session=session
        self.msgs=msgs
        self.id=id
        
    def __repr__(self):
        return f'Conversation({self.id},{self.title},{self.type},{self.session},{self.msgs})'
    def __str__(self):
        return f'Conversation({self.title})'
        
class Message():
    def __init__(self,msg=None,date=None,type=None,sender=None,show_time=None,break_space=None,conversation=None,id=0):
        self.msg = msg
        self.next = None
        self.date=date
        self.sender=sender
        self.type=type
        self.show_time=show_time
        self.break_space=break_space
        self.conversation=conversation
        self.id=id
        
    def __repr__(self):
        return f'Message({self.id},{self.type},{self.date},{self.sender},{self.msg},{self.show_time},{self.break_space},{self.conversation})'
    def __repr__(self):
        return f'Message({self.id},{self.type},{self.date},{self.sender},{self.msg},{self.show_time},{self.break_space},{self.conversation})'

class Chatters():
    def __init__(self,name=None,pov=None,color=None,conversation=None,id=0):
        self.next = None
        self.name=name
        self.pov=pov
        self.color=color
        self.conversation=conversation
        self.id=id
        
    def __repr__(self):
        return f'Chatter({self.id},{self.name},{self.pov},{self.color},{self.conversation})'
    def __repr__(self):
        return f'Chatter({self.name},{self.pov},{self.color},{self.conversation})'
        
class LinkedList(object):

    def __init__(self,title=None):
       self.head = None
       self.title =title
       self.last_id=0

    def get(self, index):
        current = self.head
        count =0
        while current:
            if count == index:
                return current
            prev=current
            current = current.next
            count += 1
        
        return None
        
    def content(self):
        content = []
        current = self.head
        while current:
            content.append(current)
            current =current.next
        return content
    
    def length(self):
        current= self.head
        length = 0
        while current:
            length += 1
            current = current.next
        return length
        
    def add(self,Node):
        self.last_id += 1
        current = self.head
        Node.id=self.last_id
        if current is None:
            self.head = Node
        else:
            while current.next:
                current = current.next
            current.next = Node

    def filter_by(self,attr,val,condition):
        result = []
        if condition == '=':
            for chatter in self:
                if getattr(chatter, attr) == val:
                    result.append(chatter)
        else:
            for chatter in self:
                if getattr(chatter, attr) != val:
                    result.append(chatter)
        return result

    def clear(self):
        if self.head:
            self.head.next=None
            self.head=None
            self.last_id=0
            
    def __repr__(self):
        return f'LinkedList({self.content()})'
    def __repr__(self):
        return f'LinkedList({self.content()})'
        
    def __iter__(self):
        self.current=self.head
        return self
        
    def __next__(self):
        if self.current:
            now=self.current
            self.current=self.current.next
            return now
        else:
            raise StopIteration

conversations=LinkedList('Conversations')
people=LinkedList('Chatters')
msgs=LinkedList('Msgs')