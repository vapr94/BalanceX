Here is the refactored and rewritten code:

```import streamlit as st

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
    len_start_str = len(start_string)
    matched_str = []
    for corpus_str in corpus:
        if not len(corpus_str) < len_start_str:
            if start_string == corpus_str[:len_start_str]:
                matched_str.append(corpus_str)
    return matched_str

def countParentheses(matched_str, start_string):
    pos = len(start_string)
   s
    count_open = 0
    count_close = 0
    for curr_str in matched_str:
        if len(curr_str) > pos:
            if curr_str[pos] == '(':
                count_open += 1
            if curr_str[pos] == ')':
                count_close += 1
    return count_open, count_close

def chooseProbability(temperature, count_open, count_close):
    from numpy.random import choice
    if count_open >= count_close:
        draw = choice([')', '('], 1, p=[temperature, 1 - temperature])
    else:
        draw = choice(['(', ')'], 1, p=[temperature, 1 - temperature])
    return draw

temperature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    total_length = total_length + 1

    for n in range(1, total_length):
        parentheses_string = ""
        if n % 2 == 0:
            generateParenthesis(n/2, n/2, parentheses_string, initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")

    matched_str = findMatchingStrings(start_string, initial_corpus)
    if len(matched_str) > 0:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
        count_open, count_close = countParentheses(match