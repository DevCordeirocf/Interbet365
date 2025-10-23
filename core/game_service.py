import random
import streamlit as st
from core.db import init_supabase_client
from core.user_service import update_user_balance


def calculate_baccarat_value(hand):

    value = 0
    for card in hand:

        card_value = card[:-1]
        
        if card_value in ['K', 'Q', 'J', '10']:
            value += 0
        elif card_value == 'A':
            value += 1
        else:
            value += int(card_value)
    return value % 10

def simulate_baccarat_hand():

    values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    # C=Copas, E=Espadas, O=Ouros, P=Paus
    suits = ['C', 'E', 'O', 'P']

    deck = [value + suit for value in values for suit in suits]
    random.shuffle(deck)

    player_hand = []
    banker_hand = []


    player_hand.append(deck.pop())
    banker_hand.append(deck.pop())
    player_hand.append(deck.pop())
    banker_hand.append(deck.pop())

    player_value = calculate_baccarat_value(player_hand)
    banker_value = calculate_baccarat_value(banker_hand)

    if player_value >= 8 or banker_value >= 8:
        pass 
    else:
        player_needs_third = False
        if player_value <= 5:
            player_hand.append(deck.pop())
            player_needs_third = True
            player_value = calculate_baccarat_value(player_hand)
        
        if not player_needs_third:
            if banker_value <= 5:
                banker_hand.append(deck.pop())
        else:
            player_third_card = player_hand[-1][:-1] 
            player_third_card_value = 0
            if player_third_card in ['K', 'Q', 'J', '10']: player_third_card_value = 0
            elif player_third_card == 'A': player_third_card_value = 1
            else: player_third_card_value = int(player_third_card)

            if banker_value <= 2: banker_hand.append(deck.pop())
            elif banker_value == 3 and player_third_card_value != 8: banker_hand.append(deck.pop())
            elif banker_value == 4 and player_third_card_value in [2, 3, 4, 5, 6, 7]: banker_hand.append(deck.pop())
            elif banker_value == 5 and player_third_card_value in [4, 5, 6, 7]: banker_hand.append(deck.pop())
            elif banker_value == 6 and player_third_card_value in [6, 7]: banker_hand.append(deck.pop())
        
        banker_value = calculate_baccarat_value(banker_hand)

    if player_value > banker_value:
        outcome = "Player"
    elif banker_value > player_value:
        outcome = "Banker"
    else:
        outcome = "Tie"

    return {
        "outcome": outcome,
        "player_hand": player_hand, 
        "banker_hand": banker_hand, 
        "player_value": player_value,
        "banker_value": banker_value
    }

def calculate_baccarat_payout(bet_on: str, outcome: str, bet_amount: float) -> float:

    if bet_on == outcome:
        if outcome == "Player":
            return bet_amount + (bet_amount * 1)
        elif outcome == "Banker":
            return bet_amount + (bet_amount * 0.95)
        elif outcome == "Tie":
            return bet_amount + (bet_amount * 8)

    elif outcome == "Tie" and bet_on in ["Player", "Banker"]:
        return bet_amount
    else:
        return 0.0

def log_game_bet(user_id: str, game_name: str, bet_amount: float, bet_on: str, outcome: str, payout_amount: float) -> bool:
    supabase = init_supabase_client()
    if not supabase: return False
    try:
        log_data = {"user_id": user_id, "game_name": game_name, "bet_amount": bet_amount, "bet_on": bet_on, "outcome": outcome, "payout_amount": payout_amount}
        supabase.table('game_bets').insert(log_data).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao registrar aposta do jogo: {e}"); return False

def play_baccarat_hand(user_id: str, bet_on: str, bet_amount: float) -> dict | None:
    debit_success = update_user_balance(user_id, -bet_amount)
    if not debit_success:
        st.error("Erro ao debitar a aposta. Saldo insuficiente ou erro no DB."); return None

    simulation_result = simulate_baccarat_hand()
    outcome = simulation_result["outcome"]
    payout_amount = calculate_baccarat_payout(bet_on, outcome, bet_amount)

    credit_success = True
    if payout_amount > 0:
        credit_success = update_user_balance(user_id, payout_amount)
        if not credit_success:
            st.error("ERRO CRÍTICO: Falha ao creditar o prêmio! Contate o suporte.")

    log_success = log_game_bet(user_id=user_id, game_name="Baccarat", bet_amount=bet_amount, bet_on=bet_on, outcome=outcome, payout_amount=payout_amount)

    return {
        "simulation": simulation_result, "bet_on": bet_on, "bet_amount": bet_amount,
        "payout_amount": payout_amount, "log_success": log_success, "credit_success": credit_success
    }