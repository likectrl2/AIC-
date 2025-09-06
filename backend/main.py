from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# 初始化 Flask 应用并配置 CORS
app = Flask(__name__)
CORS(app)

# 配置文件上传相关参数
app.config['UPLOAD_FOLDER']='uploads/'  # 上传文件保存路径
app.config['MAX_CONTENT_LENGTH']=16*10024*1024  # 最大文件大小限制为16MB
os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)  # 创建上传目录

# 用于存储项目数据的内存字典
projects = {}

def allowed_file(filename):
    """
    检查文件是否为允许的图片格式
    Args:
        filename: 文件名
    Returns:
        bool: 是否为允许的文件格式
    """
    return'.' in filename and filename.rsplit('.',1)[1].lower()in{'png','jpg','jpeg','gif','bmp'}

@app.route('/api/project', methods=['POST'])
def handle_project():
    """
    处理新项目创建请求
    - 接收上传的图片
    - 生成项目ID
    - 保存图片文件
    - 处理图片生成电路结构数据
    - 生成面包板布局数据
    Returns:
        JSON响应包含项目信息
    """
    if request.method == 'POST':
        # 检查是否上传了图片
        if 'Image' not in request.files:
            return jsonify({"error": "缺少'Image'文件"}), 400
        image = request.files['Image']
        if image.filename == '':
            return jsonify({"error": "未选择文件"}), 400
        
        # 生成唯一的项目ID
        project_id = str(uuid.uuid4())

        # 保存上传的图片
        filename = f"{project_id}_{secure_filename(image.filename)}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # 使用AI处理图片
        struct_data = useImgToStructAi(image)
        layout_data = useStructToLayoutAi(struct_data)

        # 保存项目信息到内存
        projects[project_id] = {
            "id": project_id,
            "image_filename": filename,
            "image_path": image_path,
            "struct_data": struct_data,
            "layout_data": layout_data,
            "created_at": datetime.now().isoformat(),
            "conversations": []  # 存储对话历史
        }

        return jsonify({
            "project_id": project_id,
            "struct_data": struct_data,
            "layout_data": layout_data,
            "message": "项目创建成功"
        })

@app.route('/api/project/<project_id>', methods=['GET'])
def get_project(project_id):
    """
    获取特定项目的信息
    Args:
        project_id: 项目ID
    Returns:
        JSON响应包含项目详细信息
    """
    if request.method == 'GET':   
        project = projects.get(project_id)
        if project:
            # 返回项目信息（排除对话历史）
            project_info = {k: v for k, v in project.items() if k != 'conversations'}
            return jsonify(project_info)
        else:
            return jsonify({"error": "Project not found"}), 404

@app.route('/api/project/<project_id>/chat', methods=['POST'])
def handle_chat(project_id):
    """
    处理项目相关的AI对话请求
    Args:
        project_id: 项目ID
    Returns:
        JSON响应包含对话记录
    """
    if request.method == 'POST':
        project = projects.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "缺少消息内容"}), 400
        
        user_message = data['message']
        ai_response = useLlama(user_message, project['struct_data'])
        
        # 记录对话
        conversation = {
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        project['conversations'].append(conversation)
        
        return jsonify({
            "project_id": project_id,
            "conversation": conversation
        })

@app.route('/api/project/<project_id>/conversations', methods=['GET'])
def get_conversations(project_id):
    """
    获取项目的所有对话历史
    Args:
        project_id: 项目ID
    Returns:
        JSON响应包含对话历史列表
    """
    if request.method == 'GET':
        project = projects.get(project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        return jsonify({
            "project_id": project_id,
            "conversations": project.get('conversations', [])
        })

@app.route('/api/projects', methods=['GET'])
def list_projects():
    """
    获取所有项目的列表
    Returns:
        JSON响应包含所有项目的基本信息
    """
    projects_list = []
    for project_id, project_data in projects.items():
        projects_list.append({
            "id": project_id,
            "image_filename": project_data.get('image_filename'),
            "created_at": project_data.get('created_at'),
            "conversation_count": len(project_data.get('conversations', []))
        })
    
    return jsonify({
        "projects": projects_list,
        "count": len(projects_list)
    })

def useImgToStructAi(image):
    """
    AI模型：将图片转换为电路结构数据
    Args:
        image: 上传的图片文件
    Returns:
        dict: 电路结构数据
    """
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

def useStructToLayoutAi(struct):
    """
    AI模型：将电路结构数据转换为面包板布局数据
    Args:
        struct: 电路结构数据
    Returns:
        dict: 面包板布局数据
    """
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
def useLlama(propmt, input):
    return {
        "message": [
            {"id": "sug1", "text": "建议将电阻R1的阻值从1kΩ改为220Ω，以保护LED。"},
            {"id": "sug2", "text": "检测到555定时器的VCC引脚未连接到电源，可能导致电路不工作。"}
        ]
    }

def useFindError(input):
    return useLlama("帮助指出电路设计图中的错误 *输入结构描述* *输出结构要求*", input)

# 启动应用
if __name__ == '__main__':
    app.run(port=5000, debug=True)