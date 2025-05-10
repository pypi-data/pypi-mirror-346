class Hesaplayici:
    def __init__(self):
        self.sonuc = 0

    def topla(self, a, b):
        self.sonuc = a + b
        return self.sonuc

    def carp(self, a, b):
        self.sonuc = a * b
        return self.sonuc

    def sifirla(self):
        self.sonuc = 0
