from pathlib import Path
import re

import pytest

from tests.functional.base_functional_tests import BaseFunctionalTest
import ssh2net

TEST_DEVICE = {"setup_host": "172.18.0.12", "auth_user": "vrnetlab", "auth_password": "VR-netlab9"}

dummy_conn = ssh2net.NXOSDriver(**TEST_DEVICE)
PRIV_LEVELS = dummy_conn.privs
# remove exec priv level as it is not configured on the vrnetlab host for testing
PRIV_LEVELS.pop("exec")


class TestNXOS(BaseFunctionalTest):
    def setup_method(self):
        self.platform_driver = ssh2net.NXOSDriver

        self.device_type = Path(__file__).resolve().parts[-2]
        self.func_test_dir = (
            f"{Path(ssh2net.__file__).parents[1]}/tests/functional/{self.device_type}/"
        )
        self.test_device = TEST_DEVICE
        self.disable_paging_ext_function = f"tests.functional.{self.device_type}.ext_test_funcs.{self.device_type.split('_')[1]}_disable_paging"

    @staticmethod
    def _replace_trailing_chars_running_config(input_data):
        execute_trailing_chars_pattern = re.compile(r"^line vty.*$", flags=re.M | re.I | re.S)
        input_data = re.sub(execute_trailing_chars_pattern, "line vty", input_data)
        return input_data

    @staticmethod
    def _replace_timestamps(input_data):
        datetime_pattern = re.compile(
            r"(mon|tue|wed|thu|fri|sat|sun)\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d+\s+\d+:\d+:\d+\s\d+",
            flags=re.M | re.I,
        )
        input_data = re.sub(datetime_pattern, "TIME_STAMP_REPLACED", input_data)
        return input_data

    @staticmethod
    def _replace_crypto_strings(input_data):
        crypto_pattern = re.compile(r"^(.*?\s(?:5|md5)\s)[\w$\.\/]+.*$", flags=re.M | re.I)
        input_data = re.sub(crypto_pattern, "CRYPTO_REPLACED", input_data)
        return input_data

    def disable_paging(self, cls):
        cls.send_inputs("term length 0")

    @pytest.mark.parametrize("setup_use_paramiko", [False, True], ids=["ssh2", "paramiko"])
    def test_send_inputs_interact(self, setup_use_paramiko):
        """
        expected output for this test is somewhat massaged to make this test pass
        in "real" device ssh session there aren't new lines between response and the prompt
        there is also a space after the prompt and before the "n"
        given that this is just for interactive "solving" these problems is not worth the effort
        """
        interact = ["delete bootflash:virtual-instance.conf", "(yes/no/abort)   [y]", "n"]
        super().test_send_inputs_interact(setup_use_paramiko, interact)

    @pytest.mark.parametrize("setup_use_paramiko", [False, True], ids=["ssh2", "paramiko"])
    @pytest.mark.parametrize("priv_level", [priv for priv in PRIV_LEVELS.values()])
    def test_acquire_all_priv_levels(self, setup_use_paramiko, priv_level):
        super().test_acquire_all_priv_levels(setup_use_paramiko, priv_level)

    @pytest.mark.parametrize("setup_use_paramiko", [False, True], ids=["ssh2", "paramiko"])
    def test__determine_current_priv_special_configuration(self, setup_use_paramiko):
        with self.platform_driver(
            **self.test_device, setup_use_paramiko=setup_use_paramiko
        ) as conn:
            conn.send_inputs(["configure terminal", "interface Ethernet1/128"])
            current_prompt = conn.get_prompt()
            current_priv = conn._determine_current_priv(current_prompt)
        assert current_priv.name == "special_configuration"
