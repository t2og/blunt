import os

OUTPUT_DIR = "output"


def load(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return ""
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return ""


def save(text: str, filename: str, output_dir: str = OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    with open(output_path, "w") as output:
        output.write(text)
