from libs.BugReport.BugReport import BugReport
from datetime import datetime

def main():
    report = BugReport("1u88yKDi46j1AjpSxVr2tp1sdt1oKyCzoLkSXZ99cGh4")
    report.__MaxBugs__ = int(2 + 60 / 10 * 24)
    report.initColumns("times")
    report.initSheets("times")
    report.getSheets()
    report.addData(sheet=report.__Sheets__[datetime.now().day - 1], data=[[str(datetime.now()),
                                                                           "00:05:01","00:05:01","00:05:01","00:05:01","00:05:01","00:05:01"]])


if __name__=="__main__":
    main()