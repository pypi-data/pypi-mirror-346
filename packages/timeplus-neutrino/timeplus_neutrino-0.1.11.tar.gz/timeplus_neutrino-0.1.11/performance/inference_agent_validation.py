import json
from neutrino.onboard.agent import DataOnboardingAgent
from neutrino.utils.tools import extract_code_blocks_with_type
from neutrino.conf import TimeplusAgentConfig



def test_case_to_table_name(test_case_name):
    """
    Convert a test case name to a valid database table name by:
    1. Converting to lowercase
    2. Replacing spaces with underscores
    3. Removing any characters that aren't alphanumeric or underscores
    4. Ensuring the name doesn't start with a digit (prefixes with 't_' if needed)
    
    Args:
        test_case_name (str): The name of the test case
        
    Returns:
        str: A valid database table name
    """
    # Convert to lowercase
    table_name = test_case_name.lower()
    
    # Replace spaces with underscores
    table_name = table_name.replace(' ', '_')
    
    # Remove any characters that aren't alphanumeric or underscores
    table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
    
    # Ensure the name doesn't start with a digit
    if table_name and table_name[0].isdigit():
        table_name = 't_' + table_name
        
    return table_name

#agent_config = TimeplusAgentConfig()
#agent_config.config("default", "http://localhost:11434/v1", "ollama", "codellama:latest")

# generating code read json

with open("inference.json", "r") as f:
    data = json.load(f)

for testcase in data:
    print(f"testcase : {testcase}")
    agent = DataOnboardingAgent()
    inference_ddl, inference_json = agent.inference(testcase["data_payload"],test_case_to_table_name(testcase["test_case_name"]))
    print(f"schema sql : {inference_ddl}")
    print(f"schema json : {inference_json}")
    
    

