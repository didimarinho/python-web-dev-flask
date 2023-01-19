
from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskdb.sqlite3"
db.init_app(app)


frutas = []
registros = []


class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    carga_h = db.Column(db.Integer)
    

    
    def __init__(self, nome, descricao, carga_h):
        self.nome = nome
        self.descricao = descricao
        self.carga_h = carga_h



@app.route("/", methods=['GET', 'POST'])
def principal():

    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))
    return render_template('index.html', frutas=frutas)



@app.route('/sobre', methods=['GET', 'POST'])
def sobre():

    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({
                'aluno': request.form.get('aluno'),
                'nota': request.form.get('nota')
            })

    return render_template('sobre.html', registros=registros)




@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=7443b22948eb056c0a215d29299aaeb0"
        
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=7443b22948eb056c0a215d29299aaeb0"
        
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=7443b22948eb056c0a215d29299aaeb0"
        
    elif propriedade == 'drama':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&primary_release_year=2014&api_key=7443b22948eb056c0a215d29299aaeb0"
        
    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=7443b22948eb056c0a215d29299aaeb0"
        
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    return render_template('filmes.html', filmes = jsondata['results'])


@app.route('/cursos')
def lista_cursos():
    return render_template('cursos.html', cursos = cursos.query.all())


#! Postagem do campos da tabela no db
@app.route('/cria_curso', methods = ['GET', 'POST'])
def cria_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    carga_h = request.form.get('ch')
    
    if request.method == 'POST':
        
        #? vai criar um objeto do tipo curso da classe cursos
        curso = cursos(nome, descricao, carga_h)
        
        #? vai adicionar o objeto no banco de dados
        db.session.add(curso)
        
        #? vai salvar o objeto no banco de dados
        db.session.commit()
        
        #? vai redirecionar para a pagina de cursos atribuidos no db
        return redirect(url_for('lista_cursos'))
        

    return render_template('novo_curso.html')




#!###################################################
@app.route('/teste')
def teste():
    return render_template('teste.html')
#!###################################################


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='localhost', port=5000)
