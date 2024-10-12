# CrackTech

Coding round

## Run the project ##  

You need to have docker installed on your machine for testing the application
easily. To install Docker on your machine, please follow the official
documentation from [Docker](https://docs.docker.com/engine/install/).

After that, clone this repository to your machine.

```commandline
git clone https://github.com/ahmadalsajid/CrackTech.git
```

Now, `cd` into the `CrackTech` directory and rename `sample.env` to `env`. Put
your own credentials there, if you want to. Now, spin up the containers

```
$ docker compose up
```

After all the containers are up and running, execute the custom command to
populate some data for testing. It might take ~10 minutes or so.

```
$ docker compose exec api python /app/manage.py create_data
```

You can check all the data visually fom the Django Admin panel at <http://localhost:8000/admin/>.  
Also, you can check the query insights from <http://localhost:8000/silk/>

Once you are done, remove all the containers and associated objects by

```
$ docker compose down --rmi local -v
```

The user can:

* Login API: [Login API](#login-api)
* Mark questions as "Read" or "Unread."
    * Mark Read Question API: [Mark Question as Read API](#mark-question-as-read-api)
    * Mark Unread Question API: [Mark Question as Unread API](#mark-question-as-unread-api)

* Add questions to their "Favorite" list or remove them.
    * Mark Favorite Question API: [Mark Question as Favorite API](#mark-question-as-favorite-api)
    * Remove Favorite Question API: [Remove Question as Favorite API](#remove-question-as-favorite-api)
* Use a filter option at the top of the page to view only "Read" questions (e.g., if the user has marked 10 questions as
  read, they will see only those 10).
    * All Read Questions API: [View All Read Question API](#view-all-read-question-api)
* Filter for "Unread" questions, excluding those 10.
    * All unread Questions API: [View All Unread Question API](#view-all-unread-question-api)
* View all their "Favorite" questions.
    * All Favorite questions API: [View All Favorite Question API](#view-all-favorite-question-api)

Query:

1. GET - Tag list in each step with ( Tag total Question Count, user total read
   count, user total favorite count ). Example: Show all Tags under “Parts of
   Speech” Tag with all count
    * Tag summary API: [Tag Summary API](#tag-summary-api)

2. GET - Filter Question based on (“all”) ( All Question in the tag ). Example:
   I want to see all question under “Noun” Tag
    * Questions API: [Get Questions API](#get-questions-api)

3. GET - Filter Question based on (“read”) ( All Read Question in the tag ).
   Example: I want to see all question under “Noun” Tag which i have already
   marked as “Read”
    * Questions API: [Get Questions API](#get-questions-api)
4. GET - Filter Question based on (“!read”) ( All Unread Question in the
   tag ). Example: I want to see all question under “Noun” Tag which I have
   not read yet.
    * Questions API: [Get Questions API](#get-questions-api)

## API Documentation

* **Swagger-UI**: http://localhost:8000/api/schema/swagger-ui/
* **Redoc**: http://localhost:8000/api/schema/redoc/

### Login API

Make a `POST` request to <http://localhost:8000/api/customer/login/> with the user credential
from [Postman](https://www.postman.com/) or similar tool. i.e.

```bash
POST http://localhost:8000/api/login/
Content-Type: application/json
{
    "username":"sajid@mail.com",
    "password":"1qweqwe23"
}
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "token": {
        "refresh": "eyJhbxxxx.bkxxxxiOjF9.l9zxxxxslSQ",
        "access": "eyJhbxxxx.eyJxxxxX0.qSOxxxxIY"
    }
}
```

### Get Questions API

Make a `GET` request to <http://localhost:8000/api/quiz/questions/> with the `JWT token` in the
Authorization header. If you want to filter by Tag, pass tag ID in query param,
i.e. `tag_id=5`, to filter by `read` or `unread` questions, add query param
`status=read` or `status=unread` respectively. To filter favourite questions,
pass `favorite=true` in the URL. So, the complete URL would be
<http://localhost:8000/api/quiz/questions/?tag_id=5&status=read&favorite=true>

```bash
GET http://localhost:8000/api/quiz/questions/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### Mark Question as Read API

Make a `POST` request to <http://localhost:8000/api/quiz/reads/int:question_id/> with the `JWT token` in the
Authorization header.

```bash
POST http://localhost:8000/api/quiz/reads/199/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### Mark Question as Unread API

Make a `DELETE` request to <http://localhost:8000/api/quiz/reads/int:question_id/> with the `JWT token` in the
Authorization header.

```bash
DELETE http://localhost:8000/api/quiz/reads/199/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "detail": "Removed question from read"
}
```

### Mark Question as Favorite API

Make a `POST` request to <http://localhost:8000/api/quiz/favorites/int:question_id/> with the `JWT token` in the
Authorization header.

```bash
POST http://localhost:8000/api/quiz/favorites/199/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### Remove Question as Favorite API

Make a `DELETE` request to <http://localhost:8000/api/quiz/favorites/int:question_id/> with the `JWT token` in the
Authorization header.

```bash
DELETE http://localhost:8000/api/quiz/favorites/199/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "detail": "Removed question from favorite"
}
```

### View All Favorite Question API

Make a `GET` request to <http://localhost:8000/api/quiz/favorites/> with the `JWT token` in the
Authorization header. Also, you can paginate appending the query params, i.e. `?page=1&page_size=20`

```bash
GET http://localhost:8000/api/quiz/favorites/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 9,
    "next": "http://localhost:8000/api/quiz/favorites/?page=2&page_size=20",
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### View All Read Question API

Make a `GET` request to <http://localhost:8000/api/quiz/reads/> with the `JWT token` in the
Authorization header. Also, you can paginate appending the query params, i.e. `?page=1&page_size=20`

```bash
GET http://localhost:8000/api/quiz/reads/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 9,
    "next": "http://localhost:8000/api/quiz/favorites/?page=2&page_size=20",
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### View All Unread Question API

Make a `GET` request to <http://localhost:8000/api/quiz/reads/?status=unread> with the `JWT token` in the
Authorization header. Also, you can paginate appending the query params, i.e. `?page=1&page_size=20`

```bash
GET http://localhost:8000/api/quiz/reads/?status=unread
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "count": 9,
    "next": "http://localhost:8000/api/quiz/favorites/?page=2&page_size=20",
    "previous": null,
    "results": [
        {
            "id": 300,
            "question": "What album did The Lumineers release in 2016?",
            "option_1": "Winter",
            "option_2": "Cleopatra",
            "option_3": "The Lumineers",
            "option_4": "Tracks From The Attic",
            "correct_answer": 2,
            "created_at": "2024-10-11T00:29:43.475159Z",
            "updated_at": "2024-10-11T00:29:43.475239Z",
            "tags": [
                19,
                12,
                7,
                6,
                2,
                1
            ],
            "users": []
        },
        ...
}
```

### Tag Summary API

Make a `GET` request to <http://localhost:8000/api/quiz/tags-summary/> with the
`JWT token` in the Authorization header. Also, you can set any child tag as the
parent to get data by passing the `tag_id` appending the query params,
i.e. `?tag_id=2`

```bash
GET http://localhost:8000/api/quiz/tags-summary/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1
```

You will get the response in a JSON format (when no parent is selected)

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
[
    {
        "id": 1,
        "total_questions": 1000,
        "user_total_favorites": 250,
        "user_total_reads": 250,
        "name": "English Language",
        "parent": null,
        "tags": [
            {
                "id": 28,
                "total_questions": 204,
                "user_total_favorites": 250,
                "user_total_reads": 250,
                "name": "Syntax",
                "parent": 1,
                "tags": [
                    {
                        "id": 30,
                        "total_questions": 70,
                        "user_total_favorites": 219,
                        "user_total_reads": 248,
                        "name": "Sentence Types",
                        "parent": 28,
                        "tags": []
                    },
                    {
                        "id": 29,
                        "total_questions": 68,
                        "user_total_favorites": 207,
                        "user_total_reads": 249,
                        "name": "Word Order",
                        "parent": 28,
                        "tags": []
                    }
                ]
            },
            ...            
            {
                "id": 2,
                "total_questions": 516,
                "user_total_favorites": 250,
                "user_total_reads": 250,
                "name": "Parts of Speech",
                "parent": 1,
                "tags": [
                    {
                        "id": 9,
                        "total_questions": 178,
                        "user_total_favorites": 243,
                        "user_total_reads": 250,
                        "name": "Adjective",
                        "parent": 2,
                        "tags": [
                            {
                                "id": 11,
                                "total_questions": 49,
                                "user_total_favorites": 191,
                                "user_total_reads": 246,
                                "name": "Superlative",
                                "parent": 9,
                                "tags": []
                            },
                            {
                                "id": 10,
                                "total_questions": 60,
                                "user_total_favorites": 189,
                                "user_total_reads": 250,
                                "name": "Comparative",
                                "parent": 9,
                                "tags": []
                            }
                        ]
                    },
                    {
                        "id": 6,
                        "total_questions": 182,
                        "user_total_favorites": 245,
                        "user_total_reads": 250,
                        "name": "Verb",
                        "parent": 2,
                        "tags": [
                            {
                                "id": 8,
                                "total_questions": 62,
                                "user_total_favorites": 213,
                                "user_total_reads": 250,
                                "name": "Linking Verb",
                                "parent": 6,
                                "tags": []
                            },
                            {
                                "id": 7,
                                "total_questions": 69,
                                "user_total_favorites": 218,
                                "user_total_reads": 249,
                                "name": "Action Verb",
                                "parent": 6,
                                "tags": []
                            }
                        ]
                    },
                    {
                        "id": 3,
                        "total_questions": 173,
                        "user_total_favorites": 248,
                        "user_total_reads": 250,
                        "name": "Noun",
                        "parent": 2,
                        "tags": [
                            {
                                "id": 5,
                                "total_questions": 51,
                                "user_total_favorites": 198,
                                "user_total_reads": 248,
                                "name": "Common Noun",
                                "parent": 3,
                                "tags": []
                            },
                            {
                                "id": 4,
                                "total_questions": 69,
                                "user_total_favorites": 213,
                                "user_total_reads": 248,
                                "name": "Proper Noun",
                                "parent": 3,
                                "tags": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
]
```

Or, you will get the response in a JSON format (when a tag is selected),
i.e. `http://localhost:8000/api/quiz/tags-summary/?tag_id=2`

```bash
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
[
    {
        "id": 2,
        "total_questions": 516,
        "user_total_favorites": 250,
        "user_total_reads": 250,
        "name": "Parts of Speech",
        "parent": 1,
        "tags": [
            {
                "id": 9,
                "total_questions": 178,
                "user_total_favorites": 243,
                "user_total_reads": 250,
                "name": "Adjective",
                "parent": 2,
                "tags": [
                    {
                        "id": 11,
                        "total_questions": 49,
                        "user_total_favorites": 191,
                        "user_total_reads": 246,
                        "name": "Superlative",
                        "parent": 9,
                        "tags": []
                    },
                    {
                        "id": 10,
                        "total_questions": 60,
                        "user_total_favorites": 189,
                        "user_total_reads": 250,
                        "name": "Comparative",
                        "parent": 9,
                        "tags": []
                    }
                ]
            },
            {
                "id": 6,
                "total_questions": 182,
                "user_total_favorites": 245,
                "user_total_reads": 250,
                "name": "Verb",
                "parent": 2,
                "tags": [
                    {
                        "id": 8,
                        "total_questions": 62,
                        "user_total_favorites": 213,
                        "user_total_reads": 250,
                        "name": "Linking Verb",
                        "parent": 6,
                        "tags": []
                    },
                    {
                        "id": 7,
                        "total_questions": 69,
                        "user_total_favorites": 218,
                        "user_total_reads": 249,
                        "name": "Action Verb",
                        "parent": 6,
                        "tags": []
                    }
                ]
            },
            {
                "id": 3,
                "total_questions": 173,
                "user_total_favorites": 248,
                "user_total_reads": 250,
                "name": "Noun",
                "parent": 2,
                "tags": [
                    {
                        "id": 5,
                        "total_questions": 51,
                        "user_total_favorites": 198,
                        "user_total_reads": 248,
                        "name": "Common Noun",
                        "parent": 3,
                        "tags": []
                    },
                    {
                        "id": 4,
                        "total_questions": 69,
                        "user_total_favorites": 213,
                        "user_total_reads": 248,
                        "name": "Proper Noun",
                        "parent": 3,
                        "tags": []
                    }
                ]
            }
        ]
    }
]
```

## References

* https://stackoverflow.com/questions/47867760/django-quiz-app-model-for-multiple-choice-questions
* https://www.django-rest-framework.org/api-guide/caching/
* https://forum.djangoproject.com/t/redis-cache-in-django-5-0/27131
* https://stackoverflow.com/questions/71431687/how-to-generate-a-schema-for-a-custom-pagination-in-django-rfw-with-drf-spectacu
* https://forum.djangoproject.com/t/get-all-children-of-self-referencing-django-model-in-nested-hierarchy/16761