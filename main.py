from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client['gerenciamento_db']
collection = db['registros']


def cadastrar_registro():
    id = input("\nDigite o ID: ")

    registro_existente = collection.find_one({"_id": id})

    if registro_existente:
        print(f"\nErro: O ID {id} já está cadastrado.\n")
        return

    nome = input("Digite o Nome: ")
    email = input("Digite o Email: ")
    telefone = input("Digite o Telefone: ")

    novo_registro = {
        "_id": id,
        "nome": nome,
        "email": email,
        "telefone": telefone
    }
    
    collection.insert_one(novo_registro)
    print(f"\nRegistro {nome} adicionado com sucesso!\n")


def listar_registros():
    num_registros = collection.count_documents({})
    
    if num_registros == 0:
        print("\nNenhum registro encontrado.\n")
    else:
        print(f"\nListando {num_registros} registro(s)...")
        for registro in collection.find():
            print(f"ID: {registro['_id']}, Nome: {registro['nome']}, Email: {registro['email']}, Telefone: {registro['telefone']}")
        print('')


def atualizar_registro():
    id = input("\nDigite o ID do registro que deseja atualizar: ")

    registro_existente = collection.find_one({"_id": id})

    if not registro_existente:
        print(f"\nErro: O ID {id} não existe.\n")
        return

    novo_nome = input("Digite o novo Nome (pressione Enter para manter o atual): ")
    novo_email = input("Digite o novo Email (pressione Enter para manter o atual): ")
    novo_telefone = input("Digite o novo Telefone (pressione Enter para manter o atual): ")

    filtro = {"_id": id}
    novos_valores = {"$set": {}}

    if novo_nome:
        novos_valores["$set"]["nome"] = novo_nome
    if novo_email:
        novos_valores["$set"]["email"] = novo_email
    if novo_telefone:
        novos_valores["$set"]["telefone"] = novo_telefone

    collection.update_one(filtro, novos_valores)
    print(f"\nRegistro {id} atualizado com sucesso!\n")


def excluir_registro():
    id = input("\nDigite o ID do registro que deseja excluir: ")

    registro_existente = collection.find_one({"_id": id})

    if not registro_existente:
        print(f"\nErro: O ID {id} não existe.\n")
        return

    resposta = input(f'\nTem certeja que deseja excluir o registro com ID {id}? Tecle 1 para SIM e 2 para NÃO ')

    while True:
        if resposta == '1':
            collection.delete_one({"_id": id})
            print(f"\nRegistro {id} excluído com sucesso!\n")
            break
        elif resposta == '2':
            print('Cancelado...')
            break
        else:
            print("Opção inválida...")
            break


def contar_registros():
    total = collection.count_documents({})
    print(f"\nTotal de registros: {total}\n")


def listar_por_dominio_email():
    pipeline = [
        {"$group": {"_id": {"$substr": ["$email", {"$indexOfBytes": ["$email", "@"]}, -1]}, "total": {"$sum": 1}}}
    ]
    resultados = collection.aggregate(pipeline)
    for resultado in resultados:
        print(f"\nDomínio: {resultado['_id']}, Total: {resultado['total']}\n")


def menu():
    while True:
        print("==== CRUD MongoDB ====")
        print("1. Cadastrar novo registro")
        print("2. Listar todos os registros")
        print("3. Atualizar um registro")
        print("4. Excluir um registro")
        print("5. Contar total de registros")
        print("6. Listar registros por domínio de email")
        print("7. Sair")

        opcao = input("\nEscolha uma opção (1-7): ")

        if opcao == '1':
            cadastrar_registro()
        elif opcao == '2':
            listar_registros()
        elif opcao == '3':
            atualizar_registro()
        elif opcao == '4':
            excluir_registro()
        elif opcao == '5':
            contar_registros()
        elif opcao == '6':
            listar_por_dominio_email()
        elif opcao == '7':
            print("\nSaindo do programa...\n")
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")


if __name__ == "__main__":
    menu()
