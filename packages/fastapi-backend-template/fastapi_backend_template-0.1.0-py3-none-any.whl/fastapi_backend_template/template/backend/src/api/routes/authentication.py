import fastapi

from src.api.dependencies.repository import get_repository
from src.api.dependencies.response import format_200_response, format_201_response, format_202_response
from src.models.schemas.account import AccountInCreate, AccountInLogin, AccountInResponse, AccountWithToken
from src.models.schemas.response import DataResponse
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_generator


router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup",
    name="auth:signup",
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    account_create: AccountInCreate,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_201_response,
) -> DataResponse:
    # 检查用户名和邮箱是否已被占用
    await account_repo.is_username_taken(username=account_create.username)
    await account_repo.is_email_taken(email=account_create.email)

    new_account = await account_repo.create_account(account_create=account_create)
    access_token = jwt_generator.generate_access_token(account=new_account)

    account_response = AccountInResponse(
        id=new_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=new_account.username,
            email=new_account.email,  # type: ignore
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at,
            updated_at=new_account.updated_at,
        ),
    )
    
    return format_response(account_response)


@router.post(
    path="/signin",
    name="auth:signin",
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def signin(
    account_login: AccountInLogin,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_202_response,
) -> DataResponse:
    # 验证身份并获取账户
    db_account = await account_repo.read_user_by_password_authentication(account_login=account_login)
    access_token = jwt_generator.generate_access_token(account=db_account)

    account_response = AccountInResponse(
        id=db_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=db_account.username,
            email=db_account.email,  # type: ignore
            is_verified=db_account.is_verified,
            is_active=db_account.is_active,
            is_logged_in=db_account.is_logged_in,
            created_at=db_account.created_at,
            updated_at=db_account.updated_at,
        ),
    )
    
    return format_response(account_response)
