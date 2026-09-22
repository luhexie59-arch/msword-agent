# MSword-agent
Auto type-in Microsoft Word with realistic typos and pauses

## How to use
1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run main script**
- Usage
```bash
python main.py [-h] [-o OUTPUT] [-c] filename
```
- example
```bash
python main.py example.txt -o example_out.docx -c
```

| Arguments | Explanation |
| -- | -- |
| filename | TXT file containing the text you want to write |
| -o, --output | Output file: *.docx |
| -c, --close_word | Close Word's window automatically after task if set to true

## Warning
Unintended actions **MAY** happen. Only run this program in a virtual machine or in a safe environment.