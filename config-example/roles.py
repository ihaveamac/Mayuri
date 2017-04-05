# Mayuri Roles Configuration

# Roles can be set through name or ID.
# Name should begin with &, IDs should only be numbers in a string.
# Example: '&Staff', '196635745551646720'
# These should not be blank. Disable the appropriate features per-channel if
#   you don't want to use them.
# Names should only be used if you're sure they won't change.
# To get the ID, use getroles.py to list roles for every server on the bot's
#   account based on TOKEN on core.py (there is currently no easy way to get a
#   role ID through the Discord application).

# Main staff role
# This should be the role all staff have at all times.
MAIN_STAFF_ROLE = '&Staff'

# Staff role configuration
# This lists all the staff roles and if they should use sudo or not.
# Order goes from highest to lowest in the staff hierarchy. This means if
#   "OP" is above "HalfOP", then "OP" gets everything "HalfOP" has. Users with
#   "OP" will also not have to use sudo even if they have the "HalfOP" rank.
# Roles should be entered like:
#     ('&HalfOP', True),
#     ('196637753448857600', False),
# sudo means the user must use "sudo" to obtain the role to use extra
#   permissions. Usage of sudo and unsudo are logged. Usually these permissions
#   should only be actions done through the Discord interface and not commands,
#   since command usage can be logged separately.
# TODO: explain how sudo works with roles
STAFF_ROLES = [
    ('&Owner', False),
    ('&SuperOP', False),
    ('&OP', False),
    ('&HalfOP', True),
]

# Muted role
# Role given to users to mute them.
MUTED_ROLE = '&Muted'

# No-Upload role
# Role given to users to remove file upload permissions.
NO_UPLOAD_ROLE = '&No-Upload'

# No-Preview role
# Role given to users to remove link previews.
NO_PREVIEW_ROLE = '&No-Preview'
