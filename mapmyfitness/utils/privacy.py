def privacy_enum_to_string(privacy_enum):
    #
    # From constants:
    # PRIVATE = 0
    # PUBLIC = 3
    # FRIENDS = 1
    #
    privacy_map = {
        0: 'Private',
        1: 'Friends',
        3: 'Public'
    }
    return privacy_map[privacy_enum]
