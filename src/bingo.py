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
        
        self.numbers = list(range(1, 76))  # Initialize the numbers at instantiation
        if 'used_numbers' not in st.session_state:
            self.reset_game()

    def generate_number(self):
        """Generate a random number that has not been drawn yet."""
        if not self.numbers:
            return None  # Return None when all numbers have been drawn
        number = random.choice(self.numbers)
        self.numbers.remove(number)  # Corrected line
        st.session_state['used_numbers'].add(number)
        return number

    def draw_number(self):
        """Display a random number."""
        number = self.generate_number()

        print(len(self.numbers))

        if number is None:
            st.write("All numbers have been drawn!")
        else:
            st.markdown(f"<div style='font-size: 100px; text-align: center;'>{number}</div>", unsafe_allow_html=True)

    def show_used_numbers(self):
        """Display the history of numbers that have been drawn."""
        st.write("History:")
        st.write(", ".join(map(str, st.session_state['used_numbers'])))

    def reset_game(self):
        """Reset the game state."""
        self.numbers = list(range(1, 76))  # Reinitialize the numbers
        st.session_state['used_numbers'] = set()


class BingoCard:
    def __init__(self, card_size=5):
        self.card_size = card_size  # Typically, a Bingo card is 5x5

    def create_bingo_card(self):
        """Generate a Bingo card and return it as a DataFrame."""
        card = []
        available_numbers = list(range(1, 76))
        for i in range(self.card_size):
            # Generate numbers for each column with the correct range
            start = 1 + i * 15
            end = start + 15
            valid_numbers = [n for n in available_numbers if start <= n < end]
            column_numbers = random.sample(valid_numbers, self.card_size)
            # Remove selected numbers from available pool to ensure no duplicates across columns
            available_numbers = [n for n in available_numbers if n not in column_numbers]
            card.append(column_numbers)
        
        # Convert card list into DataFrame and transpose to get correct orientation
        card_df = pd.DataFrame(card).transpose()
        card_df = card_df.sample(frac=1, axis=1).reset_index(drop=True)
        card_df = card_df.astype(str)
        card_df.columns = list('BINGO')
        card_df.iloc[int(self.card_size/2), int(self.card_size/2)] = "FREE"  # Middle space is FREE
        return card_df

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


if __name__ == "__main__":
    gen = BingoCard()
    card = gen.create_bingo_card()

    print(card)
