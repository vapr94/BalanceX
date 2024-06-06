import streamlit as st
import numpy as np

# Set the page configuration
st.set_page_config(page_title="Balanced Parentheses Test")

st.header("Balanced Parentheses Test")

def generate_parentheses(left, right, parentheses_string, output):
    if left == 0 and right == 0:
        output.append(parentheses_string)
    if left > right or left < 0 or right < 0:
        return
    generate_parentheses(left - 1, right, parentheses_string + '(', output)
    generate_parentheses(left, right - 1, parentheses_string + ')', output)

def find_string(start_string, corpus):
    len_start_str = len(start_string)
    return [corpus_str for corpus_str in corpus if corpus_str.startswith(start_string)]

def count_parentheses(matched_str, pos):
    count_open = sum(1 for s in matched_str if s[pos] == '(')
    count_close = sum(1 for s in matched_str if s[pos] == ')')
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    choices = ['(', ')']
    probabilities = [temperature, 1 - temperature] if count_open >= count_close else [1 - temperature, temperature]
    return np.random.choice(choices, p=probabilities)

temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    for n in range(1, total_length + 1):
        if n % 2 == 0:
            generate_parentheses(n // 2, n // 2, "", initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")
    matched_str = find_string(start_string, initial_corpus)

    if matched_str:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
        pos = len(start_string)
        count_open, count_close = count_parentheses(matched_str, pos)
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        while matched_str:
            str_drawn = choose_parenthesis(temperature, count_open, count_close)
            st.markdown(f"Chosen Parenthesis = **{str_drawn}**")
            start_string += str_drawn
            matched_str = find_string(start_string, matched_str)
            count_open, count_close = count_parentheses(matched_str, pos)
            st.markdown(f"Updated Open Parentheses Count= **{count_open}** , Close Parentheses Count=**{count_close}**")

        st.write("No more matching strings found.")
    else:
        st.write("No matching strings found.")