from pygtrans import Translate


if __name__ == "__main__":
    client = Translate()
    client.detect('谷歌翻译').language
    'zh-CN'
    # 单个
    text = client.translate('Hello, Google,jack', target='af')
    print(text.translatedText)