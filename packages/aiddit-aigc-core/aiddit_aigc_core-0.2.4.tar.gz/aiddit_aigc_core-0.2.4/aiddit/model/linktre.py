from openai import OpenAI

openai_client = OpenAI(
    api_key="sk-ZdUMj9U0NAXCmiw_wglkmFv8jpaOQ_psosLuN6RSLtl2lj6RbUgkocdRaZY",
    base_url="https://openai.linktre.cc/v1"
)

if __name__ == "__main__":
    note_data = [{"text": "生成一张猫狗玩耍的图片", "type": "text"}]

    response = openai_client.chat.completions.create(
        model="gpt-4o-all",
        messages=[
            {
                "role": "user",
                "content": note_data
            }
        ],
        temperature=0,
        stream=False
    )

    print(response)