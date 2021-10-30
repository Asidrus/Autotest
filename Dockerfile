FROM continuumio/miniconda3
WORKDIR /home/tester/autotest/tests/
RUN mkdir ../autotest-results ../allure-results ../autotest-results/logs
COPY req.yml ./
RUN conda env create -f req.yml
COPY . .
RUN echo "source activate autotest" > ~/.bashrc
ENV PATH /opt/conda/envs/autotest/bin:$PATH


