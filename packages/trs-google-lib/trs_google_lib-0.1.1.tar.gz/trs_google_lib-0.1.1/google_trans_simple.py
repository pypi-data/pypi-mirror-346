import httpx
import urllib.parse
from typing import Optional


class GoogleTranslate:
    """
    Асинхронный клиент для перевода текста через Google Translate.
    Поддерживает использование прокси.
    """
    def __init__(self, proxy: Optional[str] = None, timeout: float = 10.0):
        """
        :param proxy: URL прокси-сервиса, например, "http://user:pass@proxy.server:port". Если None, прокси не используется.
        :param timeout: Время ожидания ответа в секундах.
        """
        self.proxy = proxy
        self.timeout = timeout
        self.url = (
            "https://www.google.com/async/translate?vet=12ahUKEwjBk_PvrYKMAxUmEFkFHX5nF4IQqDh6BAgIEDE..i"
            "&ei=vFjQZ8HFCKag5NoP_s7dkAg&opi=89978449&yv=3&_fmt=pc&cs=0"
        )
        self.headers = {
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "origin": "https://www.google.com",
            "referer": "https://www.google.com/",
        }
        self.data_template = (
            "async=translate,sl:{source_lang},tl:{target_lang},st:{encoded_text},"
            "id:1741707472305,qc:true,ac:false,_id:tw-async-translate,_pms:s,_fmt:pc,"
            "_basejs:…"
        )

    async def translate(self, text: str, source_lang: str = "ru", target_lang: str = "en") -> str:
        """
        Переводит заданный текст с source_lang на target_lang.
        """
        encoded_text = urllib.parse.quote(text)
        data = self.data_template.format(
            source_lang=source_lang,
            target_lang=target_lang,
            encoded_text=encoded_text,
        )

        # Формируем мэппинг прокси (если передан)
        proxies = {"http://": self.proxy, "https://": self.proxy} if self.proxy else {}

        # Передаём proxies в клиент
        async with httpx.AsyncClient(proxies=proxies, timeout=self.timeout) as client:
            response = await client.post(self.url, headers=self.headers, data=data)
            response.raise_for_status()
            return response.text

# Пример использования
if __name__ == "__main__":
    import asyncio

    async def main():
        translator = GoogleTranslate(proxy=None)  # Замените proxy на нужное значение, если требуется
        text = "Чуть чуть хреново поел еды. Много соли, как будто бомжа облизал. Чур не меня!"
        result = await translator.translate(text)
        print("Результат перевода:")
        print(result)

    asyncio.run(main())
