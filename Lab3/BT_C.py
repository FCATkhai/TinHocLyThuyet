import re


def process_text(text):
    words = text.split()

    # Các từ thỏa mãn từng điều kiện
    results = {
        'contains_a_and_digit': [],
        'contains_a_followed_by_b': [],
        'starts_with_a_and_ends_with_b': [],
        'contains_only_a_to_z_and_underscore': [],
        'length_is_5': [],
        'contains_h': [],
        'starts_with_digit': [],
        'contains_underscore': [],
        'date_format_conversion': []
    }

    for word in words:
        # 1. Các từ có chứa các ký tự thường ‘a-z’ và số từ ‘0-9’
        if re.search(r'[a-z].*\d|[0-9].*[a-z]', word):
            results['contains_a_and_digit'].append(word)

        # 2. Các từ có chứa ký tự ‘a’ theo sau bởi b (b xuất hiện ít nhất 0 lần)
        if re.search(r'a*b', word):
            results['contains_a_followed_by_b'].append(word)

        # 3. Các từ bắt đầu bằng ‘a’, theo sau là ký tự bất kỳ và kết thúc bằng ‘b’
        if re.match(r'^a.*b$', word):
            results['starts_with_a_and_ends_with_b'].append(word)

        # 4. Các từ chỉ chứa ký tự thường ‘a-z’ và ‘_’
        if re.match(r'^[a-z_]+$', word):
            results['contains_only_a_to_z_and_underscore'].append(word)

        # 5. Các từ có chiều dài là 5
        if re.match(r'\b\w{5}\b', word):
            results['length_is_5'].append(word)

        # 6. Các từ có chứa ký tự ‘h’
        if 'h' in word:
            results['contains_h'].append(word)

        # 7. Các từ bắt đầu là số từ ‘0-9’
        if re.match(r'^\d', word):
            results['starts_with_digit'].append(word)

        # 8. Các từ có chứa dấu ‘_’ và thay bằng khoảng trắng
        if '_' in word:
            results['contains_underscore'].append(word.replace('_', ' '))

        # 9. Có chứa định dạng mm-dd-yy, và chuyển thành định dạng dd-mm-yy
        if re.match(r'\d{2}-\d{2}-\d{2}', word):
            new_date = re.sub(r'(\d{2})-(\d{2})-(\d{2})', r'\2-\1-\3', word)
            results['date_format_conversion'].append(new_date)

    return results


# Ví dụ sử dụng:
text = "abc123 abc bbb abb a_z 12345 hello 11-06-24 a_ b_ h h_ hello_123"

result = process_text(text)

# In kết quả
for key, value in result.items():
    print(f"{key}: {value}")
