from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from homeassistant.helpers import selector

DOMAIN = "sepay"

class SepayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="SePay Notifier", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("webhook_id", default="sepay_webhook_id"): str,
                vol.Required("tts_entity", default="tts.edge_tts"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="tts")
                ),
                vol.Required("media_player"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="media_player")
                ),
                vol.Optional("keep_days", default=7): int,
                vol.Optional("keyword_filter", default=""): str,
                vol.Optional("quiet_start", default=23): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=23, mode="box")),
                vol.Optional("quiet_end", default=6): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=23, mode="box")),
                vol.Optional("language", default="vi-VN"): str,
                vol.Optional("voice", default="vi-VN-HoaiMyNeural"): str,
                vol.Optional("rate", default="+0%"): str,
                vol.Optional("volume", default="+10%"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SepayOptionsFlowHandler()

class SepayOptionsFlowHandler(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        opt = self.config_entry.options
        dat = self.config_entry.data
        def g(k, d=""): return opt.get(k, dat.get(k, d))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("tts_entity", default=g("tts_entity", "tts.edge_tts")): selector.EntitySelector(selector.EntitySelectorConfig(domain="tts")),
                vol.Required("media_player", default=g("media_player")): selector.EntitySelector(selector.EntitySelectorConfig(domain="media_player")),
                vol.Optional("keyword_filter", default=g("keyword_filter", "")): str,
                vol.Optional("quiet_start", default=g("quiet_start", 23)): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=23, mode="box")),
                vol.Optional("quiet_end", default=g("quiet_end", 6)): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=23, mode="box")),
                vol.Optional("keep_days", default=g("keep_days", 7)): int,
                vol.Optional("voice", default=g("voice", "vi-VN-HoaiMyNeural")): str,
                vol.Optional("rate", default=g("rate", "+0%")): str,
                vol.Optional("volume", default=g("volume", "+10%")): str,
            })
        )
