import logging

logging.basicConfig(
    filename="logs.log",
    filemode="w",
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
