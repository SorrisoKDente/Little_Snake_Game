import os, json

from pathlib import Path

def get_score_path():
    try:
        docs_dir = Path.home() / '.little_snake_game'
        docs_dir.mkdir(parents=True, exist_ok=True)

        #verifica se tem permissão de escrita
        test_file = docs_dir / '.test_write'
        test_file.touch()
        test_file.unlink()

        return docs_dir / 'scores.json'

    except (PermissionError, OSError):
        current_dir = Path(__file__).parent.parent / ".scores"
        current_dir.mkdir(parents=True, exist_ok=True)
        return current_dir / 'scores.json'

score_file_path = get_score_path()

def save_score(score):
    try:
        scores = load_scores()

        scores.append(score)

        scores.sort(reverse=True)

        scores = scores[:5]

        with open(score_file_path, 'w') as f:
            json.dump(scores, f)
    except Exception as e:
        print(f"Failed to save score: {e}")

def load_scores():
    try:
        if os.path.exists(score_file_path):
            with open(score_file_path, 'r') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Failed to load scores: {e}")
        return []
