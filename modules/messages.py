import re
from src import ModuleManager, utils

class Module(ModuleManager.BaseModule):
    @utils.hook("received.command.msearch")
    @utils.spec("!-channelonly !<pattern>string")
    def msearch(self, event):
        print(event["spec"])
        pattern = re.compile(event["spec"][0], re.I)
        message_list = list(event["target"].buffer.find_all(pattern))
        message_count = len(message_list)

        if message_list:
            messages = []
            for i, message in enumerate(message_list):
                seconds = utils.datetime.seconds_since(message.line.timestamp)
                messages.append("(%d/%d) %s ago %s" % (i+1, message_count,
                    utils.datetime.to_pretty_time(seconds),
                    message.line.format()))

            event["stdout"].write("%s: found: %s"
                % (event["user"].nickname, "\n".join(messages)))
        else:
            event["stderr"].write("%s: no messages found"
                % event["user"].nickname)