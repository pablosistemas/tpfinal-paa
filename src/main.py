import sys
import re
import os

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

    def __read_line__(self):
        pass

    def __read__(self, input_file):
        file = open(input_file, 'r')
        line_n = 0
        line = file.readline()
        line_n = line_n + 1
        while line != '':
            _node = Node()
            _asn = None

            if not re.match('TIME', line):
                print(line)
                raise

            _node.__time = self.__parse_line__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__type = self.__parse_line__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__from = self.__parse_line__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__to = self.__parse_line__(line)

            _asn_source = re.search('.+\s(\w+)', _node.__from).group(1)
            _asn_dest = re.search('.+\s(\w+)', _node.__to).group(1)

            line = file.readline()
            line_n = line_n + 1
            _node.__origin = self.__parse_line__(line)
            line = file.readline()
            line_n = line_n + 1
            _node.__as_path = self.__parse_line__(line)
            line = file.readline()
            line_n = line_n + 1

            while line != '\n':
                line = file.readline()
                line_n = line_n + 1

            self.__nodes.append((_asn, _node)) 
            line = file.readline()
            line_n = line_n + 1

        file.close()


def main():
    input_file = '../data/input_bgp'
    g = Graph()
    g.__read__(input_file)
    print(g)

if __name__ == "__main__":
    main()