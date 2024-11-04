# Import necessary packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose The Fruits You Want in Your Smoothie!")

Name_on_Order = st.text_input('Name On Smoothie')
st.write("The Name on Your Smoothie Will be: ", Name_on_Order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Ingredient selection
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Create a string from ingredients list

    for Fruit_Choosen in ingredients_list:
        # Make the API call
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        
        # Check if the response content type is JSON
        if fruityvice_response.headers.get("Content-Type") == "application/json":
            try:
                response_json = fruityvice_response.json()  # Parse JSON response
                fv_df = st.dataframe(data=response_json, use_container_width=True)
            except requests.exceptions.JSONDecodeError:
                st.error("Error parsing JSON. The response may not be in the correct format.")
        else:
            st.error("The server returned a non-JSON response. Please try again later.")

    # Prepare the SQL statement for inserting into the database
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, Name_on_Order)
        values ('{ingredients_string}', '{Name_on_Order}');
    """

    # Button to submit the order
    time_to_insert = st.button('Submit')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered! {Name_on_Order}', icon="✅")
