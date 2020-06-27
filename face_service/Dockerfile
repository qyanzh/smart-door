FROM aaftio/face_recognition

VOLUME [ "code" ]

WORKDIR /code

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install flask 

ENTRYPOINT [ "python" ]

CMD [ "service.py" ]