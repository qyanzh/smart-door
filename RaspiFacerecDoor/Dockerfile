FROM zqzopencv
MAINTAINER ZhuQingzhang031702426
RUN mkdir /myapp
RUN pip3 install smbus -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install luma.oled -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /myapp
COPY myapp .