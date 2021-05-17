import pyttsx3


if __name__ == '__main__':
    engine = pyttsx3.init()
    engine.say("你好你好你好")
    engine.runAndWait()