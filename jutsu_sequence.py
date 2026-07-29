from config import JUTSU_SEQUENCES

class JNode:
    def __init__(self):
        self.children = {}
        self.jutsu = ''

class JTrie:
    def __init__(self):
        self.head = JNode()
        self.current = self.head

        for jutsu, sequence in JUTSU_SEQUENCES.items():
            current = self.head

            count = 0
            for sign in sequence:
                if sign in current.children:
                    current = current.children[sign]
                else:
                    current.children[sign] = JNode()
                    current = current.children[sign]

                    if count == len(sequence)-1:
                        current.jutsu = jutsu

                count+=1


    def next_sign(self, sign):
        if sign == 'stop':
            if self.current.jutsu != '':
                print(f"Using {self.current.jutsu}")
            self.current = self.head
        elif sign in self.current.children:
            self.current = self.current.children[sign]
        else:
            print("invalid jutsu")