import json
from pathlib import Path

GROUND_TRUTH_DATA = {str(i): int((i % 3) == 0) for i in range(100)}

PREDICTIONS_DIR = Path(__file__).parent.absolute() / 'predictions'
def dump_predictions(prediction_dict, prediction_file):
    with PREDICTIONS_DIR.joinpath(prediction_file).open('w') as f:
        json.dump(prediction_dict, f)

if __name__ == '__main__':
    all_ones = {str(i): 1 for i in range(100)}
    all_zeros = {str(i): 0 for i in range(100)}
    perfect = GROUND_TRUTH_DATA
    worst = {k: 1-v for k, v in GROUND_TRUTH_DATA.items()}
    empty_prediction = {}
    dump_predictions(all_ones, 'all_ones.json')
    dump_predictions(all_zeros, 'all_zeros.json')
    dump_predictions(perfect, 'perfect.json')
    dump_predictions(worst, 'worst.json')
    dump_predictions(empty_prediction, 'empty_prediction.json')



