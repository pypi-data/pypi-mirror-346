import fastapi
import pydantic

from src.api.dependencies.repository import get_repository
from src.api.dependencies.response import format_200_response, format_201_response
from src.models.schemas.account import AccountInResponse, AccountInUpdate, AccountWithToken
from src.models.schemas.response import DataResponse
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.formatters.response_formatter import response_formatter


router = fastapi.APIRouter(prefix="/accounts", tags=["accounts"])


@router.get(
    path="",
    name="accounts:read-accounts",
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_accounts(
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_200_response,
) -> DataResponse:
    db_accounts = await account_repo.read_accounts()
    db_account_list = []

    for db_account in db_accounts:
        access_token = jwt_generator.generate_access_token(account=db_account)
        account = AccountInResponse(
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
        db_account_list.append(account)

    return format_response(db_account_list)


@router.get(
    path="/{id}",
    name="accounts:read-account-by-id",
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_account(
    id: int,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_200_response,
) -> DataResponse:
    db_account = await account_repo.read_account_by_id(id=id)
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


@router.patch(
    path="/{id}",
    name="accounts:update-account-by-id",
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account(
    id: int,
    update_username: str | None = None,
    update_email: pydantic.EmailStr | None = None,
    update_password: str | None = None,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_200_response,
) -> DataResponse:
    account_update = AccountInUpdate(username=update_username, email=update_email, password=update_password)
    updated_db_account = await account_repo.update_account_by_id(id=id, account_update=account_update)

    access_token = jwt_generator.generate_access_token(account=updated_db_account)

    account_response = AccountInResponse(
        id=updated_db_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=updated_db_account.username,
            email=updated_db_account.email,  # type: ignore
            is_verified=updated_db_account.is_verified,
            is_active=updated_db_account.is_active,
            is_logged_in=updated_db_account.is_logged_in,
            created_at=updated_db_account.created_at,
            updated_at=updated_db_account.updated_at,
        ),
    )
    
    return format_response(account_response)


@router.delete(
    path="/{id}", 
    name="accounts:delete-account-by-id", 
    response_model=DataResponse,
    status_code=fastapi.status.HTTP_200_OK
)
async def delete_account(
    id: int, 
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    format_response: callable = format_200_response,
) -> DataResponse:
    deletion_result = await account_repo.delete_account_by_id(id=id)
    return format_response({"message": deletion_result})
