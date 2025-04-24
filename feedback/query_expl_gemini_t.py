from google import genai
import keys
from tqdm import tqdm
from time import sleep
client=genai.Client(api_key=keys.google)
from random import choice

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
    languages=["cs","hi","te","fa","uk","ar"]
    lan="en"
    for l in languages:
        if "_"+l+"_" in argv[1]:
            lan=l
    prompts=load(open(f"prompts_{lan}.json"))
    system_prompt=prompts[system_prompt]
    second_prompt=prompts[second_prompt]
    data=load(open(argv[1]))
    for d in tqdm(data):
        if "Geminie_t" in d:
            continue
        user_input,answer=prepare_user_input(d)
        repeat=3
        while repeat>0:
            try:
                cot = client.models.generate_content(
                        model="gemini-2.0-flash",
                        config=genai.types.GenerateContentConfig(
                            system_instruction=system_prompt),
                        contents=[user_input],
                    ).text.strip()
                break
            except Exception as e:
                print(e)
                repeat-=1
                sleep(2**(8-repeat))

        res="xxx"
        repeats=20
        while res[0].upper() not in ["A","B","C","D"]:
            if repeats==0:
                res="E"
                break
            repeats-=1
            try:
                res = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt),
                    contents=[prompts["You have previously given the following answer and explanation:"]+"\n"+cot+"\n"+second_prompt],
                ).text.strip()
            except Exception as e:
                print(e)
        d["Geminie_t"]={"answer":res[0].upper(), "correct":answer, "reasoning":cot}
        dump(data, open(argv[1], "w"), indent=4)

            