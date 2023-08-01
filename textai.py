import streamlit as st
import requests
import json
import uuid

conversation = {}

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
    ai_response = ''
    
    #unique_key = str(uuid.uuid4())  # Generate a random UUID as the unique key
    user_input = st.text_input("You : ")
    
    if st.button("Send"):
       # parsed_dict = json.loads(conversation)
        ai_response = get_ai_response(user_input)
        
    conversation[user_input] = ai_response
    #json_string = json.dumps(conversation)
    st.text(conversation)
        
    max_length_in_one_line = 70
    
    st.title("Conversation History")
    for user, ai in conversation.items():
        st.text("YOU : ")
        while len(user) > 0:
            st.text(f"{user[:max_length_in_one_line]}")
            user = user[max_length_in_one_line:]
            
        st.text("AI : ")
        while len(ai) > 0: 
            st.text(f"{ai[:max_length_in_one_line]}")
            ai = ai[max_length_in_one_line:]

if __name__ == "__main__":
    main()
