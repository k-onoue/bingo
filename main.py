import streamlit as st

from src.bingo import Bingo, BingoCard
from src.utils import load_base64_video


def main():
    base64_video = load_base64_video()

    with st.sidebar:
        # Reset button to restart the game
        if st.button("Reset"):
            st.session_state.game = Bingo(seed=None)  # Reset and store in session state
            st.session_state.game.reset_game()
            st.success("Game has been reset!")

        # Interface for generating bingo cards
        st.header("Bingo Card Generator")
        num_cards = st.number_input(
            "Enter the number of participants", min_value=1, value=1, step=1
        )
        if st.button("Generate Bingo Cards"):
            bingo_card_generator = BingoCard()
            pdf_file = bingo_card_generator.generate_and_save_cards(num_cards)
            st.download_button(
                label="Download Bingo Cards",
                data=pdf_file,
                file_name="bingo_cards.pdf",
                mime="application/pdf"
            )

        # Slider to adjust the background blur of the video
        blur_intensity = st.slider("Adjust Background Blur", 0, 20, 5)

    # Custom CSS to style the sidebar and other elements
    st.markdown(f"""
        <style>
            /* Adjusting the sidebar color */
            .css-18e3th9 {{
                background-color: #FF0000; /* Red color for the sidebar */
            }}
            /* Customizing the top bar */
            header .css-1py40y0 {{
                background-color: #008000; /* Green color for the top bar */
            }}
            /* Change color of all Streamlit buttons */
            .stButton>button {{
                color: white;
                border: none;
                background-color: #008000; /* Green color for buttons */
                border-radius: 5px;
                padding: 10px 24px;
                font-size: 16px;
            }}
            /* Background video and content styling */
            body, html {{
                height: 100%;
                margin: 0;
                color: white;
                overflow: hidden;
            }}
            .bg {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%; 
                min-height: 100%;
                z-index: -2;
                filter: blur({blur_intensity}px);
            }}
            .content {{
                position: relative;
                z-index: 10;
                padding: 10px;
            }}
            .stApp {{
                backdrop-filter: blur(0px);
                -webkit-backdrop-filter: blur(0px);
            }}
        </style>
        <video class="bg" autoplay loop muted playsinline>
            <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
        </video>
        <div class="content">
            <h1>Let's play!</h1>
        </div>
        """, unsafe_allow_html=True)

    # Load or initialize the game instance
    if 'game' not in st.session_state:
        st.session_state.game = Bingo()

    # Drawing number and displaying results
    st.title("Bingo Game")
    if st.button("Draw Number"):
        st.session_state.game.draw_number()
    st.session_state.game.show_used_numbers()


if __name__ == "__main__":
    main()
