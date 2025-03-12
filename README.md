## Projeto BonJournal
### Projeto de Princípios de Programação (UFRPE)

O BonJournal é um simples projeto que visa simular um diário / journal de livros lidos pelo usuário. Entre suas principais funcionalidades estão:

- **CRUD (Cadastro e Login):** O usuário realiza seu cadastro pelo programa, criando um arquivo onde é armazenado seu catálogo de livros;
  - Cadastro: É requisitado um email válido ao usuário e uma senha igualmente válida. A senha então passa por um hash para criar uma criptografia simples e então esses dados são armazenados num arquivo .txt; Ao mesmo tempo é criado um arquivo JSON que será utilizado para armazenar os futuros livros do usuário
  - Login: Após inserir as credenciais, o usuário recebe um código de Autenticação no seu e-mail inserido.
  - 2FA: No seu email, o usuário vai receber um código de autenticação necessário para logar em sua conta.
- **Catálogo de livros:** O usuário acrescenta em seu catálogo os seus livros como desejar. No catálogo é possível:
  - Acrescentar os livros propriamente ditos. Cada livro possui Título, Autor, Data de Publicação, Nota e uma Review opcional feita pelo usuário.
  - Listar os livros registrados: Mostra uma lista ordenada dos livros que foram acrescentados pelo usuário.
  - Remover livro: Caso queira, o usuário pode remover um livro acrescentado sempre que desejar.
