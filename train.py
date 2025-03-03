import zipfile
import tarfile
import random
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import CSVLogger
from data_processing import extract_zip, extract_tar, get_image_paths, show
from k_fold import create_kfold_sets, print_kfold_sets
from model import unet
from dataset import xBD
from plot import plot_history

input_dir = 'train/images'
target_dir = 'train/targets'
img_size = (1024, 1024)
num_classes = 1 # sigmoid 는 1로 설정해야한다
batch_size = 8

# 데이터 압축 해제
# zip_file_path = 'path_to_your_zip_file.zip'
tar_file_path = 'path_to_your_tar_file.tar'
extract_to_path = 'path_to_extract'

# extract_zip(zip_file_path, extract_to_path)
extract_tar(tar_file_path, extract_to_path)

# 이미지 경로 설정
input_img_paths, target_img_paths = get_image_paths(input_dir, target_dir)

show(input_img_paths[7], target_img_paths[7])

seed = 1337

random.Random(seed).shuffle(input_img_paths)
random.Random(seed).shuffle(target_img_paths)

# KFold 설정
num_folds = 28 # 예시 5
epochs_per_fold = 20  # 각 fold마다 수행할 에폭 수

# 배열을 num_folds분할
input_splits = np.array_split(input_img_paths, num_folds)
target_splits = np.array_split(target_img_paths, num_folds)

# 검증용과 훈련용 데이터셋 생성
validation_sets, train_input_sets, train_target_sets = create_kfold_sets(num_folds, input_splits, target_splits)

# 체크포인트 및 백업 기록 폴더 생성
result_dir = "path_to_your_result"
checkpoint_dir = f"{result_dir}/model" #.h5파일 담을 폴더 설정
history_dir = f"{result_dir}/histories" # history 파일 담을 폴더 설정
os.makedirs(checkpoint_dir, exist_ok=True)
os.makedirs(history_dir, exist_ok=True)

# 모델 파일 경로 및 초기 에포크와 최소 val_loss 설정
model_path = f"{checkpoint_dir}/model_epoch_000.h5"
initial_epoch = 0  # 사용자가 직접 지정
last_val_loss = 1 # 사용자가 직접 지정

# 모델 로드
if os.path.exists(model_path):
    best_model = load_model(model_path)
else:
    best_model = unet(img_size, num_classes)
    best_model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    initial_epoch = 0
    last_val_loss = np.inf  # 초기값 설정

# CSV 파일 이름 생성
history_file = os.path.join(history_dir, 'training_history.csv')

# CSVLogger 설정 (새로운 파일 생성)
csv_logger = CSVLogger(history_file, append=True)

best_model.summary()

# 학습 설정
total_epochs = epochs_per_fold * num_folds

# 데이터셋 분할 및 학습
for epoch in range(initial_epoch, total_epochs):
    fold = epoch % num_folds

    train_gen = xBD(batch_size, img_size, train_input_sets[fold], train_target_sets[fold])
    val_gen = xBD(batch_size, img_size, validation_sets[fold][0], validation_sets[fold][1])

    print(f"Epoch {epoch}/{total_epochs}")
    history = best_model.fit(train_gen, validation_data=val_gen, initial_epoch=epoch, epochs=epoch+1, verbose=1, callbacks=[csv_logger])
    # 손실 및 정확도 출력
    train_loss = history.history['loss'][0]
    train_acc = history.history['accuracy'][0]
    val_loss = history.history['val_loss'][0]
    val_acc = history.history['val_accuracy'][0]

    # 결과를 명확히 출력
    print(f"- loss: {train_loss:.4f} - accuracy: {train_acc:.4f} - val_loss: {val_loss:.4f} - val_accuracy: {val_acc:.4f}")

    # val_loss가 최소일때마다 저장하기
    current_val_loss = history.history['val_loss'][0]
    if current_val_loss < last_val_loss:
        last_val_loss = current_val_loss
        model_filename = os.path.join(checkpoint_dir, f'model_epoch_{epoch}.h5')
        best_model.save(model_filename)
        print(f"val_loss improved to {current_val_loss:.4f}, saving model to {model_filename}")

# CSV 파일 로드
plot_history(history_file)
