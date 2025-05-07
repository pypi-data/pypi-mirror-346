import logging
import time
import asyncio
import aiohttp
import gc
import os
import sys
import re
from typing import Optional, List, Callable, Dict, Any

from yandex_aiobot_py.bot_types import User, Message, Chat, Button, Poll, File, Image
import yandex_aiobot_py.apihelpers as api
from yandex_aiobot_py.handlers import MemoryStepHandler

logger = logging.getLogger(__name__)


class Client:
    def __init__(
        self,
        api_key: str,
        exclude_channels: Optional[List[str]] = None,
        ssl_verify: bool = True,
        timeout: int = 1,
        bot_inactivity_timeout: int = 300,
    ):
        if not isinstance(bot_inactivity_timeout, int):
            raise ValueError("bot_inactivity_timeout должен быть целым числом")
        self.api_key = api_key
        self.handlers: List[dict] = []
        self.next_step_handler: MemoryStepHandler = MemoryStepHandler()  # Указан тип
        self.unhandled_message_handler: Callable = self._unhandled_message_handler
        self.is_closed = False
        self.last_update_id = 0
        self.ssl_verify = ssl_verify
        self.timeout = timeout
        self.exclude_channels = exclude_channels or []
        self._session: Optional[aiohttp.ClientSession] = None
        self.is_bot_alive = True
        self.last_activity_time = time.time()
        self.bot_inactivity_timeout = bot_inactivity_timeout
        self.lock = asyncio.Lock()

    async def start_session(self):
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close_session(self):
        if self._session and not self._session.closed:
            await self._session.close()

    @staticmethod
    def _build_handler_dict_old(handler: Callable, phrase: str) -> dict:
        return {"function": handler, "phrase": phrase}

    @staticmethod
    def _build_handler_dict(
            handler: Callable, phrase: str, chat_type: str = None
    ):
        if not callable(handler):
            raise ValueError("handler должен быть вызываемым")
        if not isinstance(phrase, str):
            raise ValueError("phrase должен быть строкой")
        if chat_type is not None and not isinstance(chat_type, str):
            raise ValueError("chat_type должен быть строкой")
        return {"phrase": phrase, "function": handler, "chat_type": chat_type}

    async def run(self):
        logger.info("Bot initialized. Start polling...")
        await self.start_session()
        polling_task = asyncio.create_task(self._start_polling())
        watchdog_task = asyncio.create_task(self.keep_bot_alive())
        await asyncio.gather(polling_task, watchdog_task)

    async def run_async(self):
        logger.info("Bot initialized. Start polling...")
        await self.start_session()
        polling_task = asyncio.create_task(self._start_polling())
        watchdog_task = asyncio.create_task(self.keep_bot_alive())
        await asyncio.gather(polling_task, watchdog_task)

    @staticmethod
    def _unhandled_message_handler(message: Message):
        logger.warning(f"Unhandled message: {message.text}")

    def _is_closed(self) -> bool:
        return self.is_closed

    @staticmethod
    def _get_message_objects(message_json: Dict[str, Any]) -> Message:
        images: List[Image] = []
        file: Optional[File] = None

        image_groups = message_json.get("images")
        if image_groups:
            for image_group in image_groups:
                for image_data in image_group:
                    try:
                        image = Image(**image_data)
                        images.append(image)
                    except TypeError as e:
                        logger.warning(
                            f"Failed to create Image object: {e}, data: {image_data}"
                        )

        file_data = message_json.get("file")
        if file_data:
            try:
                file = File(**file_data)
            except TypeError as e:
                logger.warning(f"Failed to create File object: {e}, data: {file_data}")

        user = User(**message_json["from"])

        chat_data = message_json.get("chat")
        if chat_data:
            chat_data = dict(chat_data)
            chat_data.pop("type", None)
            if "id" in chat_data:
                chat_data["chat_id"] = chat_data.pop("id")
            chat = Chat(**chat_data)
        else:
            chat = None

        message_json = dict(message_json)
        message_json.pop("chat", None)
        if not message_json.get("text"):
            message_json["text"] = ""

        message = Message(
            **message_json,
            user=user,
            chat=chat,
            pictures=images,
            attachment=file,
        )
        return message

    @staticmethod
    async def _run_handler(handler: Callable, message: Message):
        if not callable(handler):
            raise ValueError("handler должен быть вызываемым")
        if not isinstance(message, Message):
            raise ValueError("message должен быть объектом Message")
        logger.debug(f"Running handler: {handler} with message: {message}")
        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(message)
            else:
                result = handler(message)
            logger.debug(f"Handler returned: {result}")
        except Exception as e_rh:
            logger.exception(f"Error executing handler: {handler} {e_rh}")

    async def keep_bot_alive(self):
        while True:
            try:
                current_time = time.time()
                async with self.lock:
                    is_bot_alive = self.is_bot_alive
                    last_activity_time = self.last_activity_time

                if not is_bot_alive or (
                    current_time - last_activity_time > self.bot_inactivity_timeout
                ):
                    logger.warning(
                        "Bot is not responding for %.0f seconds, restarting...",
                        current_time - last_activity_time,
                    )
                    gc.collect()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                await asyncio.sleep(self.bot_inactivity_timeout // 2)
            except Exception as e_kba:
                logger.error(f"Error in keep_bot_alive: {e_kba}")
                await asyncio.sleep(10)

    async def _get_updates(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        last_update_id: int = 0,
    ):
        if session is not None and not isinstance(session, aiohttp.ClientSession):
            raise ValueError("session должен быть объектом aiohttp.ClientSession")
        if not isinstance(last_update_id, int):
            raise ValueError("last_update_id должен быть целым числом")
        try:
            data = await api.get_updates(
                self, self.last_update_id + 1, session=self._session
            )
            # if data:
            async with self.lock:
                self.is_bot_alive = True
                self.last_activity_time = time.time()
            logger.debug(f"Received updates: {data}")
            for json_message in data:
                self.last_update_id = json_message["update_id"]
                chat = json_message.get("chat")
                if (
                    chat
                    and chat.get("type") == "channel"
                    and chat.get("id") in self.exclude_channels
                ):
                    continue
                handler = await self._get_handler_for_message(json_message)
                message = self._get_message_objects(json_message)
                await self._run_handler(handler, message)
        except Exception as e_gu:
            async with self.lock:
                self.is_bot_alive = False
            logger.exception(f"Error during get_updates: {e_gu}")
            return

    async def _get_handler_for_message(self, json_message: Dict[str, Any]) -> Callable:
        if not isinstance(json_message, dict):
            raise ValueError("json_message должен быть словарем")
        next_step_handlers = self.next_step_handler.get_all_handlers()
        user_login = json_message["from"]["login"]

        if next_step_handlers and user_login in next_step_handlers:
            handler = next_step_handlers[user_login]
            self.next_step_handler.delete_handler(user_login)
            return handler

        text = json_message.get("text", "")
        callback_data = json_message.get("callback_data")
        first_word = (
            callback_data.get("phrase")
            if callback_data and callback_data.get("phrase")
            else text.split(" ")[0]
        )

        chat_type = json_message["chat"]["type"]

        for handler_info in self.handlers:
            phrase = handler_info["phrase"]
            handler_func = handler_info["function"]
            handler_chat_type = handler_info.get("chat_type")

            if (handler_chat_type is None or handler_chat_type == chat_type) and (
                phrase == first_word or re.search(phrase, first_word)
            ):
                logger.debug(f"Selected handler: {handler_func}")
                return handler_func

        logger.debug(f"Selected handler: {self.unhandled_message_handler}")
        return self.unhandled_message_handler

    async def _get_handler_for_message_old(
        self, json_message: Dict[str, Any]
    ) -> Callable:
        next_step_handlers = self.next_step_handler.get_all_handlers()
        user_login = json_message["from"]["login"]

        if next_step_handlers and user_login in next_step_handlers:
            handler = next_step_handlers[user_login]
            self.next_step_handler.delete_handler(user_login)
            return handler

        text = json_message.get("text", "")
        callback_data = json_message.get("callback_data")
        first_word = (
            callback_data.get("phrase")
            if callback_data and callback_data.get("phrase")
            else text.split(" ")[0]
        )

        if not first_word:
            logger.debug(f"Selected handler: {self.unhandled_message_handler}")
            return self.unhandled_message_handler

        for handler_info in self.handlers:
            phrase = handler_info["phrase"]
            handler_func = handler_info["function"]
            if phrase == first_word or re.search(phrase, first_word):
                logger.debug(f"Selected handler: {handler_func}")
                return handler_func

        logger.debug(f"Selected handler: {self.unhandled_message_handler}")
        return self.unhandled_message_handler

    async def _start_polling(self):
        try:
            while not self._is_closed():
                try:
                    await self._get_updates()
                    await asyncio.sleep(self.timeout)
                except Exception as e_sp:
                    logger.exception(f"Polling error: {e_sp}")
                    await asyncio.sleep(5)
        except asyncio.CancelledError:
            logger.info("Polling cancelled")
            self.is_closed = True
        except KeyboardInterrupt:
            logger.info("Exit Bot. Good bye.")
            self.is_closed = True

    def register_next_step_handler(self, user_login: str, callback: Callable):
        self.next_step_handler.register_handler(user_login, callback)

    def on_message_old(self, phrase: str):
        def decorator(handler: Callable):
            self.handlers.append(self._build_handler_dict(handler, phrase))
            return handler

        return decorator

    def on_message(self, phrase: str, chat_type: str = None):
        if not isinstance(phrase, str):
            raise ValueError("phrase должен быть строкой")
        if chat_type is not None and not isinstance(chat_type, str):
            raise ValueError("chat_type должен быть строкой")

        def decorator(handler: Callable):
            self.handlers.append(self._build_handler_dict(handler, phrase, chat_type))
            return handler

        return decorator

    def unhandled_message(self):
        def decorator(handler: Callable):
            self.unhandled_message_handler = handler
            return handler

        return decorator

    async def send_message(
        self,
        text: str,
        login: str = "",
        chat_id: str = "",
        reply_message_id: int = 0,
        disable_notification: bool = False,
        important: bool = False,
        disable_web_page_preview: bool = False,
        inline_keyboard: Optional[List[Button]] = None,
    ) -> int:
        """
        Отправляет текстовое сообщение с возможностью добавления inline-кнопок

        :param text: Текст сообщения
        :param login: Логин пользователя (альтернатива chat_id)
        :param chat_id: ID чата (альтернатива login)
        :param reply_message_id: ID сообщения для ответа
        :param disable_notification: отключить уведомление
        :param important: пометить как важное
        :param disable_web_page_preview: отключить превью ссылок
        :param inline_keyboard: Список кнопок Button
        :return: ID отправленного сообщения
        """
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")

        # Преобразуем кнопки в словари
        inline_keyboard_data = []
        if inline_keyboard:
            inline_keyboard_data = [btn.to_dict() for btn in inline_keyboard]

        data = await api.send_message(
            self,
            text,
            login=login,
            chat_id=chat_id,
            reply_message_id=reply_message_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
            inline_keyboard=inline_keyboard_data,
        )
        return data

    async def create_poll(
        self,
        poll: Poll,
        login: Optional[str] = None,
        chat_id: Optional[str] = None,
        disable_notification: bool = False,
        important: bool = False,
        disable_web_page_preview: bool = False,
    ) -> int:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        data = await api.create_poll(
            self,
            poll,
            login=login,
            chat_id=chat_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
        )
        return data

    async def get_poll_results(
        self,
        message_id: int,
        chat_id: Optional[str] = None,
        login: Optional[str] = None,
        invite_hash: Optional[str] = None,
    ) -> dict:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        data = await api.get_poll_results(
            self,
            message_id,
            chat_id=chat_id or "",
            login=login or "",
            invite_hash=invite_hash or "",
        )
        return data

    async def get_poll_voters(
        self,
        message_id: int,
        answer_id: int,
        login: Optional[str] = None,
        chat_id: Optional[str] = None,
        invite_hash: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[int] = None,
    ) -> dict:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        data = await api.get_poll_voters(
            self,
            message_id,
            answer_id,
            login=login,
            chat_id=chat_id,
            invite_hash=invite_hash,
            limit=limit,
            cursor=cursor,
        )
        return data

    async def create_chat(self, chat: Chat, is_channel: bool = False) -> int:
        data = await api.chat_create(self, chat, is_channel=is_channel)
        return data

    async def change_chat_users(
        self,
        chat_id: str,
        members: Optional[List[User]] = None,
        admins: Optional[List[User]] = None,
        subscribers: Optional[List[User]] = None,
        remove: Optional[List[User]] = None,
    ):
        data: Dict[str, Any] = {"chat_id": chat_id}
        if members:
            data["members"] = [{"login": user.login} for user in members]
        if admins:
            data["admins"] = [{"login": user.login} for user in admins]
        if subscribers:
            data["subscribers"] = [{"login": user.login} for user in subscribers]
        if remove:
            data["remove"] = [{"login": user.login} for user in remove]
        data = await api.change_chat_users(self, data)
        return data

    async def delete_message(
        self, message_id: int, login: str = "", chat_id: str = ""
    ) -> int:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        data = await api.delete_message(self, message_id, login=login, chat_id=chat_id)
        return data

    async def get_user_link(self, login: str) -> dict:
        data = await api.get_user_link(self, login=login)
        return data

    async def send_file(self, path: str, login: str = "", chat_id: str = "") -> dict:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        try:
            data = await api.send_file(
                self, document=path, login=login, chat_id=chat_id
            )
            return data
        except Exception as e_sf:
            logger.error(f"Error sending file: {e_sf}")
            return {}

    async def send_image(self, path: str, login: str = "", chat_id: str = "") -> dict:
        if not chat_id and not login:
            raise ValueError("Please provide login or chat_id")
        if chat_id and login:
            raise ValueError("Provide either chat_id or login, not both.")
        try:
            data = await api.send_image(self, image=path, login=login, chat_id=chat_id)
            return data
        except Exception as e_si:
            logger.error(f"Error sending image: {e_si}")
            return {}
