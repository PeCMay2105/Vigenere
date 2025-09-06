from attack import VigenereAttack
from vigenere import Vigenere

def main():
    algorithm = Vigenere()
    attackEN = VigenereAttack(False)
    attackPT = VigenereAttack(True)

    while True:
        print("### Sistema Muito Bom de Vigenere Cipher --  SMBVC ###")
        print("1. Encriptar")
        print("2. Decriptar")
        print("3. Simular Ataque")
        print("4. Sair")
        choice = input("Escolha uma opção: ")

        if choice == "1":
            msg = input("Insira a mensagem: ")
            key = input("Qual a chave ?: ")
            print("Encrypted message:", algorithm.encrypt(msg, key))

        elif choice == "2":
            msg = input("Insira a mensagem encriptada: ")
            key = input("insira a chave: ")
            print("Decrypted message:", algorithm.decrypt(msg, key))

        elif choice == "3":
            msg = input("Insira a mensagem encriptada: ")
            lang = input("Idioma: \n 1 - Ingles \n 2 - Portugues: ")
            if lang == "2":
                print("Attack result:\n", attackPT.attack(msg))
            else:
                print("Attack result:\n", attackEN.attack(msg))

        elif choice == "4":
            break

        else:
            print("Escolha uma das opções oferecidas.")

if __name__ == "__main__":
    main()
