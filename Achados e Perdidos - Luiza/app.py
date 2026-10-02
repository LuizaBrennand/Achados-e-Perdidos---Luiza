from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED = {"png", "jpg", "jpeg", "gif", "webp"}
DB = os.path.join(app.root_path, "achados.db")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def db():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL,
          name TEXT NOT NULL, description TEXT NOT NULL, place TEXT NOT NULL,
          contact TEXT NOT NULL, image TEXT, resolved INTEGER DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

@app.route("/")
def index():
    kind=request.args.get("tipo","todos")
    q=request.args.get("q","").strip()
    sql="SELECT * FROM items WHERE 1=1"; args=[]
    if kind in ("perdido","encontrado"):
        sql+=" AND kind=?"; args.append(kind)
    if q:
        sql+=" AND (name LIKE ? OR description LIKE ? OR place LIKE ?)"
        args += [f"%{q}%"]*3
    sql+=" ORDER BY resolved ASC, created_at DESC"
    with db() as con: items=con.execute(sql,args).fetchall()
    return render_template("index.html",items=items,kind=kind,q=q)

@app.post("/novo")
def novo():
    fields=["kind","name","description","place","contact"]
    data={f:request.form.get(f,"").strip() for f in fields}
    if data["kind"] not in ("perdido","encontrado") or not all(data.values()):
        flash("Preencha todos os campos obrigatórios.", "error"); return redirect(url_for("index"))
    image=None; file=request.files.get("image")
    if file and file.filename:
        filename=secure_filename(file.filename); ext=filename.rsplit(".",1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED:
            flash("Formato de imagem não permitido.", "error"); return redirect(url_for("index"))
        import uuid
        filename=f"{uuid.uuid4().hex}.{ext}"; file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename)); image=filename
    with db() as con:
        con.execute("INSERT INTO items(kind,name,description,place,contact,image) VALUES(?,?,?,?,?,?)",
                    (*[data[f] for f in fields],image))
    flash("Item cadastrado! Obrigado por ajudar a comunidade.", "success")
    return redirect(url_for("index"))

@app.post("/resolver/<int:item_id>")
def resolver(item_id):
    with db() as con:
        con.execute("UPDATE items SET resolved=1-resolved WHERE id=?",(item_id,))
    flash("Status do item atualizado.", "success")
    return redirect(url_for("index"))

if __name__=="__main__":
    init_db()
    app.run(debug=True)
