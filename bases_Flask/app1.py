from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def index():
    titulo="PWA"
    lista=["pedro","luis","pablo"]
    return render_template("index.html",titulo=titulo,lista=lista)

@app.route("/hola")
def func():
    return "Hola ..."

@app.route("/user/<string:user>")
def user(user):
    return "Hola"+ user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1,n2):
    return "La suma es: {}".format(n1+n2)

@app.route("/operasBas", methods=["GET", "POST"])
def operasBas():
    n1 = 0
    n2 = 0
    res = 0
    operacion = ''

    if request.method == 'POST':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')

        if request.form.get('operacion') == 'sumar':
            res = float(n1) + float(n2)
            operacion = '+'

        elif request.form.get('operacion') == 'restar':
            res = float(n1) - float(n2)
            operacion = '-'

        elif request.form.get('operacion') == 'multiplicar':
            res = float(n1) * float(n2)
            operacion = '*'

    return render_template("operasBas.html",
                           n1=n1,
                           n2=n2,
                           res=res,
                           operacion=operacion)


@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    a1 = 0
    a2 = 0
    b1 = 0
    b2 = 0
    total = 0

    if request.method == "POST":
        a1 = float(request.form.get("a1"))
        a2 = float(request.form.get("a2"))
        b1 = float(request.form.get("b1"))
        b2 = float(request.form.get("b2"))

        total = ((b1 - a1)**2 + (b2 - a2)**2)**0.5

    return render_template("distancia.html",
                           a1=a1, a2=a2,
                           b1=b1, b2=b2,
                           total=total)

if __name__=="__main__":
    app.run(debug=True)




