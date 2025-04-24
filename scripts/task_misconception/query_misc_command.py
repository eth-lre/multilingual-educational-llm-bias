import cohere
import keys
from tqdm import tqdm
from time import sleep
co = cohere.ClientV2(keys.cohere)
from random import choice
def call_cohere_api(history, prompt, model="command-a-03-2025", repeat: int = 1, retries: int = 6):
    try:
        response = co.chat(
            model=model,
            messages=[{"role": "system", "content": prompt}, *history],
            temperature=0
        )
    except Exception as e:
        print(e)
        if retries==0:
            pass
        sleep(2**(8-retries))
        return call_cohere_api(history, prompt, model, repeat, retries-1)
    # print(response)
    return response.message.content[0].text

system_prompt = "You are an expert math tutor who knows about all grade-school level math misconceptions. Your task is to select the accurate type of misconceptions your student has based on the (incorrect) answer he/she gives to a multiple-choice math question. You will be given 4 misconceptions types. Your selected misconception type should correspond to the given question and answer. Explain your reasoning"
second_prompt = "Now based on your above explanation, output the option corresponding to the correct misconception. Only say 'A', 'B', 'C', or 'D' without any other text. Do not say anything else."
count=0
def prepare_user_input(data):
    global count
    count+=1
    count=count % 4
    res="Question: "+data["question"]+"\n"
    res+="Selected Answer: "+data["selected_answer"]+"\n"
    misconceptions=data["other_misconceptions"]
    misconception=data["misconception"]
    ans=count
    if misconception in misconceptions:
        ans=misconceptions.index(misconception)
    misconceptions[ans]=data["misconception"]
    misconceptions="\n".join("ABCD"[i]+": "+misconceptions[i] for i in range(4))
    res+="Misconceptions:\n"+misconceptions
    return res,"ABCD"[ans]

if __name__=="__main__":
    from sys import argv
    from json import load,dump
    data=load(open(argv[1]))
    for d in tqdm(data):
        if "Command" in d:
            continue
        user_input,answer=prepare_user_input(d)
        history=[{"role":"user","content":user_input}]
        cot=call_cohere_api(history, system_prompt, repeat=1)
        history.append({"role":"assistant","content":cot})
        history.append({"role":"user","content":second_prompt})
        res="xxx"
        repeats=20

        while res[0].upper() not in ["A","B","C","D"]:
            if repeats==0:
                res="E"
                break
            repeats-=1
            res=call_cohere_api(history, second_prompt, repeat=1)
        d["Command"]={"answer":res[0].upper(), "correct":answer, "reasoning":cot}
        dump(data, open(argv[1], "w"), indent=4)




