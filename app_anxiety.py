import streamlit as st
import pandas as pd
import hashlib
import io
import os
import pandas as pd

# Define Answer class
class Answer:
    def __init__(self, answer, comment):
        self.answer = answer
        self.comment = comment


# Define questions and answer options
questions = [
    "Numbness or tingling",
    "Feeling hot",
    "Wobbliness in legs",
    "Unable to relax",
    "Fear of worst happening",
    "Dizzy or lightheaded",
    "Heart pounding / racing",
    "Unsteady",
    "Terrified or afraid",
    "Nervous",
    "Feeling of choking",
    "Hands trembling",
    "Shaky / unsteady",
    "Fear of losing control",
    "Difficulty in breathing",
    "Fear of dying",
    "Scared",
    "Indigestion",
    "Faint / lightheaded",
    "Face flushed",
    "Hot / cold sweats",
]

answers = {
    "0": "Not at all",
    "1": "Mildly but it didn't bother me much",
    "2": "Moderately it wasn't pleasant at times",
    "3": "Severely it bothered me a lot",
}

# Function to save user answers to Excel file
def save_user_answers(user_info, answer_objects):
    # Add user info and question labels to headers
    data = {
        "Name": user_info[0],
        "Age": user_info[1],
        "Gender": user_info[2],
        **{f"Q{i+1} (Score)": "" for i in range(len(questions))},
        **{f"Q{i+1} (Comment)": "" for i in range(len(questions))},
    }

    # Update score and comment columns based on answer objects
    for i, answer_object in enumerate(answer_objects):
        data[f"Q{i+1} (Score)"] = int(answer_object.answer)
        data[f"Q{i+1} (Comment)"] = answer_object.comment

    df = pd.DataFrame(data, index=[0])
    if os.path.exists("anxiety_screening_data.csv"):
        df.to_csv("anxiety_screening_data.csv", mode="a", header=False, index=False)
    else:
        df.to_csv("anxiety_screening_data.csv", index=False)


    #df = pd.DataFrame(data, index=[0])
    # Load existing data (if any) and append new row
    #try:
    #    existing_data = pd.read_excel("anxiety_screening_data.xlsx")
    #    df = pd.concat([existing_data, df], ignore_index=True)
    #except FileNotFoundError:
    #    pass

    # Save data to Excel file
    #df.to_excel("anxiety_screening_data.xlsx", index=False)
    #df.to_csv("anxiety_screening_data.csv", index=False)

# Main app logic
st.set_page_config(page_title="Tristha Mental Health Clinic")
# Add clinic title and instructions
#st.title("Tristha Mental Health Clinic")
st.markdown("<h1 style='text-align: center;'>Tristha Mental Health Clinic</h1>", unsafe_allow_html=True)
instructions = "NOTE: Please answer the following 21 questions based on your experience.\nPlease use the following convention for options in answers :\n* 0: Not at all\n* 1: Mildly but it didn't bother me much\n* 2: Moderately it wasn't pleasant at times\n* 3: Severely it bothered me a lot"
st.markdown(instructions)



# Get user name, age, and gender
user_info = st.text_input("Name:", max_chars=50), st.number_input("Age:", min_value=1), st.selectbox("Gender:", ["Male", "Female", "Other"])

# Add comment boxes for each question and store answers in objects
answer_objects = []
for i, question in enumerate(questions):
    answer = st.selectbox(f"Question {i+1}: {question}", list(answers.values()))
    comment = st.text_input(f"Optional comment for Question {i+1}:")
    answer_objects.append(Answer(list(answers.keys())[list(answers.values()).index(answer)], comment))

# Submit button and score calculation
if st.button("Submit"):
    # Calculate score
    score = sum(int(answer_object.answer) for answer_object in answer_objects)

    # Display score and interpretation
    st.header(f"Your score is: {score}")
    st.markdown(f"Client **{user_info[0]}** is having:")
    if score <= 21:
        st.success("Low level of anxiety")
    elif score <= 35:
        st.warning("Moderate level of anxiety")
    else:
        st.error("Potentially concerning level of anxiety. Please seek professional help.")

    # Save user answers to Excel file
    save_user_answers(user_info, answer_objects)


# Show password input initially
password_input = st.text_input("For Admin Only :", type="password")

# Download button (shown only if password is correct)
if password_input == "SoumyaReadyToFly":
    try:
        #data = pd.read_csv("anxiety_screening_data.csv")  # Assuming CSV file
        # Option 1: Downloading directly from CSV file (if accessible)
        if os.path.exists("anxiety_screening_data.csv"):  # Check file existence
            with open("anxiety_screening_data.csv", "rb") as f:
                st.download_button(
                    "Download Anxiety Screening Data (CSV)",
                    f.read(),
                    file_name="anxiety_screening_data.csv",
                )
        else:
            st.error("Unable to find anxiety_screening_data.csv file!")

        # Option 2: Downloading from pandas DataFrame (alternative)
        # with io.StringIO() as tmp:
        #     data.to_csv(tmp, index=False)
        #     st.download_button(
        #         "Download Anxiety Screening Data (CSV)",
        #         tmp.getvalue(),
        #         file_name="anxiety_screening_data.csv",
        #     )

    except FileNotFoundError:
        st.error("Unable to find anxiety_screening_data.csv file!")
    except Exception as e:
        st.error(f"Error generating download data: {e}")

    