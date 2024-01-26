

import streamlit as st
import streamlit as st

# st.set_page_config(
#         page_title="My Page Title",
# )
st.header("Balanced Parantheses Test")



def generateParenthesis(left, right, parantheses_string, output):
	if left == 0 and right == 0:
		output.append(parantheses_string)
	if left > right or left < 0 or right < 0:
		# wrong
		return
	parantheses_string += '('
	generateParenthesis(left - 1, right, parantheses_string, output)
	parantheses_string = parantheses_string[:-1]
	parantheses_string += ')'
	generateParenthesis(left, right - 1, parantheses_string, output)
	parantheses_string = parantheses_string[:-1]


def fn_find_string(start_string,corpus):
  len_start_str=len(start_string)
  matched_str=[]
  # print("Corpus",corpus)
  for corpus_str in corpus:
    # print(f"corpus str={corpus_str}")
    # print("*"*80)
    if not len(corpus_str)<len_start_str:
      if start_string==corpus_str[:len_start_str]:
        matched_str.append(corpus_str)

  # print(f"Length Matched Strings={len(matched_str)}")
  # print(f"Matched String={matched_str}")
    
  return matched_str


def fn_count_parantheses(matched_str,start_string):
  pos=len(start_string)
  count_open=0
  count_close=0
  for curr_str in matched_str:
    if len(curr_str)>pos:
      if curr_str[pos]=='(':
        # print("Matched with (",curr_str)
        count_open+=1
      if curr_str[pos]==')':
        # print("Matched with )",curr_str)
        count_close+=1

  return count_open,count_close

def fn_choose_prob(temprature,count_open,count_close):
  #randomly choose with probability
  #Higher temperatures result in more diverse and unpredictable output
  from numpy.random import choice
  if count_open>=count_close:
    draw = choice([')','('], 1,
              p=[temprature,1-temprature])

  else:
    draw = choice(['(',')'], 1,
              p=[temprature,1-temprature])
  return draw




temprature = st.number_input("Enter the temperature as a probability value (between 0.0 and 1.0):", value=0.5, step=0.1, min_value=0.0, max_value=1.0)
start_string = st.text_input("Enter the substring to start with:", "")
total_length = st.number_input("Enter the length of the corpus as an integer:", value=8, step=1)


# start_string='(('
# Higher temperatures result in more diverse and unpredictable output
# temprature=0.8
if st.button('Submit'):

# total_length = 6
  initial_corpus = []

  print("total_length",total_length)
  # st.write("Corpus Length=",total_length)
  total_length=total_length +1

  for n in range(1,total_length):
    parantheses_string = ""
    # print("n",n)
    if n%2==0:
      generateParenthesis(n/2, n/2, parantheses_string, initial_corpus)
  # Now, here we print out all the combinations.
  print(f"Initial Corpus={initial_corpus}")
  st.markdown(f"Initial Corpus=**{initial_corpus}**, count= **{len(initial_corpus)}**")
  # for k in initial_corpus:
  # 	print(k)

  # print(f"Initial Corpus={initial_corpus}")
  matched_str=fn_find_string(start_string,initial_corpus)
  if len(matched_str)>0:
    st.markdown(f"Matched Strings from Corpus = **{matched_str}** , count= **{len(matched_str)}**")
    #count number of open and closed parantheses that are correct in corpus
    count_open,count_close=fn_count_parantheses(matched_str,start_string)
    print(f"Open Parantheses Count={count_open}, Close Paranthese Count={count_close}")
    st.markdown(f"Open Parantheses Count=**{count_open}**, Close Paranthese Count=**{count_close}**")

    #Choose parantheses based on temprature
    str_drawn=fn_choose_prob(temprature,count_open,count_close)
    while len(matched_str)>0:
      print("*"*80)
      st.write("---")
      corpus=matched_str.copy()
      print(f"Corpus={corpus} ")
      st.markdown(f"Corpus= **{corpus}**, count= **{len(matched_str)}**")
      print(f"Parantheses which has been choosen ={str_drawn[0]}")
      st.markdown(f"Parantheses which has been choosen = **{str_drawn[0]}**")
      start_string=start_string+str_drawn[0]
      matched_str=fn_find_string(start_string,corpus)
      count_open,count_close=fn_count_parantheses(matched_str,start_string)
      print(f"Open Parantheses Count={count_open}, Close Paranthese Count={count_close}")
      st.markdown(f"Open Parantheses Count= **{count_open}** , Close Paranthese Count=**{count_close}**")

      str_drawn=fn_choose_prob(temprature,count_open,count_close)

    st.write("Can't find any matching string")
    print(f"Failed to find any matching")

  else:
	  
    st.write("Can't find any matching string")
    # print(f"Failed to find any matching")
    print("No matching found")


