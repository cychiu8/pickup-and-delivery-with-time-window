from problem_instance import ProblemInstance
from config import project_config

NUM_OF_INSTANCE = 5
API_KEY = project_config.api_key
problem = ProblemInstance(api_key=API_KEY)
df = problem.generate_instance(NUM_OF_INSTANCE)
problem.output_generate_instance()
