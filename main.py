import os
import sgf_file
import sgf_parser

def newfile():
    """
    make a empty new sgf file, then open it with the parser
    """
    pass

def main():
    """
    main part, open file or make new file
    """
    while True:
        filename = raw_input('>>')
        if filename == '' : break
        elif filename == 'help':
            print("type 'new' to create new file, or type file's name to open.")
        elif filename == 'new': newfile()
        else:
            if os.path.exists(filename):
                # in the future version, using thread to open different file
                theFile = sgf_file.sgf_file(filename)
                theFile.lauch()
                # in the future version, the parser using GUI
                Parser = sgf_parser.sgf_parser(theFile)
                Parser.show()
            else : print(filename + ' is not exist!')

if __name__ == '__main__':
    main()
