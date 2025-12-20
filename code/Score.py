import os, json

from pathlib import Path

def get_score_path():
    # Define o caminho para a pasta atual onde o script está rodando
    base_dir = Path(__file__).parent.absolute()
    
    # Define o arquivo score.json dentro dessa mesma pasta
    score_file = base_dir / 'scores.json'
    
    return score_file

score_file_path = get_score_path()

def save_score(score):
    scores = load_scores()

    scores.append(score)

    scores.sort(reverse=True)

    scores = scores[:5]

    with open(score_file_path, 'w') as f:
        json.dump(scores, f)


def load_scores():
def load_scores():
    if os.path.exists(score_file_path):
        try:
            with open(score_file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            # Se o arquivo estiver vazio ou corrompido, retorna lista vazia
            return []
    else:
        return []
