# v8.0.0

데이터 100프로 원본 훈련시

```
정확도: 96.85%
평균 교차 IoU: 69.38%
```

![loss-accuracy.png](https://raw.githubusercontent.com/sibas-lab/xBD-Building-Segmentation/main/result/v8.0.0/loss-accuracy.png)

‌

![val_loss.png](https://raw.githubusercontent.com/sibas-lab/xBD-Building-Segmentation/main/result/v8.0.0/val_loss.png)

현재 그래프 상으로 과적합 현상 발생 없음
특징: 베이스 모델 50% 훈련 데이터일 경우 과적합이 발생했으나 훈련 데이터 증가로 인해 과적합 현상이 해소됨

다만 기존 검증 비율이 전체 데이터셋에 35프로 정도 차지하므로 일반적인 모델보다 매우 높은 비율을 가지고 있으므로 과적합 현상이 일어날수 있다.

그러므로 일반적인 비율 10 - 20%로 검증 데이터 비율로 맞춰서 실험을 진행할 필요할 수 있다.
