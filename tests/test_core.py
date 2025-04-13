import unittest
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

class TestSenha(unittest.TestCase):  
    def test_hash_senha(self):  
        senha = "123456"
        resultado = hash_senha(senha)
        self.assertEqual(len(resultado), 64)  
        self.assertTrue(resultado.isalnum())  

if __name__ == "__main__":
    unittest.main()  
