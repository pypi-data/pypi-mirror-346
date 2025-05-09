import password_check

def main():
    password = input("Digite a senha: ")
    response = password_check.is_strong(password)
    print("Senha " + f"{'Forte' if response else 'Fraca'}")