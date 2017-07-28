from check import check_jsons

BEFORE_PAYLOAD = """
[
  {
    "status": "active",
    "name": "State of Anarchy",
    "price": 2500,
    "url": "http://store.steampowered.com/app/463210/State_of_Anarchy/",
    "platforms": [
      "windows",
      "mac"
    ]
  },
  {
    "status": "active",
    "name": "There's Poop In My Soup",
    "price": 3000,
    "url": "http://store.steampowered.com/app/449540/Theres_Poop_In_My_Soup/",
    "platforms": [
      "windows",
      "mac"
    ]
  }
]
"""

LESS_PAYLOAD = """
[
  {
    "status": "active",
    "name": "State of Anarchy",
    "price": 2500,
    "url": "http://store.steampowered.com/app/463210/State_of_Anarchy/",
    "platforms": [
      "windows",
      "mac"
    ]
  }
]
"""

MORE_PAYLOAD = """
[
  {
    "status": "active",
    "name": "State of Anarchy",
    "price": 2500,
    "url": "http://store.steampowered.com/app/463210/State_of_Anarchy/",
    "platforms": [
      "windows",
      "mac"
    ]
  },
  {
    "status": "active",
    "name": "I, Zombie",
    "price": 3000,
    "url": "http://store.steampowered.com/app/307230/I_Zombie/",
    "platforms": [
      "windows",
      "mac"
    ]
  },
  {
    "status": "active",
    "name": "There's Poop In My Soup",
    "price": 3000,
    "url": "http://store.steampowered.com/app/449540/Theres_Poop_In_My_Soup/",
    "platforms": [
      "windows",
      "mac"
    ]
  }
]
"""

PREVIEW_PAYLOAD = """
[
{
  "status": "preview",
  "name": null,
  "price": 2500,
  "url": null,
  "platforms": null
},
{
  "status": "preview",
  "name": null,
  "price": 3000,
  "url": null,
  "platforms": null
},
{
  "status": "active",
  "name": "There's Poop In My Soup",
  "price": 3000,
  "url": "http://store.steampowered.com/app/449540/Theres_Poop_In_My_Soup/",
  "platforms": [
    "windows",
    "mac"
  ]
}
]
"""

REAL_PREVIEW_PAYLOAD = """
[
  {
    "status": "preview",
    "name": null,
    "price": 3500,
    "url": null,
    "platforms": null
  },
  {
    "status": "preview",
    "name": null,
    "price": 4500,
    "url": null,
    "platforms": null
  },
  {
    "status": "preview",
    "name": null,
    "price": 3000,
    "url": null,
    "platforms": null
  },
  {
    "status": "active",
    "name": "State of Anarchy",
    "price": 2500,
    "url": "http://store.steampowered.com/app/463210/State_of_Anarchy/",
    "platforms": [
      "windows",
      "mac"
    ]
  },
  {
    "status": "active",
    "name": "I, Zombie",
    "price": 3000,
    "url": "http://store.steampowered.com/app/307230/I_Zombie/",
    "platforms": [
      "windows",
      "mac"
    ]
  },
  {
    "status": "active",
    "name": "There's Poop In My Soup",
    "price": 3000,
    "url": "http://store.steampowered.com/app/449540/Theres_Poop_In_My_Soup/",
    "platforms": [
      "windows",
      "mac"
    ]
  }
]
"""

# TODO
BOTH_PAYLOAD = """
"""

def test_more():
    added, removed = check_jsons(BEFORE_PAYLOAD, MORE_PAYLOAD)
    assert len(added) == 1
    assert added[0]['name'] == 'I, Zombie'
    assert added[0]['url'] == "http://store.steampowered.com/app/307230/I_Zombie/"
    assert len(removed) == 0

def test_preview():
    added, removed = check_jsons(BEFORE_PAYLOAD, PREVIEW_PAYLOAD)
    assert len(added) == 2
    assert added[0]['name'] == None
    assert added[0]['url'] == None
    assert added[0]['status'] == 'preview'
    assert added[1]['name'] == None
    assert added[1]['url'] == None
    assert added[1]['status'] == 'preview'
    assert len(removed) == 1
    assert removed[0]['name'] == "State of Anarchy"

def test_real_preview():
    added, removed = check_jsons(MORE_PAYLOAD, REAL_PREVIEW_PAYLOAD)
    assert len(added) == 3
    assert len(removed) == 0
    for item in added:
        assert item['name'] == None
        assert item['url'] == None
        assert item['status'] == 'preview'

def test_end_preview():
    added, removed = check_jsons(PREVIEW_PAYLOAD, MORE_PAYLOAD)
    assert len(added) == 2
    assert len(removed) == 2
    for item in removed:
        assert item['name'] == None
        assert item['url'] == None
        assert item['status'] == 'preview'
    assert added[0]['name'] == "State of Anarchy"
    assert added[1]['name'] == "I, Zombie"


def test_repeat_preview():
    added, removed = check_jsons(REAL_PREVIEW_PAYLOAD, REAL_PREVIEW_PAYLOAD)
    assert len(added) == 0
    assert len(removed) == 0

def test_less():
    added, removed = check_jsons(BEFORE_PAYLOAD, LESS_PAYLOAD)
    assert len(added) == 0
    assert len(removed) == 1
    assert removed[0]['name'] == "There's Poop In My Soup"
    assert removed[0]['url'] == "http://store.steampowered.com/app/449540/Theres_Poop_In_My_Soup/"
