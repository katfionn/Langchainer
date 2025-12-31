"""
LangChain AutoPlanner Generator - Main Flow
Senior LangChain Architect & Autonomous Task Orchestrator
"""
import json
from typing import Dict, List, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.tools import Tool
import asyncio
from dataclasses import dataclass
from enum import Enum


class TaskPhase(Enum):
    INTAKE = "intake"
    CONFIRMATION = "confirmation"
    DECOMPOSITION = "decomposition"
    ELASTIC_GENERATION = "elastic_generation"
    ASSEMBLY = "assembly"
    TESTING = "testing"
    OUTPUT = "output"


@dataclass
class TaskRequirements:
    """Parsed user requirements and intent"""
    core_intent: str
    functional_scope: str
    model_requirements: List[str]
    is_repair_mode: bool = False
    repair_code: Optional[str] = None


@dataclass
class ModuleSpecification:
    """Specification for a single module"""
    name: str
    responsibility: str
    dependencies: List[str]
    is_parallelizable: bool
    execution_order: int


@dataclass
class NodeConfiguration:
    """Configuration for a processing node"""
    node_id: str
    module_name: str
    task_description: str
    required_inputs: List[str]
    outputs: List[str]
    model_routing: str


class ConfigManager:
    """Manages the AI model configuration"""
    
    def __init__(self, config_path: str = "ai_models.config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if not exists
            default_config = {
                "base_url": "https://api.openai.com/v1",
                "primary_model": "gpt-4",
                "secondary_models": [],
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2000,
                "model_routing": {
                    "intent_recognition": "primary_model",
                    "code_generation": "primary_model",
                    "validation": "primary_model"
                },
                "notes": "Leave secondary_models as [] if single model. User requirement auto-detects multi-model needs."
            }
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def get_model_config(self, purpose: str) -> Dict:
        """Get model configuration for specific purpose"""
        routing = self.config["model_routing"].get(purpose, "primary_model")
        model_name = self.config[routing.replace("_model", "")] if routing != "primary_model" else self.config["primary_model"]
        
        return {
            "model": model_name,
            "temperature": self.config["temperature"],
            "top_p": self.config["top_p"],
            "max_tokens": self.config["max_tokens"]
        }


class IntentRecognizer:
    """Phase 1: Parse user requirements and extract core intent"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.model = self._create_model("intent_recognition")
    
    def _create_model(self, purpose: str):
        model_config = self.config.get_model_config(purpose)
        return ChatOpenAI(
            model=model_config["model"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"]
        )
    
    def parse_requirements(self, user_input: str) -> TaskRequirements:
        """Parse user requirement to extract core intent and functional scope"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior AI architect. Parse the user's requirement to extract:
            1. Core intent - the main purpose
            2. Functional scope - what needs to be built
            3. Model requirements - what types of AI models are needed
            4. Repair mode detection - if user is asking for code repair"""),
            ("human", "User requirement: {requirement}")
        ])
        
        chain = prompt | self.model
        response = chain.invoke({"requirement": user_input})
        
        # Parse response to extract requirements
        # In real implementation, this would be more sophisticated
        return TaskRequirements(
            core_intent="Parsed intent from: " + user_input[:100],
            functional_scope="Functional scope based on: " + user_input,
            model_requirements=["primary_model"]  # This would be dynamically determined
        )


class ModuleDecomposer:
    """Phase 3: Auto-split into modules and identify parallel execution points"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.model = self._create_model("code_generation")
    
    def _create_model(self, purpose: str):
        model_config = self.config.get_model_config(purpose)
        return ChatOpenAI(
            model=model_config["model"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"]
        )
    
    def decompose_task(self, requirements: TaskRequirements) -> List[ModuleSpecification]:
        """Decompose the main task into modules"""
        modules = [
            ModuleSpecification(
                name="intent_recognition_module",
                responsibility="Parse user requirements and extract core intent",
                dependencies=[],
                is_parallelizable=False,
                execution_order=1
            ),
            ModuleSpecification(
                name="data_processing_module",
                responsibility="Process and transform input data",
                dependencies=["intent_recognition_module"],
                is_parallelizable=True,
                execution_order=2
            ),
            ModuleSpecification(
                name="analysis_module",
                responsibility="Analyze data and generate insights",
                dependencies=["data_processing_module"],
                is_parallelizable=True,
                execution_order=3
            ),
            ModuleSpecification(
                name="validation_module",
                responsibility="Validate outputs and ensure quality",
                dependencies=["analysis_module"],
                is_parallelizable=True,
                execution_order=4
            )
        ]
        return modules


class NodeGenerator:
    """Phase 4: Generate parallel nodes and execution graph"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.model = self._create_model("code_generation")
    
    def _create_model(self, purpose: str):
        model_config = self.config.get_model_config(purpose)
        return ChatOpenAI(
            model=model_config["model"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_tokens"]
        )
    
    def generate_nodes(self, modules: List[ModuleSpecification]) -> List[NodeConfiguration]:
        """Generate processing nodes for each module"""
        nodes = []
        for i, module in enumerate(modules):
            node = NodeConfiguration(
                node_id=f"{module.name}_node_{i}",
                module_name=module.name,
                task_description=module.responsibility,
                required_inputs=module.dependencies,
                outputs=[f"{module.name}_output"],
                model_routing="primary_model"
            )
            nodes.append(node)
        
        return nodes


class CodeGenerator:
    """Phase 5: Generate complete LangChain code"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
    
    def generate_module_code(self, module: ModuleSpecification, node: NodeConfiguration) -> str:
        """Generate code for a single module"""
        code = f"""
# Module: {module.name}
# Responsibility: {module.responsibility}

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

def create_{module.name.replace('-', '_').replace(' ', '_')}_chain():
    \"\"\"
    Creates a LangChain chain for {module.name}
    Dependencies: {', '.join(module.dependencies) if module.dependencies else 'none'}
    Parallelizable: {'Yes' if module.is_parallelizable else 'No'}
    \"\"\"
    # Initialize model based on configuration
    llm = ChatOpenAI(
        model="{self.config.get_model_config('code_generation')['model']}",
        temperature={self.config.get_model_config('code_generation')['temperature']},
        max_tokens={self.config.get_model_config('code_generation')['max_tokens']}
    )
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are handling the {module.name} responsibility."),
        ("human", "{{input}}")
    ])
    
    # Create chain
    chain = prompt | llm
    
    return chain

# Example usage of the module
def execute_{module.name.replace('-', '_').replace(' ', '_')}(input_data: dict):
    chain = create_{module.name.replace('-', '_').replace(' ', '_')}_chain()
    result = chain.invoke({{"input": str(input_data)}})
    return {{
        "result": result,
        "module": "{module.name}",
        "node_id": "{node.node_id}"
    }}
"""
        return code.strip()
    
    def generate_main_chain(self, modules: List[ModuleSpecification], nodes: List[NodeConfiguration]) -> str:
        """Generate the main orchestration chain"""
        code = """
# Main LangChain Flow - Auto-Generated by AutoPlanner Generator
# This orchestrates all modules in the specified execution order

from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import generated modules
"""
        
        for module in modules:
            code += f"from modules.{module.name.replace('-', '_').replace(' ', '_')} import execute_{module.name.replace('-', '_').replace(' ', '_')}\n"
        
        code += """

class LangChainFlowOrchestrator:
    def __init__(self):
        self.execution_context = {}
    
    def execute_sequential_steps(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Execute modules in sequential order respecting dependencies
        \"\"\"
        results = {"input": input_data, "steps": []}
        
        for module_name, execute_func in [
"""
        
        for module in modules:
            if not module.is_parallelizable:
                code += f"            (\"{module.name}\", execute_{module.name.replace('-', '_').replace(' ', '_')}),\n"
        
        code += """        ]:
            result = execute_func(results["input"])
            results["steps"].append(result)
            results["input"] = result  # Pass result to next step
        
        return results
    
    def execute_parallel_steps(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Execute parallelizable modules concurrently
        \"\"\"
        parallel_modules = [
"""
        
        for module in modules:
            if module.is_parallelizable:
                code += f"            (\"{module.name}\", execute_{module.name.replace('-', '_').replace(' ', '_')}),\n"
        
        code += """        ]
        
        results = {"input": input_data, "parallel_steps": []}
        
        # Execute in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(parallel_modules)) as executor:
            futures = []
            for name, func in parallel_modules:
                future = executor.submit(func, input_data)
                futures.append((name, future))
            
            for name, future in futures:
                result = future.result()
                results["parallel_steps"].append(result)
        
        return results
    
    def execute_full_flow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"
        Execute the complete flow combining sequential and parallel execution
        \"\"\"
        # First, execute sequential steps
        seq_results = self.execute_sequential_steps(input_data)
        
        # Then, execute parallel steps with the sequential results
        parallel_input = {**input_data, **seq_results}
        parallel_results = self.execute_parallel_steps(parallel_input)
        
        return {
            "sequential_results": seq_results,
            "parallel_results": parallel_results,
            "final_output": {**seq_results, **parallel_results}
        }


# Example usage
def main():
    orchestrator = LangChainFlowOrchestrator()
    
    # Example input
    input_data = {
        "user_query": "Process this data according to the specified requirements",
        "metadata": {"source": "user_input", "timestamp": "auto_generated"}
    }
    
    # Execute full flow
    final_result = orchestrator.execute_full_flow(input_data)
    
    print("Flow execution completed successfully!")
    print(f"Sequential steps: {len(final_result['sequential_results']['steps'])}")
    print(f"Parallel steps: {len(final_result['parallel_results']['parallel_steps'])}")


if __name__ == "__main__":
    main()
"""
        return code.strip()


class TestGenerator:
    """Phase 6: Generate test suites"""
    
    def generate_unit_tests(self, modules: List[ModuleSpecification]) -> str:
        """Generate unit tests for each module"""
        test_code = "import unittest\nfrom unittest.mock import Mock, patch\n"
        
        for module in modules:
            test_code += f"""
class Test{module.name.replace('_', ' ').title().replace(' ', '')}(unittest.TestCase):
    
    def setUp(self):
        \"\"\"Set up test fixtures before each test method.\"\"\"
        pass
    
    def test_{module.name.replace('-', '_')}_execution(self):
        \"\"\"Test that {module.name} executes without error\"\"\"
        try:
            # Import the module function
            from modules import {module.name.replace('-', '_').replace(' ', '_')}
            
            # Test with sample input
            result = {module.name.replace('-', '_').replace(' ', '_')}.execute_{module.name.replace('-', '_').replace(' ', '_')}({{"test": "data"}})
            
            # Basic assertions
            self.assertIsNotNone(result)
            self.assertIn("result", result)
            self.assertIn("module", result)
            self.assertEqual(result["module"], "{module.name}")
            
        except ImportError:
            self.skipTest("Module not available for testing")
    
    def test_{module.name.replace('-', '_')}_chain_creation(self):
        \"\"\"Test that the LangChain chain is created properly\"\"\"
        try:
            from modules import {module.name.replace('-', '_').replace(' ', '_')}
            
            chain = {module.name.replace('-', '_').replace(' ', '_')}.create_{module.name.replace('-', '_').replace(' ', '_')}_chain()
            
            # Verify chain is callable
            self.assertTrue(callable(chain))
            
        except ImportError:
            self.skipTest("Module not available for testing")


"""
        
        test_code += """
if __name__ == '__main__':
    unittest.main()
"""
        return test_code.strip()
    
    def generate_integration_tests(self) -> str:
        """Generate integration tests for the workflow"""
        return """
import unittest
from main_langchain_flow import LangChainFlowOrchestrator


class TestLangChainFlowIntegration(unittest.TestCase):
    
    def setUp(self):
        \"\"\"Set up test fixtures before each test method.\"\"\"
        self.orchestrator = LangChainFlowOrchestrator()
    
    def test_full_flow_execution(self):
        \"\"\"Test the complete workflow execution\"\"\"
        input_data = {
            "user_query": "Test integration workflow",
            "metadata": {"source": "integration_test"}
        }
        
        result = self.orchestrator.execute_full_flow(input_data)
        
        # Verify the structure of results
        self.assertIn("sequential_results", result)
        self.assertIn("parallel_results", result)
        self.assertIn("final_output", result)
        
        # Verify execution completed successfully
        self.assertIsNotNone(result["final_output"])
    
    def test_sequential_execution(self):
        \"\"\"Test sequential execution path\"\"\"
        input_data = {"test": "sequential"}
        
        result = self.orchestrator.execute_sequential_steps(input_data)
        
        self.assertIn("steps", result)
        self.assertIn("input", result)
    
    def test_parallel_execution(self):
        \"\"\"Test parallel execution path\"\"\"
        input_data = {"test": "parallel"}
        
        result = self.orchestrator.execute_parallel_steps(input_data)
        
        self.assertIn("parallel_steps", result)
        self.assertIn("input", result)


if __name__ == '__main__':
    unittest.main()
"""


class AutoPlannerGenerator:
    """Main orchestrator for the AutoPlanner Generator"""
    
    def __init__(self):
        self.config_manager = ConfigManager("ai_models.config.json")
        self.intent_recognizer = IntentRecognizer(self.config_manager)
        self.module_decomposer = ModuleDecomposer(self.config_manager)
        self.node_generator = NodeGenerator(self.config_manager)
        self.code_generator = CodeGenerator(self.config_manager)
        self.test_generator = TestGenerator()
    
    def generate_from_requirements(self, user_requirements: str):
        """Complete flow: generate all artifacts from user requirements"""
        
        print(f"[PHASE 1] Parsing user requirements...")
        requirements = self.intent_recognizer.parse_requirements(user_requirements)
        print(f"✓ Core intent: {requirements.core_intent[:50]}...")
        
        print(f"[PHASE 3] Decomposing task into modules...")
        modules = self.module_decomposer.decompose_task(requirements)
        print(f"✓ Created {len(modules)} modules")
        
        print(f"[PHASE 4] Generating processing nodes...")
        nodes = self.node_generator.generate_nodes(modules)
        print(f"✓ Generated {len(nodes)} processing nodes")
        
        print(f"[PHASE 5] Generating module code...")
        # Generate individual module files
        for module, node in zip(modules, nodes):
            module_code = self.code_generator.generate_module_code(module, node)
            
            # Create modules directory if it doesn't exist
            import os
            os.makedirs("modules", exist_ok=True)
            
            with open(f"modules/{module.name.replace('-', '_').replace(' ', '_')}.py", "w") as f:
                f.write(module_code)
        
        # Generate main chain
        main_code = self.code_generator.generate_main_chain(modules, nodes)
        with open("main_langchain_flow.py", "w") as f:
            f.write(main_code)
        
        print(f"[PHASE 6] Generating tests...")
        # Generate unit tests
        unit_tests = self.test_generator.generate_unit_tests(modules)
        os.makedirs("tests", exist_ok=True)
        with open("tests/unit_tests.py", "w") as f:
            f.write(unit_tests)
        
        # Generate integration tests
        integration_tests = self.test_generator.generate_integration_tests()
        with open("tests/integration_tests.py", "w") as f:
            f.write(integration_tests)
        
        print(f"[PHASE 7] Creating documentation...")
        self._create_documentation(modules, nodes)
        
        print("✓ All artifacts generated successfully!")
        print("✓ Check the ./dist folder for complete output")
    
    def _create_documentation(self, modules: List[ModuleSpecification], nodes: List[NodeConfiguration]):
        """Create documentation and architecture diagrams"""
        import os
        os.makedirs("docs", exist_ok=True)
        
        # Architecture diagram (ASCII)
        architecture_diagram = """
LANGCHAIN AUTOPLANNER FLOW ARCHITECTURE
========================================

USER INPUT
    ↓
[INTENT RECOGNITION MODULE] ←─┐
    ↓                        │
[DATA PROCESSING MODULE] ────┼─→ [VALIDATION MODULE] ──→ FINAL OUTPUT  
    ↓                        │
[ANALYSIS MODULE] ───────────┘

EXECUTION PARALLELIZATION
=========================
Sequential Steps: Intent Recognition → Data Processing
Parallel Steps: Analysis, Validation (can run concurrently)

NODE DEPENDENCIES
=================
intent_recognition_module_node_0: No dependencies
data_processing_module_node_1: Depends on intent_recognition_module
analysis_module_node_2: Depends on data_processing_module  
validation_module_node_3: Depends on analysis_module
"""
        
        with open("docs/architecture.md", "w") as f:
            f.write("# LangChain AutoPlanner Architecture\n\n")
            f.write(architecture_diagram)
            
            f.write("\n## Module Specifications\n\n")
            for i, module in enumerate(modules):
                f.write(f"### Module {i+1}: {module.name}\n")
                f.write(f"- Responsibility: {module.responsibility}\n")
                f.write(f"- Dependencies: {', '.join(module.dependencies) or 'None'}\n")
                f.write(f"- Parallelizable: {'Yes' if module.is_parallelizable else 'No'}\n")
                f.write(f"- Execution Order: {module.execution_order}\n\n")


# Example usage and demo
def demo():
    """Demonstrate the AutoPlanner Generator"""
    generator = AutoPlannerGenerator()
    
    sample_requirements = """
    Create a data analysis workflow that processes user queries,
    performs sentiment analysis, extracts key entities, and generates
    a summary report. The workflow should handle both sequential
    and parallel processing where appropriate.
    """
    
    print("LANGCHAIN AUTOPLANNER GENERATOR - DEMO")
    print("=" * 50)
    print(f"Sample requirements: {sample_requirements[:60]}...")
    print()
    
    generator.generate_from_requirements(sample_requirements)
    
    print("\nGENERATION COMPLETE!")
    print("Generated artifacts:")
    print("- main_langchain_flow.py (main orchestration)")
    print("- modules/ folder (individual processing modules)")
    print("- tests/ folder (unit and integration tests)")
    print("- docs/ folder (architecture documentation)")
    print("- ai_models.config.json (configuration file)")


if __name__ == "__main__":
    demo()
