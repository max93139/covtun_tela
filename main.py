import os
import random
import sys
import requests

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in environment variables.", file=sys.stderr)
        sys.exit(1)
        
    try:
        file_path = os.path.join(os.path.dirname(__file__), "phrases.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError("Файл 'phrases.txt' не найден.")
            
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            
        if not lines:
            raise ValueError("Файл 'phrases.txt' пуст или содержит только пустые строки.")
            
        selected_phrase = random.choice(lines)
        
        # Отправка сообщения
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.post(url, json={"chat_id": chat_id, "text": selected_phrase}, timeout=10)
        response.raise_for_status()
        print(f"Успешно отправлено: '{selected_phrase}'")
        
    except Exception as e:
        error_msg = f"❌ Сбой автопостинга!\n\nОшибка: {str(e)}"
        print(error_msg, file=sys.stderr)
        try:
            # Попытка отправить отчет об ошибке в Telegram
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": error_msg},
                timeout=10
            )
        except Exception as telegram_err:
            print(f"Не удалось отправить отчет об ошибке в Telegram: {str(telegram_err)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
