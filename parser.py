import json
from pathlib import Path
from collections import defaultdict

INPUT_FILE = "data/all_questions.json"
OUTPUT_DIR = Path("data")

def parse_questions():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        all_questions = json.load(f)
    
    by_category = defaultdict(list)
    by_difficulty = defaultdict(list)
    
    for question in all_questions:
        category = question.get("category", "Unknown")
        difficulty = question.get("difficulty", "unknown")
        
        by_category[category].append(question)
        by_difficulty[difficulty].append(question)
    
    for category, questions in by_category.items():
        filename = category.replace("&", "and").replace(":", "").replace("/", "-").replace(" ", "_")
        filepath = OUTPUT_DIR / f"category_{filename}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
            
    for difficulty, questions in by_difficulty.items():
        filepath = OUTPUT_DIR / f"difficulty_{difficulty}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        
if __name__ == "__main__":
    parse_questions()
    print("Parsed all_questions into respective jsons by category and difficulty.")
