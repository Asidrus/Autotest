from pageObject.googlePage import AbraCadabra

class test_google_and_pom(setup_driver):
    page = AbraCadabra(setup_driver)
    page.starDriver('https://www.google.ru/?hl=ru')  
    page.write_text('Антон. Оно работает')
    page.sleep(4)
    page.click_button
    assert "Вроде норм"
