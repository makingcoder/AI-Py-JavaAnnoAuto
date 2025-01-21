import os
import requests
import json

class DeepSeekLLM:
    def __init__(self, api_key):
        self.api_key = api_key

    def _call(self, prompt, stop=None):
        # 这里需要根据 DeepSeek 大模型的 API 调用方式进行修改，以下是一个示例，假设通过 HTTP 请求调用
        # 替换为正确的 DeepSeek API 端点
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            # 添加 API 密钥到请求头中，确保认证方式正确
            "Authorization": f"Bearer {self.api_key}"
        }
        # 调整 payload 结构，添加 messages 字段
        payload =  {
            "model": "deepseek-chat",
            "messages": [
            {"role": "system", "content": "You are a programmer. Please complete the comments in chinese"},
            {"role": "user", "content": prompt} ],
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
             # 打印响应内容，以便查看其结构
            if response.status_code == 200:
              data = json.loads(json.dumps(response.json()))  # 将 JSON 字符串转换为 Python 对象
              contents = [choice['message']['content'] for choice in data['choices'] if'message' in choice and 'content' in choice['message']]
              string = "".join(contents)
              print (string)
              return (string)
            else:
                raise Exception(f"Failed to call DeepSeek API: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error occurred: {e}")

    def __call__(self, prompt, stop=None):
        return self._call(prompt, stop)

    @property
    def _identifying_params(self):
        return {"name": "DeepSeekLLM"}


def add_comments_to_java_files(folder_path, api_key):
    # 初始化 DeepSeek 大模型，并传入 API 密钥
    llm = DeepSeekLLM(api_key)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r',encoding='utf-8') as f:
                    code = f.read()
                # 利用大模型为代码添加注释
                prompt = f"Please add comments to the following Java code: {code}"
                # 调用 DeepSeekLLM 实例
                commented_code = llm(prompt)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(commented_code)

if __name__ == "__main__":
    # 输入项目文件夹地址，将此地址替换为你实际的 Java 项目文件夹地址
    project_folder = "D:\project-large-lang-model\langchain.py\spring-test"
    # 输入你的 API 密钥，将此 API 密钥替换为你实际的 DeepSeek API 密钥
    api_key = "sk-0c698addc24e44629d62538777c3e309"
    add_comments_to_java_files(project_folder, api_key)