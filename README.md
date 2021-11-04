# python-app-template

## 背景
项目上线前，需要经过自测、专测等，所以app要适配多环境。一般是需要本地环境local、开发环境dev、测试环境release、生产环境prod
参照spring-boot，我们也增加了不同环境的配置文件。

## 说明
- 公共配置文件application.yml
- 环境的配置文件application-{profile}.yml
- 根据自己需要，可以增加更多的环境配置文件，也可以删掉不需要的环境配置文件
- 根据自己的需要，在不同的文件中设置你的配置项。
- 加载配置时，优先级高到低为: application-{profile}.yml > application.yml

## 注意
项目未像spring-boot一样，配置自动加载。如果在配置文件增加了配置项，请参考configparser.py文件，定义对应的class

