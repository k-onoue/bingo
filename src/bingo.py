import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st
from io import BytesIO

class Bingo:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        
        if 'used_numbers' not in st.session_state:
            self.reset_game()

    def generate_number(self):
        """Generate a random number that has not been drawn yet."""
        if not hasattr(self, 'numbers'):
            self.numbers = list(range(1, 76))  # Standard Bingo numbers
        if not self.numbers:
            return None
        number = random.choice(self.numbers)
        self.numbers.remove(number)
        st.session_state['used_numbers'].add(number)
        return number

    def draw_number(self):
        """Display a random number."""
        number = self.generate_number()
        if number is None:
            st.write("All numbers have been drawn!")
        else:
            st.markdown(f"<div style='font-size: 100px; text-align: center;'>{number}</div>", unsafe_allow_html=True)

    def show_used_numbers(self):
        """Display the history of numbers that have been drawn."""
        st.write("History:")
        st.write(", ".join(map(str, sorted(st.session_state['used_numbers']))))

    def reset_game(self):
        """Reset the game state."""
        st.session_state['used_numbers'] = set()


class BingoCard:
    def __init__(self, card_size=5):
        self.card_size = card_size  # Typically, a Bingo card is 5x5

    def create_bingo_card(self):
        """Generate a Bingo card and return it as a DataFrame."""
        numbers = list(range(1, self.card_size**2 + 1))
        random.shuffle(numbers)
        card = [numbers[i:i+self.card_size] for i in range(0, len(numbers), self.card_size)]
        card[int(self.card_size/2)][int(self.card_size/2)] = "FREE"  # Middle space is FREE
        return pd.DataFrame(card, columns=list('BINGO'))

    def generate_and_save_cards(self, num_cards):
        """Generate multiple Bingo cards and return them as a PDF."""
        cards = [self.create_bingo_card() for _ in range(num_cards)]
        buffer = BytesIO()
        with PdfPages(buffer, 'wb') as pp:
            for card in cards:
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.axis('off')
                the_table = ax.table(cellText=card.values, colLabels=card.columns, loc='center')
                pp.savefig(fig, bbox_inches='tight')
                plt.close(fig)
        buffer.seek(0)
        return buffer