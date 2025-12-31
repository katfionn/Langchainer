# Module: intent_recognition_module
# Responsibility: Parse user requirements and extract core intent

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

def create_intent_recognition_module_chain():
    """
    Creates a LangChain chain for intent_recognition_module
    Dependencies: none
    Parallelizable: No
    """
    # Initialize model based on configuration
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        max_tokens=2000
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are handling the intent_recognition_module responsibility."),
        ("human", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain

# Example usage of the module
def execute_intent_recognition_module(input_data: dict):
    chain = create_intent_recognition_module_chain()
    result = chain.invoke({"input": str(input_data)})
    return {
        "result": result,
        "module": "intent_recognition_module",
        "node_id": "intent_recognition_module_node_0"
    }
