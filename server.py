from flask import Flask, jsonify, request

app = Flask(__name__)

company_storage = []

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is your Flask API!'})


@app.route('/api/add_company', methods=['POST'])
def add_company():
    data = request.get_json()

    if 'company_name' in data:
        company_name = data['company_name']
        company_storage.append(company_name)
        return jsonify({'message': f'Company name "{company_name}" added successfully!'})
    else:
        return jsonify({'error': 'Missing "company_name" parameter'}), 400


@app.route('/api/get_company', methods=['GET'])
def get_company():
    return jsonify({'company_names': company_storage})

@app.route('/api/delete_company', methods=['DELETE'])
def delete_company():
    data = request.get_json()

    if 'company_name' in data:
        company_name = data['company_name']

        if company_name in company_storage:
            company_storage.remove(company_name)
            return jsonify({'message': f'Company name "{company_name}" deleted successfully!'})
        else:
            return jsonify({'error': f'Company name "{company_name}" not found'}), 404
    else:
        return jsonify({'error': 'Missing "company_name" parameter'}), 400



if __name__ == '__main__':
    app.run(debug=True)
