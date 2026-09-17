"""Endpoint and WebSocket checks for laboratory work № 6."""

import unittest

from fastapi.testclient import TestClient

from fastapi_app import app as api
from flask_app import app as flask


class WebTests(unittest.TestCase):
    def test_flask_pages(self):
        with flask.test_client() as client:
            self.assertIn("Привет Flask!".encode(), client.get("/hello").data)
            page = client.get("/")
            self.assertEqual(page.status_code, 200)
            self.assertIn(b"bootstrap@", page.data)

    def test_json_and_pydantic(self):
        with TestClient(api) as client:
            self.assertEqual(client.get("/api/info").json()["variant"], "5")
            valid = client.post("/api/messages", json={"author": "Андрей", "text": "Привет"})
            self.assertEqual(valid.status_code, 200)
            self.assertEqual(valid.json()["author"], "Андрей")
            invalid = client.post("/api/messages", json={"author": "", "text": ""})
            self.assertEqual(invalid.status_code, 422)

    def test_websocket_broadcast(self):
        with TestClient(api) as client:
            with client.websocket_connect("/ws") as first:
                with client.websocket_connect("/ws") as second:
                    first.send_json({"author": "А", "text": "Привет"})
                    self.assertEqual(first.receive_json()["text"], "Привет")
                    self.assertEqual(second.receive_json()["text"], "Привет")


if __name__ == "__main__":
    unittest.main()
