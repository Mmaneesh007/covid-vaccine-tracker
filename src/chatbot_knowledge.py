"""
Knowledge base for the COVID-19 Smart FAQ Chatbot.
Contains intents, training patterns, and responses.
"""

KNOWLEDGE_BASE = [
    {
        "intent": "greeting",
        "patterns": [
            "Hi", "Hello", "Hey", "Good morning", "Good afternoon", "Good evening", 
            "Hi there", "Hello bot", "Greetings", "Sup", "What's up", "Yo", 
            "Howdy", "Nice to meet you", "Is anyone there?", "Can you help me?",
            "Start", "Begin", "Hola", "Bonjour", "Namaste"
        ],
        "responses": [
            "Hello! 👋 I am your COVID-19 Health Assistant. How can I help you today?",
            "Hi there! I'm here to answer your questions about COVID-19 and vaccines.",
            "Greetings! I'm a smart assistant trained on health guidelines. What would you like to know?"
        ]
    },
    {
        "intent": "goodbye",
        "patterns": [
            "Bye", "Goodbye", "See you", "See ya", "Later", "Have a good day", 
            "Good night", "I'm leaving", "End chat", "Quit", "Stop", "Exit",
            "Talk to you later", "Bye bye", "Cya", "Peace out"
        ],
        "responses": [
            "Goodbye! Stay safe and healthy. 🌟",
            "You're welcome! Have a great day and stay safe.",
            "Bye! Feel free to come back if you have more questions."
        ]
    },
    {
        "intent": "thanks",
        "patterns": [
            "Thanks", "Thank you", "Thx", "Thank you so much", "Thanks a lot", 
            "Appreciate it", "That helps", "Great thanks", "Awesome thanks",
            "You're helpful", "Thanks for the info", "Good job"
        ],
        "responses": [
            "You're welcome! Happy to help.",
            "No problem! Let me know if you have other questions.",
            "Glad I could help! Stay safe."
        ]
    },
    {
        "intent": "how_are_you",
        "patterns": [
            "How are you?", "How are you doing?", "How's it going?", "How do you feel?",
            "Are you okay?", "What's up with you?", "How is your day?", "Are you fine?"
        ],
        "responses": [
            "I'm just a computer program, but I'm functioning perfectly! 🤖 I'm here to help you stay safe.",
            "I'm doing great, thanks for asking! Ready to answer your COVID-19 questions.",
            "All systems operational! How can I assist you with your health queries?"
        ]
    },
    {
        "intent": "identity",
        "patterns": [
            "Who are you?", "What are you?", "Are you a human?", "Are you a bot?", 
            "What is your name?", "Introduce yourself", "Give me your intro", 
            "Tell me about yourself", "Are you AI?", "Who made you?"
        ],
        "responses": [
            "I am a smart assistant trained on WHO and CDC guidelines to answer your questions about COVID-19, vaccines, and symptoms.",
            "I'm an automated health assistant here to provide reliable information about COVID-19.",
            "I am a chatbot designed to help you navigate COVID-19 information quickly and accurately."
        ]
    },
    {
        "intent": "vaccine_safety",
        "patterns": [
            "Is the vaccine safe?", "Are vaccines dangerous?", "Is it safe to get vaccinated?",
            "How safe are the shots?", "Are there risks with the vaccine?", "Is the covid shot safe?",
            "Should I worry about the vaccine?", "Is it experimental?", "Was it rushed?",
            "Is the vaccine tested?", "Is it safe for humans?", "Is it poisonous?",
            "Can the vaccine kill me?", "Is it safe for everyone?", "Safety data",
            "Is it approved?", "Is it FDA approved?", "Is it safe long term?"
        ],
        "responses": [
            "Yes, COVID-19 vaccines are safe and effective. They have undergone rigorous testing in clinical trials and continue to be monitored for safety. Millions of people have received them safely.",
            "The vaccines met strict safety standards before approval. Serious side effects are extremely rare, while the risk of severe illness from COVID-19 is much higher."
        ]
    },
    {
        "intent": "side_effects",
        "patterns": [
            "What are the side effects?", "Will I get sick after the shot?", "Does it hurt?",
            "Common side effects", "Adverse reactions", "Will I have a fever?",
            "Is headache normal?", "Arm pain", "Sore arm", "Fatigue after vaccine",
            "Will I feel bad?", "Side effects duration", "How long do side effects last?",
            "Is it normal to feel tired?", "Chills after vaccine", "Nausea",
            "What if I have side effects?", "Are side effects bad?", "Worst side effects"
        ],
        "responses": [
            "Common side effects are mild and temporary, including pain at the injection site, fatigue, headache, muscle pain, chills, fever, and nausea. These usually go away within a few days and are signs your body is building protection."
        ]
    },
    {
        "intent": "effectiveness",
        "patterns": [
            "Does the vaccine work?", "How effective is it?", "Will it stop me from getting covid?",
            "Is it 100% effective?", "Why get vaccinated if I can still get sick?",
            "Efficacy rate", "Does it prevent transmission?", "Does it prevent death?",
            "Is it worth it?", "Do vaccines really work?", "Protection level",
            "Does it work against variants?", "Does it work against omicron?"
        ],
        "responses": [
            "COVID-19 vaccines are highly effective at preventing severe illness, hospitalization, and death. While no vaccine is 100% effective and breakthrough infections can occur, vaccinated people usually have much milder symptoms."
        ]
    },
    {
        "intent": "booster",
        "patterns": [
            "Do I need a booster?", "When should I get a booster?", "What is a booster shot?",
            "Is a third dose necessary?", "Booster eligibility", "Can I get a booster?",
            "Why do we need boosters?", "Does immunity wane?", "Booster side effects",
            "Which booster should I get?", "Can I mix boosters?", "Fourth dose",
            "Annual shot", "How often do I need a shot?"
        ],
        "responses": [
            "Boosters are recommended for most people to maintain strong protection, as immunity can decrease over time. They significantly increase protection against variants like Omicron. Check your local health guidelines for eligibility."
        ]
    },
    {
        "intent": "children",
        "patterns": [
            "Is it safe for kids?", "Can children get vaccinated?", "Vaccine for babies",
            "Should my child get the shot?", "Is it safe for toddlers?", "Kids vaccine side effects",
            "Age limit for vaccine", "Is it approved for children?", "My child is 5",
            "My child is 12", "Do kids need it?", "Risk for children", "Myocarditis in kids",
            "Is the dose different for kids?", "Can kids get it?", "Is it safe for my son?",
            "Is it safe for my daughter?", "Vaccination for minors", "Teenagers vaccine"
        ],
        "responses": [
            "Yes, COVID-19 vaccines are available and recommended for children (age eligibility varies by country, often 6 months+). The dosage is smaller for younger children. Vaccination protects kids from severe illness and complications like MIS-C."
        ]
    },
    {
        "intent": "pregnancy",
        "patterns": [
            "Is it safe for pregnant women?", "Can I get vaccinated if I'm pregnant?",
            "Does it affect the baby?", "Breastfeeding and vaccine", "Fertility concerns",
            "Trying to conceive", "Is it safe for fertility?", "Will it make me infertile?",
            "Pregnancy risks", "Should pregnant women wait?", "CDC recommendation pregnancy"
        ],
        "responses": [
            "Yes, COVID-19 vaccination is recommended for people who are pregnant, breastfeeding, or trying to get pregnant. Pregnant people are at higher risk for severe COVID-19, and vaccination helps protect both the parent and the baby."
        ]
    },
    {
        "intent": "ingredients",
        "patterns": [
            "What is in the vaccine?", "Vaccine ingredients", "Does it contain chips?",
            "Does it contain metal?", "Does it contain pork?", "Is it halal?", "Is it kosher?",
            "Does it contain eggs?", "Does it contain fetal tissue?", "Is there mercury?",
            "Preservatives in vaccine", "List of ingredients", "Is there graphene oxide?"
        ],
        "responses": [
            "COVID-19 vaccines contain mRNA or viral vector material, lipids (fats), salts, and sugars to keep them stable. They do NOT contain microchips, metals, eggs, gelatin, pork products, fetal tissue, or preservatives like thimerosal."
        ]
    },
    {
        "intent": "how_it_works",
        "patterns": [
            "How does the vaccine work?", "What is mRNA?", "Does it change my DNA?",
            "Mechanism of action", "How do mRNA vaccines work?", "Viral vector explanation",
            "Does it give me the virus?", "Is it a live virus?", "How does it build immunity?",
            "Spike protein explanation"
        ],
        "responses": [
            "Vaccines teach your immune system to recognize and fight the virus. mRNA vaccines give instructions to your cells to make a harmless 'spike protein' found on the virus surface. Your body then produces antibodies against it. They do NOT alter your DNA."
        ]
    },
    {
        "intent": "natural_immunity",
        "patterns": [
            "I already had covid", "Do I need vaccine if I had covid?", "Natural immunity vs vaccine",
            "Is natural immunity better?", "I have antibodies", "Can I wait if I recovered?",
            "Reinfection risk", "Hybrid immunity", "Why vaccinate after infection?"
        ],
        "responses": [
            "You should still get vaccinated even if you've had COVID-19. Vaccination provides a stronger, more reliable boost to your immunity (hybrid immunity) and better protection against reinfection and new variants."
        ]
    },
    {
        "intent": "variants",
        "patterns": [
            "What about variants?", "Does it work on Omicron?", "Delta variant",
            "New strains", "Will there be more variants?", "Why does the virus mutate?",
            "Is Omicron milder?", "Do vaccines stop variants?", "Eris variant", "Pirola variant"
        ],
        "responses": [
            "Viruses mutate as they spread. Current vaccines still provide strong protection against severe disease from variants like Omicron. Updated boosters are designed to target newer strains more effectively."
        ]
    },
    {
        "intent": "long_covid",
        "patterns": [
            "What is long covid?", "Does vaccine prevent long covid?", "Symptoms of long covid",
            "How long does covid last?", "Post-covid conditions", "Brain fog",
            "Fatigue after covid", "Is long covid real?", "Can vaccinated get long covid?"
        ],
        "responses": [
            "Long COVID involves symptoms lasting weeks or months after infection (fatigue, brain fog, breathing issues). Vaccination reduces the risk of developing Long COVID if you do get infected."
        ]
    },
    {
        "intent": "symptoms",
        "patterns": [
            "What are covid symptoms?", "Signs of covid", "Do I have covid?",
            "Is a runny nose covid?", "Loss of taste", "Loss of smell", "Fever", "Cough",
            "Sore throat", "Sneezing", "Is it a cold or covid?", "Flu vs covid",
            "Early symptoms", "Emergency warning signs"
        ],
        "responses": [
            "Common symptoms include fever, cough, fatigue, loss of taste/smell, sore throat, headache, and body aches. If you have these, get tested. Seek emergency care for trouble breathing or chest pain."
        ]
    },
    {
        "intent": "testing",
        "patterns": [
            "Should I get tested?", "Where to get tested?", "PCR vs Rapid test",
            "Antigen test accuracy", "Home test kit", "When to test after exposure?",
            "How long for results?", "Is the test painful?", "False negative",
            "Positive test what to do"
        ],
        "responses": [
            "You should get tested if you have symptoms or were exposed to someone with COVID-19. Rapid antigen tests give quick results (15 mins), while PCR tests are more sensitive but take longer (lab processed)."
        ]
    },
    {
        "intent": "isolation",
        "patterns": [
            "How long to isolate?", "Quarantine rules", "I tested positive",
            "Can I go out if I'm positive?", "When can I leave isolation?",
            "Isolation for vaccinated", "Close contact rules", "Do I need to quarantine?",
            "5 day rule", "10 day rule"
        ],
        "responses": [
            "Guidelines vary by location, but generally: If positive, isolate for at least 5 days. Wear a mask for 10 days. If exposed, wear a mask and test after 5 days. Check your local health department for specific rules."
        ]
    },
    {
        "intent": "treatment",
        "patterns": [
            "How to treat covid?", "Is there a cure?", "Paxlovid", "Monoclonal antibodies",
            "Home remedies", "Vitamins for covid", "Ivermectin", "Hydroxychloroquine",
            "What to take for covid?", "Antibiotics for covid?", "Treatment options"
        ],
        "responses": [
            "Most cases can be managed at home with rest and fluids. Antiviral medications like Paxlovid are available for high-risk patients. Do NOT take antibiotics (they don't kill viruses) or unapproved drugs like Ivermectin."
        ]
    },
    {
        "intent": "masks",
        "patterns": [
            "Do masks work?", "Should I wear a mask?", "Best type of mask",
            "N95 vs surgical", "Cloth masks", "Mask mandate", "Why wear a mask?",
            "Do masks lower oxygen?", "Masks for kids", "Double masking"
        ],
        "responses": [
            "Yes, masks significantly reduce the spread of the virus. N95 or KN95 respirators offer the best protection. Masks are recommended in crowded indoor settings, especially if transmission levels are high."
        ]
    },
    {
        "intent": "transmission",
        "patterns": [
            "How does it spread?", "Is it airborne?", "Surface transmission",
            "Can I get it from food?", "Can I get it from pets?", "Asymptomatic spread",
            "Can vaccinated spread it?", "How contagious is it?", "Distance to keep"
        ],
        "responses": [
            "COVID-19 spreads mainly through respiratory droplets and aerosols when an infected person breathes, talks, coughs, or sneezes. It is very contagious. Surface transmission is less common but possible."
        ]
    },
    {
        "intent": "myths",
        "patterns": [
            "Does it make you magnetic?", "Is there a microchip?", "Does it alter DNA?",
            "Is it a bioweapon?", "Did Bill Gates make it?", "5G and covid",
            "Does it cause infertility?", "Shedding vaccine", "Mark of the beast",
            "Fake virus", "Hoax"
        ],
        "responses": [
            "These are myths. COVID-19 vaccines do not contain microchips, do not make you magnetic, do not alter DNA, and are not connected to 5G. They are legitimate medical products designed to save lives."
        ]
    },
    {
        "intent": "breakthrough",
        "patterns": [
            "I got covid after vaccine", "Breakthrough infection", "Why did I get sick?",
            "Vaccine failure", "Can vaccinated get sick?", "How common are breakthroughs?",
            "Are breakthroughs mild?"
        ],
        "responses": [
            "Breakthrough infections can happen because no vaccine is 100% effective. However, vaccinated people are much less likely to get severely ill, hospitalized, or die compared to unvaccinated people."
        ]
    },
    {
        "intent": "allergies",
        "patterns": [
            "Can I get it if I have allergies?", "Egg allergy", "Penicillin allergy",
            "Severe allergic reaction", "Anaphylaxis risk", "Allergy to PEG",
            "Is it safe for allergic people?"
        ],
        "responses": [
            "Most people with allergies (food, pollen, latex) can safely get vaccinated. If you have a history of severe anaphylaxis to vaccines or specific ingredients (like PEG), consult your doctor first."
        ]
    },
    {
        "intent": "cost",
        "patterns": [
            "How much is the vaccine?", "Is it free?", "Do I need insurance?",
            "Cost of booster", "Do I have to pay?", "Vaccine price"
        ],
        "responses": [
            "In most countries (including the US and India), COVID-19 vaccines are provided free of charge to the public, regardless of insurance or immigration status."
        ]
    },
    {
        "intent": "travel",
        "patterns": [
            "Can I travel?", "Vaccine passport", "Do I need vaccine to fly?",
            "Travel restrictions", "Test before travel", "Quarantine after travel",
            "International travel rules"
        ],
        "responses": [
            "Travel rules depend on your destination. Many countries require proof of vaccination or a negative test. Always check the official government travel advisory for your destination before booking."
        ]
    },
    {
        "intent": "mixing",
        "patterns": [
            "Can I mix vaccines?", "Mix and match", "Pfizer then Moderna",
            "Covishield then Pfizer", "Is mixing safe?", "Better immunity from mixing?"
        ],
        "responses": [
            "Yes, health authorities in many countries allow 'mix and match' dosing for boosters. Some studies suggest mixing vaccines can produce a strong immune response."
        ]
    },
    {
        "intent": "johnson",
        "patterns": [
            "Johnson and Johnson blood clots", "J&J safety", "Is J&J bad?",
            "TTS syndrome", "Janssen vaccine risks", "Should I avoid J&J?"
        ],
        "responses": [
            "The J&J vaccine has been linked to a very rare but serious blood clotting condition (TTS). For this reason, mRNA vaccines (Pfizer/Moderna) are generally preferred in many countries, though J&J remains an option."
        ]
    },
    {
        "intent": "myocarditis",
        "patterns": [
            "Heart inflammation", "Myocarditis risk", "Pericarditis",
            "Heart problems after vaccine", "Is it safe for heart?", "Young men heart risk"
        ],
        "responses": [
            "Myocarditis (heart inflammation) is a very rare side effect, mostly in young males after the second dose. Most cases are mild and recover quickly. The risk of heart damage from COVID-19 infection is much higher."
        ]
    },
    {
        "intent": "expiration",
        "patterns": [
            "Do vaccines expire?", "Shelf life", "Expired vaccine",
            "How long is it good for?", "Storage temperature"
        ],
        "responses": [
            "Vaccines have an expiration date and must be stored at specific cold temperatures. Providers check this strictly. Health authorities sometimes extend shelf life based on stability data."
        ]
    },
    {
        "intent": "origins",
        "patterns": [
            "Where did covid come from?", "Lab leak", "Wet market", "Wuhan origin",
            "Bat virus", "Did it come from animals?", "Origin of virus"
        ],
        "responses": [
            "Scientists are still investigating the exact origin. It likely jumped from animals to humans (zoonotic), possibly from bats. Investigations into all possibilities, including a lab leak, have been conducted."
        ]
    },
    {
        "intent": "herd_immunity",
        "patterns": [
            "What is herd immunity?", "When will we reach herd immunity?",
            "Percentage for herd immunity", "Is herd immunity possible?"
        ],
        "responses": [
            "Herd immunity occurs when enough people are immune to stop the spread. With COVID-19, it's difficult to achieve complete herd immunity due to new variants and waning immunity, but high vaccination rates keep the virus under control."
        ]
    },
    {
        "intent": "immunocompromised",
        "patterns": [
            "I have weak immune system", "Immunocompromised vaccine", "Cancer patient vaccine",
            "Transplant recipient", "Do I need more doses?", "Is it safe for weak immunity?"
        ],
        "responses": [
            "People with compromised immune systems are at high risk for severe COVID-19 and are strongly urged to get vaccinated. They may need additional primary doses or boosters to build sufficient protection."
        ]
    },
    {
        "intent": "flu",
        "patterns": [
            "Can I get flu shot with covid shot?", "Flu and covid vaccine together",
            "Wait between vaccines?", "Coadministration"
        ],
        "responses": [
            "Yes, you can get a COVID-19 vaccine and a flu shot at the same visit. It is safe and convenient."
        ]
    },
    {
        "intent": "covid_history",
        "patterns": [
            "When did covid start?", "When was the first case?", "History of covid",
            "Start date of pandemic", "How long has covid been around?", "When was covid discovered?",
            "First outbreak", "When did it begin?"
        ],
        "responses": [
            "COVID-19 was first identified in Wuhan, China, in December 2019. The World Health Organization (WHO) declared it a Public Health Emergency of International Concern on January 30, 2020, and a pandemic on March 11, 2020."
        ]
    },
    {
        "intent": "vaccine_inventor",
        "patterns": [
            "Who invented the vaccine?", "Who made the vaccine?", "Creator of covid vaccine",
            "Who developed Pfizer?", "Who developed Moderna?", "Scientists behind the vaccine",
            "Did one person invent it?", "Companies that made vaccines",
            "Who made Pfizer?", "Who made Moderna?", "Who made Johnson and Johnson?",
            "Who made AstraZeneca?", "Who created the vaccine?"
        ],
        "responses": [
            "COVID-19 vaccines were developed by teams of scientists at pharmaceutical companies and research institutions. Key developers include BioNTech/Pfizer (Uğur Şahin, Özlem Türeci), Moderna, Oxford/AstraZeneca (Sarah Gilbert), and Johnson & Johnson. The mRNA technology was pioneered by scientists like Katalin Karikó and Drew Weissman."
        ]
    }
]
