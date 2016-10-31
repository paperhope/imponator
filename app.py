import os
import sqlite3
import datetime
from flask import Flask, render_template, send_from_directory, request, g

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
        DATABASE=os.path.join(app.root_path, 'imponator.db'),
    ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

stuffdone_columns = ("Who", "What", "Why")
    
@app.route("/", methods=["GET"])
def imponator_list():
    impressive_list = _get_list(10)
    return render_template("list.html", list_of_stuff = impressive_list)


@app.route("/item", methods=["POST"])
def imponator_item():
    content = request.get_json()
    try:
        _save_item(content)
        return "Ok"
    except Exception as e:
        print(e)
        return "Blurgh!"

    
@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        
    return db
    
def _save_item(jcontent):

    if set(stuffdone_columns) != set(jcontent.keys()):
        raise Exception
    
    row = [None] * len(stuffdone_columns)
    for idx, val in enumerate(stuffdone_columns):
        row[idx] = jcontent[val]

    db = get_db()
    db.cursor().execute("INSERT INTO stuffdone(Who,What,Why)  VALUES(?,?,?)", row)
    db.commit()

    
def _prepare_list(rows):

    print(rows)
    result = []
    for row in rows:
        print(row.keys())
        tmp = { k: row[k] for k in stuffdone_columns}
        tmp["When"] = _timestamp_to_str(row["Timestamp"])

        result.append(tmp)
        
    result.sort(key=lambda x: x["When"], reverse=True)

    return result

def _timestamp_to_str(timestamp):
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%B %d, %Y") 
            
def _get_list(max_items):
    c = get_db().cursor()
    c.execute("SELECT * FROM stuffdone LIMIT 10")#, (max_items,))

    return _prepare_list(c.fetchall())
    
if __name__ == "__main__":
    app.run()
