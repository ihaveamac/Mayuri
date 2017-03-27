# Mayuri Messages Configuration

# To edit messages related to logs, edit logs.py.
# Leave any of the messages blank to disable them.
# Messages can share these variables:
#   General
#   * {username}                 - name of user who has joined
#   * {username_mention}         - name of user who has joined in mention
#                                  format (e.g. @user)
#   * {server_name}              - server name
#   * {welcome_channel}          - welcome channel in channels.py
#   * {welcome_channel_mention}  - welcome channel in channels.py in mention
#                                  format (channel link will be clickable)
#   Commands
#   * {command}                  - command used
#   * {command_prefixed}         - command used with prefix
#   * {prefix}                   - command prefix used

# Welcome message
# This message is sent to every user that joins the server. This can be enabled
#   with the next option.
# This message can be tested by using the welcometest command in a channel.
WELCOME_MESSAGE = """
Hello {username}, and welcome to {server_name}! Be sure to read {welcome_channel_mention}!
"""

# Failed command permission check message
# Message posted when a user does not have permission to use a command.
NO_PERMISSION_MESSAGE = "{username_mention} You don't have permission to use {command}."

# Command error message
# Message posted if an error happened while the command was running. Output is
#   posted to the terminal.
COMMAND_ERROR_MESSAGE = "An error occured while processing the `{command}` command. See output for details."

# Missing arguments message
# Message posted if a command used without all the required arguments.
MISSING_ARGUMENTS_MESSAGE = "{username_mention} You are missing required arguments."

# Append command help to missing arguments message
# Displays command arguments and description. Same result to using
#   `help {command}`.
MISSING_ARGUMENTS_APPEND_HELP = True

# Nonexistant command message
# Message posted if a user tries to use a command that does not exist.
# Due to technical limitations, command variables like {command} cannot be used
#   here.
NONEXISTANT_COMMAND_MESSAGE = "{username_mention} `{command}` does not exist."
