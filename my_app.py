import streamlit as st
import pandas as pd

st.write("""#My first app!
Hello *world!*""")
df = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 30]})
st.line_chart(df)
