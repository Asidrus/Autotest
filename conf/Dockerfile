ROM continuumio/miniconda3
WORKDIR /home/tester/autotest
RUN mkdir autotest-results allure-results autotest-results/logs
RUN git clone https://github.com/asidrus/tests tests/
COPY req.yml autotest.sh tests/
COPY config.py tests/
RUN conda env create -f tests/req.yml
CMD ["conda","activate","autotest"]