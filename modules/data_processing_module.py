# Module: data_processing_module
# Responsibility: Process and transform input data

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

def create_data_processing_module_chain():
    """
    Creates a LangChain chain for data_processing_module
    Dependencies: intent_recognition_module
    Parallelizable: Yes
    """
    # Initialize model based on configuration
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        max_tokens=2000
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are handling the data_processing_module responsibility."),
        ("human", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain

# Example usage of the module
def execute_data_processing_module(input_data: dict):
    chain = create_data_processing_module_chain()
    result = chain.invoke({"input": str(input_data)})
    return {
        "result": result,
        "module": "data_processing_module",
        "node_id": "data_processing_module_node_1"
    }
