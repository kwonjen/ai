import config

# OpenAI Conn
client = config.Init.open_ai_conn();

completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {
            'role': 'system', 'content': '당신은 물리학 선생님입니다. 초등학교 5학년한테 설명하듯이 해주세요.'
        },
        {
            'role': 'user',
            'content': '왜 하늘은 하늘색인가요?'
        }
    ],
    stream=True,
    temperature=0.0 ## 0.0 ~ 2.0 (높을수록 동일한 프롬프트에도 매번 다른 답변)
)

## 실시간 출력
for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')

## 답변 응답후 출력
# print(completion.choices[0].message.content)

