Database Format

The database is a json file store that stores an array of objects. Objects will be loaded by python as
a list of dictionaries. The file store always has a "data" key with a value of the array of objects.

{
    "data": [
        {
            "username": "user",
            "password": "12345"
        },
        {
            "username": "aaa",
            "password": "123"
        }
    ]
}