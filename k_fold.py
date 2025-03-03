import numpy as np

def create_kfold_sets(num_folds, input_splits, target_splits):
    """검증용과 훈련용 데이터셋을 나누는 함수"""
    validation_sets = []
    train_input_sets = []
    train_target_sets = []

    for i in range(num_folds):
        val_input = input_splits[i]
        val_target = target_splits[i]
        train_input = np.concatenate([input_splits[j] for j in range(num_folds) if j != i])
        train_target = np.concatenate([target_splits[j] for j in range(num_folds) if j != i])

        validation_sets.append((val_input, val_target))
        train_input_sets.append(train_input)
        train_target_sets.append(train_target)

    return validation_sets, train_input_sets, train_target_sets


def print_kfold_sets(num_folds: int, train_input_sets, train_target_sets, validation_sets):
    for i in range(num_folds):
        print(f"Fold {i+1}:")
        print(f"Validation Set - Input: {len(validation_sets[i][0])}, Target: {len(validation_sets[i][1])}")
        print(f"Train Set - Input: {len(train_input_sets[i])}, Target: {len(train_target_sets[i])}")
        print(f"First Validation Input: {validation_sets[i][0][0]}")
        print(f"First Validation Target: {validation_sets[i][1][0]}")
        print()
