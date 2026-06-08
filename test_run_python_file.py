from functions.run_python_file import run_python_file


def test_run_python_file() -> None:
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 7 * 2"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    test_run_python_file()