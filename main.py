import asyncio
import logging

from chain import process_text

SAMPLE_TEXT = """
La API de pagos está montada en FastAPI detrás de un load balancer.
Usa Redis para caché de sesiones y PostgreSQL como base principal.
Bajo carga concurrente las conexiones a la DB se saturan y aparecen timeouts 504.
"""


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    result = await process_text(SAMPLE_TEXT)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
