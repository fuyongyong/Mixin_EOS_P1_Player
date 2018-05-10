# 此处是基于Python的MiXin机器人🤖程序。

requirement.txt 是 基于Flask 的 MiXin 机器人的安装环境。

通过 sudo pip3 install -r requirement 进行安装。

如果安装时提示 ' error: command 'x86_64-linux-gnu-gcc' failed with exit status 1 '错误，输入以下命令即可：

sudo apt-get install python3 python-dev python3-dev \
     build-essential libssl-dev libffi-dev \
     libxml2-dev libxslt1-dev zlib1g-dev \
     python-pip
