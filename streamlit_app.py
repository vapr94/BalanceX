import streamlit as st
import numpy as np

# Set the page configuration
st.set_page_config(page_title="Balanced Parentheses Test")

# Display a header on the page
st.header("Balanced Parentheses Test")

def generate_parentheses(left, right, current_string, results):
    """
    Recursively generate all combinations of well-formed parentheses.
    """
    if left == 0 and right == 0:
        results.append(current_string)
        return
    if left > right or left < 0 or right < 0:
        return
    generate_parentheses(left - 1, right, current_string + '(', results)
    generate_parentheses(left, right - 1, current_string + ')', results)

def find_matching_strings(prefix, corpus):
    """
    Find all strings in the corpus that start with the given prefix.
    """
    return [s for s in corpus if s.startswith(prefix)]

def count_parentheses(strings, position):
    """
    Count the number of open and close parentheses at a specific position in the strings.
    """
    count_open = sum(s[position] == '(' for s in strings if len(s) > position)
    count_close = sum(s[position] == ')' for s in strings if len(s) > position)
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    """
    Choose a parenthesis based on the given temperature and counts of open and close parentheses.
    """
    choices = ['(', ')']
    probabilities = [temperature, 1 - temperature] if count_open >= count_close else [1 - temperature, temperature]
    return np.random.choice(choices, p=probabilities)

# User inputs
temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    for n in range(1, total_length + 1):
        if n % 2 == 0:
            generate_parentheses(n // 2, n // 2, "", initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")
    matched_strings = find_matching_strings(start_string, initial_corpus)
    
    if matched_strings:
        st.markdown(f"Matched Strings from Corpus = **{matched_strings}**, count= **{len(matched_strings)}**")
        count_open, count_close = count_parentheses(matched_strings, len(start_string))
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")
        
        while matched_strings:
            chosen_parenthesis = choose_parenthesis(temperature, count_open, count_close)
            start_string += chosen_parenthesis
            matched_strings = find_matching_strings(start_string, matched_strings)
            count_open, count_close = count_parentheses(matched_strings, len(start_string))
            st.markdown(f"Chosen Parenthesis = **{chosen_parenthesis}**")
            st.markdown(f"Updated String = **{start_string}**")
            st.markdown(f"Open Parentheses Count= **{count_open}**, Close Parentheses Count=**{count_close}**")
    else:
        st.write("No matching strings found.")