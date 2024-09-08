import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import END, StateGraph, START
import contextlib
import io
from Modules.graph  import *
from  Modules.parser import parser
import os
import glob

# Load environment variables from .env file
load_dotenv()
# Load environment variables from .env file

### Parameter
# Max tries

# solution = code_gen_chain_oai.invoke({"context":concatenated_content,"messages":[("user",question)]})


root_directory = '/home/alice/employee_fingerprint/source'

# Step 2: Add the root directory to sys.path if not already added


# Step 3: Use glob to find all Python files in the directory
python_files = glob.glob(os.path.join(root_directory, '**','*.py'))

# Step 4: Iterate over each Python file and execute it


for code_dir in python_files:
# Extract the base file name (e.g., 'mld_pre_clean.py')
    file_name = os.path.basename(code_dir)

    # Remove the file extension to get the module name (e.g., 'mld_pre_clean')
    module_name = os.path.splitext(file_name)[0]
    concatenated_content = parser(code_dir)

    workflow = StateGraph(GraphState)

    test_generator = TestGenerator(concatenated_content ,root_directory , module_name)

    # Define the nodes
    workflow.add_node("generate", test_generator.generate)  # generation solution
    workflow.add_node("check_code", test_generator.code_check)  # check code
    workflow.add_node("reflect", test_generator.reflect)  # reflect

    # Build graph
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", "check_code")
    workflow.add_conditional_edges(
        "check_code",
        test_generator.decide_to_finish,
        {
            "end": END,
            "reflect": "reflect",
            "generate": "generate",
        },
    )
    workflow.add_edge("reflect", "generate")
    app = workflow.compile()

    question = f"Write unitary test for the following code located at {code_dir}  "
    final_state = app.invoke({"messages": [("user", question)], "iterations": 0 , "error":"no" } )