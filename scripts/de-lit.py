#!/usr/bin/env python -w

import itertools, re

def print_docs(docs_, outfp):
    '''print out docs, skipping the hashes for leading/trailing blanks'''
    blank = re.compile('^\s*$')
    def blanks(lst):
        return itertools.takewhile(lambda x: blank.match(x), lst)
    def drop_blanks(lst):
        return itertools.dropwhile(lambda x: blank.match(x), lst)
    def revl(lst):
        return reversed(list(lst))
    docs = list(docs_)
    leading = sum(1 for _ in blanks(docs))
    trailing = sum(1 for _ in blanks(reversed(docs)))
    remaining = revl(drop_blanks(revl(drop_blanks(docs))))

    for x in range(leading): outfp.write('\n')
    for x in remaining: outfp.write('# %s' % x)
    for x in range(trailing): outfp.write('\n')
    
def convert_litcoffee_to_coffee(infp, outfp):
    '''convert literate coffeescript to the regular kind'''
    docs, in_doc = [], True
    coffee = re.compile('^\s{4}(.+)$')
    for line in infp:
        m = coffee.match(line)
        if m:
            if in_doc:
                print_docs(docs, outfp)
                docs = []
            outfp.write('%s\n' % m.group(1))
            in_doc = False
        else:
            docs.append(line)
            in_doc = True
    print_docs(docs, outfp)

if '__main__' == __name__:
    import sys
    convert_litcoffee_to_coffee(sys.stdin, sys.stdout)
