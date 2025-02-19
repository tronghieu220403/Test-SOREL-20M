import ember
import lightgbm as lgb
import numpy as np
import sys
import os


def extract_features(binary_path):
    """Trích xuất đặc trưng từ file PE bằng Ember"""
    print(f"Trích xuất đặc trưng từ file: {binary_path}")
    try:
        file_data = open(binary_path, "rb").read()
        extractor = ember.PEFeatureExtractor()
        return np.array(extractor.feature_vector(file_data), dtype=np.float32).reshape(1, -1)
    except Exception as e:
        print(f"Lỗi khi trích xuất đặc trưng: {e}")
        return None

def load_model(model_path):
    """Tải mô hình LightGBM đã huấn luyện"""
    try:
        sys.stdout = None
        model = lgb.Booster(model_file=model_path)
        sys.stdout = sys.__stdout__
        return model
    except Exception as e:
        print(f"Lỗi khi tải mô hình: {e}")
        return None

def predict_malware(file_path, model_path):
    """Phân loại file PE là malware hay không"""
    features = extract_features(file_path)
    if features is None:
        return "Không thể trích xuất đặc trưng"
    
    model = load_model(model_path)
    if model is None:
        return "Không thể tải mô hình"
    
    prediction = model.predict(features)[0]
    print(f"Xác suất: {prediction}")
    return "Mã độc" if prediction > 0.5 else "An toàn"

if __name__ == "__main__":
    
    file_path = "a4c0c02069ca253e4324d584c7bbebb3e732d7db9d19fd8fa350d6d537fcd3fe.exe.bin"
    model_path = "lightgbm.model"
    
    if not os.path.exists(file_path) or not os.path.exists(model_path):
        print("File hoặc model không tồn tại!")
        sys.exit(1)
    
    result = predict_malware(file_path, model_path)
    print(f"Kết quả model: {result}")
