# server.py
import os
import asyncio
from openai import AsyncOpenAI # Импортируем асинхронный клиент
from mcp.server.fastmcp import FastMCP, Context

async def call_openai_for_news_analysis(news_text: str, analysis_prompt: str,model_name: str, ctx: Context) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    base_url = "https://openrouter.ai/api/v1"

    if not api_key:
        error_msg = "OPENROUTER_API_KEY не найден в переменных окружения."
        ctx.error(error_msg)
        # В реальном приложении можно рейзить кастомное исключение или возвращать спец. ошибку
        raise ValueError(error_msg)

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    ctx.info(f"Отправка запроса к OpenAI API. Модель: {model_name}. Новость: {news_text[:50]}...")

    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": analysis_prompt},
                {"role": "user", "content": news_text}
            ]
        )
        result = response.choices[0].message.content
        ctx.info("Ответ от OpenAI API получен.")
        return result if result else "OpenAI API вернул пустой ответ."
    except Exception as e:
        ctx.error(f"Ошибка при обращении к OpenAI API: {str(e)}")
        return f"Ошибка взаимодействия с OpenAI: {str(e)}"

# --- MCP Сервер и Инструменты ---

mcp = FastMCP("NewsLawChecker")

from .prompts import NEWS_ANALYSIS_LEGAL_PROMPT, SPELL_CHECKER_PROMPT, REWRITE_PROMPT

@mcp.tool(name="check_news_law",description="Принимает текст новости, анализирует его на соответствие закону о СМИ")
async def check_news_law(news_text: str, ctx: Context) -> str:
    """
    Принимает текст новости, анализирует его на соответствие законодательству
    с использованием OpenAI API и специального промпта, и возвращает результат анализа.
    """
    ctx.info(f"Инструмент 'check_news_law' получил новость для анализа: {news_text[:70]}...")
    
    try:
        analysis_result = await call_openai_for_news_analysis(
            news_text=news_text,
            analysis_prompt=NEWS_ANALYSIS_LEGAL_PROMPT,
            model_name="google/gemini-2.5-flash-preview",
            ctx=ctx
        )
        return analysis_result
    except ValueError as ve: # Ловим ошибку отсутствия API ключа
        return str(ve)
    except Exception as e:
        ctx.error(f"Неожиданная ошибка в инструменте check_news_law: {str(e)}")
        return f"Внутренняя ошибка сервера при анализе новости. {str(e)}"

@mcp.tool(name="spell_checker",description="Принимает текст, проверяет его на орфографию и пунктуацию")
async def spell_checker(text: str, ctx: Context) -> str:
    """
    Принимает текст, проверяет его на орфографию и пунктуацию
    с использованием OpenAI API и специального промпта, и возвращает результат проверки.
    """
    ctx.info(f"Инструмент 'spell_checker' получил текст для проверки: {text[:70]}...")

    try:
        response = await call_openai_for_news_analysis(
            news_text=text,
            analysis_prompt=SPELL_CHECKER_PROMPT,
            model_name="google/gemini-2.5-pro-preview",
            ctx=ctx
        )
        return response
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        ctx.error(f"Неожиданная ошибка в инструменте spell_checker: {str(e)}")
        return f"Внутренняя ошибка сервера при проверке орфографии. {str(e)}"

@mcp.tool(name="rewrite_news",description="Принимает текст новости, переписывает его на более грамотный язык")
async def rewrite_news(news_text: str, count_symbols: str, abz_size: str, ctx: Context) -> str:
    """
    Принимает текст новости, переписывает его на более грамотный язык
    с использованием OpenAI API и специального промпта, и возвращает результат переписывания.
    """
    ctx.info(f"Инструмент 'rewrite_news' получил текст для переписывания: {news_text[:70]}...")

    final_prompt = REWRITE_PROMPT + f"\nОбъем текста: Ориентировочно {count_symbols} знаков.\nДлина абзацев: От {abz_size} примерно."

    try:
        response = await call_openai_for_news_analysis(
            news_text=news_text,
            analysis_prompt=final_prompt,
            model_name="google/gemini-2.5-pro-preview",
            ctx=ctx
        )
        return response
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        ctx.error(f"Неожиданная ошибка в инструменте rewrite_news: {str(e)}")
        return f"Внутренняя ошибка сервера при переписывании новости. {str(e)}"

if __name__ == "__main__":
    mcp.run()
