import re


def is_valid_sentence(sentence):
    # 1) Câu được bắt đầu bằng ký tự in hoa, theo sau bởi ký tự thường
    if not re.search(r"^[A-Z][a-z]", sentence):
        return False

    # 2) Kết thúc bằng dấu chấm hoặc sau một ký tự in hoa
    if not re.search(r"[A-Za-z]\.$|[A-Z]$", sentence):
        return False

    # 3) Các từ cách nhau bằng một khoảng trắng, không chấp nhận nhiều hơn 1 khoảng trắng liên tiếp
    if re.search(r"\s{2,}", sentence):
        return False

    # 4) Không tồn tại hai ký tự liên tiếp viết hoa
    if re.search(r"[A-Z]{2,}", sentence):
        return False

    return True


# Ví dụ sử dụng:
sentences = [
    "Hello world.",
    "bat dau bang ky tu in thuong.",
    "This is a Test sentence.",
    "Ket thuc la mot ky tu in hoA",
    "Incorrect  sentence due to  extra spaces.",
    "AnotherIncorrectSentence",
    "Ends with period.",
    "NO TWO uppercase letters"
]

for sentence in sentences:
    print(f"\"{sentence}\": {is_valid_sentence(sentence)}")