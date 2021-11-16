import json
from itertools import cycle
from typing import List


class Permissions:
    """Bot access permissions and other utils"""

    def __init__(self) -> None:
        self.owner: int = None
        self.admins: List[int] = []
        self.blocked: List[int] = []
        self.limited: List[int] = []

        self.permissions: dict = {}

    def isOwner(self, ctx):
        return ctx.author.id == self.owner

    def isAdmin(self, ctx):
        user_id = ctx.author.id
        return (
            user_id in self.admins and user_id not in self.blocked
        ) or user_id == self.owner

    def isBlocked(self, ctx):
        user_id = ctx.author.id
        return user_id in self.blocked and not user_id == self.owner

    def isLimited(self, ctx):
        """Extra features access enabled users"""
        user_id = ctx.author.id
        return (
            (user_id in self.limited or user_id in self.admins)
            and not user_id in self.blocked
        ) or user_id == self.owner

    def load_or_reload_perms(self):
        """Load or Reload permissions"""

        with open("perm.json", "r") as d:
            self.permissions = json.load(d)

        if self.permissions:
            self.owner = self.permissions["owner"]["id"]
            if self.permissions.get("admins", None):
                self.admins = self.permissions["admins"]
            if self.permissions.get("blocked", None):
                self.blocked = self.permissions["blocked"]

    @property
    def cycle_bot_status(self):
        """Bot statuses"""
        if self.permissions.get("bot_statuses"):
            return cycle(self.permissions["bot_statuses"])
        else:
            return cycle(["with my Owl"])

    def addAdmin(self, user_id: int):
        """Add a bot admin"""
        if user_id not in self.admins:
            if self.permissions.get("admins"):
                self.permissions["admins"].append(user_id)
            else:
                self.permissions["admins"] = [user_id]

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.admins = self.permissions.get("admins")
            return True
        return False

    def removeAdmin(self, user_id: int):
        """Remove a bot admin"""

        if self.permissions.get("admins") and user_id in self.permissions["admins"]:
            self.permissions["admins"].remove(user_id)

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.admins = self.permissions.get("admins")
            return True
        return False

    def addBlocked(self, user_id: int):
        """Add a blocked user"""
        if user_id not in self.blocked:
            if self.permissions.get("blocked"):
                self.permissions["blocked"].append(user_id)
            else:
                self.permissions["blocked"] = [user_id]

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.blocked = self.permissions.get("blocked")
            return True
        return False

    def removeBlocked(self, user_id: int):
        """Remove a blocked user from list"""

        if self.permissions.get("blocked") and user_id in self.permissions["blocked"]:
            self.permissions["blocked"].remove(user_id)

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.blocked = self.permissions.get("blocked")
            return True
        return False

    def addLimited(self, user_id: int):
        """Add a limited user"""

        if user_id not in self.limited:
            if self.permissions.get("limited"):
                self.permissions["limited"].append(user_id)
            else:
                self.permissions["limited"] = [user_id]

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.limited = self.permissions.get("limited")
            return True
        return False

    def removeLimited(self, user_id: int):
        """Remove a limited user"""

        if self.permissions.get("limited") and user_id in self.permissions["limited"]:
            self.permissions["limited"].remove(user_id)

            with open("perm.json", "w") as f:
                json.dump(self.permissions, f)

            self.limited = self.permissions.get("limited")
            return True
        return False


bot_perms = Permissions()
bot_perms.load_or_reload_perms()
