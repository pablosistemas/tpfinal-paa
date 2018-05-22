import sys
import re

class Node:
    __time = None
    __type = None
    __from = None
    __to = None
    __origin = None
    __as_path = None
    __mp_reach_nlri = None
    __next_hop = None
    __announce = None

    def __init__(self):
        pass
    

class Graph:
    __nodes = []
    def __init__(self):
        pass

    def __parse_line__(self, line): 
        match = re.search('\s*\w+:\s(.+)\n', line)
        if match != None:
            return match.group(1)
        else:
            print(line)
            return None

    def __read__(self, input_file):
        file = open(input_file, 'r')
        line = file.readline()
        while line != '':
            _node = Node()
            _asn = None

            _node.__time = self.__parse_line__(line)
            line = file.readline()
            _node.__type = self.__parse_line__(line)
            line = file.readline()
            _node.__from = self.__parse_line__(line)
            line = file.readline()
            _node.__to = self.__parse_line__(line)

            _asn = re.search('.+\s(\w+)', _node.__to).group(1)

            line = file.readline()
            _node.__origin = self.__parse_line__(line)
            line = file.readline()
            _node.__as_path = self.__parse_line__(line)
            line = file.readline()
            while line != '\n': 
                line = file.readline()

            self.__nodes.append((_asn, _node)) 
            line = file.readline()

        file.close()


def main():
    input_file = 'data/input_bgp'
    g = Graph()
    g.__read__(input_file)
    print(g)

if __name__ == "__main__":
    main()