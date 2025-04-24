# %%

MODELS = ["GPT4o", "LLama", "Claude", "Gemini", "Mistral", "Cmd-A"]

TASK_MISCONCEPTIONS = {
    "english_prompt": """
English	976	962	951	940	950	953
Hindi	945'	932'	919'	898'	918'	932'
Czech	969	951	945	923	945	941
Ukranian	957'	949	929'	933	944	949
Telugu	952'	922'	899'	869'	897'	855*
Farsi	948'	933'	930'	875'	927'	931'
Arabic	959'	930'	920'	860*	926'	934'
""",
    "translated_prompt": """
English	976	962	951	940	950	953
Hindi	955'	936'	896'	904'	906'	914'
Czech	966	958	702**	816*	410**	945
Ukranian	956'	943'	566**	904'	942	939
Telugu	942'	908'	686**	836*	355**	779**
Farsi	951'	944'	680**	883'	669**	936'
Arabic	959'	930'	928'	909'	920'	940
"""
}
ERROR_MISCONCEPTIONS = {
    "english_prompt": """
English	0	7	1	21	0	9
Hindi	0	16	4	23	0	4
Czech	1	16	1	19	0	7
Ukranian	1	16	1	22	0	3
Telugu	0	1	0	22	0	4
Farsi	0	18	2	20	0	3
Arabic	1	17	2	21	0	2
""",
    "translated_prompt": """
English	0	7	1	21	0	9
Hindi	0	9	2	25	0	1
Czech	0	14	0	7	0	5
Ukranian	0	18	4	16	0	1
Telugu	0	3	1	17	0	0
Farsi	0	16	2	29	0	1
Arabic	0	11	3	22	0	1
"""
}
TASK_FEEDBACK = {
    "english_prompt": """
English	534	382	170	511	485	397
Hindi	487'	356	130'	436'	405'	316'
Czech	499	378	141'	465'	416'	307*
Ukranian	503	332'	130'	448'	413'	322'
Telugu	452'	276*	104'	434'	340**	263*
Farsi	502	279*	113'	449'	413'	309*
Arabic	496'	287*	139'	453'	388*	333'
""",
    "translated_prompt": """
English	534	382	170	511	485	397
Hindi	321**	134**	62*	443'	186**	188**
Czech	427*	261*	192	466'	355*	356'
Ukranian	359**	196**	81*	528	310**	272*
Telugu	139**	127**	61*	377*	155**	95**
Farsi	459'	316'	163	440'	335**	355'
Arabic	488'	107**	163	481	278**	289*
"""
}
ERROR_FEEDBACK = {
    "english_prompt": """
English	0	3	0	13	0	0
Hindi	0	0	0	11	0	1
Czech	0	0	0	11	0	0
Ukranian	0	0	0	9	0	0
Telugu	0	0	0	17	0	1
Farsi	0	0	0	12	0	0
Arabic	0	0	0	15	0	1
""",
    "translated_prompt": """
English	0	3	0	13	0	0
Hindi	0	0	0	10	0	2
Czech	0	0	0	30	0	0
Ukranian	0	0	0	13	0	0
Telugu	0	2	0	18	0	1
Farsi	0	0	0	11	0	1
Arabic	0	0	0	21	0	2
"""
}
CORRECT_FEEDBACK = {
    "english_prompt": """
English	237	458	750	278	230	351
Hindi	303	423	796	349	299	479
Czech	279	395	802	302	318	490
Ukranian	273	494	803	327	335	452
Telugu	292	556	815	352	331	524
Farsi	285	525	825	316	326	455
Arabic	280	541	795	353	329	440
""",
    "translated_prompt": """
English	237	458	750	278	230	351
Hindi	555	789	877	332	689	713
Czech	349	595	678	230	331	380
Ukranian	473	697	871	207	467	497
Telugu	783	738	895	379	709	788
Farsi	216	521	751	293	303	289
Arabic	219	817	736	224	364	495
"""
}

TASK_TRANSLATIONS = {
    "english_prompt": """
Hindi	915	741	921	776	824	779
Czech	987	983	989	983	975	988
Ukranian	980	973	969	965	973	983
Telugu	772	337	810	519	487	252
Farsi	953	935	960	964	923	966
Arabic	986	979	992	988	975	990
""",
    "translated_prompt": """
Hindi	938	885	565	865	876	813
Czech	993	988	808	987	995	992
Ukranian	981	979	853	977	984	982
Telugu	828	468	407	821	671	156
Farsi	968	960	670	964	941	962
Arabic	988	983	672	986	978	979
"""
}
ERROR_TRANSLATIONS = {
    "english_prompt": """
Hindi	0	0	0	0	0	0
Czech	0	0	0	0	0	0
Ukranian	0	0	0	0	0	0
Telugu	0	0	0	0	0	0
Farsi	0	0	0	0	0	0
Arabic	0	0	0	0	0	0
""",
    "translated_prompt": """			
Hindi	0	0	2	0	0	0
Czech	0	0	28	0	0	0
Ukranian	0	0	15	0	0	0
Telugu	0	0	5	0	0	0
Farsi	0	0	0	0	0	0
Arabic	0	0	37	0	0	0
"""
}
TASK_TUTORING = {
    "english_prompt": """
English	947	970	221	930	820	955
Hindi	905	927	242	722*	735	884'
Czech	438**	441**	172	702	29**	215**
Ukranian	912	915	235	812'	715	909
Telugu	501**	395**	277	589'	29**	407**
Farsi	856'	813*	287	772	658'	778'
Arabic	914	897	243	842'	752	874
"""
}
EXTRA_TUTORING = {
    "english_prompt": """
English	960 25	975 10	965 840	935 10	820 0	960 10
Hindi	950 85	930' 5	895* 755	775** 100	735* 0	910 50
Czech	655** 325	735** 420	900' 805	715** 25	525** 510	770 645
Ukranian	930' 35	920' 10	915' 780	840* 55	715* 0	935 50
Telugu	775** 405	775** 510	855* 690	610** 40	590** 575	635 335
Farsi	890* 65	875* 115	915' 745	780** 15	695* 70	910 230
Arabic	945 59	900 5	910 770	860 35	755 5	930 105
"""
}

def format_cell(value, min, max, base_color):
    extra = ""
    if "'" in value:
        extra = r"$\cdot$ "
    elif "**" in value:
        extra = r"$\bigstar$"
    elif "*" in value:
        extra = r"$\star$ "
    value = int(value.strip("'*"))/1000
    value_color = (value - min) / (max - min) * 100 * 0.5
    return f"\\cellcolor{{{base_color}!{value_color:.0f}}} {extra}{value:.1%}".replace("%", r"\%")

def process_table(data_txt_1, data_txt_2, base_color, min=0.3, max=1.0):
    # print latex table
    print(r"\begin{tabular}{", "l" + "r"*len(MODELS) + r"@{\hspace{2mm}}c" + "r" * len(MODELS), "}")
    print(r"\toprule")
    print(
        r"& \multicolumn{", len(MODELS), r"}{c}{\bf English prompt}",
        r"&& \multicolumn{", len(MODELS), r"}{c}{\bf Translated prompt}",
        "\\\\"
    )
    print(r"\textbf{Language}", *MODELS, "", *MODELS, sep=r" & \bf ", end="\\\\\n")
    print(r"\midrule")
    for line_1, line_2 in zip(data_txt_1.strip().split("\n"), data_txt_2.strip().split("\n")):
        lang, *scores_1 = line_1.split("\t")
        _lang, *scores_2 = line_2.split("\t")
        assert lang == _lang
        print(
            lang,
            *[format_cell(score, min=min, max=max, base_color=base_color) for score in scores_1],
            "",
            *[format_cell(score, min=min, max=max, base_color=base_color) for score in scores_2],
            sep=" & ",
            end="\\\\\n"
        )
    print(r"\bottomrule")
    print(r"\end{tabular}")


def format_cell_extra(value, value1, value2, min, max, base_color):
    value = int(value.strip("'*"))/1000
    value_color = (value - min) / (max - min) * 100 * 0.5
    value1 = int(value1.strip("'*"))/1000
    value2 = 1-int(value2.strip("'*"))/1000
    return f"\\cellcolor{{{base_color}!{value_color:.0f}}} {value1*100:.1f}/{1-value2:.1%}".replace("%", r"\%")



def process_table_extra(data_txt_1, data_txt_2, base_color, min=0.3, max=1.0):
    # print latex table
    print(r"\begin{tabular}{", "l" + "r"*len(MODELS) + r"@{\hspace{1mm}}c" + "r" * len(MODELS), "}")
    print(r"\toprule")
    print(
        r"& \multicolumn{", len(MODELS), r"}{c}{\bf Harmonic mean}",
        r"&& \multicolumn{", len(MODELS), r"}{c}{\bf Success/1-Telling}",
        "\\\\"
    )
    print(r"", *MODELS, "", *MODELS, sep=r" & \bf ", end="\\\\\n")
    print(r"\midrule")
    for line_1, line_2 in zip(data_txt_1.strip().split("\n"), data_txt_2.strip().split("\n")):
        lang, *scores_1 = line_1.split("\t")
        _lang, *scores_2 = line_2.split("\t")
        # assert lang == _lang
        scores_2 = [score.split(" ") for score in scores_2]
        print(
            lang,
            *[format_cell(score, min=min, max=max, base_color=base_color) for score in scores_1],
            "",
            *[format_cell_extra(score, score1, score2, min=min, max=max, base_color=base_color) for score, (score1, score2) in zip(scores_1, scores_2)],
            sep=" & ",
            end="\\\\\n"
        )
    print(r"\bottomrule")
    print(r"\end{tabular}")




# process_table(TASK_MISCONCEPTIONS["english_prompt"], TASK_MISCONCEPTIONS["translated_prompt"], base_color="purple", min=0.3, max=1.0)
# process_table(TASK_FEEDBACK["english_prompt"], TASK_FEEDBACK["translated_prompt"], base_color="cyan", min=0.02, max=0.6)
# process_table_extra(TASK_TUTORING["english_prompt"], EXTRA_TUTORING["english_prompt"], base_color="orange", min=0, max=1)
# process_table(TASK_TRANSLATIONS["english_prompt"], TASK_TRANSLATIONS["translated_prompt"], base_color="green", min=0.15, max=1)


# process_table(ERROR_MISCONCEPTIONS["english_prompt"], ERROR_MISCONCEPTIONS["translated_prompt"], base_color="purple", min=0, max=0.05)
# process_table(ERROR_FEEDBACK["english_prompt"], ERROR_FEEDBACK["translated_prompt"], base_color="cyan", min=0, max=0.02)
# process_table(CORRECT_FEEDBACK["english_prompt"], CORRECT_FEEDBACK["translated_prompt"], base_color="cyan", min=0.2, max=0.9)
process_table(ERROR_TRANSLATIONS["english_prompt"], ERROR_TRANSLATIONS["translated_prompt"], base_color="green", min=0, max=0.02)