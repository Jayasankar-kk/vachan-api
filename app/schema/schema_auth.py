"""schema for auth related"""
from pydantic import BaseModel, validator
from pydantic import types, EmailStr

#pylint: disable=too-few-public-methods

class Registration(BaseModel):
    """kratos registration input"""
    email:str
    password:types.SecretStr
    firstname:str = None
    lastname:str = None

class EditUser(BaseModel):
    """kratos registration input"""
    firstname:str
    lastname:str

# class FilterRoles(str, Enum):
#     '''Filter roles for get users'''
#     ALL = "All"
#     AG = "Autographa"
#     VACHAN = "Vachan-online or vachan-app"
#     API = "API-user"

class UserRole(BaseModel):
    """kratos user role input"""
    userid:str
    roles:list[str]

class UserIdentity(BaseModel):
    """kratos user role input"""
    userid:str

class RegistrationOut(BaseModel):
    """registration output"""
    id:str
    email:str
    Permissions:list

class RegisterResponse(BaseModel):
    """Response object of registration"""
    message:str
    registered_details:RegistrationOut
    token:str = None

class LoginResponse(BaseModel):
    """Response object of login"""
    message:str
    token:str
    userId:str

class LogoutResponse(BaseModel):
    """Response object of logout"""
    message:str

class CommmonError(BaseModel):
    """login error"""
    error:str
    details:str

class UseroleResponse(BaseModel):
    """user role update response"""
    message:str
    role_list:list

class IdentityDeleteResponse(BaseModel):
    """user identity delete response"""
    message:str

# class TableHeading(int, Enum):
#     """Heading of permission table"""
#     ENDPOINT = 0
#     METHOD = 1
#     REQUESTAPP = 2
#     USERNEEDED = 3
#     RESOURCETYPE = 4
#     PERMISSION = 5

class IdentitityListResponse(BaseModel):
    """Response object of list of identities"""
    userId:str
    name: dict
    class Config:
        '''display example value in API documentation'''
        schema_extra = {
            "example":{
            "userId": "ecf57420-9rg0-4048-b56b-dc56fc57c4ed",
            "name": {
                "last": "lastname",
                "first": "firstname",
                "fullname": "Full Name"
            }
        }}

class UserProfileResponse(BaseModel):
    """Response object of list of identities"""
    userId:str
    traits: dict
    class Config:
        '''display example value in API documentation'''
        schema_extra = {
            "example":{
            "userId": "ecf57420-9rg0-4048-b56b-dc56fc57c4ed",
            "traits": {
                "name":{"last":"lastname", "first":"firstname"},
                "email":"useremail@test.com",
                "userrole":["AgUser, VachanUser"]
            }
        }}

class UserUpdateResponse(BaseModel):
    """Response object of User Update"""
    message:str
    data: IdentitityListResponse

class RegistrationAppContacts(BaseModel):
    """registration App output"""
    email:EmailStr
    phone:str = None

class RegistrationAppOut(BaseModel):
    """registration App output"""
    id:str
    name:str
    email:str
    organization:str
    contacts:RegistrationAppContacts

class RegisterAppResponse(BaseModel):
    """Response object of App registration"""
    message:str
    registered_details:RegistrationAppOut
    key:str

class RegistrationAppIn(BaseModel):
    """kratos app registration input"""
    email:str
    name:str
    organization:str
    password:types.SecretStr
    contacts:RegistrationAppContacts

    @validator('contacts')
    def check_phone(cls, val):#pylint: disable=no-self-argument, inconsistent-return-statements
        '''check for phone is present'''
        if val.phone is not None:
            if len(val.phone) <= 0:
                raise ValueError('Phone Should not be blank')
        return {"email" : val.email, "phone" : val.phone}

    class Config:
        '''display example value in API documentation'''
        schema_extra = {
            "example":{
            "email": "myapp@vachan",
            "name": "my app",
            "organization": "BCS",
            "password": "my secret",
            "contacts": {
                "email": "myappofficial@vachan.org",
                "phone": "+91 1234567890"
            }
        }}

class LoginResponseApp(BaseModel):
    """Response object of login for app"""
    message:str
    key:str
    appId:str

class AppUpdateResponse(BaseModel):
    """Response object of App data Update"""
    message:str
    data: RegistrationAppOut

class EditApp(BaseModel):
    """kratos App update input"""
    ContactEmail:EmailStr
    organization:str
    phone:str = None
    @validator('phone')
    def check_phone(cls, val):#pylint: disable=no-self-argument, inconsistent-return-statements
        '''check for phone is present'''
        if val is not None:
            if len(val) <= 0:
                raise ValueError('Phone Should not be blank')
        return val
    
class RoleOut(BaseModel):
    '''Return object of roles output'''
    roleId : int 
    roleName : str
    roleOfApp : str
    roleDescription : str
    class Config:
        ''' telling Pydantic exactly that "it's OK if I pass a non-dict value,
        just get the data from object attributes'''
        orm_mode = True
        # '''display example value in API documentation'''
        schema_extra = {
            "example": {
                "roleId": 100011,
                "roleName": "manager",
                "roleOfApp": "xyz",
                "roleDescription": "manager of the app"
            }
        }

class RoleResponse(BaseModel):
    """Response object of role"""

    message:str
    data: RoleOut


class Roles(BaseModel):
    """kratos roles input"""
    roleName: str
    roleOfApp : str
    roleDescription : str

class RoleReadResponse(BaseModel):
    '''Return output object of roles'''
    roleId : int
    roleName : str
    roleOfApp : str 
    roleDescription : str =None
    class Config:
        ''' telling Pydantic exactly that "it's OK if I pass a non-dict value,
        just get the data from object attributes'''
        orm_mode = True
        # '''display example value in API documentation'''
        schema_extra = {
            "example": {
                "roleId": 100011,
                "roleName": "manager",
                "roleOfApp": "xyz",
                "roleDescription": "manager of the app"
            }
        }

