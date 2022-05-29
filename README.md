# anyApp-backend
Backend for anyApp.

## API Specifications

### [Web Based Admin](#admin)
* [access](#admin_access)

### [User](#user)
* [create](#user_create)
* [login](#user_login)
* [profile](#user_profile)

### [Tweet](#tweet)
* [tweet](#tweet_tweet)
* [like](#tweet_like)

### <a name="admin"></a> Admin:

#### <a name="admin_access"></a> Access

| Method    | `GET`       |
| :--       | :--         |
| URL       | `/admin/`   |

Recieves the webpage for django admin.

### <a name="user"></a> User:

#### <a name="user_create"></a> Create

| Method    | `POST`                |
| :--       | :--                   |
| URL       | `/api/user/create/`   |

| Request   |             |
| :--       | :--         |
| username  | String      |
| password  | String      |
| email     | String      |

| Response    |             |
| :--         | :--         |
| id          | Int         |
| username    | String      |
| email       | String      |
| token       | String      |

Creates a new user, returns primary key and token.

#### <a name="user_login"></a> Login

| Method    | `POST`                |
| :--       | :--                   |
| URL       | `/api/user/login/`    |

| Request   |             |
| :--       | :--         |
| username  | String      |
| password  | String      |

| Response    |             |
| :--         | :--         |
| token       | String      |

Backend uses obtain_auth_token.

#### <a name="user_profile"></a> Profile

| Method    | `GET`                   |
| :--       | :--                     |
| URL       | `/api/user/profile/`    |

| Header          |               |
| :--             | :--           |
| Authorization   | Token String  |

| Response      |             |
| :--           | :--         |
| id            | Int         |
| profile_name  | String      |
| create_date   | String      |
| profile_info  | String      |

Obtains profile information for user.

### <a name="tweet"></a> Tweet:

#### <a name="tweet_tweet"></a> Tweet

| Method    | `POST`            |
| :--       | :--               |
| URL       | `/api/tweet/`     |

| Header          |               |
| :--             | :--           |
| Authorization   | Token String  |

| Request   |                 |
| :--       | :--             |
| text      | String          |
| replies   | Int?            |
| image     | MultipartBody   |
| video     | MultipartBody   |

| Response      |             |
| :--           | :--         |
| id            | Int         |
| text          | String      |
| imageUrl      | String      |
| videoUrl      | String      |
| replies       | Int         |

User attempts to tweet out something, if success then respond with tweet data.

#### <a name="tweet_like"></a> Like

| Method    | `POST`                  |
| :--       | :--                     |
| URL       | `/api/tweet/like/`      |

| Header          |                 |
| :--             | :--             |
| Authorization   | Token String?   |

| Request       |                 |
| :--           | :--             |
| likeTweetId   | String          |

| Response      |             |
| :--           | :--         |
| liked         | Boolean     |

User attempts to like sth => liked = true, if like already exists then => taking back the like, which means liked = false.
