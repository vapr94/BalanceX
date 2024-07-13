Here is the revised and documented version of the given code. I have added comments and docstrings to each function to explain their purpose and usage. Additionally, I have cleaned up redundant imports and streamlined the code for better readability.

```python
import streamlit as st
from numpy.random import choice

# Set up the page configuration and title
st.set_page_config(page_title="Balanced Parentheses Test")
st.header("Balanced Parentheses Test")

def generate_parenthesis(left, right, parenthesis_string, output):
    """
    Recursively generate all combinations of balanced parentheses.
    
    Args:
    left (int): Number of left parentheses remaining to be added.
    right (int): Number of right parentheses remaining to be added.
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
    start_string (str): The substring to match at the start of strings in the corpus.
    corpus (list): List of strings to search within.
    
    Returns:
    list: A list of strings from the corpus that start with start_string.
    """
    len_start_str = len(start_string)
    matched_str = [corpus_str for corpus_str in corpus if corpus_str.startswith(start_string)]
    return matched_str

def count_parentheses(matched_str, start_string):
    """
    Count the number of open and close parentheses immediately following the start_string in matched_str.
    
    Args:
    matched_str (list): List of strings that matched the start_string.
    start_string (str): The substring used for initial matching.
    
    Returns:
    tuple: A tuple containing counts of open and close parentheses.
    """
    pos = len(start_string)
    count_open = sum(1 for s in matched_str if len(s) > pos and s[pos] == '(')
    count_close = sum(1 for s in matched_str if len(s) > pos and s[pos] == ')')
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    """
    Randomly choose a parenthesis based on the counts and a temperature parameter.
    
    Args:
    temperature (float): Probability modifier that affects randomness.
    count_open (int): Count of open parentheses.
    count_close (int): Count of close parentheses.
    
    Returns:
    str: A randomly chosen parenthesis.
    """
    if count_open >= count_close:
        draw = choice([')', '('], 1, p=[temperature, 1 - temperature])
    else:
        draw = choice(['(', ')'], 1, p=[temperature, 1 - temperature])
    return draw

# Streamlit UI input elements
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
        st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
        count_open, count_close = count_parentheses(matched_str, start_string)
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")
        
        while matched_str:
            str_drawn = choose_parenthesis(temperature, count_open, count_close)
            start_string += str_drawn[0]
            matched_str = find_string(start_string, matched_str)
            count_open, count_close = count_parentheses(matched_str, start_string)
            st.markdown(f"Updated String= **{start_string}**, Open Count= **{count_open}**, Close Count= **{count_close}**")
    else:
        st.write("No matching strings found.")
```

This revised code is more organized and should be easier to understand and maintain. Each function now has a clear purpose and documentation, and the Streamlit interface is cleanly integrated with the logic.