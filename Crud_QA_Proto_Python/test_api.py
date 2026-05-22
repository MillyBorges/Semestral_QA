import requests
import time
import subprocess
import os

def test_api():
    # Inicia o servidor em background
    server_process = subprocess.Popen(["python3", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Espera o servidor iniciar

    base_url = "http://127.0.0.1:8000"
    
    try:
        # 1. Criar usuário
        print("Testando CREATE...")
        payload = {"nome": "João Silva", "email": "joao@example.com"}
        response = requests.post(f"{base_url}/usuarios/", json=payload)
        assert response.status_code == 201
        user_id = response.json()["id"]
        print(f"✅ Criado com ID: {user_id}")

        # 2. Listar usuários
        print("Testando READ (List)...")
        response = requests.get(f"{base_url}/usuarios/")
        assert response.status_code == 200
        assert len(response.json()) >= 1
        print(f"✅ Lista recebida com {len(response.json())} usuários")

        # 3. Ler usuário específico
        print("Testando READ (Single)...")
        response = requests.get(f"{base_url}/usuarios/{user_id}")
        assert response.status_code == 200
        assert response.json()["nome"] == "João Silva"
        print(f"✅ Usuário {user_id} lido corretamente")

        # 4. Atualizar usuário
        print("Testando UPDATE...")
        update_payload = {"nome": "João Santos", "email": "joao.santos@example.com"}
        response = requests.put(f"{base_url}/usuarios/{user_id}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["nome"] == "João Santos"
        print("✅ Usuário atualizado")

        # 5. Deletar usuário
        print("Testando DELETE...")
        response = requests.delete(f"{base_url}/usuarios/{user_id}")
        assert response.status_code == 204
        print("✅ Usuário deletado")

        # Verificar se foi deletado
        response = requests.get(f"{base_url}/usuarios/{user_id}")
        assert response.status_code == 404
        print("✅ Confirmação de deleção (404)")

        print("\n🚀 Todos os testes passaram com sucesso!")

    finally:
        server_process.terminate()
        stdout, stderr = server_process.communicate()
        if stderr:
            print(f"Server Error Log:\n{stderr.decode()}")
        if stdout:
            print(f"Server Output Log:\n{stdout.decode()}")

if __name__ == "__main__":
    test_api()
