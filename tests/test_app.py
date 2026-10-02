import os
import sqlite3
import tempfile
import unittest
from contextlib import contextmanager

_import_database_dir = tempfile.TemporaryDirectory()
_previous_database_url = os.environ.get("DATABASE_URL")
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_import_database_dir.name, "module.db")
try:
    from app import SURVEY_COLUMNS, app as module_app, create_app
finally:
    if _previous_database_url is None:
        os.environ.pop("DATABASE_URL", None)
    else:
        os.environ["DATABASE_URL"] = _previous_database_url


@contextmanager
def sqlite_db(path):
    conn = sqlite3.connect(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


class AppFlowsTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        module_app.extensions["wohelp_engine"].dispose()
        _import_database_dir.cleanup()

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.tempdir.name, "test.db")
        self.app = create_app({
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "DATABASE_URL": "sqlite:///" + self.db_path,
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.app.extensions["wohelp_engine"].dispose()
        self.tempdir.cleanup()

    @staticmethod
    def registration_data(**changes):
        data = {
            "nome": "Estudante Teste",
            "idade": "17",
            "curso": "Eletromecânica",
            "turma": "2",
            "aspiracao": "Ser engenheira",
            "universidade": "",
            "interesse_area_tecnica": "Não",
            "motivo_desinteresse": "Exemplo de motivo",
            "continuar_estudos": "Sim",
            "motivo_continuar_estudos": "",
            "violencia_curso": "Não",
            "motivo_violencia_curso": "",
            "violencia_futura": "Sim",
            "motivo_violencia_futura": "Exemplo de resposta",
        }
        data.update(changes)
        return data

    def test_registration_saves_one_student_and_preserves_profile_session_and_chat(self):
        response = self.client.post("/cadastrar", data=self.registration_data())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/"))
        inicio = self.client.get("/")
        self.assertIn(b"Trabalho de Fabiana Costa", inicio.data)

        with sqlite_db(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM alunos").fetchall()
            self.assertEqual(len(rows), 1)
            student = rows[0]
            self.assertEqual(student["nome"], "Estudante Teste")
            self.assertEqual(student["curso"], "Eletromecânica")
            self.assertEqual(student["turma"], "2")
            self.assertEqual(student["interesse_area_tecnica"], "Não")
            self.assertEqual(student["motivo_desinteresse"], "Exemplo de motivo")
            self.assertEqual(student["continuar_estudos"], "Sim")
            self.assertEqual(student["motivo_continuar_estudos"], "")
            self.assertEqual(student["violencia_curso"], "Não")
            self.assertEqual(student["motivo_violencia_curso"], "")
            self.assertEqual(student["violencia_futura"], "Sim")
            self.assertEqual(student["motivo_violencia_futura"], "Exemplo de resposta")
            student_id = student["id"]
            analise = conn.execute("SELECT * FROM dados_pesquisa WHERE id = ?", (student_id,)).fetchone()
            analysis_fields = {row[1] for row in conn.execute("PRAGMA table_info(dados_pesquisa)")}
            self.assertNotIn("nome", analysis_fields)
            self.assertNotIn("aspiracao", analysis_fields)
            self.assertEqual(analise["id"], student_id)
            self.assertEqual(analise["motivo_desinteresse"], "Exemplo de motivo")

        with self.client.session_transaction() as session:
            self.assertEqual(session["aluno_id"], student_id)

        profile = self.client.get("/perfil")
        self.assertEqual(profile.status_code, 200)
        self.assertIn(b"Estudante Teste", profile.data)

        updated = self.client.post("/perfil/atualizar", data={
            "nome": "Estudante Atualizada", "idade": "18",
            "aspiracao": "Liderar projetos", "universidade": "UFBA",
        })
        self.assertEqual(updated.status_code, 302)
        with sqlite_db(self.db_path) as conn:
            student = conn.execute(
                "SELECT nome, idade, curso, interesse_area_tecnica, motivo_desinteresse FROM alunos WHERE id = ?",
                (student_id,),
            ).fetchone()
            self.assertEqual(student, ("Estudante Atualizada", 18, "Eletromecânica", "Não", "Exemplo de motivo"))

        message = self.client.post("/api/chat", json={"mensagem": "Olá, WoHelp!"})
        self.assertEqual(message.status_code, 201)
        self.assertEqual(message.get_json()["mensagem"]["aluno_id"], student_id)
        chat = self.client.get("/api/chat")
        self.assertEqual(chat.status_code, 200)
        self.assertEqual(chat.get_json()["mensagens"][0]["aluno_id"], student_id)
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok"})

    def test_html_form_has_two_guided_steps_and_four_binary_questions(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('id="cad-etapa-1"', html)
        self.assertIn('id="cad-etapa-2"', html)
        self.assertIn('id="cad-continuar"', html)
        self.assertIn('id="cad-continuar" aria-controls="cad-etapa-2"', html)
        self.assertIn('<button type="button" class="btn-principal" id="cad-continuar"', html)
        self.assertIn('type="button" class="btn-principal cad-voltar"', html)
        self.assertIn('name="interesse_area_tecnica" value="Sim"', html)
        self.assertIn('name="continuar_estudos" value="Não"', html)
        self.assertIn('name="violencia_curso" value="Sim"', html)
        self.assertIn('name="violencia_futura" value="Não"', html)
        self.assertIn("As respostas são associadas ao ID numérico do cadastro", html)
        self.assertNotIn('id="btn-pesquisa"', html)
        self.assertEqual(self.client.get("/pesquisa").status_code, 404)
        self.assertEqual(self.client.get("/admin/pesquisa").status_code, 404)
        with sqlite_db(self.db_path) as conn:
            app_tables = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )}
            views = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='view'"
            )}
        self.assertEqual(app_tables, {"alunos", "mensagens"})
        self.assertEqual(views, {"dados_pesquisa"})

    def test_backend_requires_core_answers_and_allows_optional_violence_responses(self):
        missing_answer = self.registration_data(violencia_curso="talvez")
        response = self.client.post("/cadastrar", data=missing_answer)
        self.assertEqual(response.status_code, 400)

        missing_reason = self.registration_data(motivo_desinteresse="  ")
        response = self.client.post("/cadastrar", data=missing_reason)
        self.assertEqual(response.status_code, 400)

        optional_violence = self.registration_data(
            violencia_curso="Sim", motivo_violencia_curso="",
            violencia_futura="", motivo_violencia_futura="",
        )
        response = self.client.post("/cadastrar", data=optional_violence)
        self.assertEqual(response.status_code, 302)

        with sqlite_db(self.db_path) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0], 1)

    def test_motives_for_unselected_conditions_are_cleared(self):
        data = self.registration_data(
            interesse_area_tecnica="Sim", motivo_desinteresse="resíduo",
            continuar_estudos="Sim", motivo_continuar_estudos="resíduo",
            violencia_curso="Não", motivo_violencia_curso="resíduo",
            violencia_futura="Não", motivo_violencia_futura="resíduo",
        )
        response = self.client.post("/cadastrar", data=data)
        self.assertEqual(response.status_code, 302)
        with sqlite_db(self.db_path) as conn:
            stored = conn.execute(
                "SELECT motivo_desinteresse, motivo_continuar_estudos, motivo_violencia_curso, motivo_violencia_futura FROM alunos"
            ).fetchone()
        self.assertEqual(stored, ("", "", "", ""))

    def test_startup_adds_missing_columns_without_replacing_legacy_records_or_tables(self):
        legacy_path = os.path.join(self.tempdir.name, "legacy.db")
        with sqlite_db(legacy_path) as conn:
            conn.execute("CREATE TABLE alunos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, idade INTEGER NOT NULL)")
            conn.execute("INSERT INTO alunos (id, nome, idade) VALUES (7, 'Registro Antigo', 19)")
            conn.execute("CREATE VIEW dados_pesquisa AS SELECT id, nome FROM alunos")
            conn.execute("CREATE TABLE mensagens (id INTEGER PRIMARY KEY, aluno_id INTEGER NOT NULL, mensagem TEXT NOT NULL)")
            conn.execute("INSERT INTO mensagens (id, aluno_id, mensagem) VALUES (9, 7, 'mensagem antiga')")
            conn.execute("CREATE TABLE contas (id INTEGER PRIMARY KEY, username TEXT UNIQUE)")
            conn.execute("CREATE TABLE respostas (id TEXT PRIMARY KEY, versao TEXT NOT NULL)")
            conn.execute("CREATE TABLE respostas_itens (resposta_id TEXT, campo TEXT, valor TEXT)")

        app = create_app({"TESTING": True, "DATABASE_URL": "sqlite:///" + legacy_path})
        try:
            with sqlite_db(legacy_path) as conn:
                columns = {row[1] for row in conn.execute("PRAGMA table_info(alunos)")}
                self.assertTrue(set(SURVEY_COLUMNS).issubset(columns))
                self.assertEqual(conn.execute("SELECT id, nome, idade FROM alunos").fetchone(), (7, "Registro Antigo", 19))
                self.assertEqual(conn.execute("SELECT id, aluno_id, mensagem FROM mensagens").fetchone(),
                                 (9, 7, "mensagem antiga"))
                analysis_fields = {row[1] for row in conn.execute("PRAGMA table_info(dados_pesquisa)")}
                self.assertEqual(analysis_fields, {"id", "idade", *SURVEY_COLUMNS})
                self.assertNotIn("nome", analysis_fields)
                tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                self.assertNotIn("contas", tables)
                self.assertNotIn("pesquisa", tables)
                self.assertNotIn("respostas", tables)
                self.assertNotIn("respostas_itens", tables)
        finally:
            app.extensions["wohelp_engine"].dispose()

    def test_startup_preserves_populated_legacy_survey_tables(self):
        legacy_path = os.path.join(self.tempdir.name, "legacy-with-responses.db")
        with sqlite_db(legacy_path) as conn:
            conn.execute("CREATE TABLE contas (id INTEGER PRIMARY KEY, username TEXT UNIQUE)")
            conn.execute("INSERT INTO contas VALUES (3, 'legado')")
            conn.execute("CREATE TABLE respostas (id TEXT PRIMARY KEY, versao TEXT NOT NULL)")
            conn.execute("CREATE TABLE respostas_itens (resposta_id TEXT, campo TEXT, valor TEXT)")
            conn.execute("INSERT INTO respostas VALUES ('legado', '1')")
            conn.execute("INSERT INTO respostas_itens VALUES ('legado', 'campo', 'valor')")

        app = create_app({"TESTING": True, "DATABASE_URL": "sqlite:///" + legacy_path})
        try:
            with sqlite_db(legacy_path) as conn:
                self.assertEqual(conn.execute("SELECT id, username FROM contas").fetchone(), (3, "legado"))
                self.assertEqual(conn.execute("SELECT id, versao FROM respostas").fetchone(), ("legado", "1"))
                self.assertEqual(conn.execute("SELECT resposta_id, campo, valor FROM respostas_itens").fetchone(),
                                 ("legado", "campo", "valor"))
        finally:
            app.extensions["wohelp_engine"].dispose()


if __name__ == "__main__":
    unittest.main()
