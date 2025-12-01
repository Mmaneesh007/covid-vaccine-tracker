# 📚 How to Add Medical Knowledge to Your Chatbot

## ✅ Your Chatbot Now Supports Multiple Sources

The chatbot will automatically read **all `.txt` files** from the `knowledge/` folder.

---

## 🎯 **Recommended Medical Resources**

### 1. **WHO (World Health Organization)**

- **COVID-19 Vaccine Safety Surveillance Manual**: [Download PDF](https://iris.who.int/bitstream/handle/10665/352959/9789240047372-eng.pdf)
- **COVID-19 Vaccines Technical Documents**: [WHO Page](https://www.who.int/teams/regulation-prequalification/eul/covid-19)
- **COVID-19 Q&A**: [WHO FAQ](https://www.who.int/news-room/questions-and-answers/item/coronavirus-disease-covid-19-vaccines)

### 2. **CDC (Centers for Disease Control)**

- **Vaccine Information Statements**: [CDC](https://www.cdc.gov/vaccines/hcp/vis/vis-statements/covid19.html)
- **COVID-19 Vaccine Facts PDF**: [Direct Download](https://www.cdc.gov/coronavirus/2019-ncov/downloads/vaccines/facts-about-covid-vaccines.pdf)
- **Clinical Considerations**: [CDC Guidelines](https://www.cdc.gov/vaccines/covid-19/clinical-considerations/interim-considerations-us.html)

### 3. **Medical Journals & Research**

- **The Lancet COVID-19 Resource Centre**: [Free Articles](https://www.thelancet.com/coronavirus)
- **NEJM COVID-19 Collection**: [Free Resources](https://www.nejm.org/coronavirus)
- **NIH COVID-19 Treatment Guidelines**: [PDF Available](https://www.covid19treatmentguidelines.nih.gov/)

---

## 📥 **How to Add a New Source**

### Option 1: Text Files (Easiest)

1. Get your medical PDF or document
2. Copy the text content (Ctrl+A, Ctrl+C from the PDF)
3. Create a new `.txt` file in the `knowledge/` folder
4. Paste the text and name it descriptively (e.g., `who_vaccine_safety.txt`)
5. **Delete the old cache**: Delete `data/tfidf_cache.pkl`
6. Restart Streamlit - done!

### Option 2: Using the PDF Extractor Script

1. Put your PDF in the project folder
2. Run:

   ```bash
   python extract_pdf.py your_document.pdf
   ```

3. Move the output `.txt` file to `knowledge/`
4. Delete `data/tfidf_cache.pkl`
5. Restart Streamlit

---

## ⚙️ **Current Knowledge Sources**

The chatbot currently has:

- ✅ `covid_ebook_1.txt` (Your original eBook)

Add more by dropping `.txt` files into the `knowledge/` folder!

---

## 🚫 **What NOT to Add**

❌ **Dictionaries** - Won't improve medical knowledge  
❌ **General Wikipedia dumps** - Too broad, makes search slow  
❌ **Non-medical content** - Dilutes the chatbot's focus  
❌ **Copyrighted books without permission** - Legal issues

---

## ✅ **What TO Add**

✅ WHO official documents  
✅ CDC fact sheets  
✅ Medical journal articles (open-access)  
✅ Government health guidelines  
✅ Clinical trial summaries  
✅ Vaccine manufacturer information sheets

---

## 🔄 **Refreshing the Knowledge Base**

After adding new files:

1. Delete `data/tfidf_cache.pkl` (forces rebuild)
2. Restart your Streamlit app
3. Check the console - you'll see: `Loading knowledge from X file(s)`

---

## 💡 **Tips for Best Results**

- **Keep it focused**: Medical/health content only
- **Quality over quantity**: 5 good sources > 50 random ones
- **Use official sources**: WHO, CDC, NIH are best
- **Check file size**: Keep individual files under 5MB for performance
- **Name files clearly**: `who_safety_2024.txt` not `document1.txt`

---

*The chatbot now intelligently searches across all your knowledge sources to give the best answer!*
