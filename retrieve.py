import time
import json
import requests
import sys

TOKEN_URL = "https://opentdb.com/api_token.php?command=request"
TOTAL_QUESTIONS_URL = "https://opentdb.com/api_count_global.php"
API_URL = "https://opentdb.com/api.php"
OUTPUT_FILE = "./data/all_questions.json"
API_DELAY_SECONDS = 5.1

def get_token():
    r = requests.get(TOKEN_URL)
    r.raise_for_status()
    data = r.json()
    return data["token"]

def get_total_questions():
    r = requests.get(TOTAL_QUESTIONS_URL)
    r.raise_for_status()
    data = r.json()
    return data["overall"]["total_num_of_verified_questions"]

def fetch_batch(token, amount=50):
    params = {
        "amount": amount,
        "token": token
    }
    r = requests.get(API_URL, params=params)
    r.raise_for_status()
    return r.json()

def progress_bar(current, total, bar_length=40):
    fraction = current / total
    filled = int(bar_length * fraction)
    bar = "#" * filled + "-" * (bar_length - filled)
    percent = int(fraction * 100)
    batches_remaining = (total - current) / 50
    time_to_complete = batches_remaining * API_DELAY_SECONDS
    mins, secs = divmod(time_to_complete, 60)

    sys.stdout.write(f"\r[{bar}] {percent}% | ETA: {int(mins)}m {int(secs)}s")
    sys.stdout.flush()

def main():
    token = get_token()
    total_questions = get_total_questions()
    
    print(f"Total questions: {total_questions}")
    print(f"Session token: {token}")

    all_questions = []
    
    if total_questions % 50 != 0: # As API returns 50, fetches the remainder first
        results = fetch_batch(token, amount=(total_questions%50)).get("results", [])
        all_questions.extend(results)
        time.sleep(API_DELAY_SECONDS)

    
    while True:
        data = fetch_batch(token)
        code = data.get("response_code")
        
        if code == 0: # Success 
            results = data.get("results", [])
            all_questions.extend(results)
            progress_bar(len(all_questions), total_questions)
        elif code == 4: # No more questions
            break
        else:
            raise RuntimeError(f"Unexpected error: {code}")
        time.sleep(API_DELAY_SECONDS)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(all_questions)} questions.")

if __name__ == "__main__":
    main()
