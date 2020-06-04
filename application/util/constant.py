"""
Constant module
"""
ACTIVE_ROLES = ["super_admin", "admin", "user"]


class CacheKey:
    """
    Get key for cache value
    """
    @staticmethod
    def user_role(user_id: int):
        """
        User role key
        @param user_id:
        @return:
        """
        return f"user:{user_id}:role"
