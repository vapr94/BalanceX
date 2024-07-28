import streamlit as st
import numpy as np

st.header("Balanced Parentheses Test")

def generateParenthesis(left, right, parentheses_string, output):
    if left == 0 and right == 0:
        output.append(parentheses_string)
    if left > right or left < 0 or right < 0:
        return
    parentheses_string += '('
    generateParenthesis(left - 1, right, parentheses_string, output)
    parentheses_string = parentheses_string[:-1]
    parentheses_string += ')'
    generateParenthesis(left, right - 1, parentheses_string, output)
    parentheses_string = parentheses_string[:-1]

def findMatchingStrings(start_string, corpus):
    matched_strings = [corpus_str for corpus_str in corpus if len(corpus_str) >= len(start_string) and start_string == corpus_str[:len(start_string)]]
    return matched_strings

def countParentheses(matched_strings, start_string):
    pos = len(start_string)
    count_open = sum(1 for curr_str in matched_strings if len(curr_str) > pos and curr_str[pos] == '(')
    count_close = sum(1 for curr_str in matched_strings if len(curr_str) > pos and curr_str[pos] == ')')
    return count_open, count_close

def chooseParentheses(temperature, count_open, count_close):
    if count_open >= count_close:
        draw = np.random.choice([')', '('], 1, p=[temperature, 1 - temperature])
    else:
        draw = np.random.choice(['(', ')'], 1, p=[temperature, 1 - temperature])
    return draw

temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    total_length += 1

    for n in range(1, total_length):
        parentheses_string = ""
        if n % 2 == 0:
            generateParenthesis(n // 2, n // 2, parentheses_string, initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")

    matched_strings = findMatchingStrings(start_string, initial_corpus)
    if len(matched_strings) > 0:
        st.markdown(f"Matched Strings from Corpus = **{matched_strings}** , count= **{len(matched_strings)}**")
        count_open, count_close = countParentheses(matched_strings, start_string)
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        str_drawn = chooseParentheses(temperature, count_open, count_close)
        while len(matched_strings) > 0:
            st.write("---")
            corpus = matched_strings.copy()
            st.markdown(f"Corpus= **{corpus}**, count= **{len(matched_strings)}**")
            st.markdown(f"Parantheses which has been chosen = **{str_drawn[0]}**")
            start_string += str_drawn[0]
            matched_strings = findMatchingStrings(start_string, corpus)
            count_open, count_close = countParentheses(matched_strings, start_string)
            st.markdown(f"Open Parentheses Count= **{count_open}**, Close Parentheses Count=**{count_close}**")
            str_drawn = chooseParentheses(temperature, count_open, count_close)

        st.write("Can't find any matching string")

    else:
        st.write("Can't find any matching string")