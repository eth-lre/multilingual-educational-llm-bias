import json
from re import search
from typing import List
import os

from src.helper.utils import read_jsonl

# Configuration
OUTPUT_FOLDER = "/cluster/project/sachan/vansh/practicalWork/MathDial-Multilingual/out/results"
SAVE_FOLDER = "/cluster/project/sachan/vansh/practicalWork/MathDial-Multilingual/out/evals"
MAX_K = 5
MODEL_NAME_MAP = {
    "claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
    "gpt-4o": "gpt-4o",
    "gemini-2": "gemini-2.0-flash",
    "llama-v3p1-405b-instruct": "accounts/fireworks/models/llama-v3p1-405b-instruct",
    "mistral-large-latest": "mistral-large-latest",
    "cohere-command-a": "command-a-03-2025",
}


def findall(regexp: str, text: str):
    matches = []
    while True:
        res = search(regexp, text)
        if res:
            matches.append(text[res.start():res.end()])
            text = text[res.end():]
        else:
            break
    return matches


def _is_float(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_match(text: str, gt_answer: str):
    all_numbers = findall(r'[0-9]+(\.[0-9]+)?', text.replace(",", ""))
    answer = gt_answer.replace(",", "")
    if _is_float(answer):
        float_answer = float(answer)
        for number in all_numbers:
            if _is_float(number):
                float_number = float(number)
                if abs(float_answer - float_number) < 1e-7:
                    return True
    else:
        return answer in all_numbers


def all_match(role: str, conversation: List[str], answer: str) -> float:
    count = 0
    for utterance in conversation:
        utterance = utterance.strip().strip("\n")
        if utterance.startswith(role):
            if get_match(utterance, answer):
                return count
            count += 1.
    return float('inf')


def evaluate_at_k(utterances_list: List[str], answer, k) -> (bool, bool):
    student = all_match("Student" + ":", utterances_list, answer)
    teacher = all_match("Teacher" + ":", utterances_list, answer)
    is_success_at_k = student <= k
    is_telling_at_k = teacher <= min(student, k)
    return is_success_at_k, is_telling_at_k


if __name__ == '__main__':
    for filename in os.listdir(OUTPUT_FOLDER):
        if filename.startswith("test_") and filename.endswith(".jsonl"):
            # Extract model name and language code from the filename
            parts = filename.split("_")
            language_code = parts[1]
            model_key = parts[2].split(".")[0]
            model_name = MODEL_NAME_MAP.get(model_key, model_key)

            # Load data
            input_file = os.path.join(OUTPUT_FOLDER, filename)
            data = read_jsonl(input_file)

            dataset_success_at_k = [0] * (MAX_K + 1)
            dataset_telling_at_k = [0] * (MAX_K + 1)
            tutoring_at_k = [0] * (MAX_K + 1)

            for problem in data:
                for k_point in range(1, MAX_K + 1):
                    conversation_utterances_list = problem[model_name].split(
                        "<EOM>")

                    # Ground truth is in the last line of the ground truth solution
                    ground_truth_solution = problem["ground_truth"].split(
                        "\n")[-1].strip()
                    numerical_solution = ground_truth_solution.split("\\n")[-1].strip()

                    success_at_k, telling_at_k = evaluate_at_k(
                        conversation_utterances_list, numerical_solution, k_point)
                    dataset_success_at_k[k_point] += success_at_k / len(data)
                    dataset_telling_at_k[k_point] += telling_at_k / len(data)
                    temp_S, temp_T = dataset_success_at_k[k_point], dataset_telling_at_k[k_point]
                    tutoring_at_k[k_point] = 2*temp_S*(temp_S-temp_T)/(2*temp_S-temp_T + 1e-4)

            results = {
                "success_at_k": dataset_success_at_k[1:],  # Remove index 0 (unused)
                "telling_at_k": dataset_telling_at_k[1:],
                "tutoring_at_k": tutoring_at_k[1:]
            }

            # Save as JSON
            output_file = os.path.join(SAVE_FOLDER, filename.replace(".jsonl", ".json"))
            with open(output_file, "w") as f:
                json.dump(results, f, indent=4)

            print(f"Saved results to {output_file}")