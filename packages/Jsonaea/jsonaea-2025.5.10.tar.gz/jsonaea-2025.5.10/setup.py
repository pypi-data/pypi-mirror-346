import setuptools #导入setuptools打包工具
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def processDate(date:int):
    date = str(date)
    year = "20" + date[:1]
    month = str(int(date[2:3]))
    day = str(int(date[4:5]))
    return "%s.%s.%s"%(year,month,day)

setuptools.setup(
    name="Jsonaea", # 用自己的名替换其中的YOUR_USERNAME_
    version="2025.5.10",    #包版本号，便于维护版本
    author="Begloon(321bug)",    #作者，可以写自己的姓名
    author_email="bugbugbug321@163.com",    #作者联系方式，可写自己的邮箱地址
    description="将Arcaea游戏中铺面文件（x.aff）转换为json文件，亦可将json文件转换回铺面文件的实用库",#包的简述
    long_description=long_description,    #包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://github.com/321bug/Jsonaea",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',    #对python的最低版本要求
)
