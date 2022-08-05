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
    response = dict()

    conn = connect_to_db()
    cursor = conn.cursor()

    if content_type == 'application/json':
        json = request.json
        
        if all (key in json for key in ("table_name",)):
            table_name = json["table_name"]
            
            cursor.execute("""SELECT * FROM information_schema.tables
                WHERE table_schema = 'public'""")

            exists = False
            result = cursor.fetchall()
            for step in result:
                if table_name in step:
                    exists = True
            
            response["response"] = exists
            response["tables"] = result
    
    conn.close()

    return jsonify(response)

@app.route('/create', methods=['POST'])
def create():
    content_type = request.headers.get('Content-Type')
    response = {
        "response": True
    }

    conn = connect_to_db()
    cursor = conn.cursor()

    if content_type == 'application/json':
        json = request.json

        if all (key in json for key in ("sql_command",)):
            try:
                cursor.execute(json["sql_command"])
                conn.commit()
            except psycopg2.errors.DuplicateTable:
                response["error"] = "Table already exists"
                response["response"] = False
            except Exception as error:
                response["error"] = error
                response["response"] = False

    conn.close()

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)