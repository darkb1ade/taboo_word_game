# taboo_word_game

## API
### Specification
1. `POST /init_engine` = initialize players, avatars, word collection (if needed) \
    **Request**

    FIELD NAME | Description
    ---------  | ----------------------------------------
    names      | List of players' name
    avatars    | List of avatars' name (default is None for randomly select)
    words      | Reset current word collection or not. Value should be true or false

    **Response**\
    OK message
2. `POST /add` = add word to the word collection\
    **Request**
    FIELD NAME | Description
    ---------  | ----------------------------------------
    word       | word to add to the collection

    **Response**\
    OK or error message
3. `GET /random` = random word for each player \
    **Request**\
        -\
    **Response**
    
    FIELD NAME | Description
    ---------  | ----------------------------------------
    players    | List of players' name (`name`) and url linked to player card (`url`)
    message    | Response message
3. `GET /reset_word` = reset word collection \
    **Request**\
        -\
    **Response**\
    ok message

4. `GET /check_status` = check status of word collection \
    **Request**\
        -\
    **Response**
    FIELD NAME | Description
    ---------  | ----------------------------------------
    num_word   | Number of word inside word collection

### Testing
1. run `make run_app`
2. open terminal from local
    ```python
    import requests
    requests.post("http://127.0.0.1:5000/init_engine?names=a,b")
    requests.post("http://127.0.0.1:5000/add?word=test1")
    requests.post("http://127.0.0.1:5000/add?word=test2")
    requests.post("http://127.0.0.1:5000/add?word=test3")
    requests.post("http://127.0.0.1:5000/random")
    requests.post("http://127.0.0.1:5000/reset_word")
    ```
3. Check response from log inside container