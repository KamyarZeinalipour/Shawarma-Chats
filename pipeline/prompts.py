"""Prompt templates used to build ShawarmaChats (Section 3 of the paper), kept verbatim.

Generation  (str.format, placeholder {text}):
    standard_prompt, egyptian_prompt, maghrebi_prompt    paragraph -> six-turn dialogue (JSON)
Grading     (placeholders {text}, {dialogue}):
    standard_evaluation_prompt, egy_evaluation_prompt, mag_evaluation_prompt
                                                         dialogue -> rating A-D with a reason (JSON)
Repair      (str.format, placeholders {dialogue}, {text}, {rating}, {reason}):
    std_fix_prompt, egy_fix_prompt, mag_fix_prompt        low-rated dialogue -> revised dialogue
"""

egyptian_prompt = """
Your task is to take Arabic texts and make a conversation based on the provided text, Generate a 6 turns conversation between two people. The dialogue should have the following features:
    

1.	General Framework:
• Be natural, relatable, and culturally appropriate in Egyptian Dialect Arabic.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Egyptian Dialect Arabic.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Egyptian Dialect Arabic, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Egyptian Dialect Arabic.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
• Generate the output just in Arabic Script except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent. 
• Generate The generated output of the Egyptian Dialect Arabic should be just a valid JSON object nothing else.

Output format:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
      "reference": "-Reference-"
    }},
    {{
      "speaker": "B",
      "text": -Text-,
      "reference": -Reference-
    }},
    ...
   ]
}}

Text:
{text}
"""


standard_prompt = """
Your task is to take Arabic texts and make a conversation based on the provided text, Generate a 6 turns conversation between two people. The dialogue should have the following features:
    

1   General Framework:
• Be natural, relatable, and culturally appropriate in Modern Standard Arabic.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Modern Standard Arabic.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Modern Standard Arabic, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Modern Standard Arabic.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
• Generate the output just in Arabic Script except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent. 
• Generate the generated output of the Modern Standard Arabic should be just a valid JSON object nothing else.


Output format:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
      "reference": "-Reference-"
    }},
    {{
      "speaker": "B",
      "text": -Text-,
      "reference": -Reference-
    }},
    ...
   ]
}}

Text:
{text}
"""

maghrebi_prompt = """

Your task is to take Arabic texts and make a conversation based on the provided text, Generate a 6 turns conversation between two people. The dialogue should have the following features:
    

1.	General Framework:
• Be natural, relatable, and culturally appropriate in Darija Arabic.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Darija Arabic.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Darija Arabic, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Maghrebi Darija.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
• Generate the output just in Arabic Script except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent. 
• Generate the generated output of the Maghrebi Darija should be just a valid JSON object nothing else.

Output format:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
      "reference": "-Reference-"
    }},
    {{
      "speaker": "B",
      "text": -Text-,
      "reference": -Reference-
    }},
    ...
   ]
}}

Text:
{text}
"""


general_prompt = """
Your task is to take Arabic texts and make a conversation based on the provided text, Generate a 6 turns conversation between two people. The dialogue should have the following features:
    

1.	General Framework:
• Be natural, relatable, and culturally appropriate in {dialect}.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in {dialect}.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use {dialect}, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than {dialect}.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
• Generate the output just in Arabic Script except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent. 
• Generate the generated output of the {dialect} should be just a valid JSON object nothing else.


Output format:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
      "reference": "-Reference-"
    }},
    {{
      "speaker": "B",
      "text": -Text-,
      "reference": -Reference-
    }},
    ...
   ]
}}

Text:
{text}
"""

egy_evaluation_prompt = """
You are a linguistics expert with over 20 years of experience in Arabic dialectology, and a native speaker of Egyptian Dialect Arabic.  
You will be given a Text and an AI-generated conversation in Egyptian Dialect Arabic. Your task is to evaluate AI‑generated conversations in Egyptian Dialect Arabic and assign each one a rating from A to D, using the detailed criteria below:

Rating A:  
- The conversation is fully correct in Egyptian Dialect Arabic without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Egyptian Dialect Arabic.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Egyptian Dialect Arabic, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Egyptian Dialect Arabic but without smooth transitions.


Rating C:  
- The conversation contains minor issues even if it is correct in Egyptian Dialect Arabic or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Egyptian Dialect Arabic (e.g., Modern Standard Arabic terms, or words from non Egyptian Arabic dialects).  
- These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in Egyptian Dialect Arabic with some MSA or any other non Egyptian Dialect Arabic words/expressions.
  - The conversation has spelling errors.

Rating D:  
- The conversation exhibits significant problems in Egyptian Dialect Arabic or contains non-Arabic scripts, for example:  
  - Most of the conversation is in non-Egyptian Arabic dialects (MSA, Tunisian, Algerian, or Modern Standard Arabic).
  - It uses a non-Arabic script (e.g., English, French, etc.) except if there is a term or expression that is not in Arabic Script for example: (BBC,Time News etc.) that can be in Arabic or Latin Script.  
  - Such inconsistencies seriously undermine the authenticity and coherence.
- The conversation is irrillevant to the text.
For example:
  - The conversation is Mostly in MSA or any other non-Egyptian Arabic dialects.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.
  - The conversation is irrillevant to the text.

- Take care that the Egyptian Dialect Arabic shares some words and expressions with Levantine Dialect Arabic.
if the conversation can be evaluated different ratings from above because of mixed issues then choose the worst

  For each dialogue, produce a JSON object with an array named "annotation". Each entry must include:
  - "rating": one of "A", "B", "C", or "D".  
  - "reason": a concise explanation of why you chose that rating, referencing the criteria above. in English

Output format `json`:
{{
  "annotation": [
    {{
      "rating": "Rating",
      "reason": "Explain why it meets the Rating criteria in English"
    }}
  ]
}}

Examples:

Example 1:
  Text: شر والدعاية ويحدد المزيج الترويجي مقدار الاهتمام الذي يجب أن يحظى به كل من الفئات الفرعية الخمسة ومقدار الأموال التي يجب أن تُخصص لميزانية كل فئة منها. وقد يكون للخطة الترويجية مجموعة كبيرة من الأهداف تتضمن: زيادة المبيعات أو قبول المنتج الجديد أو خلق قيمة للعلامة التجارية أو التمركز في السوق أو الرد بالمثل على المنافسين أو تكوين صورة للشركة. إلا أن هناك بشكل أساسي ثلاثة أهداف رئيسية للترويج، وهي:
  تقديم المعلومات للمستهلكين والأشخاص الآخرين.
  زيادة الطلب.
  تحقيق التميز للمنتج.هناك طرق مختلفة للترويج لمنتج ما في مجالات الإعلام المختلفة. حيث يستخدم المروجون الإعلان عن طريق الإنترنت والفعاليات الخاصة والتصديقات والصحف للإعلان عن منتجاتهم. وكثيرًا ما يكون شراء المنتج مصحوبًا بحافز مثل الخصومات أو الهدايا المجانية أو المسابقات. والهدف من ذلك هو زيادة مبيعات منتج ما.
  إن مصطلح «ترويج» هو تعبير «داخلي» عادةً ما يُستخدم داخليًا في شركات التسويق، ولكنه لا يُستخدم عادةً مع العامة أو السوق - فعبارات مثل «عرض خاص» أكثر شيوعًا. ومن بين أمثلة العروض الترويجية المتكاملة طويلة الأجل وواسعة النطاق جوائز كوكاكولا (My Coke Rewards) وبيبسي ستاف (Pepsi Stuff). والنسخة البريطانية من جوائز كوكاكولا هي كوك زون (Coke Zone).
  ويعرف الترويج على أنه  الجهد الذي يبذله البائع في إبراز الخصائص المميزة للسلعة أو الخدمة التي يتم الترويج لها كالتصميم، والتغليف، واسم العلامة، والجودة، والسعر ثم إقناع هذا المشتري بتلك الخصائص لشراء هذه السلعة أو الخدمة 
  ويعرف الترويج بأنه تلك  المحفزات التي تستعملها المؤسسة لحث (تجار الجملة، وتجار التجزئة، قنوات التوزيع الأخرى) على التبادل، أو المستهلكين لشراء العلامة التجارية، وتشجيع قوى البيع على تصريفها .

  Dialogue to evaluate:
    "dialogue": [
      {{
        "speaker": "A",
        "text": "سمعتك بتتكلم عن الترويج، هو إيه بالظبط؟",
        "reference": "الترويج هو أحد عناصر المزيج التسويقي وهو مصطلح كثيرًا ما يُستخدم في مجال التسويق."
      }},
      {{
        "speaker": "B",
        "text": "الترويج ببساطة هو طريقة لتسويق المنتج عن طريق الإعلان أو الخصومات.",
        "reference": "هذه العناصر هي البيع الشخصي والإعلان وتنشيط المبيعات والتسويق المباشر والدعاية."
      }},
      {{
        "speaker": "A",
        "text": "يعني إيه خطة ترويجية؟",
        "reference": "يحدد المزيج الترويجي مقدار الاهتمام الذي يجب أن يحظى به كل من الفئات الفرعية الخمسة."
      }},
      {{
        "speaker": "B",
        "text": "الخطة دي بتحدد إزاي هتسوق المنتج وبخصص ميزانية لكل طريقة.",
        "reference": "ومقدار الأموال التي يجب أن تُخصص لميزانية كل فئة منها."
      }},
      {{
        "speaker": "A",
        "text": "طب ليه الشركات بتستخدم الترويج؟",
        "reference": "زيادة المبيعات أو قبول المنتج الجديد أو خلق قيمة للعلامة التجارية."
      }},
      {{
        "speaker": "B",
        "text": "عشان تزيد المبيعات وتخلق وعي بالمنتج عند الناس.",
        "reference": "زيادة الطلب. تحقيق التميز للمنتج."
      }}
    ]
  

  Output:
  {{
    "annotation": [
      {{
        "rating": "A",
        "reason": "The conversation is fully correct in Egyptian Dialect Arabic and flows naturally and coherently, with smooth transitions and contextual expressions."
      }}
    ]
  }}

Example 2:
  Text: شر والدعاية ويحدد المزيج الترويجي مقدار الاهتمام الذي يجب أن يحظى به كل من الفئات الفرعية الخمسة ومقدار الأموال التي يجب أن تُخصص لميزانية كل فئة منها. وقد يكون للخطة الترويجية مجموعة كبيرة من الأهداف تتضمن: زيادة المبيعات أو قبول المنتج الجديد أو خلق قيمة للعلامة التجارية أو التمركز في السوق أو الرد بالمثل على المنافسين أو تكوين صورة للشركة. إلا أن هناك بشكل أساسي ثلاثة أهداف رئيسية للترويج، وهي:
  تقديم المعلومات للمستهلكين والأشخاص الآخرين.
  زيادة الطلب.
  تحقيق التميز للمنتج.هناك طرق مختلفة للترويج لمنتج ما في مجالات الإعلام المختلفة. حيث يستخدم المروجون الإعلان عن طريق الإنترنت والفعاليات الخاصة والتصديقات والصحف للإعلان عن منتجاتهم. وكثيرًا ما يكون شراء المنتج مصحوبًا بحافز مثل الخصومات أو الهدايا المجانية أو المسابقات. والهدف من ذلك هو زيادة مبيعات منتج ما.
  إن مصطلح «ترويج» هو تعبير «داخلي» عادةً ما يُستخدم داخليًا في شركات التسويق، ولكنه لا يُستخدم عادةً مع العامة أو السوق - فعبارات مثل «عرض خاص» أكثر شيوعًا. ومن بين أمثلة العروض الترويجية المتكاملة طويلة الأجل وواسعة النطاق جوائز كوكاكولا (My Coke Rewards) وبيبسي ستاف (Pepsi Stuff). والنسخة البريطانية من جوائز كوكاكولا هي كوك زون (Coke Zone).
  ويعرف الترويج على أنه  الجهد الذي يبذله البائع في إبراز الخصائص المميزة للسلعة أو الخدمة التي يتم الترويج لها كالتصميم، والتغليف، واسم العلامة، والجودة، والسعر ثم إقناع هذا المشتري بتلك الخصائص لشراء هذه السلعة أو الخدمة 
  ويعرف الترويج بأنه تلك  المحفزات التي تستعملها المؤسسة لحث (تجار الجملة، وتجار التجزئة، قنوات التوزيع الأخرى) على التبادل، أو المستهلكين لشراء العلامة التجارية، وتشجيع قوى البيع على تصريفها .

  Dialogue to evaluate:
  {{
  "dialogue": [
    {{
      "speaker": "A",
      "text": "إيه رأيك في العروض اللي بنشوفها كتير دي؟",
      "reference": "الترويج هو أحد عناصر المزيج التسويقي"
    }},
    {{
      "speaker": "B",
      "text": "دي أهدافها ترويج للمنتجات، صح؟",
      "reference": "أهداف رئيسية للترويج"
    }},
    {{
      "speaker": "A",
      "text": "بالظبط، عشان تزود المبيعات مثلاً.",
      "reference": "زيادة المبيعات"
    }},
    {{
      "speaker": "B",
      "text": "وكمان بتيجي بخصومات أو هدايا مجانية.",
      "reference": "الخصومات أو الهدايا المجانية"
    }},
    {{
      "speaker": "A",
      "text": "ده بيشجع المستهلك يشتري أكتر.",
      "reference": "لزيادة مبيعات منتج ما"
    }},
    {{
      "speaker": "B",
      "text": "عشان كده الناس بيقولوا عليها 'عرض خاص' مش ترويج.",
      "reference": "فعبارات مثل «عرض خاص» أكثر شيوعًا"
    }}
  ]
}}

Output:
{{
  "annotation": [
    {{
      "rating": "B",
      "reason": "The conversation is generally correct in Egyptian Dialect Arabic, with no grammatical or vocabulary errors. but it is not as fluid as it should be. at 
      Speaker: B
      Text: وكمان بتيجي بخصومات أو هدايا مجانية.
      Speaker: A
      Text: ده بيشجع المستهلك يشتري أكتر.
    " Doesn't flow naturally and coherently, with smooth transitions and contextual expressions.
    }}
  ]
}}  

Example 3:
  Text: 
  الدور أو تيمبو هو نقلة واحدة يلعبها لاعبا الشطرنج بالتناوب ويتم فيها تحريك أحد قطع الشطرنج مرة واحدة وفق قوانين الشطرنج، حين يحقق اللاعب الوضعية التي يرغب فيها في عدد نقلات أقل بنقلة واحدة من المخطط له يقال رِبح دورا وبالعكس إن استغرق نقلة أكثر من المطلوب يقال فقدان دور فحين يجبر اللاعب الخصم على تنفيذ نقلات ليست في مخططه الأساسي فذلك ربح للنقلات لأن الخصم مضطر لتأجيل مخططه والرد على الإجبار، النقلة التي تُربح دورا تسمى في الغالب «نقلة مع دور». للدور أهمية كبيرة ومن الضروري عدم فقدان الأدوار لأن ذلك ينعكس على نجاعة الدفاع أو الهجوم انظر (شكل1)، مثال بسيط على فقدان دور هو تحريك القلعة في (الشكل2) من h1 إلى h5 في دور ثم إلى h8 في دور ثاني في حين كان يمكن فعل ذلك في نقلة واحدة وتوفير دور، مناورات كتلك لا تتسبب دائما في فقدان تيمبو ففي بعض الأحيان قد تقوم القلعة بتهديد يجب الرد عليه وفي هذه الحالة يعتبر أن كلا اللاعبين فقدا دورا وهذه النتيجة تعادل قياسا على الزمن لكن التغير الذي طرأ على الوضعية يمكن أن يكون في فائدة أحدهما أكثر من الآخر.

  Dialogue to evaluate:
  {{
    "dialogue": [
      {{
        "speaker": "A",
        "text": "معرفش الشطرنج كويس، إيه معنى ربح دور؟",
        "reference": "الدور أو تيمبو هو نقلة واحدة يلعبها لاعبا الشطرنج..."
      }},
      {{
        "speaker": "B",
        "text": "إذا لعبت نقلة جعلتك تكسب وقت على الخصم ده يبقى ربح دور.",
        "reference": "حين يحقق اللاعب الوضعية التي يرغب فيها في عدد نقلات أقل..."
      }},
      {{
        "speaker": "A",
        "text": "طيب ممكن تخسر دور؟ إزاي؟",
        "reference": "بالعكس إن استغرق نقلة أكثر من المطلوب يقال فقدان دور..."
      }},
      {{
        "speaker": "B",
        "text": "لو عملت نقلتين عشان توصل لمكان يمكنك الوصول له بنقلة واحدة.",
        "reference": "مثال بسيط على فقدان دور هو تحريك القلعة..."
      }},
      {{
        "speaker": "A",
        "text": "يعني لو حركت القلعة من h1 لـ h5 ثم h8 بدلا من مباشرة؟",
        "reference": "من h1 إلى h5 في دور ثم إلى h8 في دور ثاني..."
      }},
      {{
        "speaker": "B",
        "text": "ظبط، لكن أحيانا المناورات دي مش بتخلي بالضرورة تخسر دور.",
        "reference": "مناورات كتلك لا تتسبب دائما في فقدان تيمبو..."
      }}
    ]
  }}
  Output:
  {{
    "annotation": [
      {{
        "rating": "C",
        "reason": "Minor slip in spelling as said "ظبط" instead of "بالظبط" or "بالضبط", and some Modern Standard Arabic words like "لكن أحيانا" and "جعلتك" and so on "
      }}
    ]
  }}

Example 4:
  Text:
  عضلة القلب (بالإنجليزية: Heart muscle)‏ أو (Myocardium) هي واحدة من ثلاثة أنواع من عضلات الفقاريات، مع اثنين آخرين وهما العضلات الهيكلية والعضلات الملساء. العضلة لا إرادية مخططة وتشكل النسيج الرئيسي لجدران القلب. تشكل عضلة القلب طبقة وسطية سميكة بين الطبقة الخارجية لجدار القلب (التامور) والطبقة الداخلية (الشغاف)، مع توفير الدم عبر الدورة الدموية التاجية. وهي تتألف من خلايا القلب العضلية الفردية (خلايا القلب العضلية) المرتبطة ببعضها عن طريق أقراص مقحمة، مغلفة بألياف الكولاجين وغيرها من المواد التي تشكل النسيج البيني خارج الخلية.
تنقبض عضلة القلب بطريقة مماثلة للعضلة الهيكلية، على الرغم من بعض الاختلافات الهامة. يؤدي التحفيز الكهربائي في شكل جهد فعل قلبي إلى إطلاق الكالسيوم من مخزن الكالسيوم الداخلي للخلية (الشبكة الهيولية العضلية). يؤدي ارتفاع الكالسيوم إلى انزلاق الخيوط العضلية للخلية عبر بعضها البعض في عملية تسمى انقباض عضلي.
أمراض عضلة القلب هي ذات أهمية كبيرة. وتشمل هذه الحالات التي تتسبب في تقييد جريان الدم في العضلات الذبحة الصدرية والنوبة القلبية، وأمراض عضلة القلب الأخرى المعروفة باسم اعتلال عضلة القلب.

Dialogue to evaluate:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": "عارف إن عضلة القلب مش إرادية؟",
      "reference": "عضلة القلب ‏أو Myocardium هي واحدة من ثلاثة أنواع من عضلات الفقاريات... العضلة لا إرادية."
    }},
    {{
      "speaker": "B",
      "text": "آه، وبتكون بينها وبين الشبكة الكولاجينية، حاجة عجيبة!",
      "reference": "مغلفة بألياف الكولاجين وغيرها من المواد التي تشكل النسيج البيني خارج الخلية."
    }},
    {{
      "speaker": "A",
      "text": "طيب، التحفيز الكهربائي بيعمل إيه فيها؟",
      "reference": "يؤدي التحفيز الكهربائي في شكل جهد فعل قلبي إلى إطلاق الكالسيوم..."
    }},
    {{
      "speaker": "B",
      "text": "بيطلق كالسيوم يخلي العضلات تنقبض.",
      "reference": "يؤدي التحفيز الكهربائي... إلى إطلاق الكالسيوم من مخزن الكالسيوم الداخلي...导致的肌肉收缩."
    }},
    {{
      "speaker": "A",
      "text": "يعني الكالسيوم ده أساسي؟",
      "reference": "يؤدي ارتفاع الكالسيوم إلى انزلاق الخيوط العضلية... عملية تسمى انقباض عضلي."
    }},
    {{
      "speaker": "B",
      "text": "تمام، وكل ده مرتبط بأمراض القلب.",
      "reference": "أمراض عضلة القلب هي ذات أهمية كبيرة... وتشمل الذبحة الصدرية والنوبة القلبية، وأمراض عضلة القلب الأخرى."
    }}
  ]
}}
Output:
{{
  "annotation": [
    {{
      "rating": "D",
      "reason": "The conversation has "导致的肌肉收缩" which is not arabic nor English expression."
    }}
  ]
}}

Your Input Text:
{text}

Dialogue to evaluate:
{dialogue}
"""
# Standard Evaluation Prompt
standard_evaluation_prompt = """
You are a linguistics expert with over 20 years of experience in Arabic dialectology, and a native speaker of Modern Standard Arabic.  
You will be given a Text and an AI-generated conversation in Modern Standard Arabic. Your task is to evaluate AI‑generated conversations in Modern Standard Arabic and assign each one a rating from A to D, using the detailed criteria below:

Rating A:  
- The conversation is fully correct in Modern Standard Arabic without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Modern Standard Arabic.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Modern Standard Arabic, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Modern Standard Arabic but without smooth transitions.


Rating C:  
- The conversation contains minor issues even if it is correct in Modern Standard Arabic or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Modern Standard Arabic (e.g., Modern Standard Arabic terms, or words from non Egyptian Arabic dialects).  
- These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in MSA with some Egyptian Dialect Arabic or any other non MSA words/expressions.
  - The conversation has spelling errors.

Rating D:
- The conversation exhibits significant problems in Modern Standard Arabic or contains non-Arabic script, for example:
  - Most of the conversation is in non-Modern Standard Arabic.
  - It uses a non-Arabic script (e.g., English, French) except for isolated foreign proper nouns such as “BBC” or “Time News” that lack Arabic equivalents.
  - Such inconsistencies seriously undermine authenticity and coherence.
- The conversation is irrelevant to the text.
- Do not confuse conversations written mainly in non-Arabic script with the acceptable, limited use of foreign proper nouns.
For example:
  - The conversation is Mostly in Egyptian Dialect or any other non-Modern Standard Arabic.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.
  - The conversation is irrillevant to the text.

The conversations that has limited use of foreign proper nouns should be rated as A if it doesn't have any other issues. Otherwise, it should be rated as B or C. according to the criteria above.
if the conversation can be evaluated different ratings from above because of mixed issues then choose the worst

  For each dialogue, produce a JSON object with an array named "annotation". Each entry must include:
  - "rating": one of "A", "B", "C", or "D".  
  - "reason": a concise explanation of why you chose that rating, referencing the criteria above. in English

Output format `json`:
{{
  "annotation": [
    {{
      "rating": "Rating",
      "reason": "Explain why it meets the Rating criteria in English"
    }}
  ]
}}

Examples:

Example 1:
  Text: تاريخ الطيران يبحث في تطور الطيران الميكانيكي من المحاولات الأولى في الطائرات الورقية والطيران الشراعي حتى الطائرات الأثقل من الهواء وما بعدها.
أول ظهور محتمل لغريزة الإنسان للطيران كان في الصين منذ بداية القرن السادس الميلادي حيث كان الناس يقيدون بالطائرات الورقية كنوع من العقوبة. وقام عباس بن فرناس بأول عرض طيران شراعي في الأندلس في القرن التاسع الميلادي. وعبر ليوناردو دا فينشي في القرن الخامس عشر عن حلمه بالطيران في العديد من التصاميم لطائرات ولكنه لم يقم بأي محاولة للطيران. ثم بدأت أولى محاولات الطيران الجاد أواخر القرن الثامن عشر في أوروبا. وبدأت البالونات المملوءة بالهواء الحار والمجهزة بسلة للركاب وبدأت بالظهور في النصف الأول من القرن التاسع عشر وقد استعملت بشكل فعال في عدة حروب بذلك الوقت، خصوصا بالحرب الأهلية الأمريكية، حيث كان لها الحيز بمراقبة العدو خلال المعركة.
أرست كثرة التجارب بالطيران الشراعي الأسس لبناء آلات طائرة أثقل من الهواء، ومع بداية القرن العشرين أصبح بالإمكان ولأول مرة عمل رحلة جوية مسيرة وذات قدرة مع تطور تقنية المحركات. وبعدها بذل مصممو الطائرات جهودا مضنية لتحسين آلاتهم الطائرة لجعلها تطير بشكل أسرع ولمدى أبعد وارتفاع أعلى وجعلها سهلة بالقيادة.
العوامل المهمة التي ساهمت في بناء الطائرة هي:

التحكم: بالبداية فإن التحكم بالطائرات الشراعية يكون بواسطة تحريك الطائرة ككل حسب أوتو ليلينتال، أو إمالة الجناح كما فعل الأخوان رايت. لكن بالوقت الحالي يكون التحكم بواسطة أسطح التحكم مثل الجنيحات والروافع. وفي بعض الطائرات العسكرية تكون أسطح التحكم مهيئة بنظام كمبيوتر ليتم التوسع بالتحكم في الطيران الثابت والمستقر
الطاقة: تطور محرك الطائرة حتى أصبح أخف وزنا وأكثر كفاءة، فمن محرك كليمنت أدر البخاري إلى المكبس فالنفاث ثم محركات الصواريخ.
المواد: كان صنع الطائرات في البداية من القماش والخشب ثم بدأت تقويتها بالأنسجة والأنابيب الفولاذية، ومن عام 1918 بدأت تكسية القشرة الخارجية بالألمونيوم واستمرت بذلك خلال الحرب العالمية الثانية، لكن بالوقت الحالي يكون البناء الخارجي للطائرة من مواد مركبة.

Dialogue to evaluate:
      "dialogue": [
    {{
      "speaker": "A",
      "text": "هل تعلم أن أول محاولات الطيران كانت بالطائرات الورقية في الصين؟",
      "reference": "تاريخ الطيران يبحث في تطور الطيران الميكانيكي من المحاولات الأولى في الطائرات الورقية والطيران الشراعي حتى الطائرات الأثقل من الهواء وما بعدها."
    }},
    {{
      "speaker": "B",
      "text": "نعم! وسمعت أن عباس بن فرناس حاول الطيران الشراعي في الأندلس.",
      "reference": "وقام عباس بن فرناس بأول عرض طيران شراعي في الأندلس في القرن التاسع الميلادي."
    }},
    {{
      "speaker": "A",
      "text": "صحيح! لكن متى بدأت أول رحلة جوية مسيرة؟",
      "reference": "ومع بداية القرن العشرين أصبح بالإمكان ولأول مرة عمل رحلة جوية مسيرة وذات قدرة مع تطور تقنية المحركات."
    }},
    {{
      "speaker": "B",
      "text": "في القرن العشرين بعد تطوير المحركات. كيف تطورت مواد صناعة الطائرات؟",
      "reference": "كان صنع الطائرات في البداية من القماش والخشب ثم بدأت تقويتها بالأنسجة والأنابيب الفولاذية."
    }},
    {{
      "speaker": "A",
      "text": "من الخشب إلى الألمونيوم والآن المواد المركبة. وماذا عن التحكم بالطائرات؟",
      "reference": "لكن بالوقت الحالي يكون البناء الخارجي للطائرة من مواد مركبة."
    }},
    {{
      "speaker": "B",
      "text": "في الماضي بتحريك الطائرة ككل، والآن بأسطح تحكم كمبيوترية!",
      "reference": "لكن بالوقت الحالي يكون التحكم بواسطة أسطح التحكم مثل الجنيحات والروافع."
    }}
  ]
  

  Output:
  {{
    "annotation": [
      {{
        "rating": "A",
        "reason": "The conversation is fully correct in Modern Standard Arabic and flows naturally and coherently, with smooth transitions and contextual expressions."
      }}
    ]
  }}

Example 2:
  Text:  تاريخ الطيران يبحث في تطور الطيران الميكانيكي من المحاولات الأولى في الطائرات الورقية والطيران الشراعي حتى الطائرات الأثقل من الهواء وما بعدها.
أول ظهور محتمل لغريزة الإنسان للطيران كان في الصين منذ بداية القرن السادس الميلادي حيث كان الناس يقيدون بالطائرات الورقية كنوع من العقوبة. وقام عباس بن فرناس بأول عرض طيران شراعي في الأندلس في القرن التاسع الميلادي. وعبر ليوناردو دا فينشي في القرن الخامس عشر عن حلمه بالطيران في العديد من التصاميم لطائرات ولكنه لم يقم بأي محاولة للطيران. ثم بدأت أولى محاولات الطيران الجاد أواخر القرن الثامن عشر في أوروبا. وبدأت البالونات المملوءة بالهواء الحار والمجهزة بسلة للركاب وبدأت بالظهور في النصف الأول من القرن التاسع عشر وقد استعملت بشكل فعال في عدة حروب بذلك الوقت، خصوصا بالحرب الأهلية الأمريكية، حيث كان لها الحيز بمراقبة العدو خلال المعركة.
أرست كثرة التجارب بالطيران الشراعي الأسس لبناء آلات طائرة أثقل من الهواء، ومع بداية القرن العشرين أصبح بالإمكان ولأول مرة عمل رحلة جوية مسيرة وذات قدرة مع تطور تقنية المحركات. وبعدها بذل مصممو الطائرات جهودا مضنية لتحسين آلاتهم الطائرة لجعلها تطير بشكل أسرع ولمدى أبعد وارتفاع أعلى وجعلها سهلة بالقيادة.
العوامل المهمة التي ساهمت في بناء الطائرة هي:

التحكم: بالبداية فإن التحكم بالطائرات الشراعية يكون بواسطة تحريك الطائرة ككل حسب أوتو ليلينتال، أو إمالة الجناح كما فعل الأخوان رايت. لكن بالوقت الحالي يكون التحكم بواسطة أسطح التحكم مثل الجنيحات والروافع. وفي بعض الطائرات العسكرية تكون أسطح التحكم مهيئة بنظام كمبيوتر ليتم التوسع بالتحكم في الطيران الثابت والمستقر
الطاقة: تطور محرك الطائرة حتى أصبح أخف وزنا وأكثر كفاءة، فمن محرك كليمنت أدر البخاري إلى المكبس فالنفاث ثم محركات الصواريخ.
المواد: كان صنع الطائرات في البداية من القماش والخشب ثم بدأت تقويتها بالأنسجة والأنابيب الفولاذية، ومن عام 1918 بدأت تكسية القشرة الخارجية بالألمنيوم واستمرت بذلك خلال الحرب العالمية الثانية، لكن بالوقت الحالي يكون البناء

Dialogue to evaluate:

"dialogue": [
    {{
      "speaker": "A",
      "text": "تخيل كم تطور الطيران الميكانيكي عبر التاريخ!",
      "reference": "تاريخ الطيران يبحث في تطور الطيران الميكانيكي"
    }},
    {{
      "speaker": "B",
      "text": "بالفعل، بدأ الأمر من المحاولات الأولى كعباس بن فرناس.",
      "reference": "وقام عباس بن فرناس بأول عرض طيران شراعي في الأندلس في القرن التاسع الميلادي."
    }},
    {{
      "speaker": "A",
      "text": "وكيف تحول الأمر للطائرات الأثقل من الهواء؟",
      "reference": "حتى الطائرات الأثقل من الهواء وما بعدها."
    }},
    {{
      "speaker": "B",
      "text": "تطور المحركات كان أساسياً، من البخاري للنفاث.",
      "reference": "تطور محرك الطائرة حتى أصبح أخف وزنا وأكثر كفاءة، فمن محرك كليمنت أدر البخاري إلى المكبس فالنفاث."
    }},
    {{
      "speaker": "A",
      "text": "والمواد أيضاً! من القماش والخشب للمركبات الحديثة.",
      "reference": "كان صنع الطائرات في البداية من القماش والخشب ... لكن بالوقت الحالي يكون البناء الخارجي للطائرة من مواد مركبة."
    }},
    {{
      "speaker": "B",
      "text": "أصبحت الطائرات أسرع وأسهل بالقيادة بفضل كل التطورات.",
      "reference": "بذل مصممو الطائرات جهودا مضنية لتحسين آلاتهم الطائرة لجعلها تطير بشكل أسرع ... وجعلها سهلة بالقيادة."
    }}
  ]

Output:
{{
  "annotation": [
    {{
      "rating": "B",
      "reason": "The conversation is generally correct in Modern Standard Arabic, with no grammatical or vocabulary errors. but it is not as fluid as it should be as it feels disconnected at the end. at 
      Speaker: A
      Text:والمواد أيضاً! من القماش والخشب للمركبات الحديثة."
      Speaker: B
      Text: "أصبحت الطائرات أسرع وأسهل بالقيادة بفضل كل التطورات."
    " Doesn't flow naturally and coherently, with smooth transitions and contextual expressions.
    }}
  ]
}}  

Example 3:
  Text: 
 تاريخ الطيران يبحث في تطور الطيران الميكانيكي من المحاولات الأولى في الطائرات الورقية والطيران الشراعي حتى الطائرات الأثقل من الهواء وما بعدها.
أول ظهور محتمل لغريزة الإنسان للطيران كان في الصين منذ بداية القرن السادس الميلادي حيث كان الناس يقيدون بالطائرات الورقية كنوع من العقوبة. وقام عباس بن فرناس بأول عرض طيران شراعي في الأندلس في القرن التاسع الميلادي. وعبر ليوناردو دا فينشي في القرن الخامس عشر عن حلمه بالطيران في العديد من التصاميم لطائرات ولكنه لم يقم بأي محاولة للطيران. ثم بدأت أولى محاولات الطيران الجاد أواخر القرن الثامن عشر في أوروبا. وبدأت البالونات المملوءة بالهواء الحار والمجهزة بسلة للركاب وبدأت بالظهور في النصف الأول من القرن التاسع عشر وقد استعملت بشكل فعال في عدة حروب بذلك الوقت، خصوصا بالحرب الأهلية الأمريكية، حيث كان لها الحيز بمراقبة العدو خلال المعركة.
أرست كثرة التجارب بالطيران الشراعي الأسس لبناء آلات طائرة أثقل من الهواء، ومع بداية القرن العشرين أصبح بالإمكان ولأول مرة عمل رحلة جوية مسيرة وذات قدرة مع تطور تقنية المحركات. وبعدها بذل مصممو الطائرات جهودا مضنية لتحسين آلاتهم الطائرة لجعلها تطير بشكل أسرع ولمدى أبعد وارتفاع أعلى وجعلها سهلة بالقيادة.
العوامل المهمة التي ساهمت في بناء الطائرة هي:

التحكم: بالبداية فإن التحكم بالطائرات الشراعية يكون بواسطة تحريك الطائرة ككل حسب أوتو ليلينتال، أو إمالة الجناح كما فعل الأخوان رايت. لكن بالوقت الحالي يكون التحكم بواسطة أسطح التحكم مثل الجنيحات والروافع. وفي بعض الطائرات العسكرية تكون أسطح التحكم مهيئة بنظام كمبيوتر ليتم التوسع بالتحكم في الطيران الثابت والمستقر
الطاقة: تطور محرك الطائرة حتى أصبح أخف وزنا وأكثر كفاءة، فمن محرك كليمنت أدر البخاري إلى المكبس فالنفاث ثم محركات الصواريخ.
المواد: كان صنع الطائرات في البداية من القماش والخشب ثم بدأت تقويتها بالأنسجة والأنابيب الفولاذية، ومن عام 1918 بدأت تكسية القشرة الخارجية بالألمونيوم واستمرت بذلك خلال الحرب العالمية الثانية، لكن بالوقت الحالي يكون البناء الخارجي للطائرة من مواد مركبة.

Dialogue to evaluate:
{{
     "dialogue": [
    {{
      "speaker": "A",
      "text": "هل تعرف متى ظهرت فكرة الطيران لأول مرة؟",
      "reference": "أول ظهور محتمل لغريزة الإنسان للطيران كان في الصين منذ بداية القرن السادس الميلادي."
    }},
    {{
      "speaker": "B",
      "text": "نعم، بدأ الأمر في الصين بالطائرات الورقية كعقوبة.",
      "reference": "حيث كان الناس يقيدون بالطائرات الورقية كنوع من العقوبة."
    }},
    {{
      "speaker": "A",
      "text": "وماذا عن المحاولات الجادة لطيران الإنسان؟",
      "reference": "بدأت أولى محاولات الطيران الجاد أواخر القرن الثامن عشر."
    }},
    {{
      "speaker": "B",
      "text": "أول رحلة جوية حقيقية حدثت في أوائل القرن العشرين.",
      "reference": "مع بداية القرن العشرين أصبح بالإمكان ولأول مرة عمل رحلة جوية مسيرة."
    }},
    {{
      "speaker": "A",
      "text": "كيف تطورت تكنولوجيا التحكم بالطائرات؟",
      "reference": "التحكم بواسطة أسطح التحكم مثل الجنيحات والروافع."
    }},
    {{
      "speaker": "B",
      "text": "تغيرت المواد من الخشب إلى مركبات حديثة الآن.",
      "reference": "بالوقت الحالي يكون البناء الخارجي للطائرة من مواد مركبة."
    }}
  ]
}}

Output:
{{
    "annotation": [
      {{
        "rating": "B",
        "reason": "It feels more as Q&A specially at the end where Speaker A asked directly without any transitional expression  at 'كيف تطورت تكنولوجيا التحكم بالطائرات؟' as it could be A if there was like "و كيف" before it "
      }}
    ]
  }}

Example 4:
  Text:
 القط ذو الحذاء (بالفرنسية: Le Maître Chat, ou Le Chat Botté)‏ (بالإيطالية: Il gatto con gli stivali)‏، هي إحدى الحكايات الخرافية لشارل بيرو، وهي تحكي حياة أبناء طحان بعد موته وتقاسمه الورث، فتقاسموا أشياء مهمة ولم يتركو للأخير إلا القط لكن ابنه الثالث رضي به، في يوم كان وارث القط يلوم نفسه على ما رضي به من ورث فسمعه القط فذهب يصطاد الحيوانات وذهب بها إلى الحاكم وابنته فيقول لهما انها هدية من والي البلاد، فتيقنوا ذلك مرة فقد أمر القط صاحبه أن يسبح في النهر وخبأ ملابسه تحت صخرة، فأتى الملك وابنته يريدان أن يسلما على الفتى فقال لهم القط أن سيده في البركة يسبح وقد سرقوا ملابسه، فأعطوه ملابس فاخرة وجلس في العربة مع الأميرة التي أحبته. ثم ذهب لاحقا إلى قصر يسكنه وحش والذي يمكنه التحول إلى أي مخلوق على وجه الأرض، فتحول الغول إلى أسد فأخاف القط الذي استطاع خداعه بأن يتحول إلى فأر فهجم عليه القط والتهمه، هكذا تمكن الوريث من أخد قصر الوحش فانبهر به الملك وتزوج ابنته وعاش هو والقطه في رخاء.

Dialogue to evaluate:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": "هل سمعت عن حكاية القط ذو الحذاء؟",
      "reference": "القط ذو الحذاء هي إحدى الحكايات الخرافية لشارل بيرو."
    }},
    {{
      "speaker": "B",
      "text": "نعم، هي قصة ابن الطحان الذي ورث قطاً فقط. ما رأيك فيها؟",
      "reference": "تقاسموا أشياء مهمة ولم يتركو للأخير إلا القط."
    }},
    {{
      "speaker": "A",
      "text": "أعجبني كيف استخدم القط ذكائه لمساعدة صاحبه.",
      "reference": "فسمعه القط فذهب يصطاد الحيوانات وذهب بها إلى الحاكم وابنته."
    }},
    {{
      "speaker": "B",
      "text": "بالتأكيد، حتى خدع الملك والحاشية باستخدام مكائد بسيطة.",
      "reference": "فأتى الملك وابنته يريدان أن يسلما على الفتى فقال لهم القط أن سيده في البركة يسبح."
    }},
    {{
      "speaker": "A",
      "text": "ولم يتوقف عند هذا، بل هزم الوحش主人 القصر أيضاً.",
      "reference": "تحول الغول إلى أسد فأخاف القط الذي استطاع خداعه بأن يتحول إلى فأر."
    }},
    {{
      "speaker": "B",
      "text": "نعم، وأصبح صاحب القط غنياً وتزوج الأميرة في النهاية.",
      "reference": "أنبهر به الملك وتزوج ابنته وعاش هو والقطه في رخاء."
    }}
  ]
}}

Output:
{{
  "annotation": [
    {{
      "rating": "D",
      "reason": "The conversation has "主人" which is non Arabic script."
    }}
  ]
}}



Your Input Text:
{text}

Dialogue to evaluate:
{dialogue}
"""


# Maghrebi Evaluation Prompt

mag_evaluation_prompt = """
You are a linguistics expert with over 20 years of experience in Arabic dialectology, and a native speaker of Maghrebi Darija.  
You will be given a Text and an AI-generated conversation in Maghrebi Darija. Your task is to evaluate AI‑generated conversations in Maghrebi Darija and assign each one a rating from A to D, using the detailed criteria below:

Rating A:  
- The conversation is fully correct in Maghrebi Darija without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Maghrebi Darija.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Maghrebi Darija, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Maghrebi Darija but without smooth transitions.
  - The conversation is mostly correct but it contains a few awkward or slightly un-idiomatic phrases


Rating C:  
- The conversation contains minor issues even if it is correct in Maghrebi Darija or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Maghrebi Darija (e.g., Modern Standard Arabic terms, or words from non Maghrebi Darija like Tunisian, Algerian or Lebanon Dialects)
  - These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in MSA with some Maghrebi Darija words/expressions.
  - The Conversation is in Maghrebi Darija with some Tunisian, Algerian, Lebanon or any non Maghrebi Darija Dialects words/expressions.
  - The conversation has spelling errors.
  - The Conversation is totally correct but It is in Arabic Franco which is a method of writing Arabic using the Latin alphabet and numbers.

Rating D:  
- The conversation exhibits significant problems in Maghrebi Darija or contains non-Arabic scripts, for example:  
  - Most of the conversation is in non-Maghrebi Darija.
  - It uses a non-Arabic script but It isn't Arabic Franco (e.g., English, French, etc.) except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent.   
  - Such inconsistencies seriously undermine the authenticity and coherence.
- The conversation is irrillevant to the text.
For example:
  - The conversation is Mostly in MSA or any other non-Maghrebi Darija.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.

if the conversation can be evaluated different ratings from above because of mixed issues then choose the worst

  For each dialogue, produce a JSON object with an array named "annotation". Each entry must include:
  - "rating": one of "A", "B", "C", or "D".  
  - "reason": a concise explanation of why you chose that rating, referencing the criteria above. in English

Output format `json`:
{{
  "annotation": [
    {{
      "rating": "Rating",
      "reason": "Explain why it meets the Rating criteria in English"
    }}
  ]
}}

Example 1:
  Text: 
 القط ذو الحذاء (بالفرنسية: Le Maître Chat, ou Le Chat Botté)‏ (بالإيطالية: Il gatto con gli stivali)‏، هي إحدى الحكايات الخرافية لشارل بيرو، وهي تحكي حياة أبناء طحان بعد موته وتقاسمه الورث، فتقاسموا أشياء مهمة ولم يتركو للأخير إلا القط لكن ابنه الثالث رضي به، في يوم كان وارث القط يلوم نفسه على ما رضي به من ورث فسمعه القط فذهب يصطاد الحيوانات وذهب بها إلى الحاكم وابنته فيقول لهما انها هدية من والي البلاد، فتيقنوا ذلك مرة فقد أمر القط صاحبه أن يسبح في النهر وخبأ ملابسه تحت صخرة، فأتى الملك وابنته يريدان أن يسلما على الفتى فقال لهم القط أن سيده في البركة يسبح وقد سرقوا ملابسه، فأعطوه ملابس فاخرة وجلس في العربة مع الأميرة التي أحبته. ثم ذهب لاحقا إلى قصر يسكنه وحش والذي يمكنه التحول إلى أي مخلوق على وجه الأرض، فتحول الغول إلى أسد فأخاف القط الذي استطاع خداعه بأن يتحول إلى فأر فهجم عليه القط والتهمه، هكذا تمكن الوريث من أخد قصر الوحش فانبهر به الملك وتزوج ابنته وعاش هو والقطه في رخاء.



Dialogue to evaluate:
{{
      "dialogue": [
    {{
      "speaker": "A",
      "text": "سمعتي على هاديك القصة ديال 'القط ذو الحذاء'؟",
      "reference": "القط ذو الحذاء"
    }},
    {{
      "speaker": "B",
      "text": "آه، اللي فيها المش كان ذكي بزاف؟",
      "reference": "القط ... ذكي"
    }},
    {{
      "speaker": "A",
      "text": "بضبط! تخيل، حول ولد عادي لأمير.",
      "reference": "ابن طحان ... أعطوه ملابس فاخرة وجلس في العربة مع الأميرة ... تزوج ابنته"
    }},
    {{
      "speaker": "B",
      "text": "وكيفاش ضحك على الغول ورجعو فأر!",
      "reference": "تحول الغول إلى أسد فأخاف القط الذي استطاع خداعه بأن يتحول إلى فأر فهجم عليه القط والتهمه"
    }},
    {{
      "speaker": "A",
      "text": "آه، هاديك كانت أحسن لقطة. مكار!",
      "reference": "استطاع خداعه... التهمه"
    }},
    {{
      "speaker": "B",
      "text": "بصح بدّل حياة مولاه، من والو لقصر!",
      "reference": "تمكن الوريث من أخد قصر الوحش فانبهر به الملك وتزوج ابنته وعاش هو والقطه في رخاء"
    }}
  ]

}}

Output:
{{
    "annotation": [
      {{
        "rating": "A",
        "reason": "It is in correct Maghrebi Darija Arabic without mistakes or errors"
      }}
    ]
  }}

Example 2:
  Text:  الطلاق (يعرف أيضًا باسم فسخ الزواج) هو عملية إنهاء العلاقة الزوجية أو الارتباط الزوجي. عادة ما يستلزم الطلاق إلغاء أو إعادة تنظيم الواجبات والمسؤوليات القانونية للزواج وبالتالي فسخ روابط الزواج بين الزوجين بموجب القانون في بلد أو دولة معينة. تختلف قوانين الطلاق بشكل كبير في جميع أنحاء العالم، ولكن في معظم البلدان يتطلب الطلاق تدخل محكمة أو سلطة أخرى في الإجراءات القانونية والتي قد تنطوي على قضايا توزيع الممتلكات وحضانة الأطفال والنفقة وزيارة الأطفال / أو الوصول إليهم والوقت المخصص للأب / الأم لرؤية الأطفال وتقديم الدعم الطفل وتقسيم المصاريف. في معظم البلدان هناك قانون يلزم الأفراد بالزواج الأحادي لذا فإن الطلاق بحسب هذا القانون يسمح لكل شريك سابق بالزواج من شخص آخر.
الدول الوحيدة التي لا تسمح بالطلاق هي الفلبين ومدينة الفاتيكان. في الفلبين لا يعتبر طلاق الفلبينيين غير المسلمين أمرًا قانونيًا إلا إذا كان الزوج أو الزوجة مهاجرًا غير شرعي ويستوفي شروطًا معينة، أما مدينة الفاتيكان فهي دولة كنسية ليس لديها إجراءات للطلاق. البلدان التي أقرت الطلاق مؤخرًا نسبيًا هي إيطاليا (1970)، البرتغال (1975 على الرغم من أنه من عام 1910 إلى عام 1940 كان ذلك ممكنًا للزواج المدني والديني)، البرازيل (1977)، إسبانيا (1981)، الأرجنتين (1987)، باراغواي (1991)، كولومبيا (1991؛ من 1976 كان مسموحًا به فقط لغير الكاثوليك)، أندورا (1995)، أيرلندا (1996)، تشيلي (2004) ومالطا (2011).
يتم الطلاق عادة باتفاق الطرفين أو بإرادة أحدهما، وهو موجود لدى العديد من ثقافات العالم لكنه غير موجود لدى أتباع الكنيسة الكاثوليكية وتعتبر أشهر قضية طلاق في التاريخ عندما طلب هنري الثامن ملك إنجلترا الطلاق من كاثرين أراغون عام 1534 لكن البابا رفض ترخيص طلاقه مما أدى إلى تأسيس الكنيسة الأنجليكانية.


Dialogue to evaluate:

  "dialogue": [
    {{
      "speaker": "A",
      "text": "واش قريتي شي حاجة على هاري بوتر؟",
      "reference": "هاري بوتر شخصية خيالية مشهورة"
    }},
    {{
      "speaker": "B",
      "text": "آه، سمعت أنه قهر لورد مظلم.",
      "reference": "هاري بوتر في الانتصار على فولدمورت"
    }},
    {{
      "speaker": "A",
      "text": "واش اللي قتلوا واليديه؟",
      "reference": "وقتل أبويه"
    }},
    {{
      "speaker": "B",
      "text": "إيه، لورد فولدمورت هو اللي دارها.",
      "reference": "قتله غير أن التعويذة"
    }},
    {{
      "speaker": "A",
      "text": "واش بقى مع عائلة وحدة قريبتهم؟",
      "reference": "يعيش بعد وفاتهما مع أسرة خالته"
    }},
    {{
      "speaker": "B",
      "text": "إيه، كانوا قاسين عليه بزاف.",
      "reference": "يتعرض لاضطهاد مستمر"
    }}
  ]


Output:
{{
  "annotation": [
    {{
      "rating": "B",
      "reason": "The sentence "واش بقى مع عائلة وحدة قريبتهم؟" is very close to Moroccan Darija, but it's not entirely natural or idiomatic as-is.”
    }}
  ]
}}  

Example 3:
  Text:  الطلاق (يعرف أيضًا باسم فسخ الزواج) هو عملية إنهاء العلاقة الزوجية أو الارتباط الزوجي. عادة ما يستلزم الطلاق إلغاء أو إعادة تنظيم الواجبات والمسؤوليات القانونية للزواج وبالتالي فسخ روابط الزواج بين الزوجين بموجب القانون في بلد أو دولة معينة. تختلف قوانين الطلاق بشكل كبير في جميع أنحاء العالم، ولكن في معظم البلدان يتطلب الطلاق تدخل محكمة أو سلطة أخرى في الإجراءات القانونية والتي قد تنطوي على قضايا توزيع الممتلكات وحضانة الأطفال والنفقة وزيارة الأطفال / أو الوصول إليهم والوقت المخصص للأب / الأم لرؤية الأطفال وتقديم الدعم الطفل وتقسيم المصاريف. في معظم البلدان هناك قانون يلزم الأفراد بالزواج الأحادي لذا فإن الطلاق بحسب هذا القانون يسمح لكل شريك سابق بالزواج من شخص آخر.
الدول الوحيدة التي لا تسمح بالطلاق هي الفلبين ومدينة الفاتيكان. في الفلبين لا يعتبر طلاق الفلبينيين غير المسلمين أمرًا قانونيًا إلا إذا كان الزوج أو الزوجة مهاجرًا غير شرعي ويستوفي شروطًا معينة، أما مدينة الفاتيكان فهي دولة كنسية ليس لديها إجراءات للطلاق. البلدان التي أقرت الطلاق مؤخرًا نسبيًا هي إيطاليا (1970)، البرتغال (1975 على الرغم من أنه من عام 1910 إلى عام 1940 كان ذلك ممكنًا للزواج المدني والديني)، البرازيل (1977)، إسبانيا (1981)، الأرجنتين (1987)، باراغواي (1991)، كولومبيا (1991؛ من 1976 كان مسموحًا به فقط لغير الكاثوليك)، أندورا (1995)، أيرلندا (1996)، تشيلي (2004) ومالطا (2011).
يتم الطلاق عادة باتفاق الطرفين أو بإرادة أحدهما، وهو موجود لدى العديد من ثقافات العالم لكنه غير موجود لدى أتباع الكنيسة الكاثوليكية وتعتبر أشهر قضية طلاق في التاريخ عندما طلب هنري الثامن ملك إنجلترا الطلاق من كاثرين أراغون عام 1534 لكن البابا رفض ترخيص طلاقه مما أدى إلى تأسيس الكنيسة الأنجليكانية.


Dialogue to evaluate:
       "dialogue": [
    {{
      "speaker": "A",
      "text": "سمعت بلي الطلاق عندنا فالمغرب مختلف على الدول الأخرى، صحيح؟",
      "reference": "تختلف قوانين الطلاق بشكل كبير في جميع أنحاء العالم"
    }},
    {{
      "speaker": "B",
      "text": "إيوا، كل بلاد عندها قانون خاص بيها. حتى فلبين والفاتيكان ممنوع عندهم الطلاق أساسًا!",
      "reference": "الدول الوحيدة التي لا تسمح بالطلاق هي الفلبين ومدينة الفاتيكان"
    }},
    {{
      "speaker": "A",
      "text": "وااا! حتى لو كان الزوجين مايتافقوش ماعندهمش حل؟",
      "reference": "في الفلبين لا يعتبر طلاق الفلبينيين غير المسلمين أمرًا قانونيًا"
    }},
    {{
      "speaker": "B",
      "text": "بالضبط، غير المسلمين هناك صعيب عليهم. لكن فإيطاليا مثلا الطلاق مكنشرح حتى 1970.",
      "reference": "البلدان التي أقرت الطلاق مؤخرًا نسبيًا هي إيطاليا (1970)"
    }},
    {{
      "speaker": "A",
      "text": "حتى الكنيسة الكاثوليكية مابقاتش تسمح بالطلاق، ولا زال؟",
      "reference": "غير موجود لدى أتباع الكنيسة الكاثوليكية"
    }},
    {{
      "speaker": "B",
      "text": "إيوا، لدرجة أن ملك إنجلترا خلق كنيسة جديدة عشان يطلق!",
      "reference": "تعتبر أشهر قضية طلاق في التاريخ عندما طلب هنري الثامن ملك إنجلترا الطلاق"
    }}
  ]


  

  Output:
  {{
    "annotation": [
      {{
        "rating": "C",
        "reason": "The conversation has some expressions in Maghrebi Darija, However it has some awkward expressions like ‘ولا زال’  and "إيوا، لدرجة أن ملك إنجلترا خلق كنيسة جديدة عشان يطلق!” is more Egyptian Dialect”
      }}
    ]
  }}



Example 4:
  Text:
 جراند ثفت أوتو (بالإنجليزية: Grand Theft Auto؛ تختصر إلى GTA) هي سلسلة من ألعاب المغامرات والحركة التي أنشأها ديفيد جونز ومايك ديلي. تم تطوير العناوين اللاحقة تحت إشراف الأخوين دان وسام هاوسر، ليزلي بنزيس، وآرون جاربوت. تم تطوير اللعبة بشكل أساسي من قبل شركة التطوير البريطانية روكستار نورث (دي إم أي ديزاين (DMA Design) سابقًا)، ونشرتها الشركة الأم روكستار جيمز. يشير اسم السلسلة إلى مصطلح «جراند ثفت أوتو»، المستخدم في الولايات المتحدة لسرقة السيارات.
تركز طريقة اللعب على عالم مفتوح حيث يمكن للاعب إكمال المهام للتقدم في قصة شاملة، بالإضافة إلى الانخراط في أنشطة جانبية مختلفة. تدور معظم طريقة اللعب حول القيادة وإطلاق النار، مع لعب الأدوار من حين لآخر وعناصر التخفي. تحتوي السلسلة أيضًا على عناصر من ألعاب بيت إم السابقة من عصر 16 بت. تم وضع الألعاب في سلسلة جراند ثفت أوتو في أماكن خيالية على غرار مدن الحياة الواقعية، في نقاط زمنية مختلفة من أوائل الستينيات إلى العقد الأول من القرن الحادي والعشرين. اشتملت خريطة اللعبة الأصلية على ثلاث مدن — ليبرتي سيتي (استنادًا إلى مدينة نيويورك)، وسان أندرياس (استنادًا إلى سان فرانسيسكو)، وفايس سيتي (استنادًا إلى ميامي) — ولكن تميل العناوين اللاحقة إلى التركيز على مكان واحد عادةً ما تكون إحدى المناطق الثلاث الأصلية، وإن تم إعادة تشكيلها وتوسيعها بشكل كبير. يركز المسلسل على أبطال مختلفين يحاولون الصعود في مراتب العالم السفلي الإجرامي، على الرغم من أن دوافعهم للقيام بذلك تختلف في كل عنوان. عادةً ما يكون الخصوم شخصيات قد خانوا بطل الرواية أو منظمتهم، أو الشخصيات التي لها التأثير الأكبر في إعاقة تقدم بطل الرواية. أعرب العديد من قدامى الأفلام والموسيقى عن شخصيات في الألعاب، بما في ذلك راي ليوتا، دينيس هوبر، صامويل جاكسون، ويليام فيشتنر، جيمس وودز، ديبي هاري، أكسل روز، وبيتر فوندا.بدأت دي إم أي ديزاين السلسلة في عام 1997 بإصدار جراند ثفت أوتو. اعتبارًا من 2020، تتكون السلسلة من سبعة عناوين مستقلة وأربع حزم توسعة. يعتبر العنوان الرئيسي الثالث، جراند ثفت أوتو 3، الذي تم إصداره في عام 2001، لعبة تاريخية، حيث جلبت السلسلة إلى إعداد ثلاثي الأبعاد (3D) وتجربة أكثر مغامرة. اتبعت العناوين اللاحقة وبنيت على المفهوم الذي تم تأسيسه في جراند ثفت أوتو 3، وحظيت بإشادة كبيرة. لقد أثروا على ألعاب الحركة الأخرى في العالم المفتوح، وأدى إلى استنساخ جراند ثفت أوتو على عناوين مماثلة.
حازت السلسلة على استحسان النقاد، حيث تم تصنيف جميع الإدخالات ثلاثية الأبعاد الرئيسية في السلسلة بشكل متكرر ضمن ألعاب الفيديو التي تعد الأفضل والأكثر مبيعًا؛ شحنت أكثر من 350 مليون وحدة، مما يجعلها خامس أفضل سلسلة لألعاب الفيديو مبيعًا. في عام 2006، ظهرت جراند ثفت أوتو في قائمة أيقونات التصميم البريطانية في غريت برتِش ديزاين كويست (Great British Design Quest) التي نظمتها هيئة الإذاعة البريطانية ومتحف التصميم. في عام 2013، صنفت صحيفة ذا تلغراف جراند ثفت أوتو من بين أنجح الصادرات البريطانية. كانت السلسلة أيضًا مثيرة للجدل بسبب طبيعتها البالغة وموضوعاتها العنيفة.
في 4 فبراير 2022، أكدت روكستار أن هنالك عنوان جديد للسلسلة قيد التطوير.




Dialogue to evaluate:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": "Katchouf GTA? Silsila dyal l-lâ3ab ktab3ha bnadem bezzaf.",
      "reference": "سلسلة من ألعاب المغامرات والحركة"
    }},
    {{
      "speaker": "B",
      "text": "Ah, kan3refha. Wahed men akbar l-âbâb fel 3âlam.",
      "reference": "خامس أفضل سلسلة لألعاب الفيديو مبيعًا"
    }},
    {{
      "speaker": "A",
      "text": "Bdat f 1997, u GTA 3 hiya li bedlat kolchi f 2001.",
      "reference": "بدأت دي إم أي ديزاين السلسلة في عام 1997 بإصدار جراند ثفت أوتو. يعتبر العنوان الرئيسي الثالث، جراند ثفت أوتو 3، الذي تم إصداره في عام 2001، لعبة تاريخية"
    }},
    {{
      "speaker": "B",
      "text": "Bessa7, dak l3ab fih 3alam meftou7 u zwin bezzaf.",
      "reference": "تركز طريقة اللعب على عالم مفتوح"
    }},
    {{
      "speaker": "A",
      "text": "Wla makhbartekch, kaywjedo fiha jeu jdid daba.",
      "reference": "في 4 فبراير 2022، أكدت روكستار أن هنالك عنوان جديد للسلسلة قيد التطوير."
    }},
    {{
      "speaker": "B",
      "text": "Hada khbar zwin! Dima katbqa men a7san l-lâ3ab.",
      "reference": "حازت السلسلة على استحسان النقاد"
    }}
  ]

}}

Output:
{{
  "annotation": [
    {{
      "rating": "C",
      "reason": "The conversation is correct in Maghrebi Darija. However, it uses Arabic Franco which is an error"
    }}
  ]
}}



Example 5:
  Text:
  الدور أو تيمبو هو نقلة واحدة يلعبها لاعبا الشطرنج بالتناوب ويتم فيها تحريك أحد قطع الشطرنج مرة واحدة وفق قوانين الشطرنج، حين يحقق اللاعب الوضعية التي يرغب فيها في عدد نقلات أقل بنقلة واحدة من المخطط له يقال رِبح دورا وبالعكس إن استغرق نقلة أكثر من المطلوب يقال فقدان دور فحين يجبر اللاعب الخصم على تنفيذ نقلات ليست في مخططه الأساسي فذلك ربح للنقلات لأن الخصم مضطر لتأجيل مخططه والرد على الإجبار، النقلة التي تُربح دورا تسمى في الغالب «نقلة مع دور». للدور أهمية كبيرة ومن الضروري عدم فقدان الأدوار لأن ذلك ينعكس على نجاعة الدفاع أو الهجوم انظر (شكل1)، مثال بسيط على فقدان دور هو تحريك القلعة في (الشكل2) من h1 إلى h5 في دور ثم إلى h8 في دور ثاني في حين كان يمكن فعل ذلك في نقلة واحدة وتوفير دور، مناورات كتلك لا تتسبب دائما في فقدان تيمبو ففي بعض الأحيان قد تقوم القلعة بتهديد يجب الرد عليه وفي هذه الحالة يعتبر أن كلا اللاعبين فقدا دورا وهذه النتيجة تعادل قياسا على الزمن لكن التغير الذي طرأ على الوضعية يمكن أن يكون في فائدة أحدهما أكثر من الآخر.



Dialogue to evaluate:
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": "شفت المباراة اللي لعبها حسن مع علي بالشطرنج؟",
      "reference": "الدور أو تيمبو هو نقلة واحدة يلعبها لاعبا الشطرنج بالتناوب ويتم فيها تحريك أحد قطع الشطرنج مرة واحدة وفق قوانين الشطرنج"
    }},
    {{
      "speaker": "B",
      "text": "أيوه، حسن كان دايما يربح دورا بنقلاته.",
      "reference": "حين يحقق اللاعب الوضعية التي يرغب فيها في عدد نقلات أقل بنقلة واحدة من المخطط له يقال رِبح دورا"
    }},
    {{
      "speaker": "A",
      "text": "صحيح، علي كان فاقد دور كل مرة.",
      "reference": "وبالعكس إن استغرق نقلة أكثر من المطلوب يقال فقدان دور"
    }},
    {{
      "speaker": "B",
      "text": "مرة حاول يجبر حسن على نقلات ليست في مخططه.",
      "reference": "حين يجبر اللاعب الخصم على تنفيذ نقلات ليست في مخططه الأساسي فذلك ربح للنقلات لأن الخصم مضطر لتأجيل مخططه والرد على الإجبار"
    }},
    {{
      "speaker": "A",
      "text": "بس حسن كان دايما يرد بنقلة مع دور.",
      "reference": "النقلة التي تُربح دورا تسمى في الغالب «نقلة مع دور»"
    }},
    {{
      "speaker": "B",
      "text": "يعني كان بيحافظ على أدواره جيد.",
      "reference": "للدور أهمية كبيرة ومن الضروري عدم فقدان الأدوار لأن ذلك ينعكس على نجاعة الدفاع أو الهجوم"
    }}
  ]

}}

Output:
{{
  "annotation": [
    {{
      "rating": "D",
      "reason": "The conversation is totally in Egyptian Dialect while it should be in Maghrebi Darija"
    }}
  ]
}}

Your Input Text:
{text}

Dialogue to evaluate:
{dialogue}
"""



# Inputs: (Text , Dialogue , Rating , Reason , Dialect)
# Output: (Fixed Dialogue)

egy_fix_prompt = """
Your task is to fix an AI-generated dialogue in Egyptian Dialect Arabic. The conversation must be based strictly on the provided source text. You should produce a six-turn dialogue (three exchanges between two speakers) that would earn an “A” rating under the rubric below.

Generated Dialogue to Fix:
{dialogue}

Source Text:
{text}

Original Rating: {rating}
Reason for Rating: {reason}

It was generated according to the following features:
***
1.	General Framework:
• Be natural, relatable, and culturally appropriate in Egyptian Dialect Arabic.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Egyptian Dialect Arabic.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Egyptian Dialect Arabic, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Egyptian Dialect Arabic.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
***

Evaluation Rubric (A–D):
***
Rating A:  
- The conversation is fully correct in Egyptian Dialect Arabic without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Egyptian Dialect Arabic.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Egyptian Dialect Arabic, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Egyptian Dialect Arabic but without smooth transitions.


Rating C:  
- The conversation contains minor issues even if it is correct in Egyptian Dialect Arabic or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Egyptian Dialect Arabic (e.g., Modern Standard Arabic terms, or words from non Egyptian Arabic dialects).  
- These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in Egyptian Dialect Arabic with some MSA or any other non Egyptian Dialect Arabic words/expressions.
  - The conversation has spelling errors.

Rating D:  
- The conversation exhibits significant problems in Egyptian Dialect Arabic or contains non-Arabic scripts, for example:  
  - Most of the conversation is in non-Egyptian Arabic dialects (MSA, Tunisian, Algerian, or Modern Standard Arabic).
  - It uses a non-Arabic script (e.g., English, French, etc.) except if there is a term or expression that is not in Arabic Script for example: (BBC,Time News etc.) that can be in Arabic or Latin Script.  
  - Such inconsistencies seriously undermine the authenticity and coherence.
- The conversation is irrillevant to the text.
For example:
  - The conversation is Mostly in MSA or any other non-Egyptian Arabic dialects.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.
  - The conversation is irrillevant to the text.

- Take care that the Egyptian Dialect Arabic shares some words and expressions with Levantine Dialect Arabic.
if the conversation can be evaluated different ratings from above because of mixed issues then choose the worst
***


Output format (JSON):
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
    }},
    {{
      "speaker": "B",
      "text": -Text-
    }},
    ...
   ]
}}

"""

std_fix_prompt = """
Your task is to fix an AI-generated dialogue in Modern Standard Arabic. The conversation must be based strictly on the provided source text. You should produce a six-turn dialogue (three exchanges between two speakers) that would earn an “A” rating under the rubric below.

Generated Dialogue to Fix:
{dialogue}

Source Text:
{text}

Original Rating: {rating}
Reason for Rating: {reason}

It was generated according to the following features:
***
1   General Framework:
• Be natural, relatable, and culturally appropriate in Modern Standard Arabic.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Modern Standard Arabic.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Modern Standard Arabic, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Modern Standard Arabic.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
***

Evaluation Rubric (A–D):
***
Rating A:  
- The conversation is fully correct in Modern Standard Arabic without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Modern Standard Arabic.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Modern Standard Arabic, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Modern Standard Arabic but without smooth transitions.


Rating C:  
- The conversation contains minor issues even if it is correct in Modern Standard Arabic or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Modern Standard Arabic (e.g., Modern Standard Arabic terms, or words from non Egyptian Arabic dialects).  
- These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in MSA with some Egyptian Dialect Arabic or any other non MSA words/expressions.
  - The conversation has spelling errors.

Rating D:
- The conversation exhibits significant problems in Modern Standard Arabic or contains non-Arabic script, for example:
  - Most of the conversation is in non-Modern Standard Arabic.
  - It uses a non-Arabic script (e.g., English, French) except for isolated foreign proper nouns such as “BBC” or “Time News” that lack Arabic equivalents.
  - Such inconsistencies seriously undermine authenticity and coherence.
- The conversation is irrelevant to the text.
- Do not confuse conversations written mainly in non-Arabic script with the acceptable, limited use of foreign proper nouns.
For example:
  - The conversation is Mostly in Egyptian Dialect or any other non-Modern Standard Arabic.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.
  - The conversation is irrillevant to the text.
***


Output format (JSON):
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
    }},
    {{
      "speaker": "B",
      "text": -Text-
    }},
    ...
   ]
}}

"""

mag_fix_prompt = """

Your task is to fix an AI-generated dialogue in Maghrebi Darija. The conversation must be based strictly on the provided source text. You should produce a six-turn dialogue (three exchanges between two speakers) that would earn an “A” rating under the rubric below.

Generated Dialogue to Fix:
{dialogue}

Source Text:
{text}

Original Rating: {rating}
Reason for Rating: {reason}

It was generated according to the following features:
***
1.	General Framework:
• Be natural, relatable, and culturally appropriate in Maghrebi Darija.
• The dialogue must be natural, smooth, and realistic.
• The dialogue should be fully in Maghrebi Darija.
• Avoid generating Q&A style conversations without proper transitions and contextual expressions.
• Use Maghrebi Darija, with cultural appropriateness.
• Each turn must be between 1 and 20 words.

2.	Content and Style:
• Choose topics that are personal, work-related, or about daily routines.
• Keep the language simple and easy to understand: avoid complex vocabulary or idioms that non‑native speakers might not grasp.
• Add a light, casual tone to make the conversation engaging.
• Avoid using dialects other than Maghrebi Darija.
• Refrain from using personal or emotional address terms.

3.	Technical Constraints:
• Do not add any information or details that are not derived from the original text.
• Do not use any special characters, symbols, or emojis.
***

Evaluation Rubric (A–D):
***
Rating A:  
- The conversation is fully correct in Maghrebi Darija without any errors or slips.
- Grammar, vocabulary, idioms, and expressions are all accurate and appropriate.  
- Dialogue flows naturally and coherently, with smooth transitions and contextual expressions.
For example: 
  - The conversation is like Q&A but with smooth transitions and contextual expressions.
  - The conversation is mainly in the Maghrebi Darija.
  - The conversation could have one or two natural standard arabic words.

Rating B:  
- The conversation is generally correct in Maghrebi Darija, with no grammatical or vocabulary errors. It doesn't have any slips or errors  
- However, the dialogue may feel slightly unnatural, for example:  
  - It is like a Q&A without smooth transitions.  
  - Some transitional phrases or idiomatic expressions are missing, making it less smooth.
  - The conversation is mostly a collection of disconnected sentences rather than a fluid conversation.
For example:
  - The conversation is like Q&A but without smooth transitions.
  - The conversation is mainly in the Maghrebi Darija but without smooth transitions.
  - The conversation is mostly correct but it contains a few awkward or slightly un-idiomatic phrases


Rating C:  
- The conversation contains minor issues even if it is correct in Maghrebi Darija or doesn't affect the understanding, such as:  
  - Slight grammatical mistakes or awkward phrasing.  
  - Occasional use of words or constructions not native to Maghrebi Darija (e.g., Modern Standard Arabic terms, or words from non Maghrebi Darija like Tunisian, Algerian or Lebanon Dialects)
  - These slips are infrequent.
For example:
  - The conversation is like Q&A but with some natural standard arabic words.
  - The conversation is in MSA with some Maghrebi Darija words/expressions.
  - The Conversation is in Maghrebi Darija with some Tunisian, Algerian, Lebanon or any non Maghrebi Darija Dialects words/expressions.
  - The conversation has spelling errors.
  - The Conversation is totally correct but It is in Arabic Franco which is a method of writing Arabic using the Latin alphabet and numbers.

Rating D:  
- The conversation exhibits significant problems in Maghrebi Darija or contains non-Arabic scripts, for example:  
  - Most of the conversation is in non-Maghrebi Darija.
  - It uses a non-Arabic script but It isn't Arabic Franco (e.g., English, French, etc.) except if there is an expression that is not in Arabic Script for example: (BBC,Time News etc.) that doesn't have an Arabic Script equivalent.   
  - Such inconsistencies seriously undermine the authenticity and coherence.
- The conversation is irrillevant to the text.
For example:
  - The conversation is Mostly in MSA or any other non-Maghrebi Darija.
  - The conversation has non-Arabic scripts or an arabic script mixed with non-Arabic scripts.
***


Output format (JSON):
{{
  "dialogue": [
    {{
      "speaker": "A",
      "text": -Text-
    }},
    {{
      "speaker": "B",
      "text": -Text-
    }},
    ...
   ]
}}

"""


