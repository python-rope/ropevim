import ropemode.decorators
import ropemode.environment
import ropemode.interface
import vim

from ._rope_omni_completer import get_omni_completer
from ._value_completer import get_value_completer
from ._vim_environment import VimEnvironment


def load_ropevim():
    python_cmd = "python3"
    completer = get_value_completer(python_cmd)
    env = VimEnvironment(completer, python_cmd)
    env.load_variables()
    env.load_shortcuts()
    env.load_menu()
    ropemode.decorators.logger.message = env.message
    ropemode.decorators.logger.only_short = True
    interface = ropemode.interface.RopeMode(env=env)
    interface.init()

    _ = get_omni_completer(
        ropemode.interface._CodeAssist(interface, env), env, python_cmd
    )
