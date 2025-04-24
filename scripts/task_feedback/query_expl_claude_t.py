import anthropic
import keys
from tqdm import tqdm
from time import sleep
from random import choice
client = anthropic.Anthropic(api_key=keys.claude)
def call_claude_api(history, prompt, model="claude-3-7-sonnet-20250219", repeat: int = 1, retries: int = 6):
    try:
        response = client.messages.create(
            model=model,
            messages=history,
            max_tokens=1024
        )
    except Exception as e:
        print(e)
        if retries==0:
            pass
        sleep(2**(8-retries))
        return call_claude_api(history, prompt, model, repeat, retries-1)
    return response.content[0].text

system_prompt = "You are an expert math tutor who specializes in providing precise and helpful feedback for grade-school level math questions. Your task is to select the correct explanation for a student's given answer to a multiple-choice math question.\n\nYou will be provided with:\n- A math question\n- A specific answer chosen by the student (which can be correct or incorrect).\n - Four possible explanations (labelled A, B, C, and D). \nYour selected explanation should accurately correspond to the given answer. Provide your reasoning for selecting the explanation."
second_prompt = "Now based on your above explanation, output the option corresponding to the correct misconception. Only say 'A', 'B', 'C', or 'D' without any other text. Do not say anything else."
count=0
def prepare_user_input(data):
    global count
    count+=1
    count=count % 4
    res="Question: "+data["question"]+"\n"
    res+="Selected Answer: "+data["selected_answer"]+"\n"
    explanations=data["other_answer_explanation"]+[data["correct_answer_explanation"]]
    ans=count
    explanations.insert(ans, data["selected_answer_explanation"])
    explanations="\n".join("ABCD"[i]+": "+explanations[i] for i in range(4))
    res+="Feedbacks:\n"+explanations
    return res,"ABCD"[ans]

if __name__=="__main__":
    from sys import argv
    from json import load,dump
    # languages=["cs","hi","te","fa","uk","ar"]
    # lan="en"
    # for l in languages:
    #     if "_"+l+"_" in argv[1]:
    #         lan=l
    # prompts=load(open(f"prompts_{lan}.json"))
    # system_prompt=prompts[system_prompt]
    # second_prompt=prompts[second_prompt]
    data=load(open(argv[1]))
    for d in tqdm(data):
        if "Claudee" in d:
            continue
        user_input,answer=prepare_user_input(d)
        history=[{"role":"user","content":user_input}]
        cot=call_claude_api(history, system_prompt, repeat=1)
        history.append({"role":"assistant","content":cot})
        history.append({"role":"user","content":second_prompt})
        res="xxx"
        repeats=20

        while res[0].upper() not in ["A","B","C","D"]:
            if repeats==0:
                res="E"
                break
            repeats-=1
            res=call_claude_api(history, second_prompt, repeat=1)
        d["Claudee"]={"answer":res[0].upper(), "correct":answer, "reasoning":cot}
        dump(data, open(argv[1], "w"), indent=4)




