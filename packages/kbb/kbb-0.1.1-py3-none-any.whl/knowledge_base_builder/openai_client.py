import asyncio
import time
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from knowledge_base_builder.llm_client import LLMClient

class OpenAIClient(LLMClient):
    """Asynchronous client for OpenAI's models via LangChain."""
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_retries: int = 3,
        max_concurrency: int = 8,
    ):
        super().__init__(api_key, model, temperature, max_retries, max_concurrency)
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
        )

    async def run_async(self, prompt: str) -> str:
        """
        Send prompt to OpenAI and return the response.
        Uses retries + exponential backoff.
        """
        start_time = time.time()
        for attempt in range(1, self.max_retries + 1):
            try:
                async with self._sem:
                    result = await self.llm.ainvoke([HumanMessage(content=prompt)])
                    end_time = time.time()
                    print(f"    ⏱️ OpenAI API call: {end_time - start_time:.2f} seconds")
                    return result.content if hasattr(result, "content") else result
            except Exception as e:
                if attempt == self.max_retries:
                    end_time = time.time()
                    print(f"    ⏱️ OpenAI API call failed after {end_time - start_time:.2f} seconds and {attempt} attempts")
                    raise
                # backoff: 2, 4, 8, ...
                backoff_time = 2 ** attempt
                print(f"    ⚠️ OpenAI API call attempt {attempt} failed, retrying in {backoff_time} seconds...")
                await asyncio.sleep(backoff_time) 