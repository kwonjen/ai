import config

# OpenAI Conn
client = config.Init.open_ai_conn();

completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': '왜 하늘은 하늘색인가요?'}],
    temperature=0.0 ## 0.0 ~ 2.0 (높을수록 동일한 프롬프트에도 매번 다른 답변)
)

print(completion.choices[0].message.content)

