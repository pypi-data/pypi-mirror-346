# Tools

## 联网搜索工具

### 百度搜索

=== "代码示例"

    ```python
    from lumix.agent.tools import BaiduSearch

    baidu = BaiduSearch(verbose=True)
    web_data = baidu.search(query="杭州天气", pages=1)
    print(web_data)
    ```

=== "Output"
    ```json
    page_content='\n【杭州天气预报15天_杭州天气预报15天查询】-中国天气网×杭州\n8~15天天气预报，是集合多家全球数值天气预报模式客观预报产品加工而成，未经预报员主观订正，反映未来一段时间内天气变化趋势，具有一定的不确定性，供公众参考，欲知更加准确的天气预报需随时关注短期天气预报和最新预报信息更新。\n今天\n03/21\n晴26/12℃西南风4-5级\n西南风3-4级\n详情周六\n03/22\n晴26/14℃西南风3-4级\n西南风3-4级\n详情周日\n03/23\n多云28/14℃西南风4-5级\n西风3-4级\n详情周一\n03/24\n晴29/14℃西风4-5级\n西南风3-4级\n详情周二\n03/25\n多云转阴32/17℃西南风5-6级\n无持续风向<3级\n详情周三\n03/26\n多云转雷阵雨34/21℃南风5-6级\n西风3-4级\n详情周四\n03/27\n小到中雨转小雨27/8℃东北风6-7级\n西北风5-6级\n详情周五\n03/28\n雨转阴10/3℃西风<3级\n西北风<3级\n详情周六\n03/29\n阴转雨13/6℃东风<3级\n东南风<3级\n详情周日\n03/30\n晴转阴17/7℃东北风<3级\n东风<3级\n详情周一\n03/31\n阴20/8℃东风<3级\n东南风<3级\n详情周二\n04/01\n阴转雨21/11℃东风<3级\n西北风<3级\n详情周三\n04/02\n雨转阴17/7℃东北风<3级\n西南风<3级\n详情周四\n04/03\n晴转阴22/7℃东风<3级\n东风<3级\n详情周五\n04/04\n阴转多云21/9℃东风<3级\n东南风<3级\n详情\n40天预报\n温度趋势\n降水趋势台风中心利奇马\n到达时间：\n2020-05-16\n中心位置：\n18.6N/120.1E\n风速风力：\n16米/秒\n中心气压：\n1000（百帕）\n未来移速：\n17公里/小时\n未来移项：\n北\n天气雷达\n我的天空精彩推荐\n 春天大幅提前！ 全国春季花粉预报地图来了 梦幻唯美！北京桃花映日出 春分：春色正中分 千花百卉争明媚 晨味时节——春分 如何理解今年气象日的主题\n未来3天公报未来10天公报 天气  推荐\n直播\n图集\n短视频\n生活\n\r\n          没有更多啦 ~\r\n        \n请使用浏览器的分享功能分享首页 \n15天 \n40天 \n地图 \n资讯 \n更多 \n气象数据来源：中央气象台 \n预报更新时间：每日06、08、12、16、20时' metadata={'url': 'http://www.baidu.com/link?url=NLXajc-CXLQoFwlgK-nap57POT1dfLvR6YdwcV3qiPUSVmjiolmkOKptDLhVUpIFW4A48F-xmKWvJNGRaJEwAa', 'title': '【杭州天气预报15天_杭州天气预报15天查询】-中国天气网', 'abstract': '杭州天气预报,及时准确发布中央气象台天气信息,便捷查询杭州今日天气,杭州周末天气,杭州一周天气预报,杭州蓝天预报,杭州天气预报,杭州40日天气预报,还提供杭州的生活指数、健...'}
    ```

### 百度图片

=== "Code"

    ```python
    from lumix.agent.tools import BaiduImageSearch
    
    baidu_image = BaiduImageSearch()
    images = baidu_image.search('杭州西湖')
    print(images[0].model_dump())
    ```

=== "Output"

    ```json
    {
      'image': <PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=800x1422 at 0x19A69EA2C00>, 
      'metadata': {
        'image_url': 'https://img2.baidu.com/it/u=1166879536,4231434679&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1422', 
        'object_url': 'https://p3-pc-sign.douyinpic.com/tos-cn-i-0813c001/oIBHGOfpAIvwziAAl75CA0CSiYIAFESgejDAn6~tplv-dy-aweme-images:q75.webp', 
        'from_url': 'http://www.douyin.com/note/7405630334227860787', 
        'from_title': '这辈子总要和心爱的人去一趟杭州西湖吧!来吹吹西湖的风'
      }
    }
    ```

> DataSchema 

- `image`: PIL的图片对象
- `metadata`:
    - `image_url`: 百度图床的图片地址
    - `object_url`: 图片源地址
    - `from_url`: 内容来源URL
    - `from_title`: 内容标题

??? note "示例"

    === "Code"
    
        ```python
        from lumix.llm import OpenAI
        from lumix.types.messages import ImageMessage
        from lumix.agent.tools import BaiduImageSearch
        
        baidu_image = BaiduImageSearch(verbose=True)
        images = baidu_image.search(query="汽车总动员")
        
        print(images)
        
        base_url = "https://api-inference.modelscope.cn/v1/"
        model = "Qwen/Qwen2.5-VL-32B-Instruct"
        llm = OpenAI(model=model, base_url=base_url, key_name="MODELSCOPE_TOKEN", verbose=False)
        
        messages = [
            ImageMessage(content="介绍这几张图片", images=[item.image for item in images]).to_openai(),
        ]
        
        completion = llm.completion(messages=messages)
        print(completion.choices[0].message.content)
        ```
    
    === "Output"
    
        ```markdown
        image=<PIL.WebPImagePlugin.WebPImageFile image mode=RGB size=500x734 at 0x2417D469E20> 
        
        metadata={
          'image_url': 'https://img0.baidu.com/it/u=1098810270,2820787263&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=734', 
          'object_url': 'https://bkimg.cdn.bcebos.com/pic/d52a2834349b033b5bb5e8860e9721d3d539b600176c', 
          'from_url': 'http://baike.baidu.com/item/%E8%B5%9B%E8%BD%A6%E6%80%BB%E5%8A%A8%E5%91%98/55472022', 
          'from_title': '赛车<strong>总动员</strong>'
        }
        
        ### 图片介绍
        
        #### **第一张图片**
        这张图片是动画电影《赛车总动员》（Cars）系列的宣传海报，具体为《赛车总动员：在路上》（Cars On The Road）。以下是图片的主要内容和细节：
        
        1. **标题信息**：
           - 海报顶部写着：“NINE NEW EPISODES, ONE EPIC ROAD TRIP.”（九个新剧集，一场史诗般的公路之旅），表明这是一部包含多个故事的连续剧或迷你剧。
        
        2. **主要角色**：
           - 中心位置是主角闪电麦昆（Lightning McQueen），红色跑车，车身有标志性的“95”号。
           - 左侧有一辆棕色卡车，可能是拖车托马斯（Tow Mater），表情夸张，显得非常兴奋。
           - 其他角色包括一个黄色小车、一只恐龙形状的怪物、以及一些其他车辆角色，营造出一种热闹和冒险的氛围。
        
        3. **背景元素**：
           - 背景是一个充满活力的夜景，天空中有烟花和降落伞，暗示着庆祝或冒险的主题。
           - 地面是一条宽阔的道路，道路上有许多车辆，显示出集体旅行的感觉。
           - 远处可以看到建筑物和霓虹灯招牌，增加了城市或小镇的氛围。
        
        4. **品牌标识**：
           - 底部有“Disney Pixar Cars”字样，明确这是迪士尼·皮克斯（Disney·Pixar）制作的作品。
           - 右下角有“Cars On The Road”的标题，以及“Disney+ Day Premiere, Sept 8 only on Disney+”，表明这是在Disney+平台独家播出的内容，并且是在某个特定日期首映。
        
        ---
        
        #### **第二张图片**
        这张图片展示了《赛车总动员》系列中的主角——闪电麦昆（Lightning McQueen）。以下是图片的主要内容和细节：
        
        1. **角色形象**：
           - 闪电麦昆是一辆红色的赛车，车身设计流畅，带有明显的速度感。
           - 车身侧面有“95”号，这是他的标志性号码。
           - 面部表情友好，眼睛大而明亮，嘴巴微笑着，显得自信且富有亲和力。
        
        2. **细节特征**：
           - 车头部分有蓝色的大灯，显得非常醒目。
           - 车轮设计精致，轮胎和轮毂都经过精心描绘。
           - 整体造型充满了动感，符合其作为赛车的角色设定。
        
        3. **文字信息**：
           - 左上角有“Disney Pixar Cars”标志，表明这是《赛车总动员》系列的一部分。
           - 右下角写着“LIGHTNING MCQUEEN”，确认了角色名称。
           - 底部的文字说明：“‘CARS 2’ Lightning McQueen (voice by Owen Wilson) ©Disney/Pixar. All Rights Reserved.”，表明这是《赛车总动员2》中的角色，配音演员是欧文·威尔逊（Owen Wilson），并声明版权归属迪士尼·皮克斯。
        
        4. **背景**：
           - 背景为纯白色，突出了闪电麦昆的形象，使其成为画面的焦点。
        
        ---
        
        ### 总结
        - **第一张图片**是《赛车总动员：在路上》的宣传海报，展示了多个角色和充满冒险的场景，强调了这部作品的连续性和趣味性。
        - **第二张图片**是《赛车总动员》系列中的主角闪电麦昆的单独展示图，突出了他的经典形象和角色特点。
        
        这两张图片共同体现了《赛车总动员》系列的活力与魅力，无论是整体剧情还是单个角色，都充满了动感和吸引力。
        ```
