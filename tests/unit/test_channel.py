from ssh2net import SSH2NetBase, SSH2NetChannel


def test__rstrip_all_lines():
    test_input = b"""
some line
another line
one final line
    """
    output = SSH2NetChannel._rstrip_all_lines(test_input)
    for line in output.splitlines():
        assert line[-1] != " "


def test__restructure_output():
    test_host = {"setup_host": "my_device  ", "auth_user": "username", "auth_password": "password"}
    conn = SSH2NetBase(**test_host)
    output = "\n\nsomedata\n3560CX#"
    output = conn._restructure_output(output)
    assert output.splitlines()[0] != ""
    assert output.splitlines()[1] != ""


def test__restructure_output_strip_prompt():
    test_host = {"setup_host": "my_device  ", "auth_user": "username", "auth_password": "password"}
    conn = SSH2NetBase(**test_host)
    output = "\n\nsomedata\n3560CX#"
    output = conn._restructure_output(output, strip_prompt=True)
    assert output.splitlines()[0] != ""
    assert output.splitlines()[-1] != "3560CX#"


def test__strip_ansi():
    output = b"[admin@CoolDevice.Sea1: \x1b[1m/\x1b[0;0m]$"
    output = SSH2NetChannel._strip_ansi(output)
    assert output == b"[admin@CoolDevice.Sea1: /]$"
