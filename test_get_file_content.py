from functions.get_file_content import get_file_content

from config import MAX_CHARS

def test_get_files_content() -> None:
    result = get_file_content("calculator", "lorem.txt")
    if (len(result) >= MAX_CHARS + 10):
        print(f"lorem.txt length: {len(result)}")
        print(f"lorem.txt truncated: {'truncated' in result}")
    else:
        print(result);
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
   


if __name__ == "__main__":
    test_get_files_content()