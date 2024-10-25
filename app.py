import openai
import streamlit as st
import pandas as pd
import os

# Set up OpenAI API key (make sure to securely store your API key in production)
openai.api_key = 'sk-insert Your OpenAI API Key'  # replace with your OpenAI API key or use an environment variable

# Initialize session state for storing player data
# Initialize session state for storing player data
if "players" not in st.session_state:
    st.session_state["players"] = []

# App title and description
st.title("Tennis Doubles Pairing App")
st.subheader("Add Players and Find Optimal Pairings using AI")

# Player Information Form
st.write("### Enter Player Details")

# Input fields for player data
name = st.text_input("Player Name")
playing_style = st.selectbox(
    "Playing Style",
    ["Baseline", "Serve-and-Volley", "All-Court", "Counterpuncher"]
)
position = st.selectbox(
    "Preferred Position",
    ["Net", "Baseline", "Flexible"]
)
skill_level = st.slider("Skill Level (1-10)", 1, 10)

# Button to add player to the list
if st.button("Add Player"):
    if name:
        st.session_state["players"].append({
            "Name": name,
            "Playing Style": playing_style,
            "Position": position,
            "Skill Level": skill_level
        })
        st.success(f"Added player {name} to the list.")
    else:
        st.error("Please enter the player's name.")

# Display current list of players
if st.session_state["players"]:
    st.write("### Player List")
    player_df = pd.DataFrame(st.session_state["players"])
    st.table(player_df)

    # Function to get AI-based pairing suggestions from OpenAI using GPT-3.5-turbo
    def get_ai_pairing_suggestions(players):
        # Create a conversation context for the AI
        messages = [{"role": "system", "content": "You are a tennis pairing expert."}]
        
        # Add player information to the prompt
        prompt = "Pair players for a tennis doubles match based on their qualities: playing style, preferred position, and skill level. Here is the list of players:\n\n"
        
        for player in players:
            prompt += f"Name: {player['Name']}, Style: {player['Playing Style']}, Position: {player['Position']}, Skill Level: {player['Skill Level']}\n"
        
        prompt += "\nProvide the most fitting pairs based on all player qualities."

        # Add the user's request to the messages list
        messages.append({"role": "user", "content": prompt})

        # Call the ChatCompletion API with the GPT-3.5-turbo model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo model
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )

        # Extract the generated pairing suggestions
        return response['choices'][0]['message']['content'].strip()

    # Button to get AI-generated pairs
    if st.button("Pair Players Using AI"):
        ai_suggestions = get_ai_pairing_suggestions(st.session_state["players"])
        
        # Display AI pairing suggestions
        st.write("### AI-Recommended Pairs")
        st.write(ai_suggestions)

else:
    st.info("Add players to see the list and create pairs.")

'''

'''