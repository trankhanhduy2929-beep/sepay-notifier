import logging
from datetime import datetime
from homeassistant.components import webhook
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

_LOGGER = logging.getLogger(__name__)
DOMAIN = "sepay"
SIG_RECV = "sepay_data_update"

async def async_setup(hass: HomeAssistant, config: dict):
    """Thiết lập component (không dùng đến trong UI flow)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Thiết lập SePay khi người dùng cài đặt qua UI."""
    hass.data.setdefault(DOMAIN, {})
    
    # Lấy thông số cấu hình
    config = {**entry.data, **entry.options}
    webhook_id = config.get("webhook_id")
    
    # Lưu webhook_id vào hass.data để gỡ bỏ an toàn khi reload
    hass.data[DOMAIN][entry.entry_id] = webhook_id

    async def handle_webhook(hass, webhook_id, request):
        try:
            data = await request.json()
            async_dispatcher_send(hass, SIG_RECV, data)

            current_config = {**entry.data, **entry.options}
            amount = data.get("transferAmount", 0)
            content = data.get("content", "").lower()
            
            if amount > 0 and data.get("transferType") == "in":
                # 1. Kiểm tra Bộ lọc từ khóa
                keyword = current_config.get("keyword_filter", "").lower()
                if keyword and keyword not in content:
                    _LOGGER.info("SePay: Bỏ qua loa vì nội dung không chứa từ khóa")
                    return

                # 2. Kiểm tra Chế độ yên tĩnh
                now = datetime.now().hour
                start_q = current_config.get("quiet_start", 23)
                end_q = current_config.get("quiet_end", 6)
                
                is_quiet = False
                if start_q > end_q:
                    if now >= start_q or now < end_q: is_quiet = True
                else:
                    if start_q <= now < end_q: is_quiet = True
                
                if is_quiet:
                    _LOGGER.info("SePay: Đang giờ yên tĩnh, không phát loa")
                    return

                # 3. Thực hiện phát loa
                amount_str = "{:,}".format(int(amount)).replace(",", ".")
                message = f"Bạn vừa nhận được {amount_str} đồng."
                
                await hass.services.async_call(
                    "tts", "speak",
                    {
                        "media_player_entity_id": [current_config.get("media_player")],
                        "message": message,
                        "language": current_config.get("language", "vi-VN"),
                        "cache": True,
                        "options": {
                            "voice": current_config.get("voice", "vi-VN-HoaiMyNeural"),
                            "rate": current_config.get("rate", "+0%"),
                            "volume": current_config.get("volume", "+10%"),
                        }
                    },
                    target={"entity_id": current_config.get("tts_entity", "tts.edge_tts")}
                )
        except Exception as e:
            _LOGGER.error("Lỗi SePay Webhook handle: %s", str(e))

    # Đăng ký webhook
    webhook.async_register(hass, DOMAIN, "SePay Webhook", webhook_id, handle_webhook)
    
    # Load các sensor
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    # Lắng nghe sự kiện thay đổi cấu hình
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload integration khi cấu hình thay đổi."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Gỡ bỏ integration sạch sẽ."""
    # Gỡ bỏ webhook sử dụng ID đã lưu trước đó
    webhook_id = hass.data[DOMAIN].pop(entry.entry_id, None)
    if webhook_id:
        try:
            webhook.async_unregister(hass, webhook_id)
        except Exception as e:
            _LOGGER.warning("Không thể gỡ bỏ webhook %s: %s", webhook_id, e)

    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
