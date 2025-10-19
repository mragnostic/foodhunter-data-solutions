import streamlit as st
import MySQLdb
import pandas
def dashboards():
    st.write('Visuals are yet to come!')
def QnA():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(
            f"""
            <div 
            style='text-align: right; padding:10px; font-size:18px; 
            border-radius:8px; margin:5px 0; display:inline-block; float:right; clear:both;
            background-color: #000000;'>
            {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
            )
        else:
            st.markdown(f"""<div style = 'padding:10px; border-radius:10px; margin:5px 0; background-color : #000000; display:inline-block;'>{msg["content"]}</div>""", unsafe_allow_html= True)
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = f"You said: {user_input}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def main():
    section = st.sidebar.selectbox(
        "Select Section", ('Dashboard', 'QnA')
    )
    if section == 'Dashboard':
        st.markdown("""
        <style>
        .custom-title{
            font-size: 35px;
            color: gray;
            font-weight: bold;
        }
        </style>
       <div class = "custom-title"> Foodhunter Dashboard </div>""", unsafe_allow_html=True)
        with st.sidebar.container(border=True):
            dbms = st.selectbox( "Select DBMS", ('MySQL', 'PostgreSQL', 'MSSQLServer'))
            host = st.text_input('Enter Host : ')
            user = st.text_input('Enter User : ')
            password = st.text_input('Enter Password : ', type = 'password')
        if dbms == 'MySQL':
            try:
                conn =  MySQLdb.connect(host = host, user = user, password = password)
                st.sidebar.success("Connected successfully!")
                tab1, tab2 = st.tabs(['View Tables', 'Visuals'])
                cursor = conn.cursor()
                with tab1:
                    cursor.execute('SHOW DATABASES;')
                    databases = [row[0] for row in cursor.fetchall()]
                    col1, col2 = st.columns(2)
                    with st.container(border=True):
                        with col1:
                            database = st.selectbox('Select Database', databases)
                            cursor.execute(f'USE {database};')
                            cursor.execute(f'SHOW TABLES;')
                            tables = [row[0] for row in cursor.fetchall()]
                        with col2:
                            table = st.selectbox('Select Table', tables)
                            cursor.execute(f"SELECT * FROM `{database}`.`{table}`;")
                            records = cursor.fetchall()
                            columns = [desc[0] for desc in cursor.description]
                        st.dataframe(pandas.DataFrame(records, columns= columns), height = 500, hide_index = True)
                with tab2:
                    dashboards()
                cursor.close()
                conn.close()
            except MySQLdb.Error as err:
                st.sidebar.error(f"Failed to connect to MySQL: {err}")
                return
        else:
            st.sidebar.warning("Hey :wave: , MySQL is required to access the data for the Foodhunter analysis.")
    if section == "QnA":
        st.markdown("""
        <style>
        .custom-title{
            font-size: 35px;
            color: gray;
            font-weight: bold;
        }
        </style>
       <div class = "custom-title"> QnA (Ask with AI) </div>""", unsafe_allow_html=True)
        QnA()
if __name__ == '__main__':
    st.set_page_config(page_title = "Foodhunter dashboard", page_icon = ':chart:', layout = "wide", initial_sidebar_state = "expanded", menu_items = None)
    main()
