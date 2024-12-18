# -*- coding: utf-8 -*-
"""solid block.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ShFnJvrGKxuOoV3leGvotwMEf5rV3r-o
"""

pip install pandas numpy openpyxl

import pandas as pd

# Upload and read the Excel file
uploaded_file_path = "solid_block2.xlsx"  # Update this with your actual file path
inspection_data = pd.read_excel(uploaded_file_path, sheet_name="Solid Blocks")  # Reading inspection data
rules_data = pd.read_excel(uploaded_file_path, sheet_name="Rules")  # Reading rules

# Step 1: Create the dictionary from the Solid Blocks sheet
reference_dimensions = {}
for _, row in inspection_data.iterrows():
    block_type = row["Block Type Name"]
    reference_dimensions[block_type] = {
        "Length": row["Reference Length"],
        "Width": row["Reference Width"],
        "Height": row["Reference Height"]
    }

# Print the created reference_dimensions dictionary
print("Reference Dimensions Dictionary:")
print(reference_dimensions)

# Step 2: Add reference dimensions to the inspection data using the dictionary
inspection_data["Reference Length"] = inspection_data["Block Type Name"].map(
    lambda x: reference_dimensions.get(x, {}).get("Length", None)
)
inspection_data["Reference Width"] = inspection_data["Block Type Name"].map(
    lambda x: reference_dimensions.get(x, {}).get("Width", None)
)
inspection_data["Reference Height"] = inspection_data["Block Type Name"].map(
    lambda x: reference_dimensions.get(x, {}).get("Height", None)
)

# Step 3: Define tolerances from the rules (e.g., ±5 mm for Length, Width, Height)
length_tolerance = 5
width_tolerance = 5
height_tolerance = 5

# Step 4: Check if the inspected dimensions are within the tolerances
inspection_data["Length Status"] = inspection_data.apply(
    lambda row: "Pass" if abs(row["Actual Length"] - row["Reference Length"]) <= length_tolerance else "Fail", axis=1
)
inspection_data["Width Status"] = inspection_data.apply(
    lambda row: "Pass" if abs(row["Actual Width"] - row["Reference Width"]) <= width_tolerance else "Fail", axis=1
)
inspection_data["Height Status"] = inspection_data.apply(
    lambda row: "Pass" if abs(row["Actual Height"] - row["Reference Height"]) <= height_tolerance else "Fail", axis=1
)

# Step 5: Final material pass/fail based on all dimensions
inspection_data["Material Status"] = inspection_data.apply(
    lambda row: "Pass" if row["Length Status"] == "Pass" and row["Width Status"] == "Pass" and row["Height Status"] == "Pass" else "Fail", axis=1
)

# Display the final processed data
print("\nProcessed Inspection Data:")
print(inspection_data)

# Export the results to a new Excel file
output_file_path = "/path_to_save_processed_data.xlsx"  # Specify the output path
inspection_data.to_excel(output_file_path, index=False)
print(f"Processed data saved to {output_file_path}")

pip install openai

import openai
import pandas as pd

# Load processed data
inspection_data = pd.read_excel("solid_block2.xlsx")  # Replace with your actual file path

# Set OpenAI API Key
openai.api_key = "insert"  # Replace with your actual OpenAI API key

# Define a function to handle queries
def query_inspection_data(question):
    # Convert the inspection data to a string format for the model
    data_context = inspection_data.to_string(index=False)

    # Ensure that the query is asking for material pass/fail counts
    if "how many materials passed inspection" in question.lower():
        # Count the number of materials that passed inspection
        pass_count = inspection_data[inspection_data['Status'] == 'Pass'].shape[0]
        return f"Number of materials that passed inspection: {pass_count}"

    # If it's not a pass/fail query, continue with the normal chat functionality
    messages = [
        {"role": "system", "content": "You are an intelligent assistant analyzing material inspection data."},
        {"role": "user", "content": f"The data is as follows:\n{data_context}\n\nQuestion: {question}"}
    ]

    # Use OpenAI's ChatGPT model
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=messages,
        max_tokens=200,  # Limit response size
        temperature=0,   # Controls randomness (0 = deterministic)
    )

    # Extract and return the response
    return response.choices[0].message.content.strip()

# Example queries
#question = "How many materials passed inspection?"
#answer = query_inspection_data(question)
#print("Q:", question)
#print("A:", answer)

"""**UI Design**"""

!pip install streamlit
!pip install gradio

import streamlit as st
# Streamlit UI Setup
st.title("Material Inspection Data Query Assistant")
st.write("Ask a question about the material inspection data.")

# Input for user question
user_question = st.text_input("Enter your question:")

if user_question:
    # Get the answer to the user's question
    answer = query_inspection_data(user_question)

    # Display the result
    st.write(f"**Answer**: {answer}")