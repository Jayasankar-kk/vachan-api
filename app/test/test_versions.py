'''Test cases for versions related APIs'''
from . import client
from . import assert_input_validation_error, assert_not_available_content
from . import check_default_get
from .test_auth_basic import login,SUPER_USER,SUPER_PASSWORD,logout_user
from .conftest import initial_test_users

UNIT_URL = '/v2/versions'

headers_auth = {"contentType": "application/json",
                "accept": "application/json",
                'Authorization': "Bearer"+" "+initial_test_users['APIUser2']['token']
            }

def assert_positive_get(item):
    '''Check for the properties in the normal return object'''
    assert "versionId" in item
    assert isinstance(item['versionId'], int)
    assert "versionAbbreviation" in item
    assert "versionName" in item
    assert "versionTag" in item
    assert "metaData" in item

def check_post(data):
    '''common steps for positive post test cases'''
    #without AUth
    headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers, json=data)
    assert response.status_code == 401
    assert response.json()['error'] == 'Authentication Error'

    #with Auth
    headers_auth = {"contentType": "application/json",
                "accept": "application/json",
                'Authorization': "Bearer"+" "+initial_test_users['APIUser2']['token']
            }
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert response.status_code == 201
    assert response.json()['message'] == "Version created successfully"
    assert_positive_get(response.json()['data'])
    assert response.json()["data"]["versionAbbreviation"] == data['versionAbbreviation']
    return response

def test_post_default():
    '''Positive test to add a new version'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    check_post(data)

def test_post_multiple_with_same_abbr():
    '''Positive test to add two version, with same abbr and diff versionTag'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    check_post(data)
    data["versionTag"] = 2
    check_post(data)

def test_post_multiple_with_same_abbr_negative():
    '''Negative test to add two version, with same abbr and versionTag'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    check_post(data)
    # headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert response.status_code == 409
    assert response.json()['error'] == "Already Exists"

def test_post_without_versionTag():
    '''versionTag field should have a default value, even not provided'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    response = check_post(data)
    assert response.json()['data']['versionTag'] == "1"

def test_post_without_metadata():
    '''metadata field is not mandatory'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "versionTag": "3"
    }
    response = check_post(data)
    assert response.json()['data']['metaData'] is None

def test_post_without_abbr():
    '''versionAbbreviation is mandatory'''
    data = {
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "some", "access-key": "123xyz"}
    }
    # headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

def test_post_wrong_abbr():
    '''versionAbbreviation cannot have space, dot etc'''
    data = {
        "versionAbbreviation": "XY Z",
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "one", "access-key": "123xyz"}
    }
    # headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

    data['versionAbbreviation'] = 'X.Y'
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

def test_post_wrong_versionTag():
    '''versionTag cannot have space, comma letters etc'''
    data = {
        "versionAbbreviation": "XY Z",
        "versionName": "Xyz version to test",
        "versionTag": "1,0",
        "metaData": {"owner": "another one", "access-key": "123xyz"}
    }
    # headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

    data['versionTag'] = "1 2"
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

    data['versionTag'] = '1a'
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

def test_post_without_name():
    '''versionName is mandatory'''
    data = {
        "versionAbbreviation": "XYZ",
        "versionTag": "1",
        "metaData": {"owner": "no one", "access-key": "123xyz"}
    }
    # headers = {"contentType": "application/json", "accept": "application/json"}
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    assert_input_validation_error(response)

def test_get():
    '''Test get before adding data to table. Usually run on new test DB on local or github.
    If the testing is done on a DB that already has data(staging), the response wont be empty.'''
    response = client.get(UNIT_URL)
    if len(response.json()) == 0:
        assert_not_available_content(response)


def test_get_wrong_abbr():
    '''abbreviation with space, number'''
    response = client.get(UNIT_URL+'?version_abbreviation=A%20A')
    assert_input_validation_error(response)

    response = client.get(UNIT_URL+'?version_abbreviation=123')
    assert_input_validation_error(response)

def test_get_wrong_versionTag():
    '''versionTag as text'''
    response = client.get(UNIT_URL+'?version_abbreviation=A%20A')
    assert_input_validation_error(response)

def test_get_after_adding_data():
    '''Add some data to versions table and test get method'''
    data = {
        'versionAbbreviation': "AAA",
        'versionName': 'test name A',
        'versionTag': 1
    }
    check_post(data)
    data['versionTag'] = 2
    check_post(data)
    data = {
        'versionAbbreviation': "BBB",
        'versionName': 'test name B',
        'versionTag': 1
    }
    check_post(data)
    data['versionTag'] = 2
    check_post(data)
    headers = {"contentType": "application/json", "accept": "application/json"}
    check_default_get(UNIT_URL, headers,assert_positive_get)

    # filter with abbr
    response = client.get(UNIT_URL + '?version_abbreviation=AAA')
    assert response.status_code == 200
    assert len(response.json()) == 2
    for item in response.json():
        assert_positive_get(item)
        assert item['versionAbbreviation'] == 'AAA'

    # filter with abbr with registered user
    response = client.get(UNIT_URL + '?version_abbreviation=AAA',headers=headers_auth)
    assert response.status_code == 200
    assert len(response.json()) == 2
    for item in response.json():
        assert_positive_get(item)
        assert item['versionAbbreviation'] == 'AAA'   

    # filter with abbr, for not available content
    response = client.get(UNIT_URL + '?version_abbreviation=CCC')
    assert_not_available_content(response)

    # filter with name
    response = client.get(UNIT_URL + '?version_name=test%20name%20B')
    assert response.status_code == 200
    assert len(response.json()) == 2
    for item in response.json():
        assert_positive_get(item)
        assert item['versionName'] == 'test name B'

   # filter with abbr and versionTag
    response = client.get(UNIT_URL + '?version_abbreviation=AAA&version_tag=2')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert_positive_get(response.json()[0])
    assert response.json()[0]['versionAbbreviation'] == 'AAA'
    assert response.json()[0]['versionTag'] == "2"

    data = {
        'versionAbbreviation': "CCC",
        'versionName': 'test name C',
        'metaData': {'owner': 'myself'}
    }
    check_post(data)

    # filter with metaData and default value for metadata
    response = client.get(UNIT_URL + '?metadata={"owner":"myself"}')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert_positive_get(response.json()[0])
    assert response.json()[0]['versionAbbreviation'] == 'CCC'
    assert response.json()[0]['versionTag'] == "1"
    assert response.json()[0]['metaData']['owner'] == 'myself'

def test_put_version():
    """test default put for versions with auth check"""
    #create version with auth
    data = {
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    headers_auth = {"contentType": "application/json",
                "accept": "application/json",
                'Authorization': "Bearer"+" "+initial_test_users['APIUser2']['token']
            }
    response = client.post(UNIT_URL, headers=headers_auth, json=data)
    version_id = response.json()['data']['versionId']

    #edit with same user created
    data = {
        "versionId": version_id,
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version to test edited",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    response = client.put(UNIT_URL, headers=headers_auth, json=data)
    assert response.status_code == 201
    assert response.json()['message'] == "Version edited successfully"
    assert response.json()["data"]["versionName"] == "Xyz version to test edited"

    headers_auth = {"contentType": "application/json",
                "accept": "application/json",
                'Authorization': "Bearer"+" "+initial_test_users['APIUser']['token']
            }
    response = client.put(UNIT_URL, headers=headers_auth, json=data)
    assert response.status_code == 403
    assert response.json()['error'] == "Permission Denied"

    #edit with super user
    data_admin   = {
    "user_email": SUPER_USER,
    "password": SUPER_PASSWORD
    }      
    response =login(data_admin)
    assert response.json()['message'] == "Login Succesfull"
    token_admin =  response.json()['token']

    data = {
        "versionId": version_id,
        "versionAbbreviation": "XYZ",
        "versionName": "Xyz version edited by admin",
        "versionTag": "1",
        "metaData": {"owner": "someone", "access-key": "123xyz"}
    }
    headers_admin = {"contentType": "application/json",
                    "accept": "application/json",
                    'Authorization': "Bearer"+" "+token_admin
            }
    response = client.put(UNIT_URL, headers=headers_admin, json=data)
    assert response.status_code == 201
    assert response.json()['message'] == "Version edited successfully"
    assert response.json()["data"]["versionName"] == "Xyz version edited by admin"

    logout_user(token_admin)