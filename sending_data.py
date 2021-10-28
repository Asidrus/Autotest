from controller import Controller
from output_result import WritingData


class FillingInFieldsWithData:

    def __init__(self, input, btn, driver, text_err):
        self.input = input
        self.btn = btn
        self.err_text_input_name = ''
        self.cntrl = Controller()
        self.driver = driver
        self.text_err = text_err


    def hasItPassedValidation(self):
            try:
                error = self.driver.find_element_by_xpath(self.text_err)
                if "русскими" in error.text:
                    return False                      #не прошло валидацию
                else:
                    return True                      #прошло валидацию

                # self.err_text_input_name = driver.find_element_by_xpath("//div[@class='form_errors']/div[2]/text()")
                # pattern = ["русск", "имя"]
                # flag = any([(pat in text) for pat in pattern])

                # print(flag)
                # print(dt[0])

            except Exception as e:
                print(str(e))
                self.driver.close()
                self.driver.quit()
 

    def get_data(self):
        arr = []
        for dt in self.cntrl.gendata():
            self.input.clear()
            self.input.send_keys(dt[0])
            self.btn.click()
            result = self.hasItPassedValidation()
            if dt[1]^result:
                arr.append({"data": dt[0], "valid": dt[1], "result": result})
        # self.wrData = WritingData(arr)
        # self.wrData.wrDataInExcel()
        return arr
