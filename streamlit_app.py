import streamlit as st
from numpy.random import choice

# Set the page configuration
st.set_page_config(page_title="Balanced Parentheses Test")

# Display a header on the page
st.header("Balanced Parentheses Test")

def generate_parentheses(left, right, parentheses_string, output):
    """
    Recursively generate all combinations of balanced parentheses.
    """
    if left == 0 and right == 0:
        output.append(parentheses_string)
        return
    if left > right or left < 0 or right < 0:
        return
    generate_parentheses(left - 1, right, parentheses_string + '(', output)
    generate_parentheses(left, right - 1, parentheses_string + ')', output)

def find_starting_with(start_string, corpus):
    """
    Find all strings in corpus that start with the given start_string.
    """
    return [s for s in corpus if s.startswith(start_string)]

def count_parentheses(strings, position):
    """
    Count the number of '(' and ')' at the specified position in each string.
    """
    count_open = sum(s[position] == '(' for s in strings if len(s) > position)
    count_close = sum(s[position] == ')' for s in strings if len(s) > position)
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    """
    Choose between '(' and ')' based on the counts and a temperature parameter.
    """
    probabilities = [temperature, 1 - temperature] if count_open >= count_close else [1 - temperature, temperature]
    return choice([')', '('], 1, p=probabilities)

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

    matched_strings = find_starting_with(start_string, initial_corpus)
    if matched_strings:
        st.markdown(f"Matched Strings from Corpus = **{matched_strings}**, count= **{len(matched_strings)}**")
        count_open, count_close = count_parentheses(matched_strings, len(start_string))
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        while matched_strings:
            str_drawn = choose_parenthesis(temperature, count_open, count_close)
            start_string += str_drawn[0]
            matched_strings = find_starting_with(start_string, matched_strings)
            count_open, count_close = count_parentheses(matched_strings, len(start_string))
            st.markdown(f"Updated String= **{start_string}**, Open Count= **{count_open}**, Close Count=**{count_close}**")
        st.write("Can't find any more matching strings.")
    else:
        st.write("No matching strings found.")