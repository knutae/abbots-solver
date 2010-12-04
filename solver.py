#!/usr/bin/env python

import sys
sys.path.append('../abbots')
import board
from collections import deque

def copy_abbots(abbots):
    # Faster than dict/list comprehensions:
    d = dict()
    for a, v in abbots.items():
        d[a] = list(v)
    return d

def search_key(abbots):
    return frozenset((a,p[0],p[1]) for a,p in abbots.items())

class SearchNode:
    def __init__(self, abbots, moves):
        self.abbots = copy_abbots(abbots)
        self.moves = moves
        self.key = search_key(abbots)
        #self.depth = len(moves) // 2
    
    def depth(self):
        return len(self.moves) // 2

class AbbotSolver:
    def __init__(self, board, verbose):
        self.board = board
        self.abbots = board.abbots
        self.root = SearchNode(self.abbots, '')
        self.verbose = verbose
    
    def enumerate_moves(self, node):
        for abbot in node.abbots.keys():
            for direction in '<^>,':
                move = abbot + direction
                self.board.abbots = copy_abbots(node.abbots) # reset board to node pos
                try:
                    self.board.move(move)
                    yield (SearchNode(self.board.abbots, node.moves + move),
                           self.board.isSolved())
                except board.IllegalMove:
                    pass

    def solve(self, max_depth):
        assert max_depth > 0
        search_map = {self.root.key: self.root}
        search_queue = deque([self.root])
        while True:
            node = search_queue.popleft()
            if node.depth() > max_depth:
                if self.verbose:
                    print 'Bailing out at depth %s (map size %)' % (
                        node.depth(), len(search_map))
                break
            for subnode, solved in self.enumerate_moves(node):
                #print subnode.moves, subnode.depth()
                #print self.board
                if solved:
                    if self.verbose:
                        print 'Found solution with depth', subnode.depth()
                        print 'Map size:', len(search_map)
                    return subnode.moves
                if subnode.key not in search_map:
                    search_map[subnode.key] = subnode
                    search_queue.append(subnode)
                #else:
                #    assert search_map[subnode.key].depth() <= subnode.depth()
        return ''

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-p', '--print-board', dest='print_board',
                      action='store_true', default=False,
                      help='Print the board before and after solving.')
    parser.add_option('-d', '--max-depth', dest='max_depth',
                      type=int, default=20,
                      help='Maximum search depth')
    parser.add_option('-v', '--verbose', dest='verbose',
                      action='store_true', default=False,
                      help='Print some debugging info')
    opts, args = parser.parse_args()

    input = sys.stdin.read()
    b = board.Board(input)
    
    if opts.print_board:
        print b
    
    solver = AbbotSolver(b, opts.verbose)
    moves = solver.solve(opts.max_depth)
    print moves
    
    if opts.print_board:
        print b
