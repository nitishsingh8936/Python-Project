

import random
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class TicTacToeGame:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]
        self.current_player = None
        self.players = {}
        self.game_history = []
        self.winner = None
        self.is_tie = False
        # Initialize matplotlib figure for real-time updates
        self.fig = None
        self.ax = None
        self.is_matplotlib_initialized = False

    def initialize_matplotlib(self):
        """Initialize matplotlib for interactive real-time updates."""
        if not self.is_matplotlib_initialized:
            plt.ion()  # Turn on interactive mode
            self.fig, self.ax = plt.subplots(figsize=(6, 6))
            self.fig.suptitle('TIC-TAC-TOE', fontsize=20, fontweight='bold')
            plt.show(block=False)  # Show window but don't block
            self.is_matplotlib_initialized = True

    def display_board_matplotlib(self):
        """Display the board using matplotlib with real-time updates."""
        if not self.is_matplotlib_initialized:
            self.initialize_matplotlib()

        # Clear the previous content
        self.ax.clear()

        # Set up the board
        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, 3)
        self.ax.set_aspect('equal')

        # Draw the grid lines
        for i in range(4):
            self.ax.axhline(i, color='black', linewidth=2)
            self.ax.axvline(i, color='black', linewidth=2)

        # Add the symbols and numbers
        for i in range(9):
            row = 2 - (i // 3)
            col = i % 3
            x = col + 0.5
            y = row + 0.5

            if self.board[i] in ['X', 'O']:
                self.ax.text(x, y, self.board[i], fontsize=36, fontweight='bold',
                           ha='center', va='center',
                           color='red' if self.board[i] == 'X' else 'blue')
            elif self.board[i] == ' ':
                pass
            else:
                self.ax.text(x, y, self.board[i], fontsize=24, fontweight='bold',
                           ha='center', va='center', color='gray')

        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Update the display using canvas methods for better performance
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)  # Small pause to allow the display to update

    def close_matplotlib(self):
        """Close the matplotlib window."""
        if self.is_matplotlib_initialized:
            plt.close(self.fig)
            plt.ioff()  # Turn off interactive mode
            self.is_matplotlib_initialized = False

    def clear_remaining_numbers(self):
        for i in range(9):
            if self.board[i] not in ['X', 'O']:
                self.board[i] = ' '

    def get_player_names(self):
        try:
            player1_name = input("Enter Player 1 name: ").strip()
            if not player1_name:
                player1_name = "Player1"

            player2_name = input("Enter Player 2 name: ").strip()
            if not player2_name:
                player2_name = "Player2"

            return player1_name, player2_name
        except Exception as e:
            print(f"Error getting player names: {e}")
            return "Player1", "Player2"

    def assign_symbols_randomly(self, player1_name, player2_name):
        try:
            first_chooser = random.choice([player1_name, player2_name])
            print(f"\n{first_chooser} gets to choose their symbol first!")

            while True:
                symbol = input(f"{first_chooser}, choose your symbol (X or O): ").upper()
                if symbol in ['X', 'O']:
                    break
                print("Please enter only X or O")

            if first_chooser == player1_name:
                self.players[player1_name] = symbol
                self.players[player2_name] = 'O' if symbol == 'X' else 'X'
            else:
                self.players[player2_name] = symbol
                self.players[player1_name] = 'O' if symbol == 'X' else 'X'

            print(f"{player1_name}: {self.players[player1_name]}")
            print(f"{player2_name}: {self.players[player2_name]}")

            return list(self.players.keys())
        except Exception as e:
            print(f"Error assigning symbols: {e}")
            self.players[player1_name] = 'X'
            self.players[player2_name] = 'O'
            return [player1_name, player2_name]

    def is_valid_move(self, position):
        try:
            pos = int(position)
            return 1 <= pos <= 9 and self.board[pos-1] not in ['X', 'O']
        except ValueError:
            return False

    def make_move(self, position, player_name):
        try:
            pos = int(position) - 1
            self.board[pos] = self.players[player_name]
            return True
        except Exception as e:
            print(f"Error making move: {e}")
            return False

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combo in win_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] and self.board[combo[0]] in ['X', 'O']):
                winning_symbol = self.board[combo[0]]
                for player, symbol in self.players.items():
                    if symbol == winning_symbol:
                        return player
        return None

    def is_board_full(self):
        return all(cell in ['X', 'O'] for cell in self.board)

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]
        self.winner = None
        self.is_tie = False

    def save_game_history(self, game_data):
        try:
            if not os.path.exists('game_history'):
                os.makedirs('game_history')

            filename = 'game_history/tic_tac_toe_history.txt'
            with open(filename, 'a') as file:
                file.write(f"Game played on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Players: {game_data['players']}\n")
                file.write(f"Result: {game_data['result']}\n")
                file.write(f"Final Board:\n")

                for i in range(0, 9, 3):
                    file.write(f"{game_data['board'][i]} | {game_data['board'][i+1]} | {game_data['board'][i+2]}\n")
                    if i < 6:
                        file.write("---------\n")

                file.write("\n" + "="*50 + "\n\n")

            print(f"Game history saved to {filename}")
        except Exception as e:
            print(f"Error saving game history: {e}")

    def display_all_game_history(self):
        try:
            filename = 'game_history/tic_tac_toe_history.txt'
            if os.path.exists(filename):
                print("\n" + "="*50)
                print("GAME HISTORY")
                print("="*50)
                with open(filename, 'r') as file:
                    content = file.read()
                    if content.strip():
                        print(content)
                    else:
                        print("No game history found.")
            else:
                print("No game history file found.")
        except Exception as e:
            print(f"Error reading game history: {e}")

    def play_single_game(self):
        try:
            player1_name, player2_name = self.get_player_names()
            player_names = self.assign_symbols_randomly(player1_name, player2_name)
            current_player_name = random.choice(player_names)

            print(f"\n{current_player_name} starts the game!")
            print("\nInitial Board:")
            self.display_board_matplotlib()

            while True:
                print(f"\n{current_player_name}'s turn ({self.players[current_player_name]})")

                while True:
                    try:
                        move = input("Enter position (1-9): ")
                        if self.is_valid_move(move):
                            break
                        else:
                            print("Invalid move! Choose an empty position between 1-9.")
                    except KeyboardInterrupt:
                        print("\nGame interrupted by user.")
                        self.close_matplotlib()
                        sys.exit()

                self.make_move(move, current_player_name)
                print(f"\nBoard after {current_player_name}'s move:")
                self.display_board_matplotlib()

                self.winner = self.check_winner()
                if self.winner:
                    print(f"\n🎉 {self.winner} wins! 🎉")
                    self.clear_remaining_numbers()
                    print("\nFinal Board:")
                    self.display_board_matplotlib()
                    break

                if self.is_board_full():
                    print("\n🤝 It's a tie! 🤝")
                    self.is_tie = True
                    self.clear_remaining_numbers()
                    print("\nFinal Board:")
                    self.display_board_matplotlib()
                    break

                current_player_name = player_names[1] if current_player_name == player_names[0] else player_names[0]

            game_data = {
                'players': f"{player1_name} ({self.players[player1_name]}) vs {player2_name} ({self.players[player2_name]})",
                'result': f"{self.winner} wins!" if self.winner else "Tie",
                'board': self.board.copy()
            }

            self.save_game_history(game_data)
            return True
        except Exception as e:
            print(f"Error during game: {e}")
            return False

    def play_game(self):
        print("🎮 Welcome to TIC-TAC-TOE Game! 🎮")
        print("="*40)
        games_played = 0

        try:
            while True:
                self.reset_board()
                if self.play_single_game():
                    games_played += 1

                while True:
                    try:
                        continue_game = input("\nDo you want to play another game? (y/n): ").lower()
                        if continue_game in ['y', 'yes']:
                            print("\n" + "="*40)
                            print("Starting new game...")
                            print("="*40)
                            break
                        elif continue_game in ['n', 'no']:
                            print(f"\nThanks for playing! You played {games_played} game(s).")
                            if games_played > 0:
                                show_history = input("Do you want to see the game history? (y/n): ").lower()
                                if show_history in ['y', 'yes']:
                                    self.display_all_game_history()
                            self.close_matplotlib()  # Close matplotlib window when exiting
                            return
                        else:
                            print("Please enter 'y' for yes or 'n' for no.")
                    except KeyboardInterrupt:
                        print("\nGoodbye!")
                        self.close_matplotlib()  # Close matplotlib window when exiting
                        return
        except Exception as e:
            print(f"Error in main game loop: {e}")
            self.close_matplotlib()  # Close matplotlib window on error

def main():
    try:
        game = TicTacToeGame()
        game.play_game()
    except Exception as e:
        print(f"Error starting game: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
