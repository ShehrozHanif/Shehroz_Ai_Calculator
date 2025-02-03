from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import tool
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    print("Tool Message:  Addition Tool is Called!")
    print("="*40)
    return a + b
@tool
def subtract(a: int, b: int) -> int:
    """Subtract two integers."""
    print("Tool Message:  Subtraction Tool is Called!")
    print("="*40)
    return a - b
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    print("Tool Message:  Multiplication Tool is Called!")
    print("="*40)
    return a * b
@tool
def divide(a: int, b: int) -> float:
    """Divide two integers."""
    print("Tool Message:  Division Tool is Called!")
    print("="*40)
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

@tool
def intro(input_str: str = "") -> str:
    """Provide Shehroz Hanif introduction."""
    print("Tool Message:  Introduction Tool is Called!")
    print("="*40)
    return (
        """Shehroz Hanif is a skilled web developer and programmer with a passion for creating dynamic, user-focused projects.
        Here is His Linkedin Profile: https://www.linkedin.com/in/shehroz-hanif-60441727a/
        His portfolio features innovative Python projects and AI solutions, including a chatbot built with LangChain and Google Gemini LLM.
        He is exploring Agentic AI and intelligent agents, driving advancements in automation and artificial intelligence."""
    )
@tool
def creator(input_str: str = "") -> str:
    """Provide Shehroz Hanif introduction."""
    print("Tool Message:  Developer Detailes Tool is Called!")
    print("="*40)
    return (
        """I am a Calculator Agent Developed By Shehroz Hanif.
        If You Want to know About Shehroz Hanif Ali Then Type Who Is Shehroz Hanif
    """
    )

@tool
def goodbye(input_str: str = "") -> str:
    """Stop the Agent."""
    print("Tool Message:  Good Bye Tool is Called!")
    print("="*40)
    return
    print("Goodbye! Thanks for your visit. Come again...")

@tool
def give_social_accounts(input_str: str = "") -> str:
    """Provide Shehroz Hanif social accounts."""
    print("Tool Message:  Contact Detailes Tool is Called!")
    print("="*40)
    return (
        """
        Shehroz Linkedin: https://www.linkedin.com/in/shehroz-hanif-60441727a/
        Shehroz Github: https://github.com/ShehrozHanif
        Shehroz Instagram: https://www.instagram.com/the.realshehroz/
        Shehroz Facebook Profile: https://www.facebook.com/muhammad.shehroz.357284
        Shehroz Email Address: Shehrozhanif18@gmail.com
        Shehroz Contact Number: 03062151026
        """
    )


tools = [
    add,
    subtract,
    multiply,
    divide,
    intro,
    creator,
    goodbye,
    give_social_accounts
]



llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",verbose=True, API_KEY=GOOGLE_API_KEY)


SYSTEM_MESSAGE = (
    "You are an AI-based calculator agent designed exclusively to operate within the scope of the provided tools. "
    "These tools include operations like addition, subtraction, multiplication, division, percentage calculations, introductions, "
    "creator information, contact details, and goodbye messages. "
    "If you receive a query or action outside the capabilities of these tools, respond politely and clearly, stating that the requested action "
    "is beyond your functionality. Avoid providing speculative or unsupported responses."
)



# Initialize the agent
agent = initialize_agent(
    tools,                        # Provide the tools
    llm,                            # LLM for fallback
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=50,
    # verbose=True                        # Enable debugging output
    system_message=SYSTEM_MESSAGE
)


st.title("Shehroz Hanif AI Calculator Agent")
st.title("AI-Based Calculator Agent")
st.write("Welcome to Shehroz Coding World!")

# Suggested queries
suggested_queries = [
    "What is 5 + 3?",
    "What is 3.6 percent Of 69 And Multiply The Output by 6.",
    "Can you subtract 10 from 20?",
    "Who is Shehroz Hanif?",
    "Who is Founder/Developer/Creator?",
    "Give me Shehroz social accounts.",
    "Multiply 7 and 8.",
    "Divide 100 by 4.",
    "Perform multiple operations like add 5 and 3, then multiply by 2."
]

st.write("### Suggested Queries:")
for query in suggested_queries:
    st.write(f"- {query}")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []  # Store user queries and responses

# Input with Arrow Button
col1, col2 = st.columns([4, 1])  # Adjust column sizes to previous proportions
with col1:
    user_query = st.text_input( "Enter your query and press ➡️")
    if st.button("➡️"):  # Arrow button for submission
        if user_query.strip():  # Check if input is not empty
            try:
                # Invoke the agent with the user's query
                response = agent.invoke({"input": user_query})
                agent_response = response.get('output', 'No output available')

                # Update conversation history
                st.session_state.conversation.append((user_query, agent_response))

                # Display the conversation history
                st.write("### Conversation History:")
                for i, (query, reply) in enumerate(st.session_state.conversation, 1):
                    st.write(f"Human Message: {query}")
                    st.write(f"Agent Response:  {reply}")
                    st.write("---")

            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query to proceed.")


