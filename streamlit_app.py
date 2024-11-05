# Import necessary packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose The Fruits You Want in Your Smoothie!")

# Take user's name for the order
Name_on_Order = st.text_input('Name On Smoothie')
st.write("The Name on Your Smoothie Will be: ", Name_on_Order)

# Connect to Snowflake to retrieve fruit options
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data = my_dataframe, use_container_width = True)
#st.stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Create a string from ingredients list

    for Fruit_Choosen in ingredients_list:
        # Use Tropical Fruit and Veg API to get information on the selected fruit
        response = requests.get(f"https://tropicalfruitandveg.com/api/tfvjsonapi.php?tfvitem={Fruit_Choosen.lower()}")
        
        # Check if the response is JSON and display the data
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/json":
            try:
                fruit_data = response.json()  # Parse JSON response
                st.write(f"Information for {Fruit_Choosen}:")
                st.json(fruit_data)  # Display the JSON data as is
            except requests.exceptions.JSONDecodeError:
                st.error("Error parsing JSON. The response may not be in the correct format.")
        else:
            st.error(f"Could not retrieve data for {Fruit_Choosen}.")

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
