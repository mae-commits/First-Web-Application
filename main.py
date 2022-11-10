import streamlit as st

import login

if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

if __name__ == "__main__":
    # ログイン認証に成功すれば処理切り替え
    if st.session_state['authentication_status']:
        # こにメインのアプリ機能を書く
        if st.button("ログアウト"):
            st.session_state['authentication_status'] = None
            st.experimental_rerun()
    else:
        login.Login("db/user.db")