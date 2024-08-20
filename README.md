# Sistema de Agendamento e Reserva de Salas
![002 (1)](https://github.com/user-attachments/assets/013238f6-5049-43a0-81a9-4f028f9be239)
<br>
O projeto RoomReservation é um sistema web de agendamento e reserva de salas para várias escolas integradas, incluindo o SESI para ensino regular e o SENAI para cursos técnicos, aperfeiçoamento, qualificação, e iniciação profissional. O sistema é desenvolvido de forma colaborativa e é open-source, buscando melhorar a eficiência no uso de recursos educacionais.

## Funcionalidades

- **Cadastro de Usuários**: Integração com sistemas de autenticação para professores e administradores.
- **Cadastro de Salas**: Integração com sistemas de autenticação para professores e administradores.
- **Agendamento de Salas**: Ferramenta fácil de usar para reserva de salas com base em disponibilidade.
- **Integração SESI/SENAI**: Diferenciação entre as reservas e agendamentos para ensino regular (SESI) e cursos técnicos/profissionalizantes (SENAI).
- **Notificações**: Alertas via e-mail ou SMS para lembrar sobre reservas e agendamentos.
- **Relatórios**: Geração de relatórios sobre o uso das salas, agendamentos futuros, e histórico de reservas.

## Tecnologias Utilizadas

- **Backend**: [Django]
- **Frontend**: [Jquery, Javascript]
- **Banco de Dados**: [MySQL]
- **Autenticação**: [ DjangoAuth]
- **Integração de Notificações**: [ EmailSend]

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/SenaiMG/RoomReservation.git
   ```

2. Navegue até o diretório do projeto:
  ```bash
   cd RoomReservation
   ```
3. Crie a Venv Instale as dependências:
```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:

Crie um arquivo .env baseado no .env.example e preencha com as configurações necessárias.

5. Inicie o servidor:

```bash
cd sistema
python manage.py runserver 
```


6. Acesse o sistema no navegador:

```bash
    http://localhost:8000
```

## Como Contribuir
Contribuições são bem-vindas! Siga as etapas abaixo para colaborar com o projeto:

1. Fork o repositório.

2. Crie uma branch para a sua feature ou correção de bug:

```bash
git branch minha-feature
git switch minha-feature
```

3. Faça commit das suas alterações:

```bash
git commit -m "{feature}: Descrição da minha feature"
```

4. Envie as suas alterações para o seu fork:

```bash
git push origin minha-feature
```

5. Abra um Pull Request no repositório original.

## Regras para Contribuição

- Código Limpo: Siga as melhores práticas de código limpo e utilize uma estrutura de commits clara e descritiva.
- Testes: Sempre que possível, inclua testes automatizados para novas funcionalidades ou correções de bugs.
- Documentação: Atualize a documentação conforme necessário para que ela reflita as mudanças que você está fazendo.
- Discussões: Utilize o espaço de Issues para discutir grandes mudanças antes de iniciar o desenvolvimento.

## Convenção de Commits

**'feat'**: Uma nova feature.<br>
**'fix'**: Correção de bug.<br>
**'docs'**: Alterações na documentação.<br>
**'style'**: Formatação, sem alterações no código.<br>
**'refactor'**: Refatoração do código.<br>
**'test'**: Adição ou correção de testes.<br>

## Licença
Este projeto é licenciado sob a [Licença](LICENSE).

## Contato

Para mais informações ou dúvidas, entre em contato através do e-mail: trabalho.computador.sjn@gmail.com.



## Equipe
Um agradecimento a todos que desenvolveram e ajudaram esse projeto de alguma forma.
<br><br>
![IMG_1110](https://github.com/user-attachments/assets/deb65cff-28a7-4a96-9952-98c858a0f69c)















## Regras para o desenvolvimento 
Atualize sempre a branch develop nunca a main 
sempre que for mexer no projeto inicie a venv e se precisar instalar alguma lib depois de instalada atualize o requeriments.txt
com o comando: 

```bash
 pip freeze > requeriments.txt
```

## Gerar Chave Django

```bash
python3 -c "from django.core.management.utils import 
get_random_secret_key; print(get_random_secret_key())"
```

## Usuários de testes
Os dados são referentes ao arquivo user.json dapasta fixtures

- Nome: Usuario Docente
- Senha: Senai@1234
- Tipo: Professor
- Email: docentesenai@gmail.com
---
- Nome: Usuario Gestor
- Senha: Senai@1234
- Tipo: Gestor
- Email: gestorsenai@gmail.com

## Realização de testes do sistema
Exemplo se quiser executar apenas um teste
```bash
python .\manage.py test reservations.tests.test_repository
```