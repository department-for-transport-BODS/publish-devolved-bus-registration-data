from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


# def test_create_upload_file():
#     # Create a test file
#     test_file = open("test_file.csv", "w")
#     test_file.write("name,age\nJohn,25\nJane,30")
#     test_file.close()

#     # Send a POST request to the endpoint with the test file
#     response = client.post("/uploadfile/", files={"file": open("test_file.csv", "rb")})

#     # Assert that the response status code is 200
#     assert response.status_code == 200

#     # Assert that the response contains the expected filename
#     Error_message = [
#         {
#             "input": {"age": "25", "name": "John"},
#             "loc": ["first_name"],
#             "msg": "Field required",
#             "type": "missing",
#         },
#         {
#             "input": {"age": "25", "name": "John"},
#             "loc": ["last_name"],
#             "msg": "Field required",
#             "type": "missing",
#         },
#         {
#             "input": {"age": "25", "name": "John"},
#             "loc": ["address"],
#             "msg": "Field required",
#             "type": "missing",
#         },
#     ]
#     assert response.json() == Error_message
#     # Clean up the test file
#     os.remove("test_file.csv")


# @pytest.mark.parametrize(
#     "test_data, expected_response",
#     [
#         (
#             "name,age\nJohn,25",
#             [
#                 {
#                     "input": {"age": "25", "name": "John"},
#                     "loc": ["first_name"],
#                     "msg": "Field required",
#                     "type": "missing",
#                 },
#                 {
#                     "input": {"age": "25", "name": "John"},
#                     "loc": ["last_name"],
#                     "msg": "Field required",
#                     "type": "missing",
#                 },
#                 {
#                     "input": {"age": "25", "name": "John"},
#                     "loc": ["address"],
#                     "msg": "Field required",
#                     "type": "missing",
#                 },
#             ],
#         ),
#         (
#             "first_name,last_name,address\nyum,Smith,123 Main St\nsam,Doe,456 Maple Ave",
#             {"filename": "test_file.csv"},
#         ),
#     ],
# )
# def test_create_upload_files(test_data, expected_response):
#     # Create a test file
#     test_file = open("test_file.csv", "w")
#     test_file.write(test_data)
#     test_file.close()

#     # Send a POST request to the endpoint with the test file
#     response = client.post("/uploadfile/", files={"file": open("test_file.csv", "rb")})
#     # Assert that the response status code is 200
#     assert response.status_code == 200

#     # Assert that the response matches the expected validation errors
#     assert response.json() == expected_response

#     # Clean up the test file
#     os.remove("test_file.csv")


def test_read_root():
    response = client.get("/api")
    assert response.status_code == 403
    # assert response.json() == {
    #     "message": "FastAPI running on AWS Lambda and is executed in region Running locally, using runtime environment Running locally"
    # }
    assert response.json() == {"detail": "Not authenticated"}
