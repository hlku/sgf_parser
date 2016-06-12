import re

class node(object):
    """
    a node interface
    """
    def __init__(self) :
        self.nodes, self.board = list(), list()
        self.comment, self.father = '', self
        
    def add_node(self, _node):
        """
        add node as child
        """
        if _node is None : pass
        else :
            _node.father = self
            self.nodes.append(_node)
    
    def brothers(self):
        """
        count the amount of this node's brothers
        """
        if self.father is self or self.father == self : return 0 # root
        else: return len(self.father.nodes) - 1
    
    def isTrunk(self):
        if self.brothers() == 0 : return 0
        else :
            i = self.father.nodes.index(self)
            if i == len(self.father.nodes) - 1 : return 0
            else : return i + 1
    
    def next_bro(self):
        """
        get next brother
        """
        bro = self.brothers()
        if bro == 0: return self
        else :
            i = self.father.nodes.index(self)
            if i == bro: i = 0
            else: i += 1
            return self.father.nodes[i]
            
    def pre_bro(self):
        """
        get previous brother
        """
        bro = self.brothers()
        if bro == 0: return self
        else :
            i = self.father.nodes.index(self)
            if i == 0: i = bro
            else: i -= 1
            return self.father.nodes[i]

class step(node):
    """
    One node of the tree, save the step information 
    """
    def __new__(self, _str):
        # one step should have B[aa] or W[aa]
        if re.search('[BW]\[[a-s]{2}\]', _str) is None: return None
        else: return object.__new__(self)
        
    def __init__(self, _str):
        super(step, self).__init__()
        _result = re.findall('[BW]\[[a-s]{2}\]', _str)[0]
        if _result[0] == 'B' : self.color = 1
        else : self.color = 2  # B:1 W:2
        self.x, self.y = ord(_result[2]) - 96, ord(_result[3]) - 96 # 96 = ord('a') - 1
        _result = re.findall('C\[[^\].]+\]', _str, re.DOTALL) # comment include newline
        if _result != []: self.comment = _result[0][2:-1]
    
    def setBoard(self):
        """
        add this step on the board
        """
        for i in self.father.board: # deep copy
            if i is None or i == []: pass
            else: self.board.append(i[:])
        #self.board = self.father.board[:] # shallow copy, will be wrong
        self.board[self.y][self.x] = self.color
        self.fresh()
        for child in self.nodes :
            if child is None : pass
            else : child.setBoard()
        
    def fresh(self):
        """
        fresh the board to be legal
        """
        dead = set() # store which stones should die
        def qi(pos): # calculate the qi of a stone
            dead.add(pos)
            y, x, i = pos[0], pos[1], 0
            four = ((y, x + 1), (y, x - 1), (y + 1, x), (y - 1, x))
            for postition in four:
                if postition not in dead: # whether traced
                    tmp = self.board[postition[0]][postition[1]]
                    if 0 == tmp: i += 1
                    elif 3 == tmp or tmp == self.color: i = i
                    else : i += qi(postition) # tmp is other color of this step
            return i
        
        _four = ((self.y, self.x + 1),
                 (self.y, self.x - 1),
                 (self.y + 1, self.x),
                 (self.y - 1, self.x))
        for _pos in _four:
            if(_pos not in dead and  # different color
               self.board[_pos[0]][_pos[1]] not in (0, 3, self.color)):
                if 0 == qi(_pos): # dead
                    clone = dead.copy()
                    for stone in clone:
                        self.board[stone[0]][stone[1]] = 0 # clear
                        dead.remove(stone)
