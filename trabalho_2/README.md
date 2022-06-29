# Implementação SMA
- Esse é um projeto que visou a implementação de um sistema multiagentes através da utilização da plataforma de desenvolvimento SPADE.

## Pré-requisitos:
- ter python instalado
- ter SPADE instalado
- para mais informações acerca da instalação do SPADE, visitar o site
```
https://spade-mas.readthedocs.io/en/latest/installation.html
```

## Guia de Uso:
1. Para rodar o código, é necessário primeiramente entrar no diretório ```trabalho_2```. 
2. No código existem 2 agentes, o Gerador e o Resolvedor, sua implementação foi dividida em 2 arquivos, o ```gerador.py``` e o ```resolvedor.py```. Eles podem ser rodas separadamente.
3. Para rodar o código do Gerador, foi utilizado o comando
```
python3 gerador.py
```
4. Para rodar o código do Resolvedor, foi utilizado o comando:
```
python3 resolvedor_teste.py
```

## Considerações:
1. O agente Gerador deve ser rodado primeiro para que ele possa estar pronto para responder as menagens enviadas pelo Resolvedor
2. Foram criados 2 contas no jix, uma para o Gerador e outra para o Resolvedor, caso seja necessário trocá-las, é possível fazer isso no final do código. Mais especificamente na inicialização do gerador no arquivo gerador.py, e nas variáveis resolvedor_jid, resolvedor_password, gerador_jid e gerador_password no arquivo resolvedor.py.
3. Caso a conta jix do Gerador seja trocada, lembrar de atulizar o novo endereço no código do Resolvedor.
	
## Autoria:
- Maria Luiza Fontes Dantas 
- André Luis Correa Barbado