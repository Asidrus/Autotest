class testcase:
    text: str
    valid: bool
    result: bool

    def __init__(self, text, valid) -> None:
        self.text = text
        self.valid = valid
        self.result = False

    @property
    def res_true(self):
        self.result = True



