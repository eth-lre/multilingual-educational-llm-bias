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
3. Copy `prompts_{language_code}.json` here if you want to use native prompts
# Execution
To run with English prompts:
`python query_expl_<model>.py <datafile.json>`

To run with translated prompts
`python query_expl_<model>_t.py <datafile.json>`
The name of the datafile must contain a 2-letter language code enclosed in underscores(_) eg `misk_expl_hi_file.json`
