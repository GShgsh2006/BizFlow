"""密码哈希与校验。

直接用 bcrypt，不再经过 passlib：
passlib 1.7.4 与 bcrypt>=4.1 不兼容——bcrypt 移除了 `__about__` 属性，
且 5.x 起对超过 72 字节的密码直接抛 ValueError 而不是自动截断。
这两点会让 passlib 的后端初始化失败，导致注册和登录接口全部 500。
"""

import bcrypt

# bcrypt 算法只使用密码的前 72 字节，超长必须先截断，否则 bcrypt 5.x 会报错。
_BCRYPT_MAX_BYTES = 72
# 与库里已有的 $2b$12$ 哈希保持一致的代价因子
_ROUNDS = 12


def _to_bcrypt_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:_BCRYPT_MAX_BYTES]


# 加密密码
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt(rounds=_ROUNDS)
    return bcrypt.hashpw(_to_bcrypt_bytes(password), salt).decode("utf-8")


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            _to_bcrypt_bytes(plain_password),
            hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        # 哈希串格式非法（脏数据）时按「验证不通过」处理，而不是抛 500
        return False
