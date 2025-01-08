# Team-Meme
Repo for our memo annotation and corpus research

Developed annotation guidelines with a group to have students in the class hand-annotate folklore to identify and classify flora and fauny in stories using brat. Using these annotations, we attempted to classify the archetypal roles flora and fauna play in these stories.

---

## **Table of Contents**
1. [Dataset](#dataset)  
   - [Annotation Process](#annotation-process)  
2. [Models](#models)  
3. [Usage](#usage)  
   - [Installation](#installation)  
   - [Running the Code](#running-the-code)  
4. [Directory Structure](#directory-structure)  

---

## **Dataset**

- Our dataset was split into two sections: scraped data from imgflip and hand-annotated data from reddit.
- In total, the imgflip dataset includes 274,748 memes examples, with each meme having one of 2,059 meme templates. Each of these meme templates are templates generated from imgflip.com.
- There were 243 hand-annotated memes in the reddit dataset, 74 of which did not have a template. Of these memes, in addition to annotating for the template, we annotated for it's meta-template. Inspired by knowyourmeme.com's meme template ontology, these were the 5 most basic categories to describe the strucutre of a meme: image macro, reacion image, exploitable, duality, and escalating progression. For more information on these annotations, see out annotation guidelines, or check knowyourmeme.com.

### **Annotation Process**:
- Two trained annotators dually annotated each meme, annotating the following:
  - The meme template, linking a webpage to it from imgflip.com or knowyourmeme.com
  - Transcribing the captioning of the meme
  - Classifying the meta-template

- The Cohen's kappa score for IAA was relatively consistently around 70% for classifying the meta template structure.

---

## **Models**

### **Statistical Models**:
- While we experimented with MobileNetV2, our we fine-tuned the off-the-shelf YOLOv11 for our classification tasks.
- With both template and meta classification we could achieve nearly 100% on test data when we exclusively trained on the scraped data. However, when we tested this on our hand-annotated reddit data, we were only able to achieve about 41% with the reddit template and 22% meta templates. What this suggests is that the YOLO model either overfitted on hand-annotated meta templates, or would basically randomly guess them, so this task needed more data in order to be compatible with this model. In the case of template identification, the model struggled with memes with a more complex or nuanced interpretation of templates that it might not have been trained on from imgflip, more work with data wrangling would likely be able to solve this.

### **LLM Promping**:
- We used OpenAI’s GPT 3.5-turbo and set its temperature to 0 to ensure deterministic responses. We tried promping the LLM with descriptions of each of the metas, image examples, or both. If we prompted the LLM with one of these, it was accurate about 42% of the time (x2 as often as YOLO), and with both it was accurate around 37%. 
- We likely could have increased with accuracy of these LLMs by implementing something like RAG, espcially if we linked our guidelines or knowyourmeme.com's ontology.

---

## **Usage**

### **Installation**
1. Clone the repository
2. For scraping from imgflip, run `scraper/run.sh`
3. For template classification, run `template-classification/reddit_yolo_tests.py` using the `best.pt` in that directory
4. For gpt prompting, run `gpt-prompting/gpt_prompting.py`
5. For meta template prompting, run `meta-template/YOLO_meta.py` with `best.pt` in that directory

---

## **Directory Structure**


