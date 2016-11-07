import time
import random
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        pass
        self.movePool = []

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating AI's move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately
    def move(self, a, b, a_fin, b_fin, t):
        # a is the slots on AI's side
        # print "ai moved"
        #For test only: return a random move
        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # Make sure to clean the file before each of your experiment

        # if random.sample(range(10), 1)[0] <= 2:
        #     return random.sample(range(6), 1)[0]

        d = 8

        f.write('depth = '+str(d)+'\n')
        t_start = time.time()
        #bestMove = self.minimax(a[:],b[:],a_fin,b_fin,depth = d)
        bestMove = self.alphabeta(a[:],b[:],a_fin,b_fin,depth = d)
        f.write(str(time.time()-t_start)+'\n')

        assert(a[bestMove] != 0)

        print "best move is", bestMove
        return bestMove#bestMove
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code.


    def heuristic(self, a, b, a_fin, b_fin):
        return a_fin - b_fin

    """
        This function will update the piece we have after we make the "move"
    """
    def updatePiece(self, move,a,b,a_fin,b_fin):
        num_balls = a[move]
        # if choose an empty slot
        if num_balls == 0:
            print "invalid move"
            return a,b,a_fin,b_fin

        num_balls_buff = num_balls

        # a round
        a_round = a[move:] + [a_fin] + b[:] + a[:move]
        a_round[0] = 0
        i = 1

        while num_balls > 0:
            a_round[i%13] += 1
            i += 1
            num_balls -= 1

        new_a = a_round[13 - move:] + a_round[:6-move]
        new_a_fin = a_round[6 - move]
        new_b = a_round[6 - move + 1: 6 - move + 1 + 6]

        # if end at an empty slot, we have ace!
        idd = num_balls_buff % 13 + move
        if idd < 6 and new_a[idd] == 1:
            num_aceBalls = new_b[5 - idd]
            new_b[5 - idd] = 0
            new_a_fin += (num_aceBalls + 1)
            new_a[idd] = 0

        # if our side is empty!
        if sum(new_a) == 0:
            return [0]*6, [0]*6, new_a_fin, b_fin + sum(new_b)
        # if their side is empty!
        if sum(new_b) == 0:
            return [0]*6, [0]*6, new_a_fin + sum(new_a), b_fin
        return new_a,new_b,new_a_fin,b_fin

    # calling function
    def minimax(self,a,b,a_fin,b_fin, depth):
        self.depth = depth
        v, bestMove = self.max_move(a,b,a_fin,b_fin, 0)

        return bestMove

    # AI move
    def max_move(self, a,b,a_fin,b_fin,level):
        # terminal test
        if level == self.depth or (sum(a) == 0 and sum(b) == 0):
            return self.heuristic(a,b,a_fin,b_fin), 0

        v = -999
        bestMove = -1

        for i in range(6):
            # if there is nothing inside, just skip
            if a[i] == 0:
                continue
            new_a, new_b,new_a_fin, new_b_fin = self.updatePiece(i, a,b,a_fin, b_fin)

            # if this is a bingo, max move again
            if a[i]%13 + i == 6:
                newv, _ = self.max_move(new_a,new_b,new_a_fin,new_b_fin, level)
            else:
                newv, _ = self.min_move(new_b,new_a,new_b_fin,new_a_fin, level + 1)

            if newv > v:
                bestMove = i
                v = newv
        return v, bestMove

    def min_move(self, a,b,a_fin,b_fin,level):
        # for min player, aka human, human's a_fin is AI's b_fin, and vice versa.
        # terminal test
        if level == self.depth or (sum(a) == 0 and sum(b) == 0):
            return self.heuristic(b,a,b_fin,a_fin), 0

        v = 999
        bestMove = -1

        for i in range(6):
            # if there is nothing inside, just skip
            if a[i] == 0:
                continue
            new_a, new_b, new_a_fin, new_b_fin = self.updatePiece(i, a,b,a_fin, b_fin)

            if a[i]%13 + i == 6:
                newv, _ = self.min_move(new_a,new_b,new_a_fin,new_b_fin, level)
            else:
                newv, _ = self.max_move(new_b,new_a,new_b_fin,new_a_fin, level + 1)

            if newv < v:
                bestMove = i
                v = newv
        return v, bestMove



    def alphabeta(self, a, b, a_fin, b_fin, depth):
        self.depth = depth
        v, bestMove = self.max_move_alpha(a[:],b[:],a_fin, b_fin, -999, 999, 0)
        return bestMove

    def max_move_alpha(self, a, b, a_fin, b_fin, alpha, beta, level):
        if level == self.depth or (sum(a) == 0 and sum(b) == 0):
            return self.heuristic(a,b,a_fin,b_fin), 0

        v = -999
        bestMove = -1

        for i in range(6):
            if a[i] == 0:
                continue

            new_a, new_b, new_a_fin, new_b_fin = self.updatePiece(i, a,b,a_fin, b_fin)

            # if it is our turn again
            if a[i]%13 + i == 6:
                newv, _ = self.max_move_alpha(new_a,new_b,new_a_fin,new_b_fin, alpha, beta, level + 1)
            else:
                newv, _ = self.min_move_alpha(new_b,new_a,new_b_fin,new_a_fin, alpha, beta, level + 1)
            if newv > v:
                v = newv
                bestMove = i
            if v >= beta:
                return v, bestMove
            alpha = max(alpha, v)

        return v, bestMove


    def min_move_alpha(self, a, b, a_fin, b_fin, alpha, beta, level):
        if level == self.depth or (sum(a) == 0 and sum(b) == 0):
            return self.heuristic(b,a,b_fin,a_fin), 0

        v = 999
        bestMove = -1

        for i in range(6):
            if a[i] == 0:
                continue

            new_a, new_b, new_a_fin, new_b_fin = self.updatePiece(i, a,b,a_fin, b_fin)
            if a[i]%13 + i == 6:
                newv, _ = self.min_move_alpha(new_a,new_b,new_a_fin,new_b_fin, alpha, beta, level + 1)
            else:
                newv, _ = self.max_move_alpha(new_b,new_a,new_b_fin,new_a_fin, alpha, beta, level + 1)
            if newv < v:
                v = newv
                bestMove = i
            if v <= alpha:
                return v, bestMove
            beta = min(beta, v)

        return v, bestMove


# XAI = ai()
# # #
# XAI.move([1,1,8,8,8,8],[7,7,7,0,7,7],2, 1, 0)
