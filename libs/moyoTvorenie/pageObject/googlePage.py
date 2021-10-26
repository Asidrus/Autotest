from baseApp import WorkWithDriver

# Класс для взаимодецйствия со страницей
class AbraCadabra(WorkWithDriver):

    def write_text(self, text):
        input = self.find_element('//input[@class="gLFyf gsfi"]')
        input.send_keys(text)
        return input

    def click_button(self):
        return self.find_element('//input[@class="RNmpXc"]').click()

    

       