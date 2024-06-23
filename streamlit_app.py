import streamlit as st
import numpy as np

# st.set_page_config(page_title="My Page Title")
st.header("Balanced Parentheses Test")

def generate_parentheses(n, left, right, s, output):
    if left == n and right == n:
        output.append(s)
        return
    if left < n:
        generate_parentheses(n, left + 1, right, s + '(', output)
    if right < left:
        generate_parentheses(n, left, right + 1, s + ')', output)

def find_starting_with(start_string, corpus):
    return [s for s in corpus if s.startswith(start_string)]

def count_parentheses(strings, pos):
    count_open = sum(s[pos] == '(' for s in strings if len(s) > pos)
    count_close = sum(s[pos] == ')' for s in strings if len(s) > pos)
    return count_open, count_close

def choose_parenthesis(temperature, count_open, count_close):
    probabilities = [temperature, 1 - temperature] if count_open >= count_close else [1 - temperature, temperature]
    return np.random.choice([')', '('], p=probabilities)

temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    for n in range(1, total_length + 1):
        if n % 2 == 0:
            generate_parentheses(n // 2, 0, 0, '', initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")
    matched_str = find_starting_with(start_string, initial_corpus)
    
    if matched_str:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}**, count= **{len(matched_str)}**")
        count_open, count_close = count_parentheses(matched_str, len(start_string))
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        while matched_str:
            str_drawn = choose_parenthesis(temperature, count_open, count_close)
            start_string += str_drawn
            matched_str = find_starting_with(start_string, matched_str)
            count_open, count_close = count_parentheses(matched_str, len(start_string))
            st.markdown(f"Updated String= **{start_string}**, Open Count= **{count_open}**, Close Count=**{count_close}**")
            if not matched_str:
                st.write("Can't find any more matching strings.")
                break
    else:
        st.write("No matching strings found initially.")