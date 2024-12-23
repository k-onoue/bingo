def load_base64_video():
    with open('assets/xmas_sora_base64.txt', 'r') as file:
        base64_data = file.read().strip()
    return base64_data

# import random
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

# # from .emoji import emoji_list

# emoji_list = [
#     "❤️", "🖕", "🫧", "🗑️", "💎",
#     "🍎", "🍉", "🍌", "🍇", "🍓",
#     "🎅", "🤶", "🦌", "🎄", "🎁",
#     "🍔", "🍟", "🍕", "🌭", "🥪",
#     "🚗", "🚕", "🚙", "🚌", "🚎",
#     "🐮", "🐷", "🐔", "🐶", "🐱",
#     "🦆", "🦉", "🦅", "🦇", "🦋",
#     "🍄", "🌰", "🍁", "🌻", "🌼",
#     "😂", "😍", "😎", "🤓", "🥺",
#     "🍣", "🍤", "🍦", "🍩", "🍫",
#     "🎸", "🎹", "🎷", "🎺", "🎻",
#     "🏈", "🏀", "⚽", "⚾", "🎾",
#     "❄️", "☃️", "⛄", "🔥", "🀄",
#     "🍺", "🍷", "🍸", "🍹", "🍾",
#     "🤩", "🫥", "🥶", "💋", "😱"
# ]


# def load_base64_video():
#     with open('assets/xmas_sora_base64.txt', 'r') as file:
#         base64_data = file.read().strip()
#     return base64_data


# class BingoCard:
#     def __init__(self, emoji_list, card_size=5):
#         self.emoji_list = emoji_list
#         self.card_size = card_size

#     def create_bingo_card(self):
#         """Generate a Bingo card and return it as a DataFrame."""
#         per_column = len(self.emoji_list) // self.card_size
#         columns = [self.emoji_list[i * per_column:(i + 1) * per_column] for i in range(self.card_size)]
#         for col in columns:
#             random.shuffle(col)
#         card = [[col[i] for col in columns] for i in range(self.card_size)]
#         card[int(self.card_size/2)][int(self.card_size/2)] = "FREE"  # Middle space is FREE
#         return pd.DataFrame(card, columns=['B', 'I', 'N', 'G', 'O'])

#     def save_cards_to_pdf(self, cards, filename="bingo_cards.pdf"):
#         """Save a list of DataFrame cards to a PDF file."""
#         pp = PdfPages(filename)
#         for card in cards:
#             fig, ax = plt.subplots(figsize=(8, 6))
#             ax.axis('tight')
#             ax.axis('off')
#             the_table = ax.table(cellText=card.values, colLabels=card.columns, loc='center', cellLoc='center')
#             the_table.auto_set_font_size(False)
#             the_table.set_fontsize(12)
#             the_table.scale(1.2, 1.2)  # Adjust scale for better readability
#             pp.savefig(fig, bbox_inches='tight')
#             plt.close(fig)
#         pp.close()

#     def generate_and_save_cards(self, num_cards, filename="bingo_cards.pdf"):
#         """Generate multiple Bingo cards and save them to a PDF."""
#         cards = [self.create_bingo_card() for _ in range(num_cards)]
#         self.save_cards_to_pdf(cards, filename)

# # Usage
# if __name__ == "__main__":
#     emoji_list = [
#         "❤️", "🖕", "🫧", "🗑️", "💎", "🍎", "🍉", "🍌", "🍇", "🍓",
#         "🎅", "🤶", "🦌", "🎄", "🎁", "🍔", "🍟", "🍕", "🌭", "🥪",
#         "🚗", "🚕", "🚙", "🚌", "🚎", "🐮", "🐷", "🐔", "🐶", "🐱",
#         "🦆", "🦉", "🦅", "🦇", "🦋", "🍄", "🌰", "🍁", "🌻", "🌼",
#         "😂", "😍", "😎", "🤓", "🥺", "🍣", "🍤", "🍦", "🍩", "🍫",
#         "🎸", "🎹", "🎷", "🎺", "🎻", "🏈", "🏀", "⚽", "⚾", "🎾",
#         "❄️", "☃️", "⛄", "🔥", "🀄", "🍺", "🍷", "🍸", "🍹", "🍾",
#         "🤩", "🫥", "🥶", "💋", "😱"
#     ]
#     bingo_card_generator = BingoCard(emoji_list)
#     bingo_card_generator.generate_and_save_cards(5)


import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import requests
from io import BytesIO

def emoji_to_image(emoji, zoom=0.3):
    url = f"https://github.com/googlefonts/noto-emoji/raw/main/png/128/emoji_u{ord(emoji):x}.png"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return OffsetImage(img, zoom=zoom)

def plot_emoji_image(ax, emoji, xy):
    image = emoji_to_image(emoji)
    ab = AnnotationBbox(image, xy, frameon=False, box_alignment=(0.5, 0.5))
    ax.add_artist(ab)

def save_cards_to_pdf(cards, filename="bingo_cards.pdf"):
    with PdfPages(filename) as pp:
        for card in cards:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.axis('off')
            ax.set_xlim(0, 5)
            ax.set_ylim(0, 5)
            # Iterate through DataFrame values correctly using np.ndenumerate
            for (i, j), val in np.ndenumerate(card):
                plot_emoji_image(ax, val, (j + 0.5, 5 - i - 0.5))
            pp.savefig(fig, bbox_inches='tight')
            plt.close(fig)

# Assuming you have a list of dataframes `cards`
# Example DataFrame generation (for illustrative purposes)
import pandas as pd
cards = [pd.DataFrame([['😀', '😃', '😄', '😁', '😆'],
                       ['😅', '😂', '🤣', '😊', '😇'],
                       ['😍', '🥰', '😘', '😗', '😙'],
                       ['😚', '😋', '😛', '😝', '😜'],
                       ['🤪', '🤨', '🧐', '🤓', '😎']], columns=list('BINGO')) for _ in range(5)]

save_cards_to_pdf(cards)
