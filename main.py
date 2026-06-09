import os
from openai import OpenAI

# LM Studioのローカルサーバーに接続するためのクライアント初期化
# APIキーは不要ですが、ライブラリの仕様上ダミーの文字列を入れておきます
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

def main():
    print("=== ローカルLLM チャットシステム（終了するには 'quit' と入力） ===")
    
    # 会話履歴を保持するリスト（システムプロンプトでキャラクター設定などを指定可能）
    messages = [
        {"role": "system", "content": "あなたは簡潔かつ正確に答える優秀なアシスタントです。"}
    ]
    
    while True:
        user_input = input("\nあなた: ")
        if user_input.lower() == 'quit':
            break
            
        if not user_input.strip():
            continue
            
        # ユーザーの入力を履歴に追加
        messages.append({"role": "user", "content": user_input})
        
        try:
            # LM Studioにリクエストを送信
            # model引数はLM Studio側で現在ロードされているモデルが自動で適用されます
            response = client.chat.completions.create(
                model="local-model", 
                messages=messages,
                temperature=0.7
            )
            
            # 応答の取得と表示
            answer = response.choices[0].message.content
            print(f"\nAI: {answer}")
            
            # AIの応答も履歴に追加して会話を継続させる
            messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")

if __name__ == "__main__":
    main()