from typing import Tuple


def get_host_port(args={}):
    if args.get("host") and args.get("port"):
        return args.get("host"), args.get("port")
    host, port = get_server_settings(args=args)
    args["host"] = host
    args["port"] = int(port)
    return host, port


def get_server_settings(args={}) -> Tuple[str, int]:
    from ..lib.system import get_system_conf
    import platform
    from ..lib.exceptions import SetupError
    from .consts import default_gui_port
    from .consts import default_gui_port_ssl

    sysconf = get_system_conf()
    if not sysconf:
        raise SetupError()
    pl = platform.platform()
    if pl.startswith("Windows"):
        def_host = "localhost"
    elif pl.startswith("Linux"):
        if "Microsoft" in pl:
            def_host = "localhost"
        else:
            def_host = "0.0.0.0"
    elif pl.startswith("Darwin"):
        def_host = "0.0.0.0"
    else:
        def_host = "localhost"
    if args.get("ssl_enabled", False):
        if "gui_host_ssl" in sysconf:
            host = sysconf["gui_host_ssl"]
        elif "gui_host" in sysconf:
            host = sysconf["gui_host"]
        else:
            host = def_host
        if "gui_port_ssl" in sysconf:
            port = sysconf["gui_port_ssl"]
        elif "gui_port" in sysconf:
            port = sysconf["gui_port"]
        else:
            port = default_gui_port_ssl
    else:
        host = get_system_conf().get("gui_host", def_host)
        port = get_system_conf().get("gui_port", default_gui_port)
    return host, port


def get_log_path(log_dir=None):
    from pathlib import Path
    from ..lib.system import get_log_dir
    from ..gui.consts import LOG_FN

    if not log_dir:
        log_dir = get_log_dir()
    if not log_dir:
        return None
    log_path = Path(log_dir) / LOG_FN
    return str(log_path)

def get_email_from_oakvar_token(token):
    import jwt
    from .consts import DEFAULT_PRIVATE_KEY

    data = jwt.decode(token, DEFAULT_PRIVATE_KEY, ["HS256"])
    email = data.get("email")
    return email

def get_token(request):
    from .consts import COOKIE_KEY
    return request.cookies.get(COOKIE_KEY)

def get_email_from_request(request, servermode):
    from ..lib.system.consts import DEFAULT_SERVER_DEFAULT_USERNAME
    from .util import get_email_from_oakvar_token
    from .util import get_token

    if not servermode:
        return DEFAULT_SERVER_DEFAULT_USERNAME
    token = get_token(request)
    if token:
        email = get_email_from_oakvar_token(token)
    else:
        email = None
    return email

async def is_loggedin(request, servermode):
    if not servermode:
        return True
    email = get_email_from_request(request, servermode)
    if email:
        return True
    else:
        return False

def copy_state(value):
    from multiprocessing.managers import ListProxy
    from multiprocessing.managers import DictProxy
    if isinstance(value, ListProxy):
        content = []
        for v in value:
            v2 = copy_state(v)
            content.append(v2)
    elif isinstance(value, DictProxy):
        content = {}
        for k, v in value.items():
            v2 = copy_state(v)
            content[k] = v2
    else:
        content = value
    return content

