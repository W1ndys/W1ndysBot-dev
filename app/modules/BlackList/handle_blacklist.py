from .data_manager import BlackListDataManager
from api.message import send_group_msg
from api.generate import generate_text_message, generate_reply_message
import logger
import re
from . import (
    MODULE_NAME,
    BLACKLIST_ADD_COMMAND,
    BLACKLIST_REMOVE_COMMAND,
    BLACKLIST_LIST_COMMAND,
    BLACKLIST_CLEAR_COMMAND,
)


class BlackListHandle:
    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.raw_message = msg.get("raw_message", "")
        self.group_id = msg.get("group_id", "")
        self.user_id = msg.get("user_id", "")

    async def add_blacklist(self):
        """
        添加黑名单
        支持以下格式：
            {command}[CQ:at,qq={user_id}]  # 添加用户到黑名单
            {command}[CQ:at,qq={user_id}] [CQ:at,qq={user_id}] ...  # 添加多个用户到黑名单
            {command}{user_id}  # 添加用户到黑名单
            {command}{user_id} {user_id} ...  # 添加多个用户到黑名单
        """
        try:
            # 删除命令
            self.raw_message = self.raw_message.replace(
                BLACKLIST_ADD_COMMAND, ""
            ).strip()

            # 解析QQ号
            user_ids = []

            # 处理at消息
            at_pattern = r"\[CQ:at,qq=(\d+)\]"
            at_matches = re.findall(at_pattern, self.raw_message)
            if at_matches:
                user_ids.extend(at_matches)
            else:
                # 处理纯QQ号
                qq_numbers = self.raw_message.split()
                for qq in qq_numbers:
                    if qq.isdigit():
                        user_ids.append(qq)

            if not user_ids:
                logger.error(f"[{MODULE_NAME}]未找到有效的QQ号")
                return False

            # 添加黑名单
            success_count = []
            with BlackListDataManager() as data_manager:
                for user_id in user_ids:
                    if data_manager.add_blacklist(self.group_id, user_id):
                        success_count.append(user_id)

            # 发送成功消息
            reply_message = f"已将以下用户添加到黑名单：{', '.join(success_count)}"
            await send_group_msg(
                self.websocket,
                self.group_id,
                [
                    generate_reply_message(reply_message),
                    generate_text_message(reply_message),
                ],
                note="del_msg=10",
            )

            return True
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]添加黑名单失败: {e}")
            return False

    async def remove_blacklist(self):
        """
        移除黑名单
        支持以下格式：
            {command}[CQ:at,qq={user_id}]  # 移除用户的黑名单
            {command}[CQ:at,qq={user_id}] [CQ:at,qq={user_id}] ...  # 移除多个用户的黑名单
            {command}{user_id}  # 移除用户的黑名单
            {command}{user_id} {user_id} ...  # 移除多个用户的黑名单
        """
        try:
            # 删除命令
            self.raw_message = self.raw_message.replace(
                BLACKLIST_REMOVE_COMMAND, ""
            ).strip()

            # 解析QQ号
            user_ids = []

            # 处理at消息
            at_pattern = r"\[CQ:at,qq=(\d+)\]"
            at_matches = re.findall(at_pattern, self.raw_message)
            if at_matches:
                user_ids.extend(at_matches)
            else:
                # 处理纯QQ号
                qq_numbers = self.raw_message.split()
                for qq in qq_numbers:
                    if qq.isdigit():
                        user_ids.append(qq)

            if not user_ids:
                logger.error(f"[{MODULE_NAME}]未找到有效的QQ号")
                return False

            # 移除黑名单
            success_count = []
            with BlackListDataManager() as data_manager:
                for user_id in user_ids:
                    if data_manager.remove_blacklist(self.group_id, user_id):
                        success_count.append(user_id)

            # 发送成功消息
            reply_message = f"已将以下用户从黑名单中移除：{', '.join(success_count)}"
            await send_group_msg(
                self.websocket,
                self.group_id,
                [
                    generate_reply_message(reply_message),
                    generate_text_message(reply_message),
                ],
                note="del_msg=10",
            )

            return True
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]移除黑名单失败: {e}")
            return False

    async def list_blacklist(self):
        """
        查看黑名单
        列出当前群组的所有黑名单用户
        """
        try:
            with BlackListDataManager() as data_manager:
                blacklist = data_manager.get_group_blacklist(self.group_id)

            if not blacklist:
                reply_message = "当前群组没有黑名单用户"
            else:
                blacklist_users = []
                for user_id, created_at in blacklist:
                    blacklist_users.append(f"{user_id}（添加时间：{created_at}）")

                reply_message = (
                    f"当前群组的黑名单用户（共{len(blacklist)}人）：\n"
                    + "\n".join(blacklist_users)
                )

            await send_group_msg(
                self.websocket,
                self.group_id,
                [
                    generate_reply_message(reply_message),
                    generate_text_message(reply_message),
                ],
                note="del_msg=10",
            )

            return True
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]查看黑名单失败: {e}")
            return False

    async def clear_blacklist(self):
        """
        清空黑名单
        清空当前群组的所有黑名单用户
        """
        try:
            # 获取当前群组的黑名单
            with BlackListDataManager() as data_manager:
                blacklist = data_manager.get_group_blacklist(self.group_id)

            if not blacklist:
                reply_message = "当前群组没有黑名单用户"
                await send_group_msg(
                    self.websocket,
                    self.group_id,
                    [
                        generate_reply_message(reply_message),
                        generate_text_message(reply_message),
                    ],
                    note="del_msg=10",
                )
                return True

            # 移除所有黑名单
            for user_id, _ in blacklist:
                with BlackListDataManager() as data_manager:
                    data_manager.remove_blacklist(self.group_id, user_id)

            reply_message = f"已清空当前群组的所有黑名单用户（共{len(blacklist)}人）"
            await send_group_msg(
                self.websocket,
                self.group_id,
                [
                    generate_reply_message(reply_message),
                    generate_text_message(reply_message),
                ],
                note="del_msg=10",
            )

            return True
        except Exception as e:
            logger.error(f"[{MODULE_NAME}]清空黑名单失败: {e}")
            return False
