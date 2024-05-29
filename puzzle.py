import csv
import argparse
from termcolor import colored

class Puzzle:
    def __init__(self, args):
        self.puzzle = self.parse_puzzle(args.puzzle)
        self.words = self.parse_words(args.words)
        self.solved = []

    def parse_puzzle(self, puzzle_name):
        # Time Complexity: O(m)
        # Explanation: This method reads a CSV file line by line, where m is the number of rows in the puzzle file.
        puzzle = []
        with open(puzzle_name, 'r') as pfile:
            p_reader = csv.reader(pfile)
            for p_row in p_reader:
                puzzle.append(p_row)
        return puzzle
    
    def parse_words(self, list_name):
        # Time Complexity: O(n)
        # Explanation: This method reads a CSV file line by line, where n is the number of words in the words list file.
        words = []
        with open(list_name, 'r') as cfile:
            c_reader = csv.reader(cfile)
            for c_row in c_reader:
                words.append(str(c_row[0]).replace(' ', ''))
        return words 

    def output_cli(self):
        # Time Complexity: O(R * C)
        # Explanation: This method iterates over each character in the puzzle (R rows and C columns).
        for ri, row in enumerate(self.puzzle):
            for chi, ch in enumerate(row[0]):
                if (ri, chi) in self.solved:
                    print(colored(f"{ch}", "red"), end=" ")
                else:
                    print(colored(f"{ch}", "blue"), end=" ")
            print()

    def find_word(self):
        # Time Complexity: O(W * (R * C))
        # Explanation: This method checks each word in the words list (W words) against the entire puzzle (R rows and C columns).
        for word in self.words:
            if self.find_horizontal(word):
                continue
            if self.find_vertical(word):
                continue
            if self.find_diagonal(word):
                continue

    def find_horizontal(self, word):
        # Time Complexity: O(R * C * W)
        # Explanation: For each word, this method iterates over each row (R rows). For each row, it checks for the word in the string representation of the row, which takes O(C) time. This is repeated for W words.
        for ri, row in enumerate(self.puzzle):
            if word in str(row):
                for i in range(0, len(word)):
                    self.solved.append((ri, str(row).find(word) - 2 + i))
                return True
            row_r = str(row)[::-1]
            if word in row_r:
                for i in range(0, len(word)):
                    self.solved.append((ri, len(row_r) - str(row_r).find(word) - 3 - i))
                return True
        return False

    def find_vertical(self, word):
        # Time Complexity: O(R * C * W)
        # Explanation: For each word, this method iterates over each column (C columns). For each column, it constructs a string from top to bottom (R rows), which takes O(R) time. This is repeated for W words.
        for char in range(len(self.puzzle[0][0])):
            temp = []
            for col in range(len(self.puzzle)):
                temp.append(self.puzzle[col][0][char])
            temp = ''.join(temp)
            temp_r = temp[::-1]
            if word in str(temp):
                for i in range(0, len(word)):
                    self.solved.append((str(temp).find(word) + i, char))
                return True
            if word in str(temp_r):
                for i in range(0, len(word)):
                    self.solved.append((len(temp_r) - str(temp_r).find(word) - 1 - i, char))
                return True
        return False

    def find_diagonal(self, word):
        # Time Complexity: O(D * W)
        # Explanation: For each word, this method checks along the diagonals of the puzzle. The number of diagonals D is approximately equal to R + C. For each diagonal, constructing the string takes O(min(R, C)) time. This is repeated for W words.
        for a in range(0, len(self.puzzle[0][0])):
            temp = [[] for i in range(8)]
            ranges = [[] for i in range(8)]
            i = 0
            while ((a - i) >= 0) and (i < len(self.puzzle)):
                coords = [[i, a-i],[29-i, a-i], [29-i, 29-(a-i)], [i, 29-(a-i)]]
                for cx, c in enumerate(coords):
                    temp[cx].append(self.puzzle[c[0]][0][c[1]])
                    ranges[cx].append((c[0], c[1]))
                    ranges[cx+4].append((c[1], c[0]))
                i+=1

            for ti in range(4):
                temp[ti] = ''.join(temp[ti])
                temp[ti+4] = temp[ti][::-1]
            for tx, t in enumerate(temp):
                if word in str(t):
                    for i in range(0, len(word)):
                        self.solved.append(ranges[tx][str(t).find(word) + i])
                    return True
        return False 
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--puzzle', help='puzzles/ws-1-puzzle.csv', default='puzzles/ws-1-puzzle.csv')
    parser.add_argument('--words', help='puzzles/ws-1-list.csv', default='puzzles/ws-1-list.csv')

    args = parser.parse_args()

    if not args.puzzle or not args.words:
        print("Please provide both --puzzle and --words arguments.")
    else:
        p = Puzzle(args)
        print("\nPROBLEM:")
        p.output_cli()
    print("\nSOLUTION:")
    p.find_word()
    p.output_cli()
