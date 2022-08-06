from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)
app.config.from_object("config.Config")

def connect_to_db():
    return psycopg2.connect(
        database=app.config["POSTGRES_DB"], 
        user=app.config["POSTGRES_USER"], 
        password=app.config["POSTGRES_PASSWORD"], 
        host=app.config["POSTGRES_HOST"], 
        port=app.config["POSTGRES_PORT"]
    )

@app.route('/check', methods=['POST'])
def check():
    content_type = request.headers.get('Content-Type')
    response = {
        "exists": False,
        "error": False,
        "created": False
    }

    conn = connect_to_db()
    cursor = conn.cursor()

    if content_type == 'application/json':
        json = request.json
        
        if all(key in json for key in ["md5_hash", "table_name"]):
            md5_hash = json["md5_hash"]
            table_name = json["table_name"]
            
            cursor.execute("""SELECT * FROM information_schema.tables""")

            result = cursor.fetchall()

            for step in result:
                current_table_name = step[2]
                cursor.execute("""SELECT MD5('{}')""".format(current_table_name))

                if cursor.fetchall()[0][0] == md5_hash:
                    response["exists"] = True
                    break

        if not response["exists"]:
            command = """CREATE TABLE {}()""".format(table_name)
            try:
                cursor.execute(command)
                conn.commit()
                response["created"] = True
            except Exception as error:
                response["error"] = True
    else:
        response["error"] = True
    
    conn.close()

    return jsonify(response)

@app.route('/apply_sql_command', methods=['POST'])
def apply_sql_command():
    content_type = request.headers.get('Content-Type')
    response = {
        "response": True,
        "error": False
    }

    conn = connect_to_db()
    cursor = conn.cursor()

    if content_type == 'application/json':
        current_json = request.json

        if all (key in current_json for key in ("sql_command",)):
            try:
                cursor.execute(current_json["sql_command"])
                conn.commit()
            except Exception as error:
                response["error"] = True
                response["response"] = False

    conn.close()

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

