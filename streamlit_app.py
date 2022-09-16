
import streamlit
import pandas
import requests
from urllib.error import URLError


streamlit.title('My Parents new Healthy diner')

streamlit.header('Breakfast Favourites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



#create the repeatable code called function 

def get_fruity_advice(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice )
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized;



streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_frunction = get_fruity_advice(fruit_choice)
    streamlit.dataframe(back_from_frunction)
except URlError as e:
  streamlit.error()
streamlit.write('The user entered ', fruit_choice)

#streamlit.stop()

import snowflake.connector
#my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit') ")

streamlit.header("View our Fruit List - Add Your Favourites")
#Snowflake-related functions
def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()
    
#Add a button to load fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_list()
    my_cnx.close()
    streamlit.dataframe(my_data_row)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into FRUIT_LOAD_LIST values ('" + new_fruit + "') ")
        return "Thanks for adding "+ new_fruit
 
add_my_fruit = streamlit.text_input('What fruit would you like to add ?')
if streamlit.button('Add Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

