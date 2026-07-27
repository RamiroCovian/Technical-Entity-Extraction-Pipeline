import logging

from langchain_core.prompts import ChatPromptTemplate

from model.factory import get_chat_model
from schemas import ExtraccionTecnica

logger = logging.getLogger(__name__)

FORMAT_INSTRUCTIONS = """
Respondé estrictamente con estos campos:
- tecnologias: lista de strings con las tecnologías detectadas (mínimo 1)
- nivel_de_criticidad: uno de: baja, media, alta
- resumen_tecnico: resumen técnico breve del texto
""".strip()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un asistente especializado en extracción de entidades técnicas. "
            "Analizá el texto del usuario y extraé la información solicitada.\n\n"
            "Instrucciones de formato:\n{format_instructions}",
        ),
        ("human", "{text}"),
    ]
).partial(format_instructions=FORMAT_INSTRUCTIONS)

model = get_chat_model()

# Cadena LCEL: Prompt + LLM con salida estructurada + reintentos
chain = (
    prompt | model.with_structured_output(ExtraccionTecnica)
).with_retry(stop_after_attempt=3)


async def process_text(text: str) -> ExtraccionTecnica:
    """Ejecuta el pipeline de extracción de forma asíncrona."""
    if not text or not text.strip():
        raise ValueError("El texto de entrada no puede estar vacío")

    logger.info("Iniciando extracción técnica (%s caracteres)", len(text))

    try:
        result = await chain.ainvoke({"text": text})
        logger.info(
            "Extracción validada: tecnologias=%s criticidad=%s",
            result.tecnologias,
            result.nivel_de_criticidad,
        )
        return result
    except Exception:
        logger.exception("Falló la extracción tras reintentos")
        raise
