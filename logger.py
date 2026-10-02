from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self):
        dir_path = Path(__file__).resolve().parent / "logs"
        dir_path.mkdir(exist_ok=True)
        filename = "logs" / Path(str(int(datetime.now().timestamp())) + ".txt")
        if not filename.exists():
            filename.touch()
        self.fhandle = open(filename, "w")

    def log(self, message: str):
        displayed_msg = "[{0}] {1}".format(
            datetime.now().strftime("%H:%M:%S.%f"),
            message
        )
        print(displayed_msg)
        self.fhandle.write(displayed_msg + "\n")

    def close(self):
        self.fhandle.close()
