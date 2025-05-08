# Quick Start

**安装**

```bash
pip install lumix
```

**基本使用**

???+ question "大模型API调用"

    === "代码示例"
        ```python
        from lumix.llm import OpenAI

        base_url = "https://open.bigmodel.cn/api/paas/v4"
        llm = OpenAI(model="glm-4-flash", base_url=base_url, api_key="your_api_key")
        
        completion = self.llm.completion(prompt="你好")
        print(completion.choices[0].message.content)
        ```
    === "Output"
        ```text
        [User] 你好
        [Assistant] 你好👋！很高兴见到你，有什么可以帮助你的吗？
        ```
-----
