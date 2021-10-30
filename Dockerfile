FROM continuumio/miniconda3
WORKDIR /home/tester/autotest/tests/
RUN mkdir ../autotest-results ../allure-results ../autotest-results/logs
COPY req.yml ./
RUN conda env create -f req.yml
COPY . .
ENV PATH /opt/conda/envs/mro_env/bin:$PATH
RUN /bin/bash -c "source activate autotest"

