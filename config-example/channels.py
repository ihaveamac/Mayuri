# Mayuri Channels Configuration

# Channels can be set through name or ID.
# Name should begin with #, IDs should only be numbers in a string.
# Example: '#general', '196635745551646720'
# These should not be blank unless specified. Disable the appropriate features
#   per-channel if you don't want to use them.
# To get the ID, enable Developer Mode (Settings -> Appearance), right-click a
#   channel then "Copy ID".

# "Welcome" channel, where rules and other info are usually stored
# This is just used for information when sending messages. This can be blank.
WELCOME_CHANNEL = '#welcome'

# "Mods" channel, usually a private area for staff to discuss topics
# Certain information is posted here, including notices about automatic mutes,
#   channel lockdowns, and staff requests.
MODS_CHANNEL = '#mods'

# "Mod logs" channel, where staff actions are logged
# What is logged:
#   * bans (through bot and Discord)
#   * unbans (through bot and Discord)
#   * timed bans (through bot)
#   * kicks (through bot)
#   * sudo and unsudo
#   * message cleanup ("clean" command)
#   * nickname addition, change, removal
#   * watch and unwatch
#   * warns
#   * mute, no-embed
#   * lockdown, softlock, super-lockdown, unlock
#   * auto-mute and auto-lockdown with deleted messages
#   * TODO: list mod-logs stuff
MOD_LOGS_CHANNEL = '#mod-logs'

# "Server logs" channel, where server events are logged
# What is logged:
#   * user joins and leaves
#   * username changes
#   * bans (through bot and Discord)
#   * timed bans (through bot)
#   * kicks (through bot)
#   * TODO: list server-logs stuff
SERVER_LOGS_CHANNEL = '#server-logs'

# "Message logs" channel, where message events and watched users are logged
# What is logged:
#   * messages from watched users
#   * use of certain terms, and if they are deleted
#   * watch and unwatch
#   * TODO: list message-logs stuff
MESSAGE_LOGS_CHANNEL = '#message-logs'
