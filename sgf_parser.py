# -*- coding: UTF-8 -*-
import visual
import board

class sgf_parser(object):
    """
    The sgf parser, can show the sgf, in the future version, using GUI
    """
    def __init__(self, sgf_file):
        self.sgf = sgf_file
        self.buffer = board.Board(pos = (-9, -9, 0)) # drawing buffer
        self.now = self.sgf.head # from 0th step
        self.count = 0  # 0th step
            
    def board(self):
        """
        To show the board.
        """
        self.buffer.setMap(self.now.board[::-1])
        t = self.now.isTrunk()
        if t == 0 : print('========= No.' + str(self.count) + ' step =========')
        else : print('========= No.' + str(self.count) + ' step(branch ' + str(t) + ') =========')
        print(self.now.comment)
        print('--------- ' + str(self.now.brothers()) + ' branches ---------')
        
    def show(self):
        """
        main part of the parser.
        """
        print('=========' + self.sgf.filename + '=========')
        for k in self.sgf.info.keys(): print(k + ':' + self.sgf.info[k])
        print('')
        self.board() # print 0th step
        while True:
            visual.rate(50)
            if visual.scene.kb.keys: instr = visual.scene.kb.getkey()
            else: instr = ''
            if instr is None or instr == '': continue
            elif instr == 'q': break
            elif instr == 'h':
                print('q\treturn to main mode')
                print('i\tview the file information')
                print('b\tnext step')
                print('n\tnext 10 steps')
                print('m\tlast step')
                print('v\tprevious step')
                print('c\tprevious 10 steps')
                print('x\tfirst step')
                print('g\tview next branch step')
                print('f\tview previou branch step')
                print('')
            elif instr == 'i':
                for k in self.sgf.info.keys(): print(k + ':' + self.sgf.info[k])
                print('')
            elif instr == 'b':
                if self.now.nodes != []: 
                    self.count += 1
                    self.now = self.now.nodes[-1] # last one is the trunk
                self.board()
            elif instr == 'n':
                for i in range(10):
                    if self.now.nodes == []: break
                    else :
                        self.count += 1
                        self.now = self.now.nodes[-1]
                self.board()
            elif instr == 'm':
                while self.now.nodes != []:
                    self.count += 1
                    self.now = self.now.nodes[-1]
                self.board()
            elif instr == 'v':
                if self.count != 0:
                    self.count -= 1
                    self.now = self.now.father
                self.board()
            elif instr == 'c':
                for i in range(10):
                    if self.count == 0: break
                    else :
                        self.count -= 1
                        self.now = self.now.father
                self.board()
            elif instr == 'x':
                self.now = self.sgf.head
                self.count = 0
                self.board()
            elif instr == 'g':
                self.now = self.now.next_bro()
                self.board()
            elif instr == 'f':
                self.now = self.now.pre_bro()
                self.board()
            else: print('Instruction "' + instr + '" not found! Please type help or h.')
