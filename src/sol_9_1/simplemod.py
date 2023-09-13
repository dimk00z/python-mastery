x = 43


def foo():
    print("x is", x)


def _foo():
    foo()


class Spam:
    def yow(self):
        print("yow")


print("Loaded simplemod")
