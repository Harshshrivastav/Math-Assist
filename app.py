# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain.chains import LLMMathChain, LLMChain
# from langchain.prompts import PromptTemplate
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain.agents.agent_types import AgentType
# from langchain.agents import Tool, initialize_agent
# from langchain.callbacks import StreamlitCallbackHandler

# ## Set upi the Stramlit app
# st.set_page_config(page_title="Text To MAth Problem Solver And Data Serach Assistant",page_icon="🧮")
# st.title("Text To Math Problem Solver Uing Google Gemma 2")

# groq_api_key=st.sidebar.text_input(label="Groq API Key",type="password")


# if not groq_api_key:
#     st.info("Please add your Groq APPI key to continue")
#     st.stop()

# llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


# ## Initializing the tools
# wikipedia_wrapper=WikipediaAPIWrapper()
# wikipedia_tool=Tool(
#     name="Wikipedia",
#     func=wikipedia_wrapper.run,
#     description="A tool for searching the Internet to find the vatious information on the topics mentioned"

# )

# ## Initializa the MAth tool

# math_chain=LLMMathChain.from_llm(llm=llm)
# calculator=Tool(
#     name="Calculator",
#     func=math_chain.run,
#     description="A tools for answering math related questions. Only input mathematical expression need to bed provided"
# )

# prompt="""
# Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
# and display it point wise for the question below
# Question:{question}
# Answer:
# """

# prompt_template=PromptTemplate(
#     input_variables=["question"],
#     template=prompt
# )

# ## Combine all the tools into chain
# chain=LLMChain(llm=llm,prompt=prompt_template)

# reasoning_tool=Tool(
#     name="Reasoning tool",
#     func=chain.run,
#     description="A tool for answering logic-based and reasoning questions."
# )

# ## initialize the agents

# assistant_agent=initialize_agent(
#     tools=[wikipedia_tool,calculator,reasoning_tool],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=False,
#     handle_parsing_errors=True
# )

# if "messages" not in st.session_state:
#     st.session_state["messages"]=[
#         {"role":"assistant","content":"Hi, I'm a MAth chatbot who can answer all your maths questions"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg['content'])

# ## LEts start the interaction
# question=st.text_area("Enter youe question:","I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

# if st.button("find my answer"):
#     if question:
#         with st.spinner("Generate response.."):
#             st.session_state.messages.append({"role":"user","content":question})
#             st.chat_message("user").write(question)

#             st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
#             response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb]
#                                          )
#             st.session_state.messages.append({'role':'assistant',"content":response})
#             st.write('### Response:')
#             st.success(response)

#     else:
#         st.warning("Please enter the question")



# V--2
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType

# Streamlit page config with updated name and icon
st.set_page_config(page_title="Math Assist", page_icon="🐢", layout="centered")

# Custom Title and description with CSS and hover effects
st.markdown(
    """
    <style>
    .container {
        background-image: url("https://cdn.pixabay.com/animation/2023/06/26/03/02/03-02-03-917_512.gif");
        background-size: cover;
        margin: 0;
        padding: 50px;
        border-radius: 5px;
        border: 1px solid #ddd;
        position: relative;
        overflow: hidden;
    }

    .container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 0;
        height: 100%;
        background-color: #AD9F2F;
        transition: width 0.5s ease;
        z-index: 0;
    }

    .container:hover::before {
        width: 100%;
    }

    .container h4,
    .container p {
        position: relative;
        z-index: 1;
        color: #fff;
        transition: color 0.5s ease;
    }

    .container:hover h4,
    .container:hover p {
        color: #000;
    }

    .calculator-container {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>

    <div class="container">
        <h4>🐢 Math Assist</h4>
        <p>Interact with AI to solve math problems and search for information.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar settings for API key
st.sidebar.title("Settings")

# API Key input
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

# Basic validation for API key
if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

# LLM setup using Groq
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Initialize the Math tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expressions."
)

# Prompt for reasoning tool
prompt = """
You're an agent tasked with solving users' mathematical questions. Logically arrive at the solution, provide a detailed explanation, and display it point-wise for the question below:
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

# Combine all the tools into a chain
chain = LLMMathChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

# Initialize the agent
assistant_agent = initialize_agent(
    tools=[calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions."}
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# Input area for the user's question
question = st.text_area("Enter your question:", "Solve: (2+3)*5")

# Simulated keyboard in the sidebar with grey background
st.sidebar.subheader("Equation Keyboard")
st.sidebar.markdown('<div class="calculator-container">', unsafe_allow_html=True)

if "equation" not in st.session_state:
    st.session_state["equation"] = ""

# Button functions to add symbols and numbers to the equation input
col1, col2, col3, col4 = st.sidebar.columns(4)
with col1:
    if st.button("7"):
        st.session_state["equation"] += "7"
    if st.button("4"):
        st.session_state["equation"] += "4"
    if st.button("1"):
        st.session_state["equation"] += "1"
    if st.button("e"):
        st.session_state["equation"] += "e"
    if st.button("("):
        st.session_state["equation"] += "("

with col2:
    if st.button("8"):
        st.session_state["equation"] += "8"
    if st.button("5"):
        st.session_state["equation"] += "5"
    if st.button("2"):
        st.session_state["equation"] += "2"
    if st.button("0"):
        st.session_state["equation"] += "0"
    if st.button("π"):
        st.session_state["equation"] += "π"

with col3:
    if st.button("9"):
        st.session_state["equation"] += "9"
    if st.button("6"):
        st.session_state["equation"] += "6"
    if st.button("3"):
        st.session_state["equation"] += "3"
    if st.button("."):
        st.session_state["equation"] += "."
    if st.button(")"):
        st.session_state["equation"] += ")"

with col4:
    if st.button("➗"):
        st.session_state["equation"] += "/"
    if st.button("✖️"):
        st.session_state["equation"] += "*"
    if st.button("➖"):
        st.session_state["equation"] += "-"
    if st.button("➕"):
        st.session_state["equation"] += "+"
    if st.button("sqrt"):
        st.session_state["equation"] += "sqrt()"

col1, col2, col3, col4 = st.sidebar.columns(4)
with col1:
    if st.button("sin"):
        st.session_state["equation"] += "sin()"
with col2:
    if st.button("cos"):
        st.session_state["equation"] += "cos()"
with col3:
    if st.button("tan"):
        st.session_state["equation"] += "tan()"
with col4:
    if st.button("log"):
        st.session_state["equation"] += "log()"

# Close the calculator container div
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Display the equation
st.sidebar.text_input("Equation:", value=st.session_state["equation"], key="equation_input")

# Button to clear the equation
if st.sidebar.button("Clear Equation"):
    st.session_state["equation"] = ""

# Process the question when the button is clicked
if st.button("Find my answer"):
    if st.session_state["equation"]:
        question = st.session_state["equation"]  # Use the equation from the keyboard
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(question, callbacks=[st_cb])
            st.session_state.messages.append({'role': 'assistant', "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter a question")
