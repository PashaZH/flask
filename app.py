from flask import Flask, jsonify, request
from typing import Any
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).parent
path_to_db = BASE_DIR / "store.db"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/quotes", methods=['GET'])
def get_quotes():
    """ Retrieve all quotes from the database """
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM quotes")
    quotes_db = cursor.fetchall()
    cursor.close()
    connection.close()

    keys = ("id", "author", "text", "rating")
    quotes = [dict(zip(keys, quote)) for quote in quotes_db]
    return jsonify(quotes), 200

@app.route("/quotes/<int:quote_id>", methods=['GET'])
def get_quote(quote_id: int):
    """ Retrieve a single quote by ID """
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    quote_db = cursor.fetchone()
    cursor.close()
    connection.close()

    if quote_db:
        keys = ("id", "author", "text", "rating")
        quote = dict(zip(keys, quote_db))
        return jsonify(quote), 200
    return jsonify(error=f"Quote with id={quote_id} not found."), 404

@app.route("/quotes", methods=['POST'])
def create_quote():
    """ Create a new quote in the database """
    new_quote = request.json
    
   
    if not new_quote or 'author' not in new_quote or 'text' not in new_quote:
        return jsonify(error="Missing required fields: author and text"), 400
    
    
    rating = new_quote.get("rating", 1)
    if rating not in range(1, 6):
        rating = 1

    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO quotes (author, text, rating) VALUES (?, ?, ?)", 
        (new_quote['author'], new_quote['text'], rating)
    )
    connection.commit()
    
    new_quote_id = cursor.lastrowid
    cursor.close()
    connection.close()

    new_quote['id'] = new_quote_id
    return jsonify(new_quote), 201

@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id: int):
    """ Update an existing quote """
    new_data = request.json
    
    
    allowed_keys = {"author", "text", "rating"}
    if not set(new_data.keys()).issubset(allowed_keys):
        return jsonify(error="Invalid fields for update"), 400

   
    if "rating" in new_data and new_data["rating"] not in range(1, 6):
        return jsonify(error="Rating must be between 1 and 5"), 400

    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()

  
    update_fields = []
    update_values = []
    for key in allowed_keys:
        if key in new_data:
            update_fields.append(f"{key} = ?")
            update_values.append(new_data[key])
    
    if not update_fields:
        cursor.close()
        connection.close()
        return jsonify(error="No valid update fields provided"), 400

    update_values.append(quote_id)
    query = f"UPDATE quotes SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(query, update_values)
    connection.commit()

 
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify(error=f"Quote with id={quote_id} not found"), 404

   
    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    updated_quote_db = cursor.fetchone()
    cursor.close()
    connection.close()

    keys = ("id", "author", "text", "rating")
    updated_quote = dict(zip(keys, updated_quote_db))
    return jsonify(updated_quote), 200

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote(quote_id: int):
    """ Delete a quote by ID """
    connection = sqlite3.connect(path_to_db)
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    connection.commit()

    
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify(error=f"Quote with id={quote_id} not found"), 404

    cursor.close()
    connection.close()
    return jsonify(message=f"Quote with id={quote_id} has been deleted"), 200

if __name__ == "__main__":
    app.run(debug=True)