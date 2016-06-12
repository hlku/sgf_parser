# -*- coding: UTF-8 -*-
import re
import Node

def find_r(str):
    """
    to find the right corresponding bracket
    """
    i = 0
    where = -1 # i don't know why using -1 instead 0 = =
    first = True # ignore the first left bracket
    while 0 < i or first:
        l = str.find('(')
        r = str.find(')')
        if -1 < l < r : # if find left bracket
            where += l + 1 # same, i don't know why add 1 ...
            str = str[l + 1:]
            i += 1
            first = False
        else : # if find right bracket
            where += r + 1
            str = str[r + 1:]
            i -= 1
    return where

def make_tree(con):
    """
    make the game steps tree
    """
    _con = con.strip(' ').strip('\n') # remove leading and ending space
    if _con == '' : return None # if end of a branch
    _br_l, _next = _con.find('('), _con.find(';')
    if -1 < _br_l < _next : # if have branch
        _now = Node.step(_con[:_br_l]) # now step
        while -1 < _br_l < _next : # if still have branch
            _br_r = find_r(_con)
            _now.add_node(make_tree(_con[_br_l + 2:_br_r])) # trace the branch
            _con = _con[_br_r + 1:]
            _br_l, _next = _con.find('('), _con.find(';')
        _now.add_node(make_tree(_con[_next + 1:])) # trace the trunk
        return _now
    else :
        if -1 == _next : return Node.step(_con[:]) # if it is a leaf
        else :
            _now = Node.step(_con[:_next]) # now step
            _now.add_node(make_tree(_con[_next + 1:])) # trace the trunk
            return _now

class sgf_file(object):
    """
    one sgf file, saving all it information
    """
    def __init__(self, _filename):
        self.filename = _filename
        self.info, self.head = {}, Node.node() # first save the 0th step
        
    def set_info(self, _information):
        """
        parse the information part of the sgf file
        """
        def adding (abbr, title, where = None):
            """
            small function to find specific abbr and change it to title.
            """
            _result = re.findall('[\] ]' + abbr + '\[[^\].]+\]', _information, re.DOTALL)
            if _result == []: pass
            else :
                _re = _result[0]
                if where is not None: return _re[_re.find('[') + 1:-1]
                else: self.info[title] = _re[_re.find('[') + 1:-1]
        # i prefer using chinese.....
        adding('AN', 'Annotations') # 解說者
        adding('AP', 'Application') # 產生軟體
        adding('BR', 'Black Rank') # 黑方棋力
        adding('BT', 'Black Team') # 黑方隊名
        #adding('CA', 'Encoding') # 編碼 give up, maybe future version support
        adding('CP', 'Copyright')
        adding('DT', 'Date')
        adding('EV', 'Event') # 標題
        adding('FF', 'File format') # sgf版本
        #adding('GM', 'Game') # must be 1, which means GO
        adding('GN', 'Game Name') # 賽名
        adding('HA', 'Handicap') # 手合
        adding('KM', 'Komi') # 貼目
        #adding('ON', 'Opening') # 置子 rarely use now, and can use AB AW instead
        adding('OT', 'Overtime') # 加時
        adding('PB', 'Black Name')
        adding('PC', 'Place')
        #adding('PL', 'Player') # 先方 rarely use now, and can use B W instead
        adding('PW', 'White Name')
        adding('RE', 'Result')
        adding('RO', 'Round')
        adding('RU', 'Rules') # like '應氏', '日式', '中式', '數子' etc
        adding('SO', 'Source') # 檔案來源
        adding('SZ', 'Size') # 棋盤大小
        adding('TM', 'Time limit')
        adding('US', 'User') # 記譜
        adding('WR', 'White Rank') # 白方棋力
        adding('WT', 'White Team') # 白方隊名
        
        #0th step information
        self.head.comment = adding('C', 'C', 0)
        # make a 19 x 19 buffer board (with  frame)
        for i in range(21):
            if i == 0 or i == 20: j = [3] * 21 # 3 for frame
            else :
                j = [3] # frame
                for k in range(19): j.append(0) # 0 for none, 1 for black, 2 for white
                j.append(3) # frame
            self.head.board.append(j[:]) # don't append the ref
        
        _result = re.findall('AB(?:\[[a-s]{2}\])+', _information) # find AB
        for k in _result:
            l = re.findall('\[[a-s]{2}\]', k) # find []
            try:
                for i in l: self.head.board[ord(i[2]) - 96][ord(i[1]) - 96] = 1
            except: pass # ignore, LGS sgf parser do like this
        
        _result = re.findall('AW(?:\[[a-s]{2}\])+', _information) # find AW
        for k in _result:
            l = re.findall('\[[a-s]{2}\]', k) # find []
            try:
                for i in l: self.head.board[ord(i[2]) - 96][ord(i[1]) - 96] = 2
            except: pass # ignore, LGS sgf parser do like this
        
    def parse(self, sgf):
        _sgf = sgf.strip(' ').strip('\n') # remove leading and ending space
        if _sgf[:2] != '(;' or _sgf[-1] != ')' :
            print('The file have syntax error')
            return
        _info_index = _sgf[2:].find(';') + 2
        _information = _sgf[2:_info_index] # game's information
        self.set_info(_information)
        
        _contain = _sgf[_info_index + 1:-1] # main part
        first = make_tree(_contain) # first step
        self.head.add_node(first) # first step is the child of 0th step
        first.setBoard() # initial the board
        
    def lauch(self):
        _sgf = ''
        try:
            with open(self.filename) as _file:
                # sgf file actually is a txt file
                _sgf = _sgf + _file.read()
        except IOError:
            print('Reading ' + self.filename + ' failed!')
            return
        except:
            print('Unexpected error!')
            return
        self.parse(_sgf)
        