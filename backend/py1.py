from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

circuits_db = {
    "proj_1a2b3c4d": {
        "projectId": "proj_1a2b3c4d",
        "projectName": "555定时器闪灯电路 (来自服务器)",
        "description": "一个使用NE555定时器芯片控制LED闪烁的基础电路。",
        "lastModified": "2025-09-05T08:30:00Z",
        "breadboard": {
            "type": "standard_half"
        },
        "components": [
            {
                "id": "comp_U1",
                "type": "ic",
                "label": "U1",
                "properties": {"name": "NE555"},
                "pins": [{"pinName": "8 (VCC)", "boardPin": "F10"}]
            }
        ],
        "wires": [
            {"id": "wire_1", "color": "red", "from": "power_positive_top_1", "to": "F10"}
        ]
    }
}

@app.route('/api/circuit/<project_id>', methods=['GET', 'POST'])
def handle_circuit(project_id):
    if request.method == 'GET':
        circuit = circuits_db.get(project_id)
        if circuit:
            return jsonify(circuit)
        else:
            return jsonify({"error": "Circuit not found"}), 404

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        print(f"收到来自前端的数据: {data}")
        
        circuits_db[project_id] = data
        
        return jsonify({
            "message": f"电路 '{project_id}' 已成功保存!",
            "receivedData": data
        }), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)