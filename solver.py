#!/usr/bin/env python

import sys
sys.path.append('../abbots')
import board
from collections import deque

def abbots_to_key(abbots):
    return frozenset((a,p[0],p[1]) for a,p in abbots.items())

def key_to_abbots(key):
    d = dict()
    for a, p1, p2 in key:
        d[a] = [p1, p2]
    return d

class SearchNode:
    def __init__(self, abbots, moves):
        self.moves = moves
        self.key = abbots_to_key(abbots)
        #self.depth = len(moves) // 2
    
    def depth(self):
        return len(self.moves) // 2
    
    def abbots(self):
        return key_to_abbots(self.key)

class AbbotSolver:
    def __init__(self, board, verbose, debug_out):
        self.board = board
        self.abbots = board.abbots
        self.root = SearchNode(self.abbots, '')
        self.verbose = verbose
        self.debug_out = debug_out
        self.search_map = {self.root.key: self.root}
        self.moves = [a+d for a in self.abbots.keys() for d in '<^>,']
        
        assert len(board.targets) == 1
        target, pos = board.targets.items()[0]
        self.target_key = (target.lower(), pos[0], pos[1])
    
    def enumerate_moves(self, node):
        for move in self.moves:
            self.board.abbots = node.abbots() # reset board to node pos
            try:
                self.board.move(move)
                new_node = SearchNode(self.board.abbots, node.moves + move)
                if new_node.key in self.search_map:
                    # Node already processed
                    #assert self.search_map[new_node.key].depth() <= new_node.depth()
                    continue
                self.search_map[new_node.key] = new_node
                solved = self.target_key in new_node.key
                if solved:
                    assert self.board.isSolved()
                yield new_node, solved
            except board.IllegalMove:
                pass

    def solve(self, max_depth):
        assert max_depth > 0
        search_queue = deque([self.root])
        while True:
            node = search_queue.popleft()
            if node.depth() > max_depth:
                if self.verbose:
                    print >>self.debug_out, 'Bailing out at depth %s (map size %)' % (
                        node.depth(), len(search_map))
                break
            for subnode, solved in self.enumerate_moves(node):
                if solved:
                    if self.verbose:
                        print >>self.debug_out, 'Found solution with depth', subnode.depth()
                        print >>self.debug_out, 'Map size:', len(self.search_map)
                    return subnode.moves
                search_queue.append(subnode)
        return ''

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-p', '--print-board', dest='print_board',
                      action='store_true', default=False,
                      help='Print the board before and after solving.')
    parser.add_option('-d', '--max-depth', dest='max_depth',
                      type=int, default=20,
                      help='Maximum search depth.')
    parser.add_option('-v', '--verbose', dest='verbose',
                      action='store_true', default=False,
                      help='Print some debugging info.')
    parser.add_option('-f', '--filename', dest='filename', type=str,
                      help='File to print debug output to, default is stderr.')
    opts, args = parser.parse_args()

    if opts.filename:
        debug_out = open(opts.filename, 'w')
    else:
        debug_out = sys.stderr

    input = sys.stdin.read()
    b = board.Board(input)
    
    if opts.print_board:
        print >>debug_out, b
    
    solver = AbbotSolver(b, opts.verbose, debug_out)
    moves = solver.solve(opts.max_depth)
    print moves

    if opts.verbose:
        print >>debug_out, 'Moves:', moves
    if opts.print_board:
        print >>debug_out, b
