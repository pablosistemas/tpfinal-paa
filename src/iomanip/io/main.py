from structures.node.main import Node
from iomanip.processing.main import *
import settings.main as global_var

import networkx as nx
import re

# nx_obj MUST BE a NetworkX object
def read_bgp_file(nx_obj, input_file):
    file = open(input_file, 'r')
    line_n = 0
    line = file.readline()
    line_n = line_n + 1
    while line != '':
        node = Node()
        status = True

        if not re.match('TIME', line):
            print(line)
            raise 'No TIME'
        
        # TIME
        node.__time = parse_bgp_line(line)
        line = file.readline()
        line_n = line_n + 1
        # TYPE
        node.__type = parse_bgp_line(line)
        line = file.readline()
        line_n = line_n + 1
        # FROM
        node.__from = parse_bgp_line(line)
        line = file.readline()
        line_n = line_n + 1
        # TO
        node.__to = parse_bgp_line(line)
        node.__asn_src = get_asn_number(node.__from)
        node.__asn_dst = get_asn_number(node.__to)

        status = node.__asn_src != None and node.__asn_dst != None

        while line != '\n' and line != '':
            line = file.readline()
            if 'ASPATH' in line:
                match = re.findall(r'(\d+)\s+', line)
                match.append(node.__asn_dst)
                for asn in match:
                    global_var.asn_unordered_set.add(int(asn))
                global_var.sets.append(map(int, match))
            line_n = line_n + 1

        if status:
            nx_obj.add_node(node.__asn_src)
            nx_obj.add_node(node.__asn_dst)
            nx_obj.add_edge(node.__asn_src, node.__asn_dst)

        line = file.readline()
        line_n = line_n + 1

    file.close()
    return
