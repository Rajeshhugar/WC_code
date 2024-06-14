import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import openpyxl

st.title("Word Cloud Generator")

st.caption("Keep the columns names as Entities and Count")

# Upload the Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Add sliders and other controls for customization
width = st.slider("Width", min_value=400, max_value=1600, value=800)
height = st.slider("Height", min_value=200, max_value=800, value=400)
background_color = st.color_picker("Background Color", value='#FFFFFF')
max_words = st.slider("Max Words", min_value=10, max_value=500, value=200)

# Function to generate word cloud
def generate_wordcloud(data, width, height, background_color, max_words):
    # Drop rows where 'Count' is NaN
    data.dropna(subset=["Count"], inplace=True)
    
    # Create a dictionary of word frequencies
    word_freq = dict(zip(data['Entities'], data['Count']))
    
    # Generate the word cloud
    wordcloud = WordCloud(width=width, height=height, background_color=background_color, max_words=max_words).generate_from_frequencies(word_freq)
    
    # Plot the word cloud
    plt.figure(figsize=(width / 100, height / 100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the word cloud image
    plt.savefig('wordcloud.png')
    return 'wordcloud.png'

# Display the word cloud if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the Excel file and get sheet names
        excel_data = pd.ExcelFile(uploaded_file)
        sheet_names = excel_data.sheet_names
        
        # Allow the user to select a sheet
        selected_sheet = st.selectbox("Select Sheet", sheet_names)
        
        # Read the selected sheet into a DataFrame
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # Check if the required columns are present
        if 'Entities' in df.columns and 'Count' in df.columns:
            # Generate and display the word cloud
            wordcloud_path = generate_wordcloud(df, width, height, background_color, max_words)
            st.image(wordcloud_path, caption="Generated Word Cloud")

            # Add a download button for the word cloud image
            with open(wordcloud_path, "rb") as file:
                btn = st.download_button(
                        label="Download image",
                        data=file,
                        file_name="wordcloud.png",
                        mime="image/png"
                    )
        else:
            st.error("Excel file must contain 'Entities' and 'Count' columns.")
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload an Excel file to generate the word cloud.")
