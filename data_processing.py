import zipfile
import tarfile
from PIL import Image
import numpy as np


def extract_zip(zip_file_path, extract_to_path):
    """zip 압축풀기"""
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
    print(f"{extract_to_path} 경로에 압축을 해제합니다.")

def extract_tar(tar_file_path, extract_to_path):
    """tar 압축풀기"""
    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extractall(extract_to_path)
    print(f"{extract_to_path} 경로에 압축을 해제합니다.")

def get_image_info(label_image_path):
    """단일 사진 클래스 개수 확인."""
    # 이미지 로드 및 nupmy 배열로 변환
    label_image = Image.open(label_image_path)
    label_image_array = np.array(label_image)

    # 레이블 이미지의 고유값과 분포 시각화
    unique, counts = np.unique(label_image_array, return_counts=True)

    # 고유값 분포를 프린트
    print("Unique pixel values in label image:", unique)
    print("Counts for each value:", counts)
    return label_image, label_image_array