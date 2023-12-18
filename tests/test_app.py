import requests
import pytest


@pytest.mark.parametrize(
    "parameter, expected_status",
    [
        ("names=a,b", 200),
        ("names=a,b&avatars=01.png,02.png", 200),
        ("names=a,b&avatars=a,b", 500),
        ("names=a,b&avatars=01.png,02.png&words=True", 200),
        ("names=a,b&avatars=01.png,02.png&words=True&card_mode=True", 200),
    ],
)
def test_init_engine(parameter, expected_status):
    resp = requests.post(f"http://127.0.0.1:5000/init_engine?{parameter}")
    assert resp.status_code == expected_status


def test_reset_word():
    resp = requests.get(f"http://127.0.0.1:5000/reset_word")
    assert resp.status_code == 200


@pytest.mark.parametrize(
    "parameter, expected_status", [("word=a", 200), ("word=b", 200), ("word=a", 500),],
)
def test_add(parameter, expected_status):
    resp = requests.post(f"http://127.0.0.1:5000/add?{parameter}")
    assert resp.status_code == expected_status


def test_random():
    requests.post("http://127.0.0.1:5000/init_engine?names=a,b&words=True")
    requests.post("http://127.0.0.1:5000/add?word=test1")
    requests.post("http://127.0.0.1:5000/add?word=test2")
    requests.post("http://127.0.0.1:5000/add?word=test3")
    resp = requests.get(f"http://127.0.0.1:5000/random")
    data = resp.json()
    assert resp.status_code == 200
    assert list(data.keys()) == ["message", "player"]
    resp = requests.get(f"http://127.0.0.1:5000/random")
    assert resp.status_code == 500


def test_random_card():
    requests.post(
        "http://127.0.0.1:5000/init_engine?names=a,b&words=True&card_mode=True"
    )
    resp = requests.get(f"http://127.0.0.1:5000/random_card")
    data = resp.json()
    assert resp.status_code == 200
    assert list(data.keys()) == ["message", "player"]
