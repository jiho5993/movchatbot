def basicOutput(output):
    result = {
        "version": "2.0",
        "template": {
            "outputs": output
        }
    }

    return result

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