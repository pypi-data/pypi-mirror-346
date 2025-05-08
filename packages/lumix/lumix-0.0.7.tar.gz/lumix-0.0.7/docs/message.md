# Message

## How to use

=== "Code"

```python
import PIL.Image
from lumix.types.messages import *
from lumix.llm import OpenAI

messages = [
    SystemMessage(content="You are a AI assistant."),
    UserMessage(content="你好"),
    AssistantMessage(content="你好, 我是AI助手。有什么可以帮助你的吗？"),
    ImageMessage(
        content="介绍这三张图片", 
        images=[
            "https://test.png", 
            PIL.Image.Image, 
            "base64,data: image/png;base64,"
        ]
    ),
]


llm = OpenAI(
    model="qwen", api_key="your_api_key", 
    base_url="https://api.openai.com/v1")
response = llm.completion(messages=messages)

print(response)
```

## BaseMessage

### SystemMessage

=== "Code"
    ```python
    from lumix.types.messages import *
    
    system_message = SystemMessage(content="你好")
    print(system_message)
    ```

=== "Example"
    ```text
    role='system' content='你好'
    ```

### UserMessage

=== "Code"
    ```python
    from lumix.types.messages import *
    user_message = UserMessage(content="你好")
    print(user_message)
    ```

=== "Example"
    ```text
    role='user' content='你好'
    ```

### AssistantMessage

=== "Code"
    ```python
    from lumix.types.messages import *
    assistant_message = AssistantMessage(content="你好")
    print(assistant_message)
    ```

=== "Example"
    ```text
    role='assistant' content='你好'
    ```

### ImageMessage

=== "Code"
    ```python
    from lumix.types.messages import *
    image_message = ImageMessage(
        content="介绍这三张图片", 
        images=[
            "https://test.png", 
            PIL.Image.Image, 
            "base64,data: image/png;base64,"
        ]
    )
    
    # Object
    print(image_message)
    # to openai message
    print(image_message.to_openai())
    # to dict
    print(image_message.to_dict())
    ```

=== "Example"
    ```text
    # Object
    role='assistant' content='介绍这三张图片' images=['https://test.png', 'PIL.Image.Image', 'base64,data: image/png;base64,']
    
    # to openai message
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "介绍这三张图片"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            },
        ],
    }
    
    # to dict
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "介绍这三张图片"
            },
            {
                "type": "image",
                "image": "image_url",
            },
            {
                "type": "image",
                "image": "image_url",
            },
        ],
    }
    ```

