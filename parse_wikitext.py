#!/bin/env/python
import argparse
from itertools import groupby
import json
import re


def parse(filename):
    with open(filename) as f:
        wiki = f.read().split("\n")

    headers = [(no, line) for no, line in enumerate(wiki) if "==" in line]

    if headers:
        brackets = [wiki[headers[x][0] + 1:headers[x + 1][0]] for x in range(len(headers) - 1)]
        brackets.append(wiki[headers[-1][0] + 1:])
    else:
        headers = [('All', 0)]
        brackets = wiki

    brackets_data = {}

    for h, b in zip(headers, brackets):
        b = [line for line in b if '|' in line or '{' in line or '}' in line]
        line_no, name = h
        brackets_data[name] = {}
        line = ''.join(b)
        keys = []
        for item in line.split('|'):
            if '=' in item:
                k, v = item.split('=', 1)
                keys.append([k.strip(), v.strip()])

        def prefix(k):
            m = re.match('[rl]\d+m\d+', k)
            if m:
                return m.group(0)

        last_pre = None
        for pre, g in groupby(keys, key=lambda k: prefix(k[0])):
            if pre:
                brackets_data[name][pre] = {k[len(pre):]: v.strip('{}') for k, v in g}
                last_pre = pre
            else:
                if last_pre:
                    brackets_data[name][last_pre]['details'] = {k: v.strip('{}') for k, v in g}

    # print(json.dumps(brackets_data, indent=4, sort_keys=True))
    return brackets_data


def __main__():
    parser = argparse.ArgumentParser(description="Parse Liquipedia wikitext into a json dict")

    parser.add_argument("infile", type=str)
    parser.add_argument("outfile", nargs='?', type=str, default=None)

    args = parser.parse_args()

    print("Parsing", args.infile)
    bracket_data = parse(args.infile)

    if not args.outfile:
        print(json.dumps(bracket_data, indent=4, sort_keys=True))
    else:
        with open(args.outfile, 'w') as f:
            json.dump(bracket_data, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    __main__()
