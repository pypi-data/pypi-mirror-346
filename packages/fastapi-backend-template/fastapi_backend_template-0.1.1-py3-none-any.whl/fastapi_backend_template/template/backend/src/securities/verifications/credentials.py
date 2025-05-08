class CredentialVerifier:
    def is_username_taken(self, username: str | None) -> bool:
        """判断用户名是否已被占用
        
        Args:
            username: 数据库查询到的用户名，None 表示未找到
            
        Returns:
            True 如果用户名已存在，False 如果用户名可用
        """
        return username is not None

    def is_email_taken(self, email: str | None) -> bool:
        """判断邮箱是否已被占用
        
        Args:
            email: 数据库查询到的邮箱，None 表示未找到
            
        Returns:
            True 如果邮箱已存在，False 如果邮箱可用
        """
        return email is not None


def get_credential_verifier() -> CredentialVerifier:
    return CredentialVerifier()


credential_verifier: CredentialVerifier = get_credential_verifier()
