import random

# Define payoff matrix
PAYOFFS = {
    ("C", "C"): (3, 3),  # Both cooperate
    ("C", "D"): (0, 5),  # Player 1 cooperates, Player 2 defects
    ("D", "C"): (5, 0),  # Player 1 defects, Player 2 cooperates
    ("D", "D"): (1, 1),  # Both defect
}

# Define strategies
def always_cooperate(history, opponent_history):
    return "C"

def always_defect(history, opponent_history):
    return "D"

def tit_for_tat(history, opponent_history):
    return "C" if not opponent_history or opponent_history[-1] == "C" else "D"

def random_strategy(history, opponent_history):
    return random.choice(["C", "D"])

def grudger(history, opponent_history):
    return "C" if "D" not in opponent_history else "D"

def forgiving_tit_for_tat(history, opponent_history):
    if not opponent_history:
        return "C"
    return "C" if opponent_history[-1] == "C" or random.random() < 0.2 else "D"

def pavlov(history, opponent_history):
    if not history:
        return "C"
    return "C" if history[-1] == opponent_history[-1] else "D"

def cooperate_then_defect(history, opponent_history):
    return "C" if len(history) % 2 == 0 else "D"

def win_stay_lose_shift(history, opponent_history):
    if not history:
        return "C"
    my_last, opp_last = history[-1], opponent_history[-1]
    return my_last if PAYOFFS[(my_last, opp_last)][0] >= 3 else ("C" if my_last == "D" else "D")
# List of strategies
strategies = [
    always_cooperate,
    always_defect,
    tit_for_tat,
    random_strategy,
    grudger,
    forgiving_tit_for_tat,
    pavlov,
    cooperate_then_defect,
    win_stay_lose_shift,
]

# Run the tournament
def play_round(strategy1, strategy2, history1, history2):
    move1 = strategy1(history1, history2)
    move2 = strategy2(history2, history1)
    payoff1, payoff2 = PAYOFFS[(move1, move2)]
    return move1, move2, payoff1, payoff2

def tournament(strategies, rounds=1000):
    scores = {strategy.__name__: 0 for strategy in strategies}
    for i, strat1 in enumerate(strategies):
        for j, strat2 in enumerate(strategies):
            if i >= j:
                continue
            history1, history2 = [], []
            for _ in range(rounds):
                move1, move2, payoff1, payoff2 = play_round(strat1, strat2, history1, history2)
                history1.append(move1)
                history2.append(move2)
                scores[strat1.__name__] += payoff1
                scores[strat2.__name__] += payoff2
    return scores

# Run and display results
results = tournament(strategies)
print("Final Scores:")
for strategy, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{strategy}: {score}")
