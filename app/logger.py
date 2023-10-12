import logging

logging.basicConfig(
    level=logging.INFO,
    filename="questions.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("bewise-question")
