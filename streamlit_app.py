import streamlit as st
import numpy as np

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Balanced Parentheses Test")

# Display a header on the page
st.header("Balanced Parentheses Test")

def generate_parenthesis(left, right, parenthesis_string, output):
    """
    Recursively generate all combinations of balanced parentheses.
    
    Args:
    left (int): Number of left parentheses remaining to add.
    right (int): Number of right parentheses remaining to add.
    parenthesis_string (str): Current string of parentheses.
    output (list): List to collect all valid combinations.
    """
    if left == 0 and right == 0:
        output.append(parenthesis_string)
    if left > right or left < 0 or right < 0:
        return
    generate_parenthesis(left - 1, right, parenthesis_string + '(', output)
    generate_parenthesis(left, right - 1, parenthesis_string + ')', output)

def find_string(start_string, corpus):
    """
    Find all strings in the corpus that start with the given start_string.
    
    Args:
    start_string (str): The substring to match at the start.
    corpus (list): List of strings to search within.
    
    Returns:
    list: A list of strings from the corpus that start with start_string.
    """
    len_start_str = len(start_string)
    matched_str = [corpus_str for corpus_str in corpus if corpus_str.startswith(start_string)]
    return matched_str

def count_parentheses(matched_str, start_string):
    """
    Count the occurrences of '(' and ')' in the matched strings after the length of start_string.
    
    Args:
    matched_str (list): List of strings that matched the start_string.
    start_string (str): The substring used for matching.
    
    Returns:
    tuple: A tuple containing counts of '(' and ')' respectively.
    """
    pos = len(start_string)
    count_open = sum(1 for s in matched_str if len(s) > pos and s[pos] == '(')
    count_close = sum(1 for s in matched_str if len(s) > pos and s[pos] == ')')
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    """
    Randomly choose between '(' and ')' based on the counts and a temperature parameter.
    
    Args:
    temperature (float): Probability factor influencing randomness.
    count_open (int): Count of '(' found.
    count_close (int): Count of ')' found.
    
    Returns:
    str: The chosen parenthesis.
    """
    if count_open >= count_close:
        draw = np.random.choice([')', '('], 1, p=[temperature, 1 - temperature])
    else:
        draw = np.random.choice(['(', ')'], 1, p=[temperature, 1 - temperature])
    return draw[0]

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
    
    matched_str = find_string(start_string, initial_corpus)
    if matched_str:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}**, count= **{len(matched_str)}**")
        count_open, count_close = count_parentheses(matched_str, start_string)
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")
        
        while matched_str:
            chosen_parenthesis = choose_parenthesis(temperature, count_open, count_close)
            start_string += chosen_parenthesis
            matched_str = find_string(start_string, matched_str)
            count_open, count_close = count_parentheses(matched_str, start_string)
            st.markdown(f"Updated String= **{start_string}**, Remaining Matches= **{len(matched_str)}**")
    else:
        st.write("No matching strings found.")