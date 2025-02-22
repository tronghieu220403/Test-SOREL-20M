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

def predict_malware(file_path, model):
    """Phân loại file PE là malware hay không"""
    features = extract_features(file_path)
    if features is None:
        return "Không thể trích xuất đặc trưng"
    try:
        prediction = model.predict(features)[0]
        print(f"Xác suất: {prediction}")
        return "Mã độc" if prediction > 0.5 else "An toàn"
    except Exception as e:
        return f"Không thể tính xác suất: {e}"

def process_files_in_directory(dir_path, model):
    for root, _, files in os.walk(dir_path):
        for file in files:
            #if file.lower().endswith(('.dll', '.exe')):  # Chỉ xử lý file .dll và .exe
                try:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    if file_size > 30 * (2 ** 20):
                        print(f"Skip {file_path}, size {file_size}")
                    else:
                        print(f"Đang xử lý: {file_path}")
                        result = predict_malware(file_path, model)
                        print(f"Kết quả model: {result}")
                except Exception as e:
                    print(f"Skip {file_path}: {e}")
                print(flush=True)

if __name__ == "__main__":
    
    model_path = "lightgbm.model"
    
    if not os.path.exists(model_path):
        print("Model không tồn tại!")
        sys.exit(1)
    
    model = load_model(model_path)
    if model is None:
        print("Không thể tải mô hình")
        sys.exit(0)
    
    sys.stdout = open("output.txt", "w", encoding="utf-8")
    process_files_in_directory("E:\\dataset\\MalDict\\maldict_disarmed_behavior_test\\f", model)

