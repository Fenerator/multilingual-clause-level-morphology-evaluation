#!/usr/bin/env python

# from Levenshtein import distance as lev # TODO
import sys
import os
import os.path


def read_file(file):
    with open(file, 'r', encoding='utf-8') as infile:
        # or without \n lines = [line.rstrip('\n') for line in infile]
        lines = infile.readlines()
        print(len(lines))

        # keep only the second part of the line after '\t'
        content = [line.rstrip().split('\t')[1] for line in lines]

    return content


def calculate_matching(gold, predictions):
    """
    Args:
        gold (list of str)
        predictions (list of str)

    Returns:
        (float, list): proportion of matching predictions, position of matching predictions
    """
    matching = []  # denotes whether predictions at the position are matching
    lev_distances = []  # stores edit distances per sentence
    z = 0
    for i, j in zip(gold, predictions):
        if i == j:
            z += 1
            matching.append(1)
        else:
            matching.append(0)

        lev_distances.append(calculate_levensthein(i, j))

    mean_distance = sum(lev_distances)/len(lev_distances)

    return z/len(gold), matching, lev_distances, mean_distance


def calculate_levensthein(gold, prediction):
    try:
        dist = lev(gold, prediction)
        return dist
    except Exception as e:
        print(f'{e}, gold: {gold}, prediction: {prediction}')
        return 300  # TODO


def main():
    # input_dir = sys.argv[1]
    # output_dir = sys.argv[2]
    input_dir = '/home/dug/Py/mrl_2022_shared_task_evaluation'
    output_dir = '/home/dug/Py/mrl_2022_shared_task_evaluation'

    submit_dir = os.path.join(input_dir, 'res')  # submission
    truth_dir = os.path.join(input_dir, 'ref')  # gold

    if not os.path.isdir(submit_dir):
        print("%s doesn't exist" % submit_dir)

    if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_filename = os.path.join(output_dir, 'scores.txt')
        output_file = open(output_filename, 'wb')

        gold_files = os.listdir(truth_dir)
        for file in gold_files:
            gold_file = os.path.join(truth_dir, file)
            corresponding_submission_file = os.path.join(submit_dir, file)
            if os.path.exists(corresponding_submission_file):
                print(
                    f'Evaluating submission: {corresponding_submission_file} (comparing to gold: {gold_file})')

                gold = read_file(gold_file)
                predictions = read_file(corresponding_submission_file)

                assert len(gold) == len(
                    predictions), f'Len of predictions ({len(predictions)}) is not same as gold ({len(gold)}) '

                accuracy, _, edit_distances, mean_edit_distance = calculate_matching(
                    gold, predictions)

                print(f'Matching predictions: {accuracy}')
                print(f'Mean edit distance: {mean_edit_distance}')

                output_file.write(b'Matching predictions %f\n' % accuracy)

                output_file.write(b'Mean edit distance %f' %
                                  mean_edit_distance)

        output_file.close()


if __name__ == "__main__":
    main()


'''
lines cannot be empty
Input:
I will give him to her
Ich werde ihn ihr geben

Gold
I will give him to her
Ich werde ihn ihr geben

Calculate exact match accuracy ratings (proportion of correctly predicted lemma and features)
using ==
Calcultate Edit Distance (Levenstein distance, averaged over all predictions)
using levenstein

both can be used for all subtasks
average over languages as well, or is test set mixed?
'''
