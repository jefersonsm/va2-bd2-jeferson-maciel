#coding: utf-8

from appJar import gui
import MySQLdb


def conectar(btn):
	global cursor
	global conexao

	ip= co.getEntry('txtip')
	usuario= co.getEntry('txtusuario')
	senha= co.getEntry('txtsenha')

	if (ip=='' or usuario=='' or senha==''):
		co.errorBox("Erro", 'Erro na conexão')
		co.stop()
		

	conexao = MySQLdb.connect(ip,usuario,senha,"mundo")
	cursor = conexao.cursor()

	co.stop()



co=gui("Conexão com Banco","300x200")

co.addEntry("txtip",0,0,2)
co.addEntry("txtusuario",1,0,2)
co.addLabel("l5", "Senha do Usuario",2,0,2)
co.addSecretEntry("txtsenha",3,0,2)
co.setEntryDefault("txtip", "Ip do Servidor")
co.setEntryDefault("txtusuario", "Usuario do Banco")
co.setEntryDefault("txtsenha")
co.addButton("Conectar-se", conectar,4,0,2)

co.go()


app=gui("CRUD de MySQL","600x300")

x=""

def usando(btn):
	#app.infoBox("Mensagem de aviso!", "Você me usou. Vou-lhe usar!")
	pass

def perquisar(btn):
	#x = app.textBox("Exibir", "Digite seu nome", parent=None)
	#app.infoBox("Resultado:", "Seu nome é:" + x)
	termo=app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		app.clearListBox("lBusca")
		cursor.execute("SELECT Cidade.nomeCidade, Estado.nomeEstado FROM Cidade INNER JOIN Estado ON Estado.idEstado = Cidade.Estado_idEstado WHERE Cidade.nomeCidade LIKE '%"+termo+"%'")
		rs=cursor.fetchall()

		for x in rs:
			app.addListItem("lBusca", x[0] + ' - ' + x[1])


def inserir(btn): #função que chamada pelo botão inserir e responsavel for exibir a subJanela
	app.showSubWindow('janela_inserir')

def salvar_estado(btn):#salva uma nova cidade em um estado
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('{}',{})".format(cidade,idestado))
	#cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
	conexao.commit()
	app.hideSubWindow('janela_inserir')


def excluir(btn):
	app.showSubWindow('janela_excluir')


def excluir_cidade(btn):
	retorno=""
	cidade = app.getEntry('txtcidade')
	retorno=app.yesNoBox('confirmarDelete', "Deseja excluir a cidade: "+ cidade, parent='janela_excluir')
	if(retorno==True):
		cursor.execute("DELETE FROM Cidade WHERE nomeCidade = '"+ cidade +"'")
		conexao.commit()
	else:
		app.infoBox("infoExcluir", "Cidade não excluida", parent='janela_excluir')
	
	app.hideSubWindow('janela_excluir')

def atualizar(btn):
	app.showSubWindow('janela_atualizar')

def atualizar_cidade(btn):
	cidade = app.getEntry('txtcidade2')
	idCidade1 = app.getEntry('txtidcidade1')
	cursor.execute(" UPDATE Cidade SET nomeCidade = '" + cidade + "'WHERE Cidade.idCidade = '"+ idCidade1 +"'")
	conexao.commit()
	app.clearEntry("txtcidade2", callFunction=True)
	app.clearEntry('txtidcidade1', callFunction=True)
	app.hideSubWindow('janela_atualizar')

def exibir(btn):
	app.showSubWindow('janela_allCidades')

	cursor.execute("SELECT Cidade.nomeCidade, Estado.nomeEstado FROM Cidade INNER JOIN Estado ON Estado.idEstado = Cidade.Estado_idEstado")
	listaCidades=cursor.fetchall()

	for x in listaCidades:
		app.addListItem("allCidades",  x[0] + ' - ' + x[1])


app.startSubWindow("janela_allCidades", modal=True)
app.addLabel("l4", "Todas as Cidade")
app.addListBox("allCidades",[])
app.stopSubWindow()



app.startSubWindow("janela_atualizar", modal=True)
app.addLabel("l3", "Atualizar Cidade")
app.addEntry('txtidcidade1')
app.addEntry('txtcidade2')
app.addButton('Atualizar cidade',atualizar_cidade)
app.setEntryDefault("txtidcidade1", "ID da Cidade")
app.setEntryDefault("txtcidade2", "Nome da cidade")
app.stopSubWindow()
	

app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton('Salvar cidade',salvar_estado)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()


# this is a pop-up
app.startSubWindow("janela_excluir", modal=True)
app.addLabel("l2", "Excluir Cidade")
app.addEntry('txtcidade1')
app.addButton('Excluir Cidade',excluir_cidade)
app.setEntryDefault("txtcidade1", "Nome da cidade")
app.stopSubWindow()


app.addLabel("lNome",'',0,0,2)
app.addButton("Exibir dados",exibir,1,0)
app.addButton("Inserir dado",inserir,1,1)
app.addButton("Atualizar dado",atualizar,2,0)
app.addButton("Excluir dado",excluir,2,1)
app.addEntry("txtBusca",3,0,2)
app.setEntryDefault("txtBusca", "Digite o termo...")
app.addButton("pesquisar", perquisar,4,0,2)
app.addListBox("lBusca",[],5,0,2)
app.setListBoxRows("lBusca",5)


app.go()