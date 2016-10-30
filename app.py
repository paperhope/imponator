import sqlite3
import datetime
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

stuffdone_columns = ("Who", "What", "Why")
database = "imponator.db"

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


def _save_item(jcontent):
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    row = [None] * len(stuffdone_columns)
    for idx, val in enumerate(stuffdone_columns):
        
        if val in jcontent:
            row[idx] = jcontent[val]
        else:
            raise Exception

    cur.execute("INSERT INTO stuffdone(Who,What,Why)  VALUES(?,?,?)", row)
    conn.commit()
    conn.close()
    
def _prepare_list(rows):

    result = []
    for row in rows:
        result.append({
            "Who": row[0],
            "What": row[1],
            "Why": row[2],
            "When": _timestamp_to_str(row[3]),
            "Timestamp": row[3]
        })

    result.sort(key=lambda x: x["Timestamp"], reverse=True)

    return result

def _timestamp_to_str(timestamp):
        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y") 
            
def _get_list(max_items):
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM stuffdone LIMIT 10")

    return _prepare_list(cur.fetchall())


def _post_item(item):
    conn = conn.sqlite3.connect(database)
    cur  = conn.cursor()
    cur.execute()
    
if __name__ == "__main__":
    app.run()
