import keys
from tqdm import tqdm
from time import sleep
import openai
openai.api_key = keys.openai
from random import choice
def call_gpt4_api(history, prompt, model="gpt-4o", repeat: int = 1, retries: int = 6):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}, *history],
            temperature=0
        )
    except Exception as e:
        print(e)
        if retries==0:
            return "0"
        sleep(2**(8-retries))
        return call_gpt4_api(history, prompt, model,repeat, retries-1)
    return response.choices[0].message.content
system_prompt = "You are a language translation evaluator. Your task is to assess the quality of a translation from English to {LANGUAGE}. You will be provided with two sentences:\n1. An original English sentence.\n2. A translated sentence in {LANGUAGE}.\nYour goal is to rate the translation on a scale from 1 to 5 based on the following criteria:\n1: The translation is incorrect, incomprehensible, or completely unrelated to the original English sentence.\n2: The translation has significant errors and distorts the meaning of the original English sentence.\n3: The translation is understandable but contains notable errors or awkward phrasing.\n4: The translation is mostly accurate with minor errors or slightly awkward phrasing.\n5: The translation is fluent, natural, and accurately conveys the meaning of the original English sentence without errors.\nExplain your decision"
second_prompt = "Now based on your above explanation, output the final score from 1 to 5. Only say '1', '2', '3', '4', or '5' without any other text. Do not say anything else."
count=0
lm_english={
    "cs":"Czech",
    "hi":"Hindi",
    "te":"Telugu",
    "fa":"Persian",
    "uk":"Ukrainian",
    "ar":"Arabic"
}
lm_native={
    "cs":"Čeština",
    "hi":"हिन्दी",
    "te":"తెలుగు",
    "fa":"فارسی",
    "uk":"Українська",
    "ar":"اَلْعَرَبِيَّةُ"
}
def prepare_user_input(orig,trans, language):
    res="English: "+orig+"\n"
    res+=language+": "+trans+"\n"
    return res
if __name__=="__main__":
    from sys import argv
    from json import load,dump
    languages=["cs","hi","te","fa","uk","ar"]
    lan="en"
    for l in languages:
        if "_"+l+"_" in argv[1]:
            lan=l
    prompts=load(open(f"prompts_{lan}.json"))
    data=load(open(argv[1]))
    for d in tqdm(data):
        if "GPT" in d:
            continue
        # first do the proper sentence
        inst={}
        for code in ["trans", "perturb"]:
            for dct, tp in [(lm_english,"english"), (lm_native, "native")]:
                user_input=prepare_user_input(d["english"],d[code], dct[lan])
                if tp=="english":
                    system_prompt_=system_prompt.format(LANGUAGE=lm_english[lan])
                    second_prompt_=second_prompt
                else:
                    system_prompt_=prompts[system_prompt]
                    second_prompt_=prompts[second_prompt] 
                history=[{"role":"user","content":user_input}]      
                cot=call_gpt4_api(history, system_prompt_, repeat=1)
                history.append({"role":"assistant","content":cot})
                history.append({"role":"user","content":second_prompt_})
                res="xxx"
                repeats=20
                while res[0].upper() not in ["1","2","3","4","5"]:
                    if repeats==0:
                        res="0"
                        break
                    repeats-=1
                    res=call_gpt4_api(history, system_prompt_, repeat=1)
                inst[code+"_"+tp]=int(res[0])
                inst[code+"_"+tp+"_reasoning"]=cot
        d["GPT"]=inst
        dump(data, open(argv[1], "w"), indent=4)

            