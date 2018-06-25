import re

def get_asn_number(line):
    match = re.search('.+\s[AS]*(\w+)', line)
    if match != None:
        return match.group(1)
    else:
        return None
    return


def parse_bgp_line(line): 
    match = re.search('\s*\w+:\s(.+)\n', line)
    if match != None:
        return match.group(1)
    else:
        print(line)
        return None
    return