from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'

def conectar_db():
    conectar = sqlite3.connect('database.db')
    conectar.row_factory = sqlite3.Row
    return conectar

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['senha']

    with conectar_db() as conn:
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()

    if user:
        flash('Login bem-sucedido!')
        cargo = user['cargo']

        if cargo == 1:
            return redirect(url_for('inicioGerente'))
        elif cargo == 2:
            return redirect(url_for('inicioAtend'))
        else:
            flash('Cargo inválido. Redirecionando para a página inicial.')
            return redirect(url_for('login'))
    else:        
        flash('Email ou senha incorretos.')
        return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['senha']
        cargo = request.form['cargo']

        with conectar_db() as conn:
            try:
                conn.execute('INSERT INTO users (email, password, cargo) VALUES (?, ?, ?)', (email, password, cargo))
                conn.commit()
                flash('Usuário cadastrado com sucesso!')
                
                if cargo == '1':
                    return redirect(url_for('inicioGerente'))
                elif cargo == '2':
                    return redirect(url_for('inicioAtend'))
                else:
                    flash('Cargo Inválido. Selecione 1 ou 2.')
                    return redirect(url_for('login'))
                    
            except sqlite3.IntegrityError:
                flash('Erro: O email já está em uso.')

    return render_template('cadastro.html')

@app.route('/inicioAtend')
def inicioAtend():
    with conectar_db() as conn:
        # Busca atendimentos
        atendimentos = conn.execute('SELECT * FROM Atendimentos').fetchall()
        
        # Busca produtos
        produtos = conn.execute('SELECT * FROM Produtos').fetchall()
        
        # Busca histórico de atendimentos
        historicos = conn.execute('SELECT * FROM Historico_Atendimentos').fetchall()
    
    return render_template('inicioAtend.html', atendimentos=atendimentos, produtos=produtos, historicos=historicos)

@app.route('/inicioGerente')
def inicioGerente():
    with conectar_db() as conn:
        # Busca vendas
        vendas = conn.execute('SELECT * FROM Vendas').fetchall()
        
        # Busca fornecedores
        fornecedores = conn.execute('SELECT * FROM Fornecedores').fetchall()
        
        # Busca avaliações
        avaliacoes = conn.execute('SELECT * FROM Avaliacoes').fetchall()

    return render_template('inicioGerente.html', vendas=vendas, fornecedores=fornecedores, avaliacoes=avaliacoes)

@app.route('/cadastrar_atendimento', methods=['POST'])
def cadastrar_atendimento():
    cliente_id = request.form['cliente_id']
    descricao = request.form['descricao']
    status = request.form['status']

    with conectar_db() as conn:
        try:
            conn.execute(
                'INSERT INTO Atendimentos (cliente_id, descricao, status) VALUES (?, ?, ?)', 
                (cliente_id, descricao, status)
            )
            conn.commit()
            flash('Atendimento cadastrado com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar atendimento: {e}")
            flash('Erro ao cadastrar atendimento.')

    return redirect(url_for('inicioAtend'))

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    preco = request.form['preco']
    estoque = request.form['estoque']

    with conectar_db() as conn:
        try:
            conn.execute(
                'INSERT INTO Produtos (nome, descricao, preco, estoque) VALUES (?, ?, ?, ?)', 
                (nome, descricao, preco, estoque)
            )
            conn.commit()
            flash('Produto cadastrado com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar produto: {e}")
            flash('Erro ao cadastrar produto.')

    return redirect(url_for('inicioAtend'))

@app.route('/cadastrar_historico', methods=['POST'])
def cadastrar_historico():
    atendimento_id = request.form['atendimento_id']
    observacoes = request.form['observacoes']

    with conectar_db() as conn:
        try:
            conn.execute(
                'INSERT INTO Historico_Atendimentos (atendimento_id, observacoes) VALUES (?, ?)', 
                (atendimento_id, observacoes)
            )
            conn.commit()
            flash('Histórico de atendimento cadastrado com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar histórico: {e}")
            flash('Erro ao cadastrar histórico.')

    return redirect(url_for('inicioAtend'))

@app.route('/vendas', methods=['POST'])
def cadastrar_venda():
    cliente_id = request.form['cliente_id']
    produto_id = request.form['produto_id']
    quantidade = request.form['quantidade']
    valor_total = request.form['valor_total']

    with conectar_db() as conn:
        try:
            conn.execute(
                'INSERT INTO Vendas (cliente_id, produto_id, quantidade, valor_total) VALUES (?, ?, ?, ?)', 
                (cliente_id, produto_id, quantidade, valor_total)
            )
            conn.commit()
            flash('Venda cadastrada com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar venda: {e}")
            flash('Erro ao cadastrar venda.')

    return redirect(url_for('inicioGerente'))

@app.route('/fornecedores', methods=['POST'])
def cadastrar_fornecedor():
    nome = request.form['nome']
    contato = request.form['contato']
    email = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']

    with conectar_db() as conn:
        try:
            conn.execute(
                'INSERT INTO Fornecedores (nome, contato, email, telefone, endereco) VALUES (?, ?, ?, ?, ?)', 
                (nome, contato, email, telefone, endereco)
            )
            conn.commit()
            flash('Fornecedor cadastrado com sucesso!')
        except Exception as e:
            print(f"Ocorreu um erro ao cadastrar fornecedor: {e}")
            flash('Erro ao cadastrar fornecedor.')

    return redirect(url_for('inicioGerente'))

@app.route('/avaliacoes', methods=['POST'])
def cadastrar_avaliacao():
   produto_id = request.form['produto_id']
   cliente_id = request.form['cliente_id']
   avaliacao = request.form['avaliacao']
   comentario = request.form['comentario']

   with conectar_db() as conn:
       try:
           conn.execute(
               'INSERT INTO Avaliacoes (produto_id, cliente_id, avaliacao, comentario) VALUES (?, ?, ?, ?)', 
               (produto_id, cliente_id, avaliacao, comentario)
           )
           conn.commit()
           flash('Avaliação cadastrada com sucesso!')
       except Exception as e:
           print(f"Ocorreu um erro ao cadastrar avaliação: {e}")
           flash('Erro ao cadastrar avaliação.')

   return redirect(url_for('inicioGerente'))

if __name__ == '__main__':
   app.run(debug=True)