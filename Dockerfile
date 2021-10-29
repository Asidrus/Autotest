FROM continuumio/miniconda3
WORKDIR /home/tester/autotest
COPY * /tests/
RUN conda env create -f tests/req.yml