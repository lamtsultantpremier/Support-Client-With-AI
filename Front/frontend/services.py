import streamlit as st
import requests
import time

if "token" not in st.session_state:
    st.session_state["token"] = None

def is_authenticated():
    return st.session_state["token"] is not None

def login():
    
    st.markdown("##### Connexion")
    with st.form("my_form"):
        username = st.text_input(label = "Username")
        password = st.text_input(label = "Password" , type = "password")

        submit = st.form_submit_button("Se connecter")
        if submit:
            # verifier le username et le mot de pass

            login_url = "http://127.0.0.1:8000/auth/login"

            data = {
                "username" : username,
                "password" :password
            }
            try : 
                response = requests.post(login_url , data = data)

                if response.status_code == 200:
                    token_data = response.json()
                    token = token_data["access_token"]
                    st.session_state["token"] = token
                    with st.status("Veuillez patientientez un momment"):
                        time.sleep(2)
                    st.success(body = "Connexion reuissi" , icon = ":material/check:")

                    st.rerun()
                else :
                    st.error(body = "Identifiant invalid" , icon = ":material/error:")
            except Exception as e: 
                st.error(e)

    
def logout():
        st.session_state["token"] = None
        with st.status("Veuillez patientez un moment"):
             time.sleep(1)
        st.success(body = "Deconnexion réuissi" , icon = ":material/check:")
        st.rerun()

def register():
    pass

