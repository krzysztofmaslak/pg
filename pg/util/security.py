__author__ = 'root'

class Security:
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ',',','.','!','?','\'','#','@','$','%','^','&','(',')','-','_','=','+',']','[','{','}','\\','|','/','"',':',';','<','>','`','~','1','2','3','4','5','6','7','8','9','0']
    key = [3,-6,2,-7,23435363, -3243543, 324]

    def encrypt(self, message):
        ciphertext = []
        pos = 0
        for c in message:
            i = self.alphabet.index(c)
            j = (i + self.key[pos]) % len(self.alphabet)
            ciphertext.append(self.alphabet[j])
            pos += 1
            if pos > len(self.key)-1: pos = 0
        return "".join(ciphertext)

    def decrypt(self, message):
        plaintext = []
        pos = 0
        for c in message:
            i = self.alphabet.index(c)
            j = (i - self.key[pos]) % len(self.alphabet)
            plaintext.append(self.alphabet[j])
            pos += 1
            if pos > len(self.key)-1: pos = 0
        return "".join(plaintext)