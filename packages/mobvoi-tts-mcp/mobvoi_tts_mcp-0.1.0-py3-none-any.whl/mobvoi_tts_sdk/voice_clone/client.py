import os, sys
import typing
import httpx
import json
import time
import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VoiceCloneClient:
    def __init__(self, *, app_key: str, app_secret: str, voice_clone_client: typing.Union[httpx.Client, httpx.AsyncClient]):
        self._client = voice_clone_client
        self._timestamp = str(int(time.time()))
        self._app_key = app_key
        self._app_secret = app_secret
        message = '+'.join([self._app_key, self._app_secret, self._timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        self._signature = m.hexdigest()
        
    def clone_url(self, *, wav_uri: str):
        print("wav_uri:", wav_uri)
        request_data = {
            'appKey': self._app_key,
            'signature': self._signature,
            'timestamp': self._timestamp,
            'wavUri': wav_uri,
        }
        try:
            _response = self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            print(f"Error: {e}")
    
    async def async_clone_url(self, *, wav_uri: str):
        print("wav_uri:", wav_uri)
        request_data = {
            'appKey': self._app_key,
            'signature': self._signature,
            'timestamp': self._timestamp,
            'wavUri': wav_uri,
        }
        try:
            _response = await self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
    
    def clone_local(self, *, audio_file_path: str):
        print("audio_file_path:", audio_file_path)
        request_data = {
            'appKey': self._app_key,
            'signature': self._signature,
            'timestamp': self._timestamp,
        }
        files = {
            'file': open(audio_file_path, 'rb')
        }
        try:
            _response = self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data,
                files=files
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
            return None
            
    async def async_clone_local(self, *, audio_file_path: str):
        print("audio_file_path:", audio_file_path)
        request_data = {
            'appKey': self._app_key,
            'signature': self._signature,
            'timestamp': self._timestamp,
        }
        files = {
            'file': open(audio_file_path, 'rb')
        }
        try:
            _response = await self._client.request(
                method="POST",
                url="https://open.mobvoi.com/clone",
                data=request_data,
                files=files
            )
            if _response.json()['code'] == 0:
                print("clone success")
                # print("speaker:", _response.json()['speaker'])
                return _response.json()['speaker']
            else:
                raise Exception(_response.json()['error'])
        except Exception as e:
            # print(f"Error: {e}")
            logger.exception(f"Error: {e}")
            return None