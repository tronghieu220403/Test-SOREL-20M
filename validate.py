import re
import os

import hashlib

def sha256_of_file(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def read_and_parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = content.strip().split('\n\n')  # Tách các phần tử theo dòng trống
    parsed_data = {}
    
    for section in sections:
        lines = section.strip().split('\n')
        if lines:
            file_name = lines[0].replace("Đang xử lý: ", "").strip()
            file_name = file_name.replace("Skip: ", "").strip()
            file_name = re.sub(r', size .*$', '', file_name)
            data = " ".join(lines[1:]).strip()  # Gộp các dòng còn lại thành 1 string
            parsed_data[file_name] = data
    
    return parsed_data

def search_strings(target, search_list):
    found_items = [item for item in search_list if item in target]
    return found_items == search_list

from pathlib import Path

def list_files(path):
    return [d.name for d in Path(path).iterdir() if not d.is_dir()]

# Ví dụ sử dụng
if __name__ == "__main__":
    output_dir = "E:\\Code\\Github\\Test-SOREL-20M\\"

    total = 0
    total_not_pe = 0
    total_skip = 0
    total_eval = 0
    total_eval_clean = 0
    total_eval_mal = 0

    for file_name in list_files(Path(output_dir)):
        if "output" not in file_name:
            continue

        file_data = read_and_parse_file(output_dir + file_name)

        # Kiểm tra nội dung đọc được
        for file, content in file_data.items():
            # print(f"File: {file}\nContent: {content}\n")
            is_not_pe = search_strings(content, ["not a PE binary"])
            is_skip = search_strings(file, ["Skip "]) or search_strings(content, ["Lỗi "]) or search_strings(content, ["Không thể "])
            total += 1
            total_not_pe += is_not_pe
            total_skip += is_skip
            if is_not_pe or is_skip:
                continue
            if not is_not_pe and not is_skip:
                total_eval += 1
            is_safe = search_strings(content, ["An toàn"])
            #if not is_safe:
                #print(file)
                #print(sha256_of_file(file))
            total_eval_clean += is_safe
            total_eval_mal += not is_safe
        
        #print(f'File: {file_name}')

    print(f'Total {total}, not PE {total_not_pe}, skip {total_skip}')
    print(f'Total evaluation {total_eval}, clean {total_eval_clean}, malware {total_eval_mal}, ratio {total_eval_mal/total_eval:.2f}')
    print()
