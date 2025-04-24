"""src.llm_baseline"""
import argparse
import json
import time
from tqdm import tqdm as tqdm

from src.helper.history import History
from src.helper.message import Message
from src.helper.students import GPTStudent
from src.helper.teachers import GPTTeacher, GeminiTeacher, MistralTeacher, LlamaTeacher, ClaudeTeacher, CohereTeacher
from src.helper.utils import read_jsonl

from src.model.load_key import *
from .params import *

STUDENT_INIT_ANSWER = {
    "en": "Hello teacher, I've solved the question.",
    "hi": "नमस्ते शिक्षक, मैंने प्रश्न हल कर लिया है।",
    "te": "నమస్కారం గురువుగారు, నేను ప్రశ్నను పరిష్కరించాను.",
    "cs": "Dobrý den paní učitelko, otázku jsem vyřešil.",
    "fa": "سلام استاد من سوال رو حل کردم",
    "uk": "Привіт вчителю, я розв'язав питання.",
    "ar": "مرحباً أستاذي، لقد قمت بحل السؤال.",
}

TEACHER_INIT_ANSWER = {
    "en": "Hi! Could you walk me through your solution?",
    "hi": "नमस्ते! क्या आप मुझे अपना समाधान बता सकते हैं?",
    "te": "హాయ్! మీరు మీ పరిష్కారం ద్వారా నన్ను నడిపించగలరా?",
    "cs": "Ahoj! Mohl byste mě provést vaším řešením?",
    "fa": "سلام! آیا می توانید راه حل خود را به من راهنمایی کنید؟",
    "uk": "привіт Чи могли б ви ознайомити мене зі своїм рішенням?",
    "ar": "مرحباً! هل يمكنك شرح الحل الذي توصلت إليه؟"
}

TEACHER_IN_LANGS = {
    "en": "Teacher",      # English
    "fa": "معلم",         # Persian (fa)
    "uk": "вчитель",      # Ukrainian (uk)
    "cs": "Učitel",       # Czech (cs)
    "te": "ఉపాధ్యాయుడు",  # Telugu (te)
    "hi": "शिक्षक",        # Hindi (hi)
    "ar": "مدرس"
}

STUDENT_IN_LANGS = {
    "en": "Student",      # English
    "fa": "دانش آموز",    # Persian (fa) 
    "uk": "Студент",     # Ukrainian (uk)
    "cs": "Student",      # Czech (cs)
    "te": "విద్యార్థి",   # Telugu (te)
    "hi": "छात्र",        # Hindi (hi)
    "ar": "طالب",
}


def export_to_jsonl(data, output_file):
    with open(output_file, 'a', encoding='utf-8') as output_file:
        for conversation in data:
            output_file.write(json.dumps(conversation, ensure_ascii=False) + '\n')


def get_teacher(lang: str):
    if modelName.startswith('gpt'):
        return GPTTeacher(GPT_KEY_SAN, lang, modelName)
    elif modelName.startswith('gemini'):
        return GeminiTeacher(Google_KEY_VAN, lang, modelName)
    elif 'mistral' in modelName:
        return MistralTeacher(Mistral_KEY_VAN, lang, modelName)
    elif 'mixtral' in modelName:
        return MistralTeacher(Mistral_KEY_VAN, lang, modelName)
    elif 'llama' in modelName:
        return LlamaTeacher(Fireworks_KEY_VAN, lang, modelName)
    elif modelName.startswith('claude'):
        return ClaudeTeacher(Anthropic_KEY, lang, modelName)
    elif modelName.startswith("command") or "cohere" in modelName:
        return CohereTeacher(Cohere_KEY, lang, modelName)
    else:
        raise ValueError("Unknown model name")


def print_conversation(question: str, ground_truth_solution: str, incorrect_solution: str, history: History):
    print("\n\n## Conversation")
    print(f"Question: {question}")
    print(f"Correct solution: {ground_truth_solution}")
    print(f"Incorrect solution: {incorrect_solution}")
    print(history)


if __name__ == '__main__':
    
    processed_ctr = 0

    for lang in LANGS:
        student = GPTStudent(lang)
        teacher = get_teacher("en")

        input_file = f"data/processed/test_{lang}.jsonl"
        temp_modelName = modelName.split("/")[-1]
        export_file = f"out/results/test_{lang}_{temp_modelName}.jsonl"

        data = read_jsonl(input_file)
        num_points = len(data) if num_sample_points == 0 else num_sample_points
        print(f"\n\n### Evaluating {lang.upper()} ({num_points - start_idx} data points)")

        processed_ctr = 0

        for i in tqdm(range(start_idx, num_points)):

            conversations = []
            time.sleep(5)
            problem = data[i]
            question = problem["question"]
            ground_truth_solution = problem["ground_truth"]
            incorrect_solution = problem["student_incorrect_solution"]

            history = History()
            student.reset()
            teacher.reset()
            if modelName.startswith('claude'): # Needed as Claude expects first message to be from "user", and teacher's the assistant from its pov
                history.add_message(Message(
                    STUDENT_IN_LANGS["en"], STUDENT_INIT_ANSWER[lang]))
            history.add_message(Message(
                TEACHER_IN_LANGS["en"], TEACHER_INIT_ANSWER[lang]))

            done = False

            for j in range(max_utterances):
                time.sleep(5)
                student_response = student.response(
                    history, question, incorrect_solution, "en")
                if student_response == None:
                    print("Error with student response. Skipping this data point")
                    break
                student_message = Message(STUDENT_IN_LANGS["en"], student_response)
                history.add_message(student_message)

                teacher_response = teacher.response_with_stop(
                    history, question, ground_truth_solution, "en")
                teacher_message = Message(TEACHER_IN_LANGS["en"], teacher_response)
                history.add_message(teacher_message)

                if "No response from Gemini" in teacher_response:
                    done = True
                    print("Teacher stopped responding. Terminating run for this question")
                    break

            if j == max_utterances-1 or done:

                processed_ctr += 1
                problem[modelName] = history.to_delimited_string("<EOM>")
                conversations.append(problem)

                export_to_jsonl(conversations, export_file)
                conversations.clear()

        print("Total data points processed:", processed_ctr)
