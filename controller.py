import csv
from typing import ContextManager
from storage.data_for_verification import testcase


class Controller:


    def __init__(self) -> None:
        self.name_file = "conf/case.csv"
        
    def gendata(self):
        with open(self.name_file, "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                mas = ",".join(row).split(",")
                yield (mas[0], mas[1].lower()=="true")



# @ContextManager()
# def example():
#     print("1")
#     yield
#     print("2")

# def main():
#     print("do main")

# if __name__ == "__main__":
#     with example() as a:
#         main()


