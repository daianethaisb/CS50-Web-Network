## Projeto 4 - Network:

> Criação de um site de rede social semelhante ao Twitter para fazer postagens e seguir usuários implementado em um código de distribuição fornecido pelo curso.

As funcionalidades implementadas permitem aos usuários

* Nova postagem: os usuários que estiverem conectados deverão poder escrever uma nova postagem baseada em texto preenchendo o texto em uma área de texto e clicando em um botão para enviar a postagem;
* Todas as postagens: o link “Todas as postagens” na barra de navegação leva o usuário a uma página onde ele pode ver todas as postagens de todos os usuários, com as postagens mais recentes primeiro;
* Página de perfil: clicar em um nome de usuário carrega a página de perfil desse usuário;
* Seguindo: O link “Seguindo” na barra de navegação leva o usuário a uma página onde ele vê todas as postagens feitas por usuários que o usuário atual segue;
* Paginação: Em qualquer página que exiba postagens, as postagens são exibidas apenas 10 por página. Se houver mais de dez postagens, um botão “Avançar” aparece para levar o usuário à próxima página de postagens;
* Editar postagem : os usuários podem clicar no botão “Editar” ou no link em qualquer uma de suas próprias postagens para editá-la;
* “Curtir” e “Não Curtir” : os usuários podem clicar em um botão ou link em qualquer postagem para alternar entre “curtir” ou não aquela postagem.
  Usando JavaScript, a pagina informa de forma assíncrona ao servidor para atualizar a contagem de curtidas (como por meio de uma chamada para fetch) e, em seguida, atualiza a contagem de curtidas da postagem exibida na página, sem exigir o recarregamento da página inteira.


**Como executar o aplicativo**

- Execute as migrações com o comando python manage.py makemigrations.
- Aplique migrações com o comando python [manage.py](http://manage.py/) migrate.
- Execute o servidor usando python [manage.py](http://manage.py/) runserver.
