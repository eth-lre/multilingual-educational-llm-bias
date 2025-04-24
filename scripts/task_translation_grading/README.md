# Setup
1. Install the api libraries for all models
2. Create a file named "keys.py" with all api keys
```
openai=""
google=""
together=""
claude=""
mistral=""
cohere=""
```
3. Copy `prompts_{language_code}.json` here 
# Execution
To run
`python query_gevl_<model>.py <datafile.json>`
The code runs for both english and translated prompts. The name of the datafile must contain a 2-letter language code enclosed in underscores(_) eg `misk_expl_hi_file.json`
