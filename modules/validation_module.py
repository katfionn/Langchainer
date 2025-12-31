# Module: validation_module
# Responsibility: Validate outputs and ensure quality

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

def create_validation_module_chain():
    """
    Creates a LangChain chain for validation_module
    Dependencies: analysis_module
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
        ("system", "You are handling the validation_module responsibility."),
        ("human", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain

# Example usage of the module
def execute_validation_module(input_data: dict):
    chain = create_validation_module_chain()
    result = chain.invoke({"input": str(input_data)})
    return {
        "result": result,
        "module": "validation_module",
        "node_id": "validation_module_node_3"
    }
