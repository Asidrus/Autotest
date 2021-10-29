FROM continuumio/miniconda3
WORKDIR /home/tester/autotest/tests/
COPY * /
RUN conda env create -f req.yml