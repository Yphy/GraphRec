# Instagram Cralwer

인스타그램 특정 유저의 포스트 정보와 특정 해시태그에 관한 포스트 정보를 크롤링하는 프로젝트

## Requirements
- Python 3.5+
```bash
$ pip install -r requirements.txt
```
- 내부적으로 selenium을 사용하여 크롤링하기 때문에 chromedriver 준비가 필요함. 크롤링 서버에 chrome이 설치되어 있어야 하며 chromedriver 버전은 chrome 버전에 맞는 드라이버를 설치해야함(https://chromedriver.chromium.org/downloads)

## Design Spectification

### User Crawling
- 특정 유저의 id는 유저의 페이지로 접속하여 url `instagram.com/`의 뒤쪽을 확인하면 추출 가능
- `insta_account.py`에서는 유저의 모든 포스트를 `requests` 라이브러리를 통해 크롤링
- 인스타그램에서는 query를 통해 포스트 정보를 받아올 수 있도록 api를 제공하며 코드 내부에서 확인 가능
- 한번 요청할 때 약 50개의 포스트 정보를 받을 수 있으며 포스트의 이미지 링크, 등록일, 입력 텍스트, 좋아요 수, 댓글 수와 같은 포스트 정보를 저장 가능
- 포스트를 크롤링할 때 이미지 링크를 크롤링하기 때문에 링크에 다시 접속하여 이미지를 받아옴

### Hashtag Crawling
- 특정 hashtags 검색 결과는 `instagram.com/tags/<query>/` 형태로 검색가능하며 실제로 해당 웹 사이트에 접근하여 태그 검색 결과를 받아옴
- selenium 라이브러리에 의해 모든 페이지 정보를 받아오면 크롬드라이버가 페이지 스크롤을 내리며 추가적인 포스트를 받아오고 포스트를 parsing하는 형태로 구현되어 있음
- 포스트 정보를 저장하는 과정은 user의 과정은 동일

## How to run the code
```bash
$ python insta_account.py
$ python main/run_insTag.py
```
- 각각 유저와 해시태그 정보를 받아오는 코드 실행 방법
- 크롤링 정보는 instagram에서 graphql을 통해 반환되는 정보로 확인 가능하며 아래 예시처럼 포스트 정보를 확인 가능
```json
{
   "node":{
      "comments_disabled":false,
      "__typename":"GraphImage",
      "id":"2322629956764872194",
      "edge_media_to_caption":{
         "edges":[
            {
               "node":{
                  "text":"Sadgril+halugril:// Im From Indonesian\u2728\n\n#fatehhalilintar #fat #fateh #hetaf #fatners #genhalilintar #genhalilintarstars #love #fashion #beauty #photography #photooftheday #loveyourself"
               }
            }
         ]
      },
      "shortcode":"CA7o6PNpq4C",
      "edge_media_to_comment":{
         "count":0
      },
      "taken_at_timestamp":1591099088,
      "dimensions":{
         "height":1080,
         "width":1080
      },
      "display_url":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/e35/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=35e0fcef8ab35cb8c2545443914e3a5c&oe=5F019B5C",
      "edge_liked_by":{
         "count":0
      },
      "edge_media_preview_like":{
         "count":0
      },
      "owner":{
         "id":"17786024726"
      },
      "thumbnail_src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/s640x640/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=fe3a44be65ddd8a2c0fcf7892ff24d73&oe=5EFF3562",
      "thumbnail_resources":[
         {
            "src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/e35/s150x150/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=d6f75b3a5a8776990130fc4b62b859eb&oe=5EFF3965",
            "config_width":150,
            "config_height":150
         },
         {
            "src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/e35/s240x240/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=78a7b6dbc25d5d562506edab398e553e&oe=5F01ACE3",
            "config_width":240,
            "config_height":240
         },
         {
            "src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/e35/s320x320/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=a17d98905cc0b648bc4f938bb07e0d9a&oe=5F01461D",
            "config_width":320,
            "config_height":320
         },
         {
            "src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/e35/s480x480/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=54cdd2b8d3ad173b28078a822cf3327e&oe=5EFE905C",
            "config_width":480,
            "config_height":480
         },
         {
            "src":"https://scontent-ssn1-1.cdninstagram.com/v/t51.2885-15/sh0.08/e35/s640x640/101517055_720126582066050_5861967196069035495_n.jpg?_nc_ht=scontent-ssn1-1.cdninstagram.com&_nc_cat=102&_nc_ohc=JKq8QIePV6cAX9ypkKa&oh=fe3a44be65ddd8a2c0fcf7892ff24d73&oe=5EFF3562",
            "config_width":640,
            "config_height":640
         }
      ],
      "is_video":false,
      "accessibility_caption":"Photo shared by Ily<3 on June 02, 2020 tagging @genifaruk, @genhalilintar, @halilintarasmid, @fatehhalilintar, and @fatehrandom. \uc0ac\uc9c4 \uc124\uba85\uc774 \uc5c6\uc2b5\ub2c8\ub2e4."
   }
}
```
