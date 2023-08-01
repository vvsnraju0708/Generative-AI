import streamlit as st
import requests

max_length_in_one_line = 80

def get_ai_response(text):
    url = "https://api.convai.com/character/getResponse"
    
    payload = {
        'userText': text,
        'charID': 'e0c25a94-27a6-11ee-8534-42010a40000b',
        'sessionID': '-1',
        'voiceResponse': 'True'
    }
    
    headers = {
        'CONVAI-API-KEY': '1e0cf4d08a1ac807ff3f5e9916d2b559'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    character_response = data["text"]
    return character_response

def main():
    st.title("Chat with AI")
    if "conversation" not in st.session_state:
        st.session_state.conversation = [("AI: ","Hello! How can I help you today?")]
    
    user_input = st.text_input("You: ")
    
    if st.button("Send"):
        ai_response = get_ai_response(user_input)
        st.session_state.conversation.append((user_input, ai_response))
     
    st.title("Conversation History")
    for user, ai in st.session_state.conversation:
        if len(user)==4:
            st.text(f"{ai}")
        if len(user) != 4:
            you="YOU: "+ user
            while len(you) > 0:
                st.write(f" {you[:max_length_in_one_line]}")
                you = you[max_length_in_one_line:]

            Ai="AI: "+ ai
            while len(Ai) > 0: 
                st.text( f" {Ai[:max_length_in_one_line]}")
                Ai = Ai[max_length_in_one_line:]

        st.text("---------------------------------------------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
