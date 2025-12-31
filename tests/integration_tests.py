import unittest
from main_langchain_flow import LangChainFlowOrchestrator


class TestLangChainFlowIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.orchestrator = LangChainFlowOrchestrator()
    
    def test_full_flow_execution(self):
        """Test the complete workflow execution"""
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
        """Test sequential execution path"""
        input_data = {"test": "sequential"}
        
        result = self.orchestrator.execute_sequential_steps(input_data)
        
        self.assertIn("steps", result)
        self.assertIn("input", result)
    
    def test_parallel_execution(self):
        """Test parallel execution path"""
        input_data = {"test": "parallel"}
        
        result = self.orchestrator.execute_parallel_steps(input_data)
        
        self.assertIn("parallel_steps", result)
        self.assertIn("input", result)


if __name__ == '__main__':
    unittest.main()
