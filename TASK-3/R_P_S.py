import tkinter as tk
from tkinter import Toplevel, messagebox
import random

# Function to determine the computer's choice
def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])

# Function to determine the winner
def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return "tie"
    elif (
        (choice1 == "rock" and choice2 == "scissors") or
        (choice1 == "scissors" and choice2 == "paper") or
        (choice1 == "paper" and choice2 == "rock")
    ):
        return "Player 1"
    else:
        return "Player 2"

# Function to handle the user's selection
def user_selection(user_choice):
    global user_score, computer_score
    if game_mode.get() == "computer":
        computer_choice = get_computer_choice()
        result = determine_winner(user_choice, computer_choice)
        
        # Update selections
        player_choice_label.config(text=f"🧍 You: {user_choice.upper()}")
        computer_choice_label.config(text=f"🤖 Computer: {computer_choice.upper()}")

        if result == "Player 1":
            user_score += 1
            result_label.config(text="🎉 You Win! 🎉", fg="green")
        elif result == "Player 2":
            computer_score += 1
            result_label.config(text="🤖 Computer Wins!", fg="red")
        else:
            result_label.config(text="😐 It's a Tie!", fg="blue")

        update_scores()
    elif game_mode.get() == "player":
        player1_select()

# Function to create a selection window for a player
def player_select_window(player_name, callback):
    window = Toplevel(root)
    window.title(f"{player_name} - Choose an Option")
    window.geometry("300x180")
    window.resizable(False, False)
    tk.Label(window, text=f"{player_name}, make your choice:", font=("Comic Sans MS", 12)).pack(pady=10)

    buttons_frame = tk.Frame(window)
    buttons_frame.pack(pady=10)

    tk.Button(buttons_frame, text="🧱 Rock", font=("Comic Sans MS", 10), command=lambda: [callback("rock"), window.destroy()], width=10).grid(row=0, column=0, padx=5)
    tk.Button(buttons_frame, text="📄 Paper", font=("Comic Sans MS", 10), command=lambda: [callback("paper"), window.destroy()], width=10).grid(row=0, column=1, padx=5)
    tk.Button(buttons_frame, text="✂️ Scissors", font=("Comic Sans MS", 10), command=lambda: [callback("scissors"), window.destroy()], width=10).grid(row=0, column=2, padx=5)

# Player 1 selection
def player1_select():
    player_select_window("Player 1", player1_choice_callback)

# Player 1 callback
def player1_choice_callback(choice):
    global player1_choice
    player1_choice = choice
    player2_select()

# Player 2 selection
def player2_select():
    player_select_window("Player 2", player2_choice_callback)

# Player 2 callback
def player2_choice_callback(choice):
    global player1_choice
    player2_choice = choice
    result = determine_winner(player1_choice, player2_choice)

    # Update selections
    player_choice_label.config(text=f"🧍 Player 1: {player1_choice.upper()}")
    computer_choice_label.config(text=f"🧍 Player 2: {player2_choice.upper()}")

    if result == "Player 1":
        result_label.config(text="🎉 Player 1 Wins! 🎉", fg="green")
    elif result == "Player 2":
        result_label.config(text="🎉 Player 2 Wins! 🎉", fg="blue")
    else:
        result_label.config(text="😐 It's a Tie!", fg="gray")

# Function to update the score labels
def update_scores():
    user_score_label.config(text=f"Your Score: {user_score}")
    computer_score_label.config(text=f"Computer Score: {computer_score}")

# Function to reset the game
def reset_game():
    global user_score, computer_score, player1_choice
    user_score = 0
    computer_score = 0
    player1_choice = ""
    player_choice_label.config(text="🧍 Player 1: ")
    computer_choice_label.config(text="🤖 Player 2/Computer: ")
    result_label.config(text="Let's Play!", fg="black")
    update_scores()
    messagebox.showinfo("Reset Game", "🔄 Scores have been reset! Let's play again!")

# Function to select game mode
def select_mode():
    if game_mode.get() == "computer":
        buttons_frame.pack(pady=20)
        mode_label.config(text="Mode: Player vs Computer")
    elif game_mode.get() == "player":
        buttons_frame.pack_forget()
        mode_label.config(text="Mode: Player vs Player")
        player1_select()

# Initialize scores
user_score = 0
computer_score = 0
player1_choice = ""

# Create the main GUI window
root = tk.Tk()
root.title("Rock-Paper-Scissors")
root.geometry("500x600")
root.resizable(False, False)
root.configure(bg="#f0f8ff")

# Title
title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Comic Sans MS", 20, "bold"), bg="#f0f8ff", fg="#ff4500")
title_label.pack(pady=10)

# Mode Selection
game_mode = tk.StringVar(value="computer")  # Default to Player vs Computer

mode_label = tk.Label(root, text="Select a Game Mode", font=("Comic Sans MS", 16), bg="#f0f8ff", fg="black")
mode_label.pack(pady=5)

mode_frame = tk.Frame(root, bg="#f0f8ff")
mode_frame.pack(pady=10)

computer_mode_button = tk.Radiobutton(
    mode_frame, 
    text="Player vs Computer", 
    variable=game_mode, 
    value="computer", 
    font=("Comic Sans MS", 12), 
    bg="#f0f8ff", 
    command=select_mode
)
computer_mode_button.grid(row=0, column=0, padx=10)

player_mode_button = tk.Radiobutton(
    mode_frame, 
    text="Player vs Player", 
    variable=game_mode, 
    value="player", 
    font=("Comic Sans MS", 12), 
    bg="#f0f8ff", 
    command=select_mode
)
player_mode_button.grid(row=0, column=1, padx=10)

# Frame for selections
selections_frame = tk.Frame(root, bg="#f0f8ff")
selections_frame.pack(pady=20)

player_choice_label = tk.Label(selections_frame, text="🧍 Player 1: ", font=("Comic Sans MS", 14), bg="#e0ffff", width=20)
player_choice_label.grid(row=0, column=0, padx=20)

computer_choice_label = tk.Label(selections_frame, text="🤖 Player 2/Computer: ", font=("Comic Sans MS", 14), bg="#ffe4e1", width=20)
computer_choice_label.grid(row=0, column=1, padx=20)

# Result Label
result_label = tk.Label(root, text="Let's Play!", font=("Comic Sans MS", 16, "bold"), bg="#f0f8ff", fg="black")
result_label.pack(pady=10)

# Score Frame
scores_frame = tk.Frame(root, bg="#f0f8ff")
scores_frame.pack(pady=10)

user_score_label = tk.Label(scores_frame, text="Your Score: 0", font=("Comic Sans MS", 14), bg="#e0ffff")
user_score_label.grid(row=0, column=0, padx=20)

computer_score_label = tk.Label(scores_frame, text="Computer Score: 0", font=("Comic Sans MS", 14), bg="#ffe4e1")
computer_score_label.grid(row=0, column=1, padx=20)

# Buttons Frame
buttons_frame = tk.Frame(root, bg="#f0f8ff")
buttons_frame.pack(pady=20)

rock_button = tk.Button(buttons_frame, text="🧱 Rock", font=("Comic Sans MS", 16), command=lambda: user_selection("rock"), bg="#d3d3d3", fg="black", width=10)
rock_button.grid(row=0, column=0, padx=10)

paper_button = tk.Button(buttons_frame, text="📄 Paper", font=("Comic Sans MS", 16), command=lambda: user_selection("paper"), bg="#d3d3d3", fg="black", width=10)
paper_button.grid(row=0, column=1, padx=10)

scissors_button = tk.Button(buttons_frame, text="✂️ Scissors", font=("Comic Sans MS", 16), command=lambda: user_selection("scissors"), bg="#d3d3d3", fg="black", width=10)
scissors_button.grid(row=0, column=2, padx=10)

# Reset Button
reset_button = tk.Button(root, text="🔄 Reset Game", font=("Comic Sans MS", 14), command=reset_game, bg="red", fg="white", width=15)
reset_button.pack(pady=20)

# Run the GUI loop
root.mainloop()
