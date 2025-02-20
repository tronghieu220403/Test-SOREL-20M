import re

def read_and_parse_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = content.strip().split('\n\n')  # Tách các phần tử theo dòng trống
    parsed_data = {}
    
    for section in sections:
        lines = section.strip().split('\n')
        if lines:
            file_name = lines[0].replace("Đang xử lý: ", "").strip()
            data = " ".join(lines[1:]).strip()  # Gộp các dòng còn lại thành 1 string
            parsed_data[file_name] = data
    
    return parsed_data

def search_strings(target, search_list):
    found_items = [item for item in search_list if item in target]
    return found_items == search_list

# Ví dụ sử dụng
if __name__ == "__main__":
    file_data = read_and_parse_file("output.txt")
    
    total = 0
    total_true = 0
    total_false = 0

    # Kiểm tra nội dung đọc được
    for file, content in file_data.items():
        # print(f"File: {file}\nContent: {content}\n")
        is_not_pe = search_strings(content, ["not a PE binary"])
        is_skip = search_strings(file, ["Skip "]) or search_strings(content, ["Lỗi "]) or search_strings(content, ["Không thể "])
        if not is_not_pe and not is_skip:
           total += 1
           is_safe = search_strings(content, ["An toàn"])
           if not is_safe:
               print(file)
           total_true += is_safe
           total_false += not is_safe
    
    print(total, total_true, total_false)
    