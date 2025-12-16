# stock/utils.py
def has_profile(user):
    return hasattr(user, "userprofile") and user.userprofile is not None

def is_manager(user):
    return has_profile(user) and user.userprofile.role == "manager"

def is_chef(user):
    return has_profile(user) and user.userprofile.role == "chef"

def is_staff_role(user):
    return has_profile(user) and user.userprofile.role == "staff"
