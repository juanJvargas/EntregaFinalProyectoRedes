from flask import Flask, abort, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
data = SQLAlchemy(app)


class descargaspendientes(data.Model):
    _tablename_ = 'descargaspendientes'
    id = data.Column(data.String(10), primary_key=True)
    nombre = data.Column(data.String(500))
    magnetlink = data.Column(data.String(500))
    estado = data.Column(data.String(50))
    progreso = data.Column(data.String(50))

    def __init__(self, id, nombre, magnetlink, estado, progreso):
        self.id = id
        self.nombre = nombre
        self.magnetlink = magnetlink
        self.estado = estado
        self.progreso = progreso


class memoria(data.Model):
    _tablename_ = 'memoria'
    memoria_virtual = data.Column(data.String(50))
    memoria_inactiva = data.Column(data.String(50))
    buffer = data.Column(data.String(50))
    cache = data.Column(data.String(50))
    ide = data.Column(data.Integer, primary_key=True)

    def __init__(self, ide, memoria_virtual, memoria_inactiva, buffer, cache):
        self.memoria_virtual = memoria_virtual
        self.memoria_inactiva = memoria_inactiva
        self.buffer = buffer
        self.cache = cache
        self.ide = ide


from app import app, data

with app.app_context():
    data.create_all()


@app.route('/descargar', methods = ['GET', 'POST'])
def descargar():
    if request.method == 'POST':
        url= request.form['magnet_url']
        all_reg = descargaspendientes.query.all()
        size = len(all_reg)
        registro = descargaspendientes(size + 1, "none", url, "pendiente", "0")
        data.session.add(registro)
        data.session.commit()
        return render_template("lista.html")
    else:
        return render_template("magnet.html")


@app.route('/actualizar/<magnets>')
def actualizar(magnets):
    all_reg = magnets.split(",")
    if len(all_reg) == 3:
        if all_reg[2] != 100:
            name = all_reg[0]
            name = name.replace("=", " ")
            reg = descargaspendientes.query.filter_by(nombre=name).first_or_404()
            reg.progreso = all_reg[2]
            reg.estado = "en progreso"
            data.session.commit()
        else:
            name = all_reg[0]
            name = name.replace("=", " ")
            reg = descargaspendientes.query.filter_by(nombre=name).first_or_404()
            reg.progreso = all_reg[2]
            reg.estado = "completa"
            data.session.commit()
        return """se modifico la base de datos"""
    else:
        magnet = all_reg[0]
        magnet = magnet.replace("$", "?")
        magnet = magnet.replace("^", ".")
        magnet = magnet.replace("|", "%")
        reg = descargaspendientes.query.filter_by(magnetlink=magnet).first_or_404()
        name = all_reg[1]
        reg.nombre = name
        data.session.commit()
        return """se modifico la base de datos"""


@app.route('/pendiente')
def pendiente():
    all_reg = descargaspendientes.query.all()
    size = len(all_reg)
    aux = 0
    ms1 = ""
    while aux != size:
        reg = descargaspendientes.query.filter_by(id=aux + 1).first_or_404()
        if reg.estado == "pendiente":
            ms1 = ms1 + """{magnet},""".format(magnet=reg.magnetlink)
        aux = aux + 1
    return ms1


@app.route('/memoria/<datos>')
def estadom(datos):
	all_reg = memoria.query.all()
	size = len(all_reg)
	info = datos.split(",")
	registro = memoria(size+1, info[0], info[1], info[2], info[3])
	data.session.add(registro)
	data.session.commit()
	return """se añadio con exito"""




@app.route('/eliminar')
def eliminar():
    all_reg = descargaspendientes.query.all()
    size = len(all_reg)
    aux = 0
    m = ""
    while aux != size:
        descargaspendientes.query.filter_by(id=aux + 1).delete()
        data.session.commit()
        aux = aux + 1
    return """<h1>echo</h1>"""

@app.route('/registros/')
def registros():
	all_reg = memoria.query.all()
	size = len(all_reg)
	aux = 0
	ms2 = ""
	while aux != size:
		reg = memoria.query.filter_by(ide=aux + 1).first_or_404()
		ms2 = ms2 + """<p>{id}: Virtual:{virtual}, inactiva:{inact}, buffer:{buf}, cahe:{cahe}</p>""".format(
		id=reg.ide,virtual=reg.memoria_virtual, inact=reg.memoria_inactiva, buf=reg.buffer, cahe=reg.cache)
		aux = aux + 1
	return """
		<p>Estado de memoria actual:</p>
		<p>""" + ms2 + """</p>
		"""


@app.route('/')
def homepage():
    all_reg = descargaspendientes.query.all()
    size = len(all_reg)
    aux = 0
    ms1 = ""
    while aux != size:
        reg = descargaspendientes.query.filter_by(id=aux + 1).first_or_404()
        ms1 = ms1 + """<p>{ide}, {magnet}, {status}, {progres}%</p>""".format(ide=reg.id, magnet=reg.magnetlink,
                                                                              status=reg.estado, progres=reg.progreso)
        aux = aux + 1

    all_reg = memoria.query.all()
   
    all_reg = descargaspendientes.query.all()
    size = len(all_reg)

    return """
    		<h1>Proyecto fundamentos de redes</h1>
		<p>Juan David torres cañon 1526750</p>
		<p>Juan Jose Vargas Vargas 1523382</p>
		<p>La base de datos cuenta con {tamano} registros</p>
		<p>""".format(tamano=size) + ms1 + """</p>
		<img src="https://i0.wp.com/occidente.co/wp-content/uploads/2015/11/univalle-nov-201.jpg?fit=600%2C338">"""


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
