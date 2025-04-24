from .history import History
from src.model.llm import GPT, MistralClass, Llama, Gemini, Claude, Cohere

TEACHER_BASE = """A tutor and a student work together to solve the following math word problem. 
Math problem: {problem}
The correct solution is as follows:
{ground_truth}
You need to role-play the tutor while the user roleplays the student, Kayla. The tutor is a soft-spoken empathetic man who dislikes giving out direct answers to students, and instead likes to answer questions with other questions that would help the student understand the concepts, so that she can solve the problem themselves. 
Kayla has come up with a solution, but it is incorrect. Please start the conversation, one line at a time, aiming to figure out what is Kayla's solution and what is wrong with it. Then try to get her to fix it.
"""

TEACHER_BASE = {
    "en": """A tutor and a student work together to solve the following math word problem. 
Math problem: {problem}
The correct solution is as follows:
{ground_truth}
You need to role-play the tutor while the user roleplays the student, Kayla. The tutor is a soft-spoken empathetic man who dislikes giving out direct answers to students, and instead likes to answer questions with other questions that would help the student understand the concepts, so that she can solve the problem themselves. 
Kayla has come up with a solution, but it is incorrect. Please start the conversation, one line at a time, aiming to figure out what is Kayla's solution and what is wrong with it. Then try to get her to fix it.
""",
    "hi": """एक शिक्षक और एक छात्र निम्नलिखित गणित शब्द समस्या को हल करने के लिए एक साथ काम करते हैं।
गणित समस्या: {problem}
सही समाधान इस प्रकार है:
{ground_truth}
आपको शिक्षक की भूमिका निभानी होगी जबकि उपयोगकर्ता छात्र, कायला की भूमिका निभाएगा। शिक्षक एक मृदुभाषी सहानुभूतिपूर्ण व्यक्ति है जो छात्रों को सीधे उत्तर देना पसंद नहीं करता है, और इसके बजाय अन्य प्रश्नों के साथ उत्तर देना पसंद करता है जो छात्र को अवधारणाओं को समझने में मदद करेंगे, ताकि वह स्वयं समस्या को हल कर सके।
कायला ने एक समाधान निकाला है, लेकिन यह गलत है। कृपया बातचीत शुरू करें, एक बार में एक पंक्ति, यह पता लगाने के उद्देश्य से कि कायला का समाधान क्या है और इसमें क्या गलत है। फिर उसे इसे ठीक करने के लिए कहें।
""",
    "te": """క్రింది గణిత పద సమస్యను పరిష్కరించడానికి ఒక ట్యూటర్ మరియు విద్యార్థి కలిసి పని చేస్తారు.
గణిత సమస్య: {problem}
సరైన పరిష్కారం క్రింది విధంగా ఉంది:
{ground_truth}
విద్యార్థి కైలాను వినియోగదారు రోల్ ప్లే చేస్తున్నప్పుడు మీరు ట్యూటర్‌ను రోల్ ప్లే చేయాలి. ట్యూటర్ మృదు భాషా సానుభూతిగల వ్యక్తి, అతను విద్యార్థులకు నేరుగా సమాధానాలు ఇవ్వడం ఇష్టపడడు మరియు బదులుగా విద్యార్థికి భావనలను అర్థం చేసుకోవడానికి సహాయపడే ఇతర ప్రశ్నలతో ప్రశ్నలకు సమాధానం ఇవ్వడానికి ఇష్టపడతాడు, తద్వారా ఆమె సమస్యను స్వయంగా పరిష్కరించగలదు.
కైలా ఒక పరిష్కారంతో ముందుకు వచ్చింది, కానీ అది తప్పు. దయచేసి కైలా యొక్క పరిష్కారం ఏమిటి మరియు దానిలో తప్పు ఏమిటి అని గుర్తించే లక్ష్యంతో సంభాషణను ప్రారంభించండి. అప్పుడు ఆమె దాన్ని సరిదిద్దడానికి ప్రయత్నించండి.
""",
    "cs": """Lektor a student spolupracují na řešení následujícího matematického slovního problému.
Matematický problém: {problem}
Správné řešení je následující:
{ground_truth}
Musíte hrát roli učitele, zatímco uživatel hraje roli studenta Kayla. Lektor je měkký empatický muž, který nerad dává přímé odpovědi studentům a místo toho rád odpovídá na otázky jinými otázkami, které by studentce pomohly porozumět pojmům, aby mohla problém vyřešit sama.
Kayla přišla s řešením, ale není správné. Začněte prosím konverzaci, jeden řádek po druhém, s cílem zjistit, jaké je Kaylino řešení a co je na něm špatného. Pak ji zkuste přimět, aby to napravila.
""",
    "uk": """Репетитор і учень працюють разом, щоб розв'язати наведену нижче математичну текстову задачу.
Математична задача: {problem}
Правильне рішення полягає в наступному:
{ground_truth}
Вам потрібно зіграти роль репетитора, а користувач — учня Кайлу. Репетитор — це лагідна співчутлива людина, яка не любить давати студентам прямі відповіді, а натомість любить відповідати на запитання іншими запитаннями, які допоможуть студенту зрозуміти поняття, щоб він міг вирішити проблему самостійно.
Кайла придумала рішення, але воно неправильне. Будь ласка, почніть розмову по рядку за раз, намагаючись з’ясувати, що таке рішення Кейли та що з ним не так. Потім спробуйте змусити її це виправити.
""",
    "fa": """یک مربی و یک دانش آموز با هم کار می کنند تا مشکل کلمه ریاضی زیر را حل کنند.
مسئله ریاضی: {problem}
راه حل صحیح به شرح زیر است:
{ground_truth}
شما باید معلم را ایفا کنید در حالی که کاربر نقش دانش آموز، Kayla را بازی می کند. استاد راهنما مردی همدل و آرام است که از دادن پاسخ های مستقیم به دانش آموزان بدش می آید و در عوض دوست دارد به سؤالات با سؤالات دیگری پاسخ دهد که به دانش آموز در درک مفاهیم کمک کند تا خودش بتواند مشکل را حل کند.
کایلا راه حلی ارائه کرده است، اما نادرست است. لطفاً مکالمه را یک خط در یک زمان شروع کنید تا بفهمید راه حل کایلا چیست و چه اشکالی دارد. سپس سعی کنید او را وادار به رفع آن کنید.
""",
    "ar": """يعمل مُعلّم وطالبة معًا لحل مسألة رياضية كلامية.
المسألة الرياضية: {problem}
الحل الصحيح هو كما يلي:
{ground_truth}
عليك أن تُجسّد دور المُعلّم بينما يُجسّد المستخدم دور الطالبة كايلا. المُعلّم رجلٌ هادئ الكلام ومتعاطف، لا يُحبّذ إعطاء إجابات مباشرة للطلاب، بل يُفضّل الإجابة على الأسئلة بأسئلة أخرى تُساعد الطالبة على فهم المفاهيم، حتى تتمكن من حل المسألة بنفسها.
لقد توصلت كايلا إلى حل، ولكنه غير صحيح. يُرجى بدء المحادثة، سطرًا سطرًا، بهدف معرفة حل كايلا وما هو الخطأ فيه. ثم حاول إقناعها بإصلاحه.
"""
}

STOP = [
    "Student:",      # English
    "student:",
    "دانش آموز:",    # Persian (fa)
    "студент:",      # Ukrainian (uk)
    "Студент:",
    "Student:",      # Czech (cs)
    "student:",
    "విద్యార్థి:",   # Telugu (te)
    "छात्र:",        # Hindi (hi)
    "طالب:",        # Arabic (ar)
]

TEACHER_IN_LANGS = {
    "en": "Teacher",      # English
    "fa": "معلم",         # Persian (fa)
    "uk": "вчитель",      # Ukrainian (uk)
    "cs": "Učitel",       # Czech (cs)
    "te": "ఉపాధ్యాయుడు",  # Telugu (te)
    "hi": "शिक्षक",        # Hindi (hi)
    "ar": "مدرس",
}

STUDENT_IN_LANGS = {
    "en": "Student",      # English
    "fa": "دانش آموز",    # Persian (fa) 
    "uk": "Студент",     # Ukrainian (uk)
    "cs": "Student",      # Czech (cs)
    "te": "విద్యార్థి",   # Telugu (te)
    "hi": "छात्र",        # Hindi (hi)
    "ar": "طالب"
}

ROLE_MAPPING = {
    "Teacher": "assistant",
    "معلم": "assistant",
    "вчитель": "assistant",
    "Učitel": "assistant",
    "ఉపాధ్యాయుడు": "assistant",
    "शिक्षक": "assistant",
    "مدرس": "assistant",

    "Student": "user",
    "دانش آموز": "user",
    "Студент": "user",
    "విద్యార్థి": "user",
    "छात्र": "user",
    "طالب": "user",
}

class LLMTeacher(object):
    def __init__(self, lang: str):
        self.persona = TEACHER_IN_LANGS[lang]
        self.name = "GPT Robot"

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        raise NotImplementedError(
            "Should have been overridden by child class.")

    def response_with_stop(self, history: History, question: str, ground_truth_solution: str, lang: str):
        temp_response = self.response(history, question, ground_truth_solution, lang)
        for stop_sequence in STOP:
            pos = temp_response.find(stop_sequence)
            if pos != -1:
                return temp_response[:pos]

        return temp_response


class ClaudeTeacher(LLMTeacher):
    def __init__(self, key, lang, model="gpt-4o"):
        super().__init__(lang)
        self.llm = Claude(key, model)

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format( # System prompt
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="claude")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        generated_response = response[0].content[0].text.strip()
        return generated_response

class CohereTeacher(LLMTeacher):
    def __init__(self, key, lang, model="command-a-03-2025"):
        super().__init__(lang)
        self.llm = Cohere(key, model)
    
    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format(
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="gpt")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        generated_response = response[0].message.content[0].text.strip()
        return generated_response


class GeminiTeacher(LLMTeacher):
    def __init__(self, key, lang, model="gemini-1.5-pro"):
        super().__init__(lang)
        self.llm = Gemini(key, model)

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format(
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="gemini")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        generated_response = response[0].content.parts[0].text.strip()
        return generated_response


class GPTTeacher(LLMTeacher):
    def __init__(self, key, lang, model="gpt-4o"):
        super().__init__(lang)
        self.llm = GPT(key, model)

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format(
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="gpt")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        generated_response = response[0].message.content.strip()
        return generated_response


class LlamaTeacher(LLMTeacher):
    def __init__(self, key, lang, model="llama-13b-chat"):
        super().__init__(lang)
        self.llm = Llama(key, model)

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format(
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="llama")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        generated_response = response[0][0].message.content.strip()
        return generated_response


class MistralTeacher(LLMTeacher):
    def __init__(self, key, lang, model="..."):
        super().__init__(lang)
        self.llm = MistralClass(key, model)

    def reset(self):
        pass

    def response(self, history: History, question: str, ground_truth_solution: str, lang: str):
        prompt = TEACHER_BASE[lang].format(
            problem=question, ground_truth=ground_truth_solution)
        messages = history.to_llm_messages(ROLE_MAPPING, llm_format="mistral")
        response = self.llm.attempt_completion(
            messages, prompt, stop=STOP, TEMP=1)
        # NOTE: This will change if number of outputs is greater than 1
        generated_response = response[0][0].message.content.strip()
        return generated_response
