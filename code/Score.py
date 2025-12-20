import os, json

from pathlib import Path

def get_score_path():
    docs_dir = Path.home() / '.little_snake_game'
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir / 'scores.json'

score_file_path = get_score_path()

def save_score(score):
    scores = load_scores()

    scores.append(score)

    scores.sort(reverse=True)

    scores = scores[:5]

    with open(score_file_path, 'w') as f:
        json.dump(scores, f)


def load_scores():
    if os.path.exists(score_file_path):
        with open(score_file_path, 'r') as f:
            return json.load(f)
    else:
        return []
