import streamlit as st
import numpy as np

# Set the page configuration
st.set_page_config(page_title="Balanced Parentheses Test")

st.header("Balanced Parentheses Test")

def generate_parenthesis(left, right, parenthesis_string, output):
    """
    Recursively generate all combinations of balanced parentheses.
    """
    if left == 0 and right == 0:
        output.append(parenthesis_string)
        return
    if left > 0:
        generate_parenthesis(left - 1, right, parenthesis_string + '(', output)
    if right > left:
        generate_parenthesis(left, right - 1, parenthesis_string + ')', output)

def find_starting_string_matches(start_string, corpus):
    """
    Find all strings in the corpus that start with the given start_string.
    """
    return [s for s in corpus if s.startswith(start_string)]

def count_parentheses(matched_strings, position):
    """
    Count the number of open and close parentheses at a specific position in matched strings.
    """
    count_open = sum(1 for s in matched_strings if len(s) > position and s[position] == '(')
    count_close = sum(1 for s in matched_strings if len(s) > position and s[position] == ')')
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    """
    Choose a parenthesis based on the given temperature and counts of open and close parentheses.
    """
    choices = ['(', ')']
    probabilities = [1 - temperature, temperature] if count_open >= count_close else [temperature, 1 - temperature]
    return np.random.choice(choices, p=probabilities)

# User inputs
temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    for n in range(1, total_length + 1):
        if n % 2 == 0:
            generate_parenthesis(n // 2, n // 2, "", initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")

    matched_strings = find_starting_string_matches(start_string, initial_corpus)
    if matched_strings:
        st.markdown(f"Matched Strings from Corpus = **{matched_strings}** , count= **{len(matched_strings)}**")
        count_open, count_close = count_parentheses(matched_strings, len(start_string))
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        while matched_strings:
            chosen_parenthesis = choose_parenthesis(temperature, count_open, count_close)
            start_string += chosen_parenthesis
            matched_strings = find_starting_string_matches(start_string, matched_strings)
            count_open, count_close = count_parentheses(matched_strings, len(start_string))
            st.markdown(f"Updated String= **{start_string}**, Open Count= **{count_open}**, Close Count= **{count_close}**")
    else:
        st.write("No matching strings found.")