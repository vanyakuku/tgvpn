# vpn_manager.py — менеджер, работающий со всеми серверами
from vpn_api import ThreeXUI
from servers_config import SERVERS


class VPNManager:
    """Управляет всеми серверами через единый интерфейс"""

    async def create_subscription(self, server_code: str, 
                                   telegram_id: int, 
                                   expire_days: int, 
                                   traffic_gb: int) -> str:
        """
        Создаёт подписку на выбранном сервере.
        Возвращает vless:// ссылку.
        """
        server = SERVERS[server_code]
        email = f"tg_{telegram_id}"

        async with ThreeXUI(
            api_url=server["api_url"],
            username=server["username"],
            password=server["password"]
        ) as api:
            await api.login()
            inbounds = await api.get_inbounds()
            vless_inbound = next(ib for ib in inbounds if ib["protocol"] == "vless")

            client = await api.add_client(
                inbound_id=vless_inbound["id"],
                email=email,
                expire_days=expire_days,
                traffic_gb=traffic_gb
            )

            link = await api.build_vless_link(
                client_uuid=client["uuid"],
                email=email,
                inbound=vless_inbound
            )
            return link, server["name"]
