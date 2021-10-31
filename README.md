<p>auto deploy test 4</p>
<b>Git</b>
1. Получить обновления с master's ветки:<br>
<i>git pull</i></br>
<i>git checkout kote</i><br>
<i>git merge master</i><br>


2. Добавление нового кода<br>
<i>git add </i></br>
<i>git commit -m "kote"</i><br>
<i>git push origin kote</i><br>


3. Слияние с master's веткой<br>
<i>git checkout master</i><br>
<i>git pull</i></br>
<i>git merge kote</i><br>
<i>git push origin master</i><br>
<i>git chechout kote</i><br>
---
<b>Conda</b><br>
<ul>
<li>Создать файл окружения:<br>
<i>conda env export --name autotest > req.yml</i><br></li>
<li>Импортировать окружение из файла:<br>
<i>conda env create --file req.yml</i><br></li></ul>

---

run.sh - запуск теста в докере, например<br>
sudo docker run -it autotest bash /tests/run.sh pytest --param1 --param2 test_formSending.py

---
