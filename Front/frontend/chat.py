import streamlit as st
import numpy as np
import configs
import requests
import services
st.set_page_config(layout = "wide")

#Header for authentication
headers = {
   "Authorization" : f"Bearer {st.session_state["token"]}"
}
try:
   current_user = requests.get(f"{configs.BACKEND_URL}/auth/me" , headers = headers)
   user_connected = current_user.json()
except:
   if current_user.status_code == 401:
      st.error("Vous devriez vous reconnecter svp")
      services.logout()

if "messages" not in st.session_state:
   st.session_state["messages"]=[]

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 300px !important;
        }
        div[data-testid="stSidebarContent"] {
            width: 300px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if "session_id" not in st.session_state:
     session_payload = {"statut_id" : 1}
     session_id = requests.post(f"{configs.BACKEND_URL}/sessions" , json = session_payload , headers = headers).json()
     st.session_state["session_id"] = session_id
     
with st.sidebar:
         with st.form("my_conversation_form" , border = False):
            if st.form_submit_button(label = "Nouvelle Conversation"):
               session_payload = {"statut_id" : 1}
               session_id = requests.post(f"{configs.BACKEND_URL}/sessions" , json = session_payload , headers = headers).json()
               st.session_state["session_id"] = session_id
               st.session_state.messages= []

         st.markdown("### _Historique des messages_")

         sessions  = []

         for session in user_connected["sessions"] :
           sessions.append({"session_id" : session["session_id"] , "messages" : session["messages"]})

         for session in sessions:
             if session["messages"] != []:
               message_split = session["messages"][0]["content"][0:29]+"......."
               if st.button(label = message_split, key = session["session_id"] ,use_container_width = True):
                  st.session_state.messages = session["messages"]
             
with st.container():
   col2 , col1 = st.columns([0.8,0.2])

   st.markdown(
            f"<div style='border-left: 2px solid gray; height: 100%; margin: auto;'></div>",
            unsafe_allow_html = True 
         )
   with col1 :
      deconnexion = st.button(label = "Deconnexion" , use_container_width = True)
      if deconnexion:
         services.logout()
    
   with col2:
      st.markdown("#### _Bievenu sur SmartBot le Chatbot de Smart Support_")
      chat_placeholder = st.container()
      with chat_placeholder:
         for msg in st.session_state["messages"]:
            st.chat_message(name = msg["role"] , 
                           avatar = ":material/account_circle:" if  msg["role"] == "user" else ":material/robot_2:").write(msg['content'])
              
      
      prompt = st.chat_input(placeholder = "Comment puis-je vous aidez ? ")
      if prompt:
         if "session_id" in st.session_state:
            with chat_placeholder:
               st.chat_message(name = "user" , avatar = ":material/account_circle:").write(prompt)
            user_message = {"session_id" : st.session_state["session_id"] , "role" : "user" , "content" : prompt}

            chatbot_response = requests.post(f"{configs.BACKEND_URL}/messages" , json = user_message ,headers = headers).json()
            
            with chat_placeholder:
               # st.chat_message(name = "user" , avatar = ":material/account_circle:").write(prompt)
               st.chat_message(name = "assistant" , avatar = ":material/robot_2:").write(chatbot_response)

            st.session_state["messages"].append({"role" : "user" , "content" : prompt})
            st.session_state["messages"].append({"role" : "assistant" , "content" : chatbot_response})

