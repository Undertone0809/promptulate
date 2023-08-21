import requests
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel

from promptulate import utils
from promptulate.utils import get_logger


logger = get_logger()


class ErnieTokenPool(BaseModel):
    @staticmethod
    def _get_access_token(key: str, secret: str) -> str:
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": key,
            "client_secret": secret,
        }
        return str(requests.post(url, params=params).json().get("access_token"))

    def get_token(self) -> str:
        return utils.get_cache()["ERNIE_TOKEN"]

    def _task(self, key: str, secret: str):
        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        logger.debug(f"[pne update token %Y-%m-%d %H:%M:%S] {ts}")
        utils.get_cache()["ERNIE_TOKEN"] = self._get_access_token(key, secret)

    def nocache_get_token(self, key: str, secret: str) -> str:
        return self._get_access_token(key, secret)

    def start(self, key: str, secret: str):
        schemed = BackgroundScheduler(timezone="MST")
        self._task(key, secret)
        schemed.add_job(
            self._task, "interval", id="token_job", seconds=3600, args=(key, secret)
        )
        schemed.start()
