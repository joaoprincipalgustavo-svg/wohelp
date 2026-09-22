import os
import tempfile
import unittest

from app import create_app


class AppFlowsTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE_URL": "sqlite:///" + os.path.join(self.tempdir.name, "test.db"),
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_json_registration_and_profile_update(self):
        response = self.client.post("/api/alunos", json={
            "nome": "  maria silva ", "idade": 22,
            "aspiracao": "ser engenheira", "universidade": "ufba",
        })
        self.assertEqual(response.status_code, 201)
        profile = response.get_json()["aluno"]
        self.assertEqual(profile["nome"], "Maria Silva")
        self.assertEqual(profile["universidade"], "Ufba")
        self.assertGreater(profile["id"], 0)

        response = self.client.get("/api/perfil")
        self.assertEqual(response.get_json()["aluno"]["id"], profile["id"])
        response = self.client.patch("/api/perfil", json={
            "nome": "Maria Souza", "idade": 23,
            "aspiracao": "ser pesquisadora", "universidade": "ufba",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["aluno"]["idade"], 23)

    def test_validation_and_html_registration(self):
        bad = self.client.post("/api/alunos", json={"nome": "", "idade": 500, "aspiracao": ""})
        self.assertEqual(bad.status_code, 400)
        html = self.client.post("/cadastrar", data={
            "nome": "ana", "idade": "20", "aspiracao": "estudar", "universidade": "",
        })
        self.assertEqual(html.status_code, 302)
        self.assertIn("/perfil", html.headers["Location"])

    def test_health(self):
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
