# Module: analysis_module
# Responsibility: Analyze data and generate insights

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

def create_analysis_module_chain():
    """
    Creates a LangChain chain for analysis_module
    Dependencies: data_processing_module
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
        ("system", "You are handling the analysis_module responsibility."),
        ("human", "{input}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain

# Example usage of the module
def execute_analysis_module(input_data: dict):
    chain = create_analysis_module_chain()
    result = chain.invoke({"input": str(input_data)})
    return {
        "result": result,
        "module": "analysis_module",
        "node_id": "analysis_module_node_2"
    }
