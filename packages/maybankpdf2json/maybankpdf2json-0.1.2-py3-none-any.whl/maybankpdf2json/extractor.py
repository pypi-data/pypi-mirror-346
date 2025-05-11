import io
from .utils import convert_to_json


class MaybankPdf2Json:
    def __init__(self, buffer: io.BufferedReader, pwd: str):
        self.buffer: io.BufferedReader = buffer
        self.pwd: str = pwd

    def json(self) -> list:
        return convert_to_json(self)
