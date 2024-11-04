# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose The Fruits You Want in Your Smoothie!""")

Name_on_Order = st.text_input('Name On Smoothie')
st.write("The Name on Your Smoothie Will be : ", Name_on_Order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose Upto 5 ingredients:', my_dataframe, max_selections = 5)
if ingredients_list:
    ingredients_string = ''

    for Fruit_Choosen in ingredients_list:
        ingredients_string += Fruit_Choosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, Name_on_Order)
            values ('""" + ingredients_string + """','""" +Name_on_Order+ """');"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ! ' + Name_on_Order,icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data = fruityvice_response.json(), use_container_width = True)
