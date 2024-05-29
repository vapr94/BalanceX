import streamlit as st

# Function to generate all possible balanced parentheses combinations
def generateParenthesis(left, right, parentheses_string, output):
    """
    Generate all possible balanced parentheses combinations.

    Parameters:
    left (int): Number of left parentheses remaining.
    right (int): Number of right parentheses remaining.
    parentheses_string (str): Current parentheses string being built.
    output (list): List to store the generated combinations.

    Returns:
    None
    """
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

# Function to find strings in corpus that start with a given substring
def find_string(start_string, corpus):
    """
    Find strings in corpus that start with a given substring.

    Parameters:
    start_string (str): Substring to start with.
    corpus (list): List of strings to search within.

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

# Function to count the number of open and closed parentheses in matched strings
def count_parentheses(matched_str, start_string):
    """
    Count the number of open and closed parentheses in matched strings.

    Parameters:
    matched_str (list): List of matched strings.
    start_string (str): Substring to start with.

    Returns:
    tuple: Number of open and closed parentheses.
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

# Function to choose a parentheses based on temperature probability
def choose_prob(temperature, count_open, count_close):
    """
    Choose a parentheses based on temperature probability.

    Parameters:
    temperature (float): Probability value between 0.0 and 1.0.
    count_open (int): Number of open parentheses.
    count_close (int): Number of closed parentheses.

    Returns:
    str: Chosen parentheses.
    """
    from numpy.random import choice
    if count_open >= count_close:
        draw = choice([')', '('], 1, p=[temperature, 1 - temperature])
    else:
        draw = choice(['(', ')'], 1, p=[temperature, 1 - temperature])
    return draw

# Streamlit interface
st.header("Balanced Parentheses Test")

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

    matched_str = find_string(start_string, initial_corpus)

    if len(matched_str) > 0:
        st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
        count_open, count_close = count_parentheses(matched_str, start_string)
        st.markdown(f"Open Parentheses Count=**{count_open}**, Close Parentheses Count=**{count_close}**")

        str_drawn = choose_prob(temperature, count_open, count_close)

        while len(matched_str) > 0:
            st.write("---")
            corpus = matched_str.copy()
            st.markdown(f"Corpus= **{corpus}**, count= **{len(matched_str)}**")
            st.markdown(f"Parantheses which has been chosen = **{str_drawn[0]}**")
            start_string = start_string + str_drawn[0]
            matched_str = find_string(start_string, corpus)
            count_open, count_close = count_parentheses(matched_str, start_string)
            st.markdown(f"Open Parentheses Count= **{count_open}** , Close Parentheses Count=**{count_close}**")
            str_drawn = choose_prob(temperature, count_open, count_close)

        st.write("Can't find any matching string")

    else:
        st.write("Can't find any matching string")