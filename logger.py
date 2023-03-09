import logging

logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
