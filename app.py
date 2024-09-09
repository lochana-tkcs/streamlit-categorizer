import streamlit as st
import openai
import pandas as pd

# Set your OpenAI API key
openai.api_key = "sk-RFaIBKAoluVwK0GzBKLGL8ITWZjCgQS_0YdB0v0CdpT3BlbkFJOkPsTB2K_HW5OqCs0ciJKARnJ-ZEGNj7UtxcW37VwA"

# Inject custom CSS to handle overflow content
st.markdown(
    """
    <style>
    .wrap-text {
        word-wrap: break-word;
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to identify column categories
def identify_column_categories(df, prompt_template):
    num_rows = min(len(df), 20)
    prompt = prompt_template + "\nDataset:\n"

    for col in df.columns:
        prompt += f"\nColumn: {col}\n"
        prompt += "Values:\n" + ", ".join(df[col].head(num_rows).astype(str).tolist()) + "\n"

    prompt += "\nFor each column, provide the column name and the category it falls into."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0
    )

    categories = response['choices'][0]['message']['content'].strip()
    return categories

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Define prompt templates
    prompt_template_1 = """
    I have a dataset with the following columns and some rows of values. 
    Please categorize each column into different categories

    Dataset:
    """

    prompt_template_2 = """
    I have a dataset with several columns, and I need you to categorize each column based on the type of data it contains. 
    The categories you should use are:

    - Email
    - Primary Key/Identifier
    - Phone number
    - Geographical Data (e.g., address, city, country)
    - Date/Time
    - Categorical/Type (e.g., labels or codes representing categories)
    - Person/Name
    - Department
    - Brand
    - Organisation
    - Product/Service Category
    - Product/Service Description
    - Items (e.g., product lists, inventory)
    - Boolean (e.g., true/false, yes/no)
    - URLs
    - IP Address
    - Gender
    - Numerical
    - Latitude/Longitude
    - Zipcode
    - Quantity/Counts (like number_of_items, number_of_visits etc)
    - Amount (such as total_cost, price, transaction_amount, salary, annual_income etc)
    - Age/Years (years_experience etc)
    - Measurements (like height, weight, temperature etc)

    Please analyze the values in each text-based column and categorize them into the most appropriate category from the list. Ensure the category matches the patterns and nature of the data in each column.

    Here is the dataset with some sample rows of values:
    """

    # Process the dataframe through two prompts
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Prompt 1 - Categories")
        categories_1 = identify_column_categories(df, prompt_template_1)
        st.markdown(f"<div class='wrap-text'>{categories_1}</div>", unsafe_allow_html=True)

    with col2:
        st.write("### Prompt 2 - Categories")
        categories_2 = identify_column_categories(df, prompt_template_2)
        st.markdown(f"<div class='wrap-text'>{categories_2}</div>", unsafe_allow_html=True)
