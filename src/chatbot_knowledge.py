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
        "intent": "source_of_info",
        "patterns": [
            "Where do you get your answers?", "From where you will give the answers?",
            "What is your data source?", "Are you reliable?", "Who taught you?",
            "Can I trust you?", "Source of information", "Where is this data from?"
        ],
        "responses": [
            "My knowledge is based on official guidelines from the World Health Organization (WHO), the Centers for Disease Control and Prevention (CDC), and verified medical data sources. I do not make up information."
        ]
    },
    {
        "intent": "vaccine_history",
        "patterns": [
            "History of vaccination", "First vaccine ever", "Who invented the first vaccine?",
            "Edward Jenner", "Smallpox vaccine", "How long have vaccines existed?",
            "Are vaccines new technology?"
        ],
        "responses": [
            "Vaccines have a long history dating back to 1796 when Dr. Edward Jenner developed the first successful vaccine against smallpox. Since then, vaccines have eliminated or controlled many deadly diseases like polio, measles, and tetanus."
        ]
    },
    {
        "intent": "covishield",
        "patterns": [
            "What is Covishield?", "Is Covishield safe?", "Who made Covishield?",
            "AstraZeneca India", "Serum Institute of India vaccine", "Covishield efficacy",
            "Gap between Covishield doses"
        ],
        "responses": [
            "Covishield is the Oxford-AstraZeneca vaccine manufactured locally by the Serum Institute of India. It is a viral vector vaccine that is highly effective against severe COVID-19. The recommended gap between doses is 12-16 weeks."
        ]
    },
    {
        "intent": "covaxin",
        "patterns": [
            "What is Covaxin?", "Is Covaxin safe?", "Who made Covaxin?",
            "Bharat Biotech vaccine", "Covaxin efficacy", "Is Covaxin effective?",
            "Covaxin vs Covishield"
        ],
        "responses": [
            "Covaxin is India's indigenous COVID-19 vaccine developed by Bharat Biotech in collaboration with ICMR. It is an inactivated virus vaccine (traditional technology) and has demonstrated high efficacy in clinical trials."
        ]
    },
    {
        "intent": "sputnik",
        "patterns": [
            "What is Sputnik V?", "Russian vaccine", "Is Sputnik safe?",
            "Sputnik efficacy", "Gamaleya Institute"
        ],
        "responses": [
            "Sputnik V is a viral vector vaccine developed by the Gamaleya Research Institute in Russia. It uses two different adenoviruses for the first and second doses to boost immunity."
        ]
    },
    {
        "intent": "pfizer_moderna",
        "patterns": [
            "Pfizer vs Moderna", "What is Comirnaty?", "Spikevax",
            "American vaccines", "mRNA vaccines list"
        ],
        "responses": [
            "Pfizer-BioNTech (Comirnaty) and Moderna (Spikevax) are mRNA vaccines. They are widely used globally and have shown very high efficacy (over 90% in initial trials) against symptomatic COVID-19."
        ]
    },
    {
        "intent": "missed_dose",
        "patterns": [
            "I missed my second dose", "Late for second dose", "Can I take second dose late?",
            "Gap too long", "Forgot my appointment", "Is it too late to get vaccinated?"
        ],
        "responses": [
            "If you missed your scheduled second dose, get it as soon as possible. You do NOT need to restart the series. Just go to a vaccination center and get the remaining shot."
        ]
    },
    {
        "intent": "lost_certificate",
        "patterns": [
            "I lost my vaccine certificate", "How to download certificate?",
            "Where to find vaccine proof?", "CoWIN certificate download",
            "Get my records"
        ],
        "responses": [
            "You can download your vaccination certificate from your country's official portal. In India, use the CoWIN website (cowin.gov.in) or the Aarogya Setu app. In the US, check with your state health department or pharmacy."
        ]
    },
    {
        "intent": "tested_positive_recently",
        "patterns": [
            "I tested positive yesterday", "Can I get vaccine if I have covid now?",
            "Vaccine during infection", "I have covid symptoms should I vaccinate?"
        ],
        "responses": [
            "No, you should wait until you have recovered from the acute illness and are no longer isolating. In many countries, it is recommended to wait 3 months after a COVID-19 infection before getting a booster."
        ]
    },
    {
        "intent": "mrna_vs_vector",
        "patterns": [
            "Difference between mRNA and viral vector", "How are vaccines different?",
            "Which technology is better?", "Types of covid vaccines"
        ],
        "responses": [
            "mRNA vaccines (Pfizer, Moderna) use genetic code to teach cells to make a protein. Viral vector vaccines (Covishield, Sputnik) use a harmless virus to deliver instructions. Both types train the immune system effectively."
        ]
    },
    {
        "intent": "alcohol",
        "patterns": [
            "Can I drink alcohol after vaccine?", "Alcohol and covid shot",
            "Beer after vaccine", "Is it safe to drink?"
        ],
        "responses": [
            "There is no evidence that moderate alcohol consumption reduces vaccine effectiveness. However, avoiding alcohol for a day or two may help you feel better if you have side effects like fatigue or headache."
        ]
    },
    {
        "intent": "exercise",
        "patterns": [
            "Can I exercise after vaccine?", "Gym after vaccine", "Workout after shot",
            "Running after vaccination"
        ],
        "responses": [
            "Yes, you can exercise if you feel well enough. However, listen to your body. If you feel tired or have arm pain, it's okay to take a rest day."
        ]
    },
    {
        "intent": "blood_donation",
        "patterns": [
            "Can I donate blood after vaccine?", "Blood donation rules",
            "Waiting period for blood donation"
        ],
        "responses": [
            "In most cases, you can donate blood immediately after vaccination if you feel well and have no symptoms. Check with your local blood donation center for specific guidelines."
        ]
    },
    {
        "intent": "variants_names",
        "patterns": [
            "What are the variant names?", "Alpha Beta Gamma Delta",
            "Why Greek letters?", "Who names the variants?"
        ],
        "responses": [
            "The WHO names variants using Greek letters (Alpha, Beta, Delta, Omicron) to avoid stigmatizing countries where they were first detected and to simplify public communication."
        ]
    },
    {
        "intent": "pandemic_end",
        "patterns": [
            "When will the pandemic end?", "Is covid over?", "End of covid",
            "Are we in endemic phase?"
        ],
        "responses": [
            "The WHO declared the end of COVID-19 as a global health emergency in May 2023. However, the virus is still circulating and is now considered an established and ongoing health issue (endemic) rather than an emergency."
        ]
    },
    {
        "intent": "vaccine_cost_india",
        "patterns": [
            "Price of vaccine in India", "Cost of Covishield", "Cost of Covaxin",
            "Private hospital vaccine price"
        ],
        "responses": [
            "In India, vaccines are free at government centers. Private hospitals charge a capped price (approx ₹225 + service charge) per dose. Prices may vary slightly, so check the CoWIN portal."
        ]
    },
    {
        "intent": "fear_of_needles",
        "patterns": [
            "I am scared of needles", "Needle phobia", "Does the shot hurt a lot?",
            "I hate injections"
        ],
        "responses": [
            "It's common to be nervous. The COVID-19 vaccine needle is very thin and the injection takes only a second. Many people report feeling just a tiny pinch or nothing at all. Tell the nurse you are nervous; they can help."
        ]
    },
    {
        "intent": "vaccine_mandate",
        "patterns": [
            "Is the vaccine mandatory?", "Do I have to get it?", "Forced vaccination",
            "Government mandate"
        ],
        "responses": [
            "Vaccination mandates vary by country and employer. In general, governments encourage vaccination to protect public health but do not force individuals. However, some jobs or travel may require proof of vaccination."
        ]
    },
    {
        "intent": "future_vaccines",
        "patterns": [
            "Nasal vaccine", "Future of covid vaccines", "Pan-coronavirus vaccine",
            "Universal vaccine"
        ],
        "responses": [
            "Scientists are working on next-generation vaccines, including nasal sprays that stop infection in the nose and 'pan-coronavirus' vaccines that could protect against many different coronaviruses at once."
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
    },
    {
        "intent": "virology_structure",
        "patterns": [
            "Structure of the virus", "What does the virus look like?", "Is it an RNA virus?",
            "SARS-CoV-2 structure", "Spike protein function", "Viral envelope"
        ],
        "responses": [
            "SARS-CoV-2 is a positive-sense single-stranded RNA virus. It has four structural proteins: spike (S), envelope (E), membrane (M), and nucleocapsid (N). The spike protein gives it a crown-like appearance (corona) and allows it to enter human cells."
        ]
    },
    {
        "intent": "ace2_receptor",
        "patterns": [
            "How does it enter cells?", "ACE2 receptor", "Mechanism of infection",
            "How does covid infect?", "Cell entry"
        ],
        "responses": [
            "The virus enters human cells by binding its Spike protein to the Angiotensin-Converting Enzyme 2 (ACE2) receptor, which is found on the surface of cells in the lungs, heart, kidneys, and intestines."
        ]
    },
    {
        "intent": "r0_reproduction",
        "patterns": [
            "How contagious is it?", "What is the R0?", "Reproduction number",
            "R-naught", "How many people does one person infect?"
        ],
        "responses": [
            "The basic reproduction number (R0) varies by variant. The original strain had an R0 of 2-3, Delta was around 5-7, and Omicron variants are even higher (often 10+), making it one of the most contagious viruses known."
        ]
    },
    {
        "intent": "incubation_period",
        "patterns": [
            "Incubation period", "How long until symptoms show?", "Time from infection to symptoms",
            "Latent period"
        ],
        "responses": [
            "The incubation period is typically 2 to 14 days, with an average of about 5 days. However, with newer variants like Omicron, symptoms often appear faster, usually within 2 to 4 days."
        ]
    },
    {
        "intent": "diagnosis_methods",
        "patterns": [
            "How is it diagnosed?", "Diagnostic tests", "CT scan for covid",
            "Chest X-ray covid", "Ground glass opacities"
        ],
        "responses": [
            "COVID-19 is diagnosed via RT-PCR (the gold standard) or rapid antigen tests. Chest CT scans can also detect characteristic signs like 'ground-glass opacities' in the lungs, even before a test result is available."
        ]
    },
    {
        "intent": "cytokine_storm",
        "patterns": [
            "What is a cytokine storm?", "Immune system overreaction", "Severe covid mechanism",
            "Why do people die from covid?"
        ],
        "responses": [
            "A 'cytokine storm' is a severe immune reaction where the body releases too many inflammatory signals (cytokines). This can damage the body's own tissues and organs, leading to respiratory failure and multi-organ failure."
        ]
    },
    {
        "intent": "prone_positioning",
        "patterns": [
            "Prone positioning", "Lying on stomach", "Why lie on stomach?",
            "Proning for covid"
        ],
        "responses": [
            "Prone positioning (lying on the stomach) helps improve oxygen levels in patients with severe respiratory distress. It reduces pressure on the lungs and helps open up more air sacs (alveoli) for breathing."
        ]
    },
    {
        "intent": "dexamethasone",
        "patterns": [
            "Dexamethasone", "Steroids for covid", "Corticosteroids",
            "Drugs for severe covid"
        ],
        "responses": [
            "Dexamethasone is a corticosteroid that has been proven to reduce mortality in critically ill COVID-19 patients requiring oxygen or ventilation. It works by suppressing the harmful overreaction of the immune system."
        ]
    },
    {
        "intent": "comorbidities",
        "patterns": [
            "Risk factors", "Who is at high risk?", "Comorbidities",
            "Diabetes and covid", "Obesity and covid", "Hypertension and covid"
        ],
        "responses": [
            "People with underlying medical conditions (comorbidities) are at higher risk for severe illness. Major risk factors include age (65+), obesity, diabetes, hypertension, cardiovascular disease, and chronic lung diseases."
        ]
    },
    {
        "intent": "mortality_rate",
        "patterns": [
            "What is the death rate?", "Mortality rate", "Case fatality rate",
            "Infection fatality rate", "How deadly is it?"
        ],
        "responses": [
            "The mortality rate varies greatly by age and vaccination status. The Case Fatality Rate (CFR) varies by country (often 1-3%). The Infection Fatality Rate (IFR) is lower (estimated 0.15-1%) because many mild cases go undetected. Vaccination drastically reduces this risk."
        ]
    },
    {
        "intent": "patient_zero",
        "patterns": [
            "Who was patient zero?", "First person to get covid", "Index case",
            "Huanan Seafood Market"
        ],
        "responses": [
            "The exact 'Patient Zero' has not been conclusively identified. Early cases were linked to the Huanan Seafood Wholesale Market in Wuhan, but some earlier cases had no link to the market, suggesting the virus may have been circulating silently before."
        ]
    },
    {
        "intent": "economic_impact",
        "patterns": [
            "Economic impact of covid", "Recession caused by covid", "Financial cost of pandemic",
            "Supply chain disruption"
        ],
        "responses": [
            "The pandemic caused the largest global economic recession since the Great Depression. It disrupted supply chains, caused massive unemployment, closed businesses, and increased global poverty and inequality."
        ]
    },
    {
        "intent": "social_stigma",
        "patterns": [
            "Social stigma", "Discrimination against asians", "Xenophobia covid",
            "Stigma against healthcare workers"
        ],
        "responses": [
            "The pandemic led to increased social stigma and xenophobia, particularly against people of Asian descent. Healthcare workers and survivors of the disease also faced discrimination and isolation in some communities."
        ]
    },
    {
        "intent": "environmental_impact",
        "patterns": [
            "Environmental impact", "Pollution reduction covid", "Nature healing",
            "Carbon emissions drop"
        ],
        "responses": [
            "Lockdowns temporarily reduced global carbon emissions and air pollution due to reduced travel and industry. However, the pandemic also created massive plastic waste from disposable masks, gloves, and PPE."
        ]
    },
    {
        "intent": "mental_health",
        "patterns": [
            "Mental health impact", "Depression during pandemic", "Anxiety covid",
            "Loneliness lockdowns"
        ],
        "responses": [
            "The pandemic triggered a global mental health crisis, with rates of anxiety and depression increasing by 25% worldwide (WHO). Factors included isolation, fear of infection, grief, and financial stress."
        ]
    },
    {
        "intent": "education_impact",
        "patterns": [
            "Impact on education", "School closures", "Online learning",
            "Learning loss"
        ],
        "responses": [
            "School closures affected over 1.6 billion students globally. The shift to remote learning highlighted the 'digital divide,' as many students lacked internet access, leading to significant learning losses."
        ]
    },
    {
        "intent": "zoonosis",
        "patterns": [
            "Is it a zoonotic disease?", "Did it come from animals?", "Animal to human transmission",
            "Intermediate host"
        ],
        "responses": [
            "Yes, COVID-19 is a zoonotic disease, meaning it jumped from animals to humans. The closest known relative is a bat coronavirus (RaTG13), but an intermediate host (like pangolins) may have been involved."
        ]
    },
    {
        "intent": "ventilation",
        "patterns": [
            "Importance of ventilation", "Airflow", "Open windows",
            "HEPA filters", "Indoor transmission"
        ],
        "responses": [
            "Good ventilation is crucial because the virus accumulates in stagnant indoor air. Opening windows, using fans, and installing HEPA filters significantly reduce the risk of airborne transmission."
        ]
    },
    {
        "intent": "hand_hygiene",
        "patterns": [
            "Hand washing", "Sanitizer vs soap", "How to wash hands",
            "Does soap kill the virus?"
        ],
        "responses": [
            "Soap destroys the virus's lipid (fatty) envelope, effectively killing it. Washing hands with soap and water for 20 seconds is more effective than sanitizer, though alcohol-based sanitizer (60%+) is a good alternative."
        ]
    },
    {
        "intent": "asymptomatic_transmission",
        "patterns": [
            "Can you spread it without symptoms?", "Asymptomatic carriers", "Silent spreaders",
            "Pre-symptomatic transmission"
        ],
        "responses": [
            "Yes, infected people can spread the virus 1-3 days before symptoms appear (pre-symptomatic) or even if they never develop symptoms (asymptomatic). This 'silent spread' makes controlling the virus very difficult."
        ]
    },
    {
        "intent": "glossary_ace2",
        "patterns": [
            "What is ACE2?", "Define ACE2", "ACE2 receptor meaning", "Explain ACE2"
        ],
        "responses": [
            "ACE2 (Angiotensin-Converting Enzyme 2) is a protein on the surface of cells in the lungs, heart, and other organs. The coronavirus uses this receptor as an entry point to infect human cells."
        ]
    },
    {
        "intent": "glossary_antibody",
        "patterns": [
            "What are antibodies?", "Define antibodies", "Antibody meaning", "Explain antibodies"
        ],
        "responses": [
            "Antibodies are proteins produced by the immune system to neutralize foreign invaders (like viruses). They recognize and bind to specific parts of the pathogen, marking it for destruction."
        ]
    },
    {
        "intent": "glossary_antigen",
        "patterns": [
            "What is an antigen?", "Define antigen", "Antigen meaning", "Antigen test"
        ],
        "responses": [
            "An antigen is a foreign substance (like a piece of virus) that triggers an immune response. Rapid antigen tests detect viral proteins to diagnose COVID-19."
        ]
    },
    {
        "intent": "glossary_asymptomatic",
        "patterns": [
            "What does asymptomatic mean?", "Define asymptomatic", "Asymptomatic meaning"
        ],
        "responses": [
            "Asymptomatic means infected with a virus but showing no symptoms. Asymptomatic individuals can still spread COVID-19 to others."
        ]
    },
    {
        "intent": "glossary_comorbidity",
        "patterns": [
            "What is a comorbidity?", "Define comorbidity", "Comorbidity meaning"
        ],
        "responses": [
            "A comorbidity is a pre-existing medical condition (like diabetes or heart disease) that exists alongside another disease. Comorbidities increase the risk of severe COVID-19."
        ]
    },
    {
        "intent": "glossary_contact_tracing",
        "patterns": [
            "What is contact tracing?", "Define contact tracing", "Contact tracing meaning"
        ],
        "responses": [
            "Contact tracing is the process of identifying people who have been in close contact with an infected person. It helps prevent further spread by alerting contacts to quarantine and get tested."
        ]
    },
    {
        "intent": "glossary_ct_value",
        "patterns": [
            "What is CT value?", "Define CT value", "Cycle threshold", "CT in PCR"
        ],
        "responses": [
            "CT (Cycle Threshold) value indicates the number of PCR cycles needed to detect the virus. A lower CT value means higher viral load (more virus in the sample)."
        ]
    },
    {
        "intent": "glossary_epidemiology",
        "patterns": [
            "What is epidemiology?", "Define epidemiology", "Epidemiology meaning"
        ],
        "responses": [
            "Epidemiology is the study of how diseases spread in populations. Epidemiologists track infection rates, identify risk factors, and inform public health decisions."
        ]
    },
    {
        "intent": "glossary_droplet",
        "patterns": [
            "What are respiratory droplets?", "Define droplet transmission", "Droplets meaning"
        ],
        "responses": [
            "Respiratory droplets are small liquid particles expelled when a person coughs, sneezes, talks, or breathes. COVID-19 can spread through these droplets."
        ]
    },
    {
        "intent": "glossary_aerosol",
        "patterns": [
            "What are aerosols?", "Define aerosol transmission", "Aerosol meaning"
        ],
        "responses": [
            "Aerosols are tiny airborne particles that can remain suspended in the air for hours. COVID-19 can spread via aerosols, especially in poorly ventilated indoor spaces."
        ]
    },
    {
        "intent": "glossary_fomite",
        "patterns": [
            "What is a fomite?", "Define fomite", "Fomite transmission"
        ],
        "responses": [
            "A fomite is an object or surface (like a doorknob or phone) that can carry infectious particles. COVID-19 can survive on fomites, though this is not the primary mode of transmission."
        ]
    },
    {
        "intent": "glossary_genome",
        "patterns": [
            "What is a genome?", "Define genome", "Viral genome"
        ],
        "responses": [
            "A genome is the complete set of genetic material in an organism. SARS-CoV-2 has an RNA genome containing about 30,000 genetic letters (nucleotides)."
        ]
    },
    {
        "intent": "glossary_herd_immunity_def",
        "patterns": [
            "Define herd immunity", "What is herd immunity?", "Herd immunity meaning"
        ],
        "responses": [
            "Herd immunity occurs when enough people in a community are immune (through vaccination or prior infection) to make disease spread unlikely, protecting those who aren't immune."
        ]
    },
    {
        "intent": "glossary_hypoxia",
        "patterns": [
            "What is hypoxia?", "Define hypoxia", "Hypoxia meaning", "Silent hypoxia"
        ],
        "responses": [
            "Hypoxia is a condition where the body or tissues don't get enough oxygen. 'Silent hypoxia' in COVID-19 patients means dangerously low oxygen levels without noticeable breathlessness."
        ]
    },
    {
        "intent": "glossary_immunocompromised",
        "patterns": [
            "What does immunocompromised mean?", "Define immunocompromised", "Immunocompromised meaning"
        ],
        "responses": [
            "Immunocompromised means having a weakened immune system due to disease, medication, or medical treatment. These individuals are at higher risk for severe COVID-19."
        ]
    },
    {
        "intent": "glossary_incubation",
        "patterns": [
            "What is incubation period?", "Define incubation", "Incubation meaning"
        ],
        "responses": [
            "The incubation period is the time between infection and the appearance of symptoms. For COVID-19, it's typically 2-14 days, with an average of 5 days."
        ]
    },
    {
        "intent": "glossary_intubation",
        "patterns": [
            "What is intubation?", "Define intubation", "Intubation meaning"
        ],
        "responses": [
            "Intubation is inserting a tube through the mouth into the airway to help a patient breathe. It's used for severe COVID-19 patients who need mechanical ventilation."
        ]
    },
    {
        "intent": "glossary_mrna",
        "patterns": [
            "What is mRNA?", "Define mRNA", "Messenger RNA", "mRNA meaning"
        ],
        "responses": [
            "mRNA (messenger RNA) carries genetic instructions from DNA to cells to make proteins. mRNA vaccines use this to teach cells to make the virus's spike protein, triggering immunity."
        ]
    },
    {
        "intent": "glossary_neutralizing_antibody",
        "patterns": [
            "What are neutralizing antibodies?", "Define neutralizing antibodies"
        ],
        "responses": [
            "Neutralizing antibodies block the virus from entering cells, preventing infection. They are a key measure of vaccine effectiveness and natural immunity."
        ]
    },
    {
        "intent": "glossary_pandemic",
        "patterns": [
            "What is a pandemic?", "Define pandemic", "Pandemic vs epidemic"
        ],
        "responses": [
            "A pandemic is a disease outbreak that spreads across multiple countries or continents. COVID-19 was declared a pandemic by the WHO on March 11, 2020."
        ]
    },
    {
        "intent": "glossary_pcr",
        "patterns": [
            "What is PCR?", "Define PCR", "PCR test meaning", "RT-PCR"
        ],
        "responses": [
            "PCR (Polymerase Chain Reaction) is a lab technique that amplifies viral genetic material to detect infection. RT-PCR is the gold standard test for diagnosing COVID-19."
        ]
    },
    {
        "intent": "glossary_pneumonia",
        "patterns": [
            "What is pneumonia?", "Define pneumonia", "COVID pneumonia"
        ],
        "responses": [
            "Pneumonia is lung inflammation where air sacs fill with fluid or pus. COVID-19 can cause viral pneumonia, leading to breathing difficulties and requiring hospitalization."
        ]
    },
    {
        "intent": "glossary_quarantine",
        "patterns": [
            "What is quarantine?", "Define quarantine", "Quarantine vs isolation"
        ],
        "responses": [
            "Quarantine separates people who were exposed to a disease but aren't yet sick. Isolation separates people who are already infected. Both prevent disease spread."
        ]
    },
    {
        "intent": "glossary_r0_def",
        "patterns": [
            "What is R0?", "Define R0", "R-naught meaning", "Basic reproduction number"
        ],
        "responses": [
            "R0 (basic reproduction number) is the average number of people an infected person will infect. An R0 above 1 means the outbreak is growing; below 1 means it's shrinking."
        ]
    },
    {
        "intent": "glossary_seroprevalence",
        "patterns": [
            "What is seroprevalence?", "Define seroprevalence", "Seroprevalence meaning"
        ],
        "responses": [
            "Seroprevalence is the percentage of people in a population who have antibodies to a disease. It indicates how many people have been infected or vaccinated."
        ]
    },
    {
        "intent": "glossary_spike_protein",
        "patterns": [
            "What is spike protein?", "Define spike protein", "Spike protein meaning"
        ],
        "responses": [
            "The spike protein is a structure on the virus surface that allows it to enter human cells. Vaccines train the immune system to recognize and attack this protein."
        ]
    },
    {
        "intent": "glossary_t_cell",
        "patterns": [
            "What are T-cells?", "Define T-cells", "T-cell immunity"
        ],
        "responses": [
            "T-cells are white blood cells that help the immune system. Some kill infected cells (killer T-cells), while others coordinate the immune response (helper T-cells). They provide long-lasting immunity."
        ]
    },
    {
        "intent": "glossary_thrombosis",
        "patterns": [
            "What is thrombosis?", "Define thrombosis", "Blood clots COVID"
        ],
        "responses": [
            "Thrombosis is the formation of blood clots inside blood vessels. COVID-19 can increase clotting risk, leading to complications like pulmonary embolism or stroke."
        ]
    },
    {
        "intent": "glossary_vaccine_efficacy",
        "patterns": [
            "What is vaccine efficacy?", "Define vaccine efficacy", "Efficacy vs effectiveness"
        ],
        "responses": [
            "Vaccine efficacy measures how well a vaccine works in controlled trials. Effectiveness measures real-world performance. A 95% efficacy means 95% reduction in disease among vaccinated people."
        ]
    },
    {
        "intent": "glossary_ventilator",
        "patterns": [
            "What is a ventilator?", "Define ventilator", "Mechanical ventilation"
        ],
        "responses": [
            "A ventilator is a machine that helps patients breathe when they can't do so on their own. Severe COVID-19 patients may need ventilation due to respiratory failure."
        ]
    },
    {
        "intent": "glossary_viral_load",
        "patterns": [
            "What is viral load?", "Define viral load", "Viral load meaning"
        ],
        "responses": [
            "Viral load is the amount of virus in a sample (blood, saliva, etc.). Higher viral load generally means more infectious and potentially more severe illness."
        ]
    },
    {
        "intent": "glossary_zoonotic_def",
        "patterns": [
            "What does zoonotic mean?", "Define zoonotic", "Zoonotic disease"
        ],
        "responses": [
            "Zoonotic means a disease that can jump from animals to humans. COVID-19 is believed to be zoonotic, likely originating from bats."
        ]
    },
    {
        "intent": "glossary_anosmia",
        "patterns": [
            "What is anosmia?", "Define anosmia", "Loss of smell"
        ],
        "responses": [
            "Anosmia is the loss of the sense of smell. It's a distinctive symptom of COVID-19, often occurring without nasal congestion."
        ]
    },
    {
        "intent": "glossary_dyspnea",
        "patterns": [
            "What is dyspnea?", "Define dyspnea", "Shortness of breath medical term"
        ],
        "responses": [
            "Dyspnea is the medical term for shortness of breath or difficulty breathing. It's a common symptom of severe COVID-19."
        ]
    },
    {
        "intent": "glossary_cytokine",
        "patterns": [
            "What are cytokines?", "Define cytokines", "Cytokine meaning"
        ],
        "responses": [
            "Cytokines are signaling proteins that regulate immune and inflammatory responses. In severe COVID-19, excessive cytokine release (cytokine storm) can cause tissue damage."
        ]
    },
    {
        "intent": "glossary_convalescent_plasma",
        "patterns": [
            "What is convalescent plasma?", "Define convalescent plasma", "Plasma therapy"
        ],
        "responses": [
            "Convalescent plasma is blood plasma from recovered COVID-19 patients containing antibodies. It was used as a treatment early in the pandemic, though evidence of effectiveness is mixed."
        ]
    },
    {
        "intent": "glossary_ecmo",
        "patterns": [
            "What is ECMO?", "Define ECMO", "ECMO meaning"
        ],
        "responses": [
            "ECMO (Extracorporeal Membrane Oxygenation) is a machine that oxygenates blood outside the body. It's used as a last resort for critically ill COVID-19 patients when ventilators aren't enough."
        ]
    },
    {
        "intent": "glossary_monoclonal",
        "patterns": [
            "What are monoclonal antibodies?", "Define monoclonal antibodies", "Antibody therapy"
        ],
        "responses": [
            "Monoclonal antibodies are lab-made proteins that mimic natural antibodies. They can bind to the virus and prevent it from infecting cells, used as a COVID-19 treatment."
        ]
    },
    {
        "intent": "glossary_remdesivir",
        "patterns": [
            "What is remdesivir?", "Define remdesivir", "Remdesivir drug"
        ],
        "responses": [
            "Remdesivir is an antiviral medication that inhibits viral replication. It's approved for treating hospitalized COVID-19 patients and can shorten recovery time."
        ]
    },
    {
        "intent": "glossary_flattening_curve",
        "patterns": [
            "What does flatten the curve mean?", "Flatten the curve meaning", "Define flatten the curve"
        ],
        "responses": [
            "Flattening the curve means slowing the spread of disease to prevent healthcare systems from being overwhelmed. Measures like social distancing help spread cases over a longer period."
        ]
    },
    {
        "intent": "glossary_super_spreader",
        "patterns": [
            "What is a super spreader?", "Define super spreader", "Super spreader event"
        ],
        "responses": [
            "A super spreader is a person who infects an unusually large number of others. A super spreader event is a gathering where many people get infected at once."
        ]
    },
    {
        "intent": "niv_india",
        "patterns": [
            "What is NIV?", "National Institute of Virology", "NIV Pune",
            "BSL-4 lab India", "Who sequences virus in India?"
        ],
        "responses": [
            "The National Institute of Virology (NIV) in Pune is India's premier virology lab. It has a Bio-Safety Level-4 (BSL-4) facility to culture novel viruses and sequence viral genomes. NIV sequenced SARS-CoV-2 from Indian patients."
        ]
    },
    {
        "intent": "lopinavir_ritonavir",
        "patterns": [
            "What is Lopinavir?", "Lopinavir-Ritonavir", "Anti-HIV drugs for COVID",
            "India treatment protocol"
        ],
        "responses": [
            "Lopinavir and Ritonavir are anti-HIV drugs that were used early in the pandemic for high-risk COVID-19 patients (elderly, diabetic, immunocompromised). However, evidence of effectiveness was limited and they can cause significant side effects."
        ]
    },
    {
        "intent": "thermal_scanners",
        "patterns": [
            "Do thermal scanners work?", "Temperature screening", "Airport screening effective?",
            "Thermal cameras COVID"
        ],
        "responses": [
            "Thermal scanners can detect fever (high temperature) but cannot detect people who are infected but not yet sick. Since incubation is 2-14 days, many infected people pass through without fever."
        ]
    },
    {
        "intent": "swimming_pool_safety",
        "patterns": [
            "Can I get COVID from swimming pool?", "Swimming pool transmission", "Chlorine kills virus?",
            "Is pool safe?"
        ],
        "responses": [
            "Highly unlikely. COVID-19 is a respiratory droplet infection, not waterborne. Chlorination of swimming pools to recommended levels can inactivate the virus."
        ]
    },
    {
        "intent": "meat_safety",
        "patterns": [
            "Is eating chicken safe?", "Can I eat meat?", "Food transmission COVID",
            "Is it a foodborne virus?"
        ],
        "responses": [
            "Yes, it's safe to eat meat. COVID-19 is a respiratory virus, not a foodborne one. There's no evidence of transmission through food, including chicken, mutton, or any meat products."
        ]
    },
    {
        "intent": "myth_hot_climate",
        "patterns": [
            "Can heat kill COVID?", "Does hot weather stop COVID?", "Summer and coronavirus",
            "Tropical countries immune?"
        ],
        "responses": [
            "Myth: This is FALSE. COVID-19 can be transmitted in ALL climates, including hot and humid areas. Climate does not prevent transmission. Protection measures (masks, hand hygiene) are needed everywhere."
        ]
    },
    {
        "intent": "myth_mosquito",
        "patterns": [
            "Can mosquitoes spread COVID?", "Mosquito transmission", "Is it like malaria?"
        ],
        "responses": [
            "Myth: This is FALSE. There is no evidence that mosquitoes can transmit COVID-19. It spreads through respiratory droplets, not insect bites."
        ]
    },
    {
        "intent": "myth_garlic",
        "patterns": [
            "Does garlic cure COVID?", "Home remedies COVID", "Garlic prevent coronavirus?",
            "Natural cures"
        ],
        "responses": [
            "Myth: While garlic is healthy and has some antimicrobial properties, there is NO evidence it can prevent or treat COVID-19. Rely on proven measures like vaccination and hygiene."
        ]
    },
    {
        "intent": "myth_pneumonia_vaccine",
        "patterns": [
            "Does pneumonia vaccine protect against COVID?", "Pneumococcal vaccine", "Hib vaccine COVID"
        ],
        "responses": [
            "No. Pneumonia vaccines (pneumococcal, Hib) do NOT protect against COVID-19. The virus is so new it needs its own vaccine. However, these vaccines are still recommended for overall respiratory health."
        ]
    },
    {
        "intent": "flu_vs_covid_symptoms",
        "patterns": [
            "Difference between flu and COVID?", "Is it flu or COVID?", "How to tell them apart?"
        ],
        "responses": [
            "Cough and cold alone could be an allergy. Fever with cough/cold suggests flu. Fever with cough AND breathlessness is a key COVID-19 symptom. Get tested if you have trouble breathing."
        ]
    },
    {
        "intent": "sari_definition",
        "patterns": [
            "What is SARI?", "Define SARI", "Severe Acute Respiratory Infection"
        ],
        "responses": [
            "SARI (Severe Acute Respiratory Infection) is a clinical term for severe respiratory illness. COVID-19 patients often present with SARI, which includes severe pneumonia, ARDS (Acute Respiratory Distress Syndrome), sepsis, or septic shock."
        ]
    },
    {
        "intent": "india_testing_labs",
        "patterns": [
            "Where to get tested in India?", "COVID labs India", "ICMR labs", "NCDC labs"
        ],
        "responses": [
            "In India, you can get tested at 52 ICMR (Indian Council of Medical Research) labs, 10 NCDC (National Centre for Disease Control) labs, and the NIV in Pune. Private labs are also authorized."
        ]
    },
    {
        "intent": "respiratory_hygiene",
        "patterns": [
            "How to cough safely?", "Respiratory hygiene", "Cough etiquette",
            "How to sneeze properly?"
        ],
        "responses": [
            "Cover your mouth and nose with your bent elbow or a tissue when coughing or sneezing. Dispose of used tissues immediately in a closed bin. Then wash your hands."
        ]
    },
    {
        "intent": "lipid_envelope_detail",
        "patterns": [
            "How does soap kill virus?", "Lipid envelope explanation", "Why soap works",
            "Soap science"
        ],
        "responses": [
            "Soap molecules have a water-loving head and an oil-loving tail. The tail inserts into the virus's fatty (lipid) envelope and breaks it apart like a crowbar. This dissolves the virus, which is then washed away by water."
        ]
    },
    {
        "intent": "ards_definition",
        "patterns": [
            "What is ARDS?", "Define ARDS", "Acute Respiratory Distress Syndrome"
        ],
        "responses": [
            "ARDS (Acute Respiratory Distress Syndrome) is a life-threatening condition where fluid builds up in the lungs' air sacs, preventing oxygen from reaching the bloodstream. Severe COVID-19 can cause ARDS, requiring ventilation."
        ]
    }
]
