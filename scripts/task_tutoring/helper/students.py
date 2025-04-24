import openai
import time

from .history import History

from src.model.load_key import GPT_KEY_SAN

STUDENT_PROMPT = {
    "en": """
Student Persona: (STUDENT PERSONA)

Math problem: (MATH PROBLEM)

Student solution: (STUDENT SOLUTION)

Context: You need to role-play the student, (STUDENT NAME), while the user roleplays the tutor. (STUDENT NAME) thinks their answer is correct. Only when the teacher provides several good reasoning questions, (STUDENT NAME) understands the problem and corrects the solution. (STUDENT NAME) can use calculator and thus makes no calculation errors. Send <EOM> tag at end of the student message.

(DIALOG HISTORY)

Student:
""",

    "fa": """
شخصیت دانشجویی: (STUDENT PERSONA)

مسئله ریاضی: (MATH PROBLEM)

راه حل دانشجویی: (STUDENT SOLUTION)

زمینه: شما باید نقش دانش‌آموز، (STUDENT NAME)، را بازی کنید، در حالی که کاربر نقش معلم را بازی می‌کند. (STUDENT NAME) فکر می کند که پاسخ آنها صحیح است. فقط زمانی که معلم چندین سؤال استدلالی خوب ارائه می دهد (STUDENT NAME) مسئله را می فهمد و راه حل را تصحیح می کند. (STUDENT NAME) می تواند از ماشین حساب استفاده کند و در نتیجه هیچ خطای محاسباتی ایجاد نمی کند. برچسب <EOM> را در انتهای پیام دانش آموز ارسال کنید.

(DIALOG HISTORY)

دانش آموز:
""",

    "uk": """
Персона студента: (STUDENT PERSONA)

Математична задача: (MATH PROBLEM)

Студентське рішення: (STUDENT SOLUTION)

Контекст: Вам потрібно зіграти роль студента, (STUDENT NAME), тоді як користувач гратиме роль вчителя. (STUDENT NAME) вважає свою відповідь правильною. Лише коли вчитель дає кілька аргументованих запитань, (STUDENT NAME) розуміє проблему та виправляє рішення. (STUDENT NAME) вміє користуватися калькулятором і тому не допускає помилок у розрахунках. Надішліть тег <EOM> у кінці повідомлення студента.

(DIALOG HISTORY)

студент:
""",

    "cs": """
Studentská osoba: (STUDENT PERSONA)

Matematický problém: (MATH PROBLEM)

Studentské řešení: (STUDENT SOLUTION)

Kontext: Musíte hrát roli studenta, (STUDENT NAME), zatímco uživatel hraje roli učitele. (STUDENT NAME) si myslí, že jejich odpověď je správná. Pouze tehdy, když učitel položí několik otázek s dobrým uvažováním, (STUDENT NAME) pochopí problém a opraví řešení. (STUDENT NAME) umí používat kalkulačku, a proto nedělá žádné chyby ve výpočtu. Na konci studentské zprávy odešlete značku <EOM>.

(DIALOG HISTORY)

Student:
""",

    "te": """
విద్యార్థి వ్యక్తిత్వం: (STUDENT PERSONA)

గణిత సమస్య: (MATH PROBLEM)

విద్యార్థి పరిష్కారం: (STUDENT SOLUTION)

సందర్భం: మీరు (STUDENT NAME) అనే విద్యార్థిగా పాత్ర పోషించాలి, ఇక యూజర్ ఉపాధ్యాయుడిగా పాత్ర పోషిస్తారు। (STUDENT NAME) వారి సమాధానం సరైనదని భావిస్తున్నారు. ఉపాధ్యాయుడు అనేక మంచి తార్కిక ప్రశ్నలను అందించినప్పుడు మాత్రమే, (STUDENT NAME) సమస్యను అర్థం చేసుకుని, పరిష్కారాన్ని సరిచేస్తాడు. (STUDENT NAME) కాలిక్యులేటర్‌ని ఉపయోగించవచ్చు మరియు దీని వలన గణన లోపాలు ఉండవు. విద్యార్థి సందేశం చివర <EOM> ట్యాగ్‌ని పంపండి.

(DIALOG HISTORY)

విద్యార్థి:
""",

    "hi": """
छात्र व्यक्तित्व: (STUDENT PERSONA)

गणित समस्या: (MATH PROBLEM)

छात्र समाधान: (STUDENT SOLUTION)

संदर्भ: आपको छात्र (STUDENT NAME) की भूमिका निभानी है, जबकि उपयोगकर्ता शिक्षक की भूमिका निभाएगा। (STUDENT NAME) को लगता है कि उनका उत्तर सही है। केवल जब शिक्षक कई अच्छे तर्क प्रश्न प्रदान करता है, (STUDENT NAME) समस्या को समझता है और समाधान को सही करता है। (STUDENT NAME) कैलकुलेटर का उपयोग कर सकता है और इस प्रकार कोई गणना त्रुटि नहीं करता है। छात्र संदेश के अंत में <EOM> टैग भेजें।

(DIALOG HISTORY)

छात्र:
""",

    "ar": """
    شخصية الطالب: (STUDENT PERSONA)

مسألة رياضية: (MATH PROBLEM)

حل الطالب: (STUDENT SOLUTION)

السياق: عليك تمثيل دور الطالب (STUDENT NAME)، بينما يقوم المستخدم بدور المعلم. يعتقد (STUDENT NAME) أن إجابته صحيحة. فقط عندما يطرح المعلم عدة أسئلة منطقية جيدة، يفهم (STUDENT NAME) المسألة ويصحح الحل. يستطيع (STUDENT NAME) استخدام الآلة الحاسبة، وبالتالي لا يرتكب أي أخطاء حسابية. أرسل وسم <EOM> في نهاية رسالة الطالب.

(DIALOG HISTORY)

الطالب:
"""
}


STUDENT_NAME = {
    "en": "Kayla",
    "fa": "کایلا",
    "uk": "Кайла",
    "cs": "Kayla",
    "te": "కైలా",
    "hi": "कायला",
    "ar": "كايلا",
}
STUDENT_PERSONA = {
    "en": "Kayla is a 7th grade student. She has problem with understanding of what steps or procedures are required to solve a problem.",
    "fa": "کایلا دانش آموز کلاس هفتم است. او با درک اینکه چه مراحل یا رویه هایی برای حل یک مشکل نیاز است مشکل دارد.",
    "uk": "Кайла є ученицею 7-го класу. Вона має проблеми з розумінням того, які кроки або процедури потрібні для вирішення проблеми.",
    "cs": "Kayla je studentkou 7. třídy. Má problém pochopit, jaké kroky nebo postupy jsou nutné k vyřešení problému.",
    "te": "కైలా 7వ తరగతి విద్యార్థిని. సమస్యను పరిష్కరించడానికి ఎలాంటి చర్యలు లేదా విధానాలు అవసరమో అర్థం చేసుకోవడంలో ఆమెకు సమస్య ఉంది.",
    "hi": "कायला 7वीं कक्षा की छात्रा है। उसे यह समझने में समस्या है कि किसी समस्या को हल करने के लिए कौन से चरण या प्रक्रियाएँ आवश्यक हैं।",
    "ar": "كايلا طالبة في الصف السابع. تواجه صعوبة في فهم الخطوات أو الإجراءات اللازمة لحل مشكلة ما."
}

STOP_STUDENT_IN_LANGS = [
    "Student:",      # English
    "student:",
    "دانش آموز:",    # Persian (fa)
    "студент:",      # Ukrainian (uk)
    "Студент:",
    "Student:",      # Czech (cs)
    "student:",
    "విద్యార్థి:",   # Telugu (te)
    "छात्र:",        # Hindi (hi)
    "طالب:"         # Arabic (ar)
]

STOP_TEACHER_IN_LANGS = [
    "Teacher:",      # English
    "teacher:",
    "معلم:",         # Persian (fa)
    "вчитель:",      # Ukrainian (uk)
    "Učitel:",       # Czech (cs)
    "učitel:",
    "ఉపాధ్యాయుడు:",  # Telugu (te)
    "शिक्षक:",        # Hindi (hi)
    "مدرس:"         # Arabic (ar)
]

STUDENT_IN_LANGS = {
    "en": "Student",      # English
    "fa": "دانش آموز",    # Persian (fa) 
    "uk": "Студент",     # Ukrainian (uk)
    "cs": "Student",      # Czech (cs)
    "te": "విద్యార్థి",   # Telugu (te)
    "hi": "छात्र",        # Hindi (hi)
    "ar": "طالب",
}

ROLE_MAPPING = {
    "Teacher": "user",
    "معلم": "user",
    "вчитель": "user",
    "Učitel": "user",
    "ఉపాధ్యాయుడు": "user",
    "शिक्षक": "user",
    "مدرس": "user",    

    "Student": "assistant",
    "دانش آموز": "assistant",
    "Студент": "assistant",
    "విద్యార్థి": "assistant",
    "छात्र": "assistant",
    "طالب": "assistant",
}

class GPTStudent(object):
    def __init__(self, lang: str):
        self.persona = STUDENT_IN_LANGS[lang]
        self.name = STUDENT_NAME[lang]
        self.key = GPT_KEY_SAN

    def reset(self):
        pass

    def response(self, history: History, question: str, incorrect_solution: str, lang: str):
        response = ""
        user_messages = messages = history.to_llm_messages(ROLE_MAPPING, llm_format="gpt")
        student_prompt = STUDENT_PROMPT[lang].replace("(STUDENT PERSONA)", STUDENT_PERSONA[lang]).replace("(STUDENT SOLUTION)",
                                                                                             incorrect_solution).replace(
            "(MATH PROBLEM)", question).replace("(STUDENT NAME)", STUDENT_NAME[lang]).replace(
            "(DIALOG HISTORY)", "")
        messages = [{"role": "system", "content": student_prompt}, *user_messages]
        errors_counter = 0
        global_err = None
        done = False
        while (done==False and errors_counter<5):
            if (errors_counter>0):
                print(f"\nERROR: Student model (GPT-4o-mini) ran into an ERROR ({global_err}). Starting {errors_counter+1}th time")
            try:
                openai.api_key = self.key
                response = openai.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages = messages,
                    temperature=0.4,
                    # max_tokens=512,
                )
                response = response.choices[0].message.content.strip()
                for stop_sequence in STOP_TEACHER_IN_LANGS:
                    pos = response.find(stop_sequence)
                    if pos != -1:
                        return response[:pos]
                done = True
            except Exception as e:
                global_err = e
                errors_counter += 1
                time.sleep(10)
        for stop_stud in STOP_STUDENT_IN_LANGS:
            response = response.replace(stop_stud, "")
        utterance = response.replace(STUDENT_NAME[lang] + ":", "").replace("<EOM>", "").strip(
            "\n")
        if errors_counter==5:
            return None
        return utterance
