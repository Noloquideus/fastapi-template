import bcrypt
from src.application.contracts.i_hash_service import IHashService
from src.infrastructure.logger import Logger


class HashService(IHashService):

    def __init__(self, logger: Logger):
        self.__logger = logger

    def hash(self, value: str) -> str:
        hashed_value = bcrypt.hashpw(value.encode(), bcrypt.gensalt())
        self.__logger.info(f'Hash value {hashed_value}')
        return hashed_value.decode()

    def verify(self, hashed_value: str, plain_value: str) -> bool:
        self.__logger.info(f'Hash value {hashed_value}')
        return bcrypt.checkpw(plain_value.encode(), hashed_value.encode())
