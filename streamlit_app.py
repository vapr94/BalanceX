import streamlit as st

st.header("Balanced Parantheses Test")

def generateParenthesis(left, right, parantheses_string, output):
    """
    Generate all valid combinations of parentheses using backtracking.

    Parameters:
    left (int): Number of left parentheses remaining.
    right (int): Number of right parentheses remaining.
    parantheses_string (str): Current string of parentheses.
    output (list): List to store valid combinations.

    Returns:
    None
    """
    if left == 0 and right == 0:
        output.append(parantheses_string)
    if left > right or left < 0 or right < 0:
        return
    parantheses_string += '('
    generateParenthesis(left - 1, right, parantheses_string, output)
    parantheses_string = parantheses_string[:-1]
    parantheses_string += ')'
    generateParenthesis(left, right - 1, parantheses_string, output)
    parantheses_string = parantheses_string[:-1]

def fn_find_string(start_string, corpus):
    """
    Find strings in the corpus that start with the given substring.

    Parameters:
    start_string (str): Substring to start with.
    corpus (list): List of strings to search.

    Returns:
    list: List of matched strings.
    """
    len_start_str = len(start_string)
    matched_str = []
    for corpus_str in corpus:
        if not len(corpus_str) < len_start_str:
            if start_string == corpus_str[:len_start_str]:
                matched_str.append(corpus_str)
    return matched_str

def fn_count_parantheses(matched_str, start_string):
    """
    Count the number of open and close parentheses in matched strings.

    Parameters:
    matched_str (list): List of matched strings.
    start_string (str): Substring to start with.

    Returns:
    tuple: Count of open and close parentheses.
    """
    pos = len(start_string)
    count_open = 0
    count_close = 0
    for curr_str in matched_str:
        if len(curr_str) > pos:
            if curr_str[pos] == '(':
                count_open += 1
            if curr_str[pos] == ')':
                count_close += 1
    return count_open, count_close

def fn_choose_prob(temprature, count_open, count_close):
    """
    Choose a parenthesis based on temperature probability.

    Parameters:
    temprature (float): Probability value between 0.0 and 1.0.
    count_open (int): Count of open parentheses.
    count_close (int): Count of close parentheses.

    Returns:
    str: Chosen parenthesis.
    """
    from numpy.random import choice
    if count_open >= count_close:
        draw = choice([')', '('], 1, p=[temprature, 1 - temprature])
    else:
        draw = choice(['(', ')'], 1, p=[temprature, 1 - temprature])
    return draw

temprature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)

if st.button('Submit'):
    initial_corpus = []
    total_length = total_length + 1

    for n in range(1, total_length):
        parantheses_string = ""
        if n % 2 == 0:
            generateParenthesis(n/2, n/2, parantheses_string, initial_corpus)

    st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")

    matched_str = fn_find_string(start_string, initial_corpus)
    if len(matched_str) > 0:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
        count_open, count_close = fn_count_parantheses(matched_str, start_string)
        st.markdown(f"Open Parantheses Count=**{count_open}**, Close Paranthese Count=**{count_close}**")

        str_drawn = fn_choose_prob(temprature, count_open, count_close)
        while len(matched_str) > 0:
            st.write("---")
            corpus = matched_str.copy()
            st.markdown(f"Corpus= **{corpus}**, count= **{len(matched_str)}**")
            st.markdown(f"Parantheses which has been choosen = **{str_drawn[0]}**")
            start_string = start_string + str_drawn[0]
            matched_str = fn_find_string(start_string, corpus)
            count_open, count_close = fn_count_parantheses(matched_str, start_string)
            st.markdown(f"Open Parantheses Count= **{count_open}** , Close Paranthese Count=**{count_close}**")
            str_drawn = fn_choose_prob(temprature, count_open, count_close)

        st.write("Can't find any matching string")

    else:
        st.write("Can't find any matching string")