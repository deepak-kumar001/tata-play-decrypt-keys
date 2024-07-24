# Import dependencies
from flask import Flask, request, jsonify
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from scripts import decrypt as decrypt_module
import scripts


# Define Flask app object
app = Flask(__name__)

# Route for root '/'
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return jsonify({
            'Name': "TPlay Keys",
            'Description': "Decrypt keys from WV licence response"
        })
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            decrypt_response = scripts.decrypt.decrypt_content(
                in_pssh=data.get('PSSH'),
                license_url=data.get('License URL'),
            )
            return jsonify(decrypt_response)
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'An error occurred'}), 500

# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
