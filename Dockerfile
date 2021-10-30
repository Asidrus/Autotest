FROM continuumio/miniconda3
WORKDIR /home/tester/autotest/tests/
RUN mkdir ../autotest-results ../allure-results ../autotest-results/logs
COPY req.yml ./
RUN conda env create -f req.yml
COPY . .
CMD source /opt/conda/etc/profile.d/conda.sh
CMD conda activate autotest
