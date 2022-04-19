from problem_instance import ProblemInstance
from dotenv import load_dotenv
import os

load_dotenv(".env")
NUM_OF_INSTANCE = 5
API_KEY = os.environ["API_KEY"]
problem = ProblemInstance(api_key=API_KEY)
df = problem.generate_instance(NUM_OF_INSTANCE)
problem.output_generate_instance()
