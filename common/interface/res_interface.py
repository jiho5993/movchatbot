# https://chatbot.kakao.com/docs/skill-response-format#simpletext
def basicOutput(output, quickReplies=None):
    if quickReplies is not None:
        result = {
            "version": "2.0",
            "template": {
                "outputs": output,
                "quickReplies": quickReplies
            }
        }
    else:
        result = {
            "version": "2.0",
            "template": {
                "outputs": output,

            }
        }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#carousel
def carouselOutput(type, output):
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": type,
                        "items": output
                    }
                }
            ]
        }
    }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#예제코드-1
def TextAndCarouselOutput(type, output, text):
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                },
                {
                    "carousel": {
                        "type": type,
                        "items": output
                    }
                }
            ]
        }
    }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#quickreplies
def QuickRepliesAndCarouselOutput(type, output, quickReplies):
    result = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": type,
                        "items": output
                    }
                }
            ],
            "quickReplies": quickReplies
        }
    }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#basiccard
def basicCard(title, desc, img, btnList):
    result = {
        "title": title,
        "description": desc,
        "thumbnail": {
            "imageUrl": img
        },
        "buttons": btnList
    }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#itemcard
def itemCard(title, desc, img, itemList, btnList):
    result = {
        "imageTitle": {
            "title": title,
            "description": desc
        },
        "thumbnail": {
            "imageUrl": img,
            "width": 800,
            "height": 400
        },
        "itemList": itemList,
        "buttons": btnList
    }

    return result

# https://chatbot.kakao.com/docs/skill-response-format#quickreplies
def quickReplies(label, msgText, blockId, action="block"):
    if action == 'block':
        result = {
            "label": label,
            "action": 'block',
            "messageText": msgText,
            "blockId": blockId
        }
    else:
        result = {
            "label": label,
            "action": 'message',
            "messageText": msgText,
        }

    return result