import os
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def main():
    print("=== ローカルLLM チャットシステム（終了するには 'quit' と入力） ===")
    
    while True:
        user_input = input("\nあなた: ")
        if user_input.lower() == 'quit':
            break
            
        if not user_input.strip():
            continue
            
        try:
            # 変更点: chat.completions ではなく、Qiitaの記事と同じ responses を使用
            # 引数の messages も、最新の「model」「input」というシンプルな形式に合わせます
            stream = client.responses.create(
                model="local-model",
                input=user_input,
                stream=True
            )
            
            print("\nAI: ", end="", flush=True)
            
            # 変更点: 届くイベントの型に合わせて、テキストの断片（delta）を取り出す
            for event in stream:
                # Qiitaの `event.type === "response.output_text.delta"` と同じ判定
                if event.type == "response.output_text.delta":
                    if event.delta:
                        print(event.delta, end="", flush=True)
            
            print() # 最後に改行
            
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()