"""代读引擎 - 核心提示词模板与 LLM 调用"""
from openai import OpenAI
import config

SYSTEM_PROMPT = """你将扮演一位私人学者，替我仔细阅读用户提供的书籍内容，然后按照下面的结构为我呈现内容。

**重要原则**：
- 不要只给结论，必须保留书中最有说服力的具体案例、实验、故事作为证据。
- 回答应当是一篇详细的深度转述，不少于 5000 字。
- 如果你不确定某个细节，请标注"此处信息不确定"，不要编造。
- 使用中文回答。

请严格按照以下六部分展开，每部分用二级标题（##）标记：

## 一、这本书到底在解决什么问题？

- 用一句话概括核心问题。
- 附上书中导致作者想写这本书的那个核心事件或现象，尽量详细。

## 二、核心主张与论证链条

- 列出本书最主要的 3-5 个主张。
- 每个主张之下，必须配上书中至少一个具体的例子/实验/人物故事来详细说明。
- 如果书中某个主张没有提供实证，请标注"作者在此处未给出实例"，不要自己编造。

## 三、最颠覆或最反直觉的 3 个点

- 摘出书中与大众常识截然相反的观点。
- 每个点都要附上它用来颠覆读者的那个关键实验或真实案例的详细描述。

## 四、如果只记住一个故事

- 选出全书最精彩、最适合以后讲给别人听的一个完整故事。
- 请像写一篇微型小说一样，详细转述其背景、人物、经过、结果和作者的分析。
- 不少于 800 字。

## 五、我可能会质疑的地方

- 客观分析书中的论证是否存在逻辑跳跃、以偏概全、幸存者偏差等问题。
- 如果有，请用书中具体内容举例说明。

## 六、这本书与我生活最直接的一个接口

- 假设我是一个普通上班族/学生，不创业也不做研究。
- 从书中挑一个能立刻用上的具体行动建议，并补充原文中的操作细节。
- 写清楚具体怎么做、什么场景下做、预期什么效果。"""

CASE_ENHANCED_SUFFIX = """

**额外要求（案例加厚版）**：
- 每个核心主张必须配 2-3 个书中案例，而不是 1 个。
- "最颠覆直觉"部分扩展为 5 个点。
- 在每个案例后附加"这个案例之所以有力，是因为……"的分析句。
- 整体字数目标：8000-12000 字。"""


def get_client() -> OpenAI:
    return OpenAI(
        api_key=config.OPENAI_API_KEY,
        base_url=config.OPENAI_BASE_URL,
    )


def generate_report(
    book_title: str = "",
    book_content: str = "",
    mode: str = "标准版",
) -> str:
    """
    生成代读报告。
    :param book_title: 书名
    :param book_content: 书籍文本内容（来自文件解析或手动输入）
    :param mode: "标准版" 或 "案例加厚版"
    :return: Markdown 格式的代读报告
    """
    system = SYSTEM_PROMPT
    if mode == "案例加厚版":
        system += CASE_ENHANCED_SUFFIX

    if book_content:
        user_msg = f"请代读以下书籍内容。书名：《{book_title}》\n\n---\n\n{book_content}"
    elif book_title:
        user_msg = f"请代读《{book_title}》这本书。请根据你对这本书的了解来生成代读报告。"
    else:
        raise ValueError("必须提供书名或书籍内容")

    client = get_client()
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.7,
        max_tokens=16000,
        stream=True,
    )

    full_text = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            full_text += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content


def generate_followup(book_title: str, report: str, question: str) -> str:
    """对已有报告进行追问"""
    client = get_client()
    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": f"你是一位私人学者，刚刚为用户代读了《{book_title}》。"
                f"以下是你的代读报告：\n\n{report}\n\n"
                f"现在用户对报告的某个部分有追问，请基于书中的具体内容回答。"
                f"保持详细、有案例支撑的风格。用中文回答。",
            },
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        max_tokens=8000,
        stream=True,
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
