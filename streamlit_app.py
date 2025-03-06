# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize Your Smoothie!!!!! :cup_with_straw:")
st.write(
    f"""Choose the fruits, the flavours, the essence you want in your very Smoothie!!!!
     """)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name_on_order)

cnx= st.connection ("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select (col( 'FRUIT_NAME' ))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
    'Chooes up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''
    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Button')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+ ' ' + name_on_order, icon="✅");
    
    #st.write(my_insert_stmt)
    #st.stop()

#sepsrate section to import smoothie nutiriton
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())



