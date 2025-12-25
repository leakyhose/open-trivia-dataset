# Open Trivia Dataset

A dataset of around 4,700 trivia questions extracted from the [Open Trivia Database](https://opentdb.com/). The Open Trivia Database API restricts question retrieval to 50 questions per request, and there is no way to access all the questions in one go.

## How It Works

### `retrieve.py`
Repeatedly fetches questions in batches of 50, fetching the modulo of the number of questions first. Has a 5.1 second delay to avoid rate limiting. Maintains a consistent session token to avoid duplicates. Takes 8 minutes to retrieve all the questions currently.

### `parser.py`
Organizes the complete dataset by splitting it into organized files split by category and difficulty. All output files are saved to the `data/` directory.