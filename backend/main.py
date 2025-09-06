from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#储存project_id和对应数据的键值对表
# projects = {}

@app.route('/api/project', methods=['POST'])
def handle_project():
    if request.method == 'POST':
        if 'Image' not in request.files:
            return jsonify({"error": "缺少'Image'文件"}), 400
        image = request.files['Image']
        if image.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        return useStructToLayoutAi(useImgToStructAi(image))


# @app.route('/api/project/<project_id>', methods=['GET'])
# def handle_project(project_id):
#     if request.method == 'GET':   
#         project = projects[project_id]     
#         if project:
#             return jsonify(project)
#         else:
#             return jsonify({"error": "Project not found"}), 404



if __name__ == '__main__':
    app.run(port=5000, debug=True)


#调用ai1，实现将图片转为电路结构数据
def useImgToStructAi(image):
    return {
        "components": [
            { "id": "R1", "type": "Resistor", "value": "220Ω", "pins": [{"id": "R1-1", "coord": "C7"}, {"id": "R1-2", "coord": "C12"}] },
            { "id": "LED1", "type": "LED", "color": "red", "pins": [{"id": "LED1-anode", "coord": "I15"}, {"id": "LED1-cathode", "coord": "J15"}] }
        ],
        "wires": [
            { "id": "wire-1", "from": "J15", "to": "NEG_TOP", "color": "black" },
            { "id": "wire-2", "from": "C12", "to": "I15", "color": "blue" }
        ]
    }

#调用llama
# def useLlama(propmt, input):
#     return {
#         "message": [
#             {"id": "sug1", "text": "建议将电阻R1的阻值从1kΩ改为220Ω，以保护LED。"},
#             {"id": "sug2", "text": "检测到555定时器的VCC引脚未连接到电源，可能导致电路不工作。"}
#         ]
    # }

# def useFindError(input):
#     return useLlama("帮助指出电路设计图中的错误 *输入结构描述* *输出结构要求*", input)

#调用ai2，将电路结构数据转成面包板布局数据
def useStructToLayoutAi(struct):
    return {
        "components": [
            { "id": "R1", "type": "Resistor", "value": "220Ω", "pins": [{"id": "R1-1", "coord": "C7"}, {"id": "R1-2", "coord": "C12"}] },
            { "id": "LED1", "type": "LED", "color": "red", "pins": [{"id": "LED1-anode", "coord": "I15"}, {"id": "LED1-cathode", "coord": "J15"}] }
        ],
        "wires": [
            { "id": "wire-1", "from": "J15", "to": "NEG_TOP", "color": "black" },
            { "id": "wire-2", "from": "C12", "to": "I15", "color": "blue" }
        ]
    }