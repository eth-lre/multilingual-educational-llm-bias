# Number of times to retry the API call in case of failure. Raise error afterwards
max_attempts = 5
retry_delay = 20  # seconds

start_idx = 0 # Remember that they are 0-indexed
num_sample_points = 0 # For debugging purposes to run script on fewer data points. 0 to run on all data points

max_utterances = 5

LANGS = ["en", "uk", "hi", "cs", "fa", "te"]
  
############################ MODEL SELECTION ####################################
########## GPT ###########
modelName = "gpt-4o"
# modelName = "gpt-4o-mini" # As of 20 July 2024, this calls "gpt-4o-mini-2024-07-18"
# modelName = "gpt-3.5-turbo-0125"


########## Gemini ###########
# modelName = "gemini-2.0-flash"
# modelName = "gemini-1.5-pro"
# modelName = "gemini-1.5-flash"


########## Llama ############
# modelName = "accounts/fireworks/models/llama-v3p1-405b-instruct"


########## Mistral ############
# modelName = "mistral-large-latest"


########## Claude ############
# modelName = "claude-3-7-sonnet-20250219"
# modelName = "claude-3-5-sonnet-20240620"

########## Cohere ############
# modelName = "command-a-03-2025"