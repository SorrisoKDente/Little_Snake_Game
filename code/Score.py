import os, json

score_file_path = os.path.join(os.path.dirname(__file__), '..', 'asset', 'scores.json')

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