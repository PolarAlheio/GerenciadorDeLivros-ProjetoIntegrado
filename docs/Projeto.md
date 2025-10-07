# 📚 Documentação do Projeto: Gerenciador de Catálogo de Livros

## 1. Descrição geral do projeto
Aplicação para gerenciamento de um catálogo de livros desenvolvida em Python.  
Permite importar, exportar e editar registros do catálogo.

---

## 2. Objetivos do projeto
- Gerenciar livros de forma organizada.
- Permitir importação/exportação em JSON e XML.
- Suporte à função "desfazer" com histórico de até 10 estados.
- Aplicar padrões de projeto na implementação.
- Organizar o código e documentação conforme boas práticas de engenharia de software.

---

## 3. Módulos do sistema
- **main.py**: ponto de entrada da aplicação.
- **models/**: contém as classes do sistema (Livro, Catálogo, etc.).
- **utils/**: funções auxiliares.
- **commands/**: implementação de comandos especiais (desfazer/refazer).

---

## 4. Descrição de cada módulo
### 4.1 main.py
- Inicializa o sistema.
- Carrega os dados do catálogo.
- Gerencia interação com o usuário.

### 4.2 models/
- **Livro**: representa um livro com título, autor, ISBN, editora e número de páginas.  
- **Catálogo**: gerencia a coleção de livros, adicionando, removendo ou editando registros.

### 4.3 utils/
- Funções de leitura/escrita de arquivos JSON e XML.  
- Funções auxiliares de validação de dados.

### 4.4 commands/
- Implementa a função de desfazer/refazer ações realizadas no catálogo.  
- Mantém histórico de até 10 estados anteriores.

---

## 5. Levantamento de requisitos
- Importação/exportação de catálogos (JSON e XML).  
- Cadastro, edição e exclusão de livros.  
- Função desfazer/refazer com histórico de 10 estados.  
- Interface de interação (terminal, web ou GUI).  
- Aplicação de ao menos 3 padrões de projeto diferentes.  

> Obs: os requisitos podem ser detalhados em tópicos ou tabela à medida que forem definidos.

---

## 6. Cronograma e backlog
- Planejamento inicial do projeto, dividido em tarefas.  
- Histórico de execução (backlog) mostrando prioridades, responsáveis e status.  
- Pode ser mantido em Markdown ou integrado a ferramentas como Trello/GitHub Projects.

---

## 7. Diagramas e arquitetura
- Diagrama de classes UML dos módulos principais.  
- Diagrama de fluxo ou sequência das operações críticas.  
- Esquema de organização do projeto (pastas e dependências).

---

## 8. Estratégia de testes
- Casos de teste unitários para classes Livro e Catálogo.  
- Testes de importação/exportação de arquivos JSON e XML.  
- Teste da função desfazer/refazer.  
- Registro de resultados e correções.

---

## 9. Controle de versão
- Toda alteração no código e documentação será registrada no GitHub.  
- Permite rastrear mudanças, colaborar entre integrantes e manter histórico confiável.

---

## 10. Referências
- Linguagem Python 3.x.  
- Material da disciplina de POO II e Projeto Integrado.  
- Documentação de padrões de projeto aplicados.
