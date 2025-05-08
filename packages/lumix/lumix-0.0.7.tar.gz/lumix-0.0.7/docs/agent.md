# Agent

???+ tip "Agent Search"

    === "代码示例"
    
        ```python
        from lumix.llm import OpenAI
        from lumix.agent import ToolsAgent, Tools
        from lumix.agent.tools import baidu_search
        from lumix.types.messages import SystemMessage, UserMessage
        
        base_url = "https://api-inference.modelscope.cn/v1/"
        model = "Qwen/Qwen2.5-14B-Instruct-1M"
        llm = OpenAI(model=model, base_url=base_url, key_name="MODELSCOPE_TOKEN", verbose=False)
        tools = Tools(tools=[baidu_search])
        agent = ToolsAgent(tools=tools, llm=llm, verbose=True)
        
        messages = [
            SystemMessage(content="You are a helpful assistant. Use search tool before answer user's question. Answer in Markdown format and give the corresponding url quote."),
            UserMessage(content="目前国际乒乓积分排名前五的是哪些人，积分是多少？")
        ]
        completion = agent.completion(messages=messages)
        print(completion.choices[0].message.content)
        ```
    
    === "Output"
    
        ```text
        根据最新的国际乒乓球联合会（WTT）排名，以下是男女单打排名前五的情况：
        
        ### 男子单打：
        1. 林诗栋 - 8025 分
        2. 王楚钦 - 7925 分
        3. 梁靖崑 - 5425 分
        4. 张本智和 - 4950 分
        5. 马龙 - 4850 分
        
        ### 女子单打：
        1. 孙颖莎 - 11300 分
        2. 王曼昱 - 8850 分
        3. 王艺迪 - 5425 分
        4. 陈幸同 - 4250 分
        5. 早田希娜 - 4200 分
        
        以上数据来源于[世界乒联最新排名](http://www.baidu.com/link?url=s8C6OqE8cFjCm09asXg5hNcgb4I1-jxnlk_cyyY3R_o9H3oirLenCJ3WPh2G76tYCRePLavp0IhnsKmW5rJIn5ByXntcmlg73kuNnqtlveO)。
        ```

-----
