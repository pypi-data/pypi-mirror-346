system_template = """
You will summarization code with a strict structure like in the below but 
loader will change depending on the input
###
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
def {function_name}(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)
if {argument}:
    {variable} = summarize(argument)
else:
    variable = ""
###
"""

human_template = """
Here is the part of the code that you are supposed to continue:
{code_snippets}

Write a summarize function for the argument name and variable below:
Argument Name : {argument}
Variable Name : {variable}
Summarization Code:
"""

imports = """
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
"""

functions = """
def {function_name}({argument}):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", openai_api_key=openai_api_key)
    chain = load_summarize_chain(llm, chain_type="stuff")
    with st.spinner('DemoGPT is working on it. It might take 5-10 seconds...'):
        return chain.run({argument})
"""