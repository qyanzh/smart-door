FROM python

VOLUME [ "code" ]

WORKDIR /code

COPY ./requirements.txt ./

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "service.py" ]