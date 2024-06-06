import streamlit as st
import numpy as np

# st.set_page_config(page_title="My Page Title")
st.header("Balanced Parentheses Test")

def generate_parenthesis(left, right, parenthesis_string, output):
    if left == 0 and right == 0:
        output.append(parenthesis_string)
        return
    if left > right or left < 0 or right < 0:
        return
    generate_parenthesis(left - 1, right, parenthesis_string + '(', output)
    generate_parenthesis(left, right - 1, parenthesis_string + ')', output)

def find_string(start_string, corpus):
    len_start_str = len(start_string)
    return [corpus_str for corpus_str in corpus if corpus_str.startswith(start_string)]

def count_parentheses(matched_str, pos):
    count_open = sum(1 for s in matched_str if len(s) > pos and s[pos] == '(')
    count_close = sum(1 for s in matched_str if len(s) > pos and s[pos] == ')')
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
            generate_parenthesis(n // 2, n // 2, "", initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")
    matched_str = find_string(start_string, initial_corpus)
    if matched_str:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}**, count= **{len(matched_str)}**")
        count_open, count_close = count_parentheses(matched_str, len(start_string))
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        str_drawn = choose_parenthesis(temperature, count_open, count_close)
        while matched_str:
            st.write("---")
            st.markdown(f"Corpus= **{matched_str}**, count= **{len(matched_str)}**")
            st.markdown(f"Parentheses which has been chosen = **{str_drawn}**")
            start_string += str_drawn
            matched_str = find_string(start_string, matched_str)
            count_open, count_close = count_parentheses(matched_str, len(start_string))
            st.markdown(f"Open Parentheses Count= **{count_open}**, Close Parentheses Count=**{count_close}**")
            str_drawn = choose_parenthesis(temperature, count_open, count_close)

        st.write("Can't find any matching string")
    else:
        st.write("Can't find any matching string")