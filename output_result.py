import os
import errno
import re


class WritingData:

    def __init__(self, arr):
        self.array = arr


    def wrDataInExcel(self):           
        # if not os.path.exists("conf/res.xlsx"):
        #     try:
        #         f = open("conf/res.xlsx", "w+")
        #         f.close()
        #     except OSError as exc: # Guard against race condition
        #         if exc.errno != errno.EEXIST:
        #             raise
        # else:
        #     writer = pd.ExcelWriter("conf/res.xlsx", engine='xlsxwriter')
        #     for item in self.array.keys():
        #         self.array[item].to_excel(writer, sheet_name=item, index=False)

        #     writer.save()
        f = open("conf/res.txt", "w+")
        for item in self.array:
            f.write(str(item) + '\n')

        f.close()
