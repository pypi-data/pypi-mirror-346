import os
import sys
import re
import copy
import ntpath

import Orange.data
from Orange.data import StringVariable, Domain, Table
from AnyQt.QtWidgets import QApplication
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.llm import lmstudio
    from Orange.widgets.orangecontrib.AAIT.utils import thread_management
    from Orange.widgets.orangecontrib.AAIT.utils.import_uic import uic
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_local_store_path
    from Orange.widgets.orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
    from Orange.widgets.orangecontrib.AAIT.llm import answers, chunking, prompt_management
else:
    from orangecontrib.AAIT.llm import lmstudio
    from orangecontrib.AAIT.utils import thread_management
    from orangecontrib.AAIT.utils.import_uic import uic
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path
    from orangecontrib.AAIT.utils.initialize_from_ini import apply_modification_from_python_file
    from orangecontrib.AAIT.llm import answers


@apply_modification_from_python_file(filepath_original_widget=__file__)
class OWGenerateSynthesis(widget.OWWidget):
    name = "Generate Synthesis"
    description = "Generate Synthesis on the column 'content' of an input table"
    icon = "icons/owgeneratesynthesis.png"
    if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
        icon = "icons_dev/owgeneratesynthesis.png"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owgeneratesynthesis.ui")
    want_control_area = False
    priority = 1060

    class Inputs:
        data = Input("Data", Orange.data.Table)
        data_lmstudio = Input("Data for LMStudio", Orange.data.Table)
        model_path = Input("Model", str)
        embedder =Input("Embedder", SentenceTransformer, auto_summary=False)

    class Outputs:
        data = Output("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        self.data_lmstudio = None
        if self.autorun:
            self.run()

    @Inputs.data_lmstudio
    def set_data_lmstudio(self, in_data):
        self.data_lmstudio = in_data
        self.data = None
        if self.autorun:
            self.run()

    @Inputs.model_path
    def set_model_path(self, in_model_path):
        self.model_path = in_model_path
        #answers.check_gpu(in_model_path, self)
        if self.autorun:
            self.run()

    @Inputs.embedder
    def set_embedder(self, in_embedder):
        self.embedder = in_embedder
        if self.autorun:
            self.run()

    def __init__(self):
        super().__init__()
        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)

        # Data Management
        self.data = None
        self.data_lmstudio = None
        self.model_path = None
        self.embedder = None
        self.thread = None
        self.autorun = True
        self.use_gpu = False
        self.can_run = True
        self.result = None
        self.post_initialized()

    def run(self):
        self.error("")
        # Si un thread est en cours, on quitte
        if self.thread is not None:
            self.thread.safe_quit()
            return

        # Vérification des entrées
        if self.data is None and self.data_lmstudio is None:
            return

        if self.data and self.data_lmstudio:
            self.error('You cannot have both inputs Data and LMStudio.')
            return

        if self.model_path is None:
            return

        if self.embedder is None:
            return

        # Si LMStudio est utilisé : vérification des paramètres
        if self.data_lmstudio is not None:
            llm = 'lmstudio'
            data = self.data_lmstudio
            model_list = lmstudio.get_model_lmstudio()
            if isinstance(model_list, str) and model_list == "Error":
                self.error("Please launch the LMStudio app and start the server.")
                return
            # Vérification que le répertoire des modèles est défini dans LMStudio (aait_store)
            if model_list is None:
                self.error("Your models directory in LMStudio is not set properly.")
                return

            # Vérification que le modèle fourni existe dans la liste des modèles de LMStudio
            if not any(ntpath.basename(d["id"]).lower() == ntpath.basename(self.model_path.lower()) for d in model_list["data"]):
                self.error(f"Model not found in LMStudio. You are trying to use {ntpath.basename(self.model_path.lower())}, please verify that this model's API identifier exists in LMStudio.")
                return
            for d in model_list["data"]:
                if ntpath.basename(d["id"]).lower() == ntpath.basename(self.model_path.lower()):
                    self.model_path = d["id"]

        # Si GPT4All est utilisé
        if self.data is not None:
            llm = 'gpt4all'
            data = self.data

        # Vérification de la présence de la colonne "content"
        try:
            data.domain["content"]
        except KeyError:
            self.error('You need a "content" column in input data')
            return

        if type(data.domain["content"]).__name__ != 'StringVariable':
            self.error('"content" column needs to be a Text')
            return

        # Démarrage de la progress bar
        self.progressBarInit()

        # Lancement du thread avec la fonction principale
        self.thread = thread_management.Thread(self.generate_synthesis_on_table, data, self.model_path, self.embedder, llm)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def handle_progress(self, value: float) -> None:
        self.progressBarSet(value)

    def handle_result(self, result):
        try:
            self.result = result
            self.Outputs.data.send(result)
        except Exception as e:
            print("An error occurred when sending out_data:", e)
            self.Outputs.data.send(None)
            return

    def handle_finish(self):
        print("Question generation finished")
        self.progressBarFinished()
        self.thread = None

    def post_initialized(self):
        pass


    def generate_synthesis_on_table(self, table, model_path, embedder, llm="gpt4all", progress_callback=None, argself=None):
        """
        Applique la synthèse sur chaque ligne de la table et ajoute le résumé dans une nouvelle colonne.
        """
        # Copy of input data
        data = copy.deepcopy(table)
        new_metas = list(data.domain.metas) + [StringVariable("Synthesis")]
        new_domain = Domain(data.domain.attributes, data.domain.class_vars, new_metas)

        # Load model
        model = answers.load_model(model_path=model_path, use_gpu=True, n_ctx=25000)

        new_rows = []
        for i, row in enumerate(data):
            print(f"\n\n -- Working on row {i}")
            content = row["content"].value
            synthesis = self.generate_synthesis_on_row(content, model, embedder, max_tokens=4096, llm=llm)
            new_metas_values = list(row.metas) + [synthesis]
            new_instance = Orange.data.Instance(new_domain,
                                                [row[x] for x in data.domain.attributes] +
                                                [row[y] for y in data.domain.class_vars] +
                                                new_metas_values)
            new_rows.append(new_instance)
            if progress_callback is not None:
                progress_value = float(100 * (i + 1) / len(data))
                progress_callback(progress_value)
            if argself:
                if argself.stop:
                    break

        out_data = Table.from_list(domain=new_domain, rows=new_rows)
        return out_data

    def generate_synthesis_on_row(self, text, model, embedder, max_tokens=None, llm="gpt4all"):
        """
        Découpe le texte en chunks adaptés à la taille maximale en tokens
        et applique directement la synthèse en cascade sur ces chunks pour obtenir un résumé final.
        """
        # Utilisation de la valeur de self.context_length si max_tokens n'est pas spécifié
        if max_tokens is None:
            max_tokens = 4096

        # Découpage du texte en chunks avec marge de sécurité
        #chunks = self.split_text_into_chunks(text, max_tokens, safety_margin=1000, tokenizer=self.tokenizer)
        print(0)
        chunks, _ = chunking.chunk_tokens(text, embedder.tokenizer, chunk_size=25000, chunk_overlap=200)
        print("Chunked into", len(chunks), "chunks")

        # Application directe de la synthèse en cascade sur les chunks
        final_summary = self.cascade_summary_on_summaries(chunks, model, embedder, max_tokens=25000, llm=llm, safety_margin=1000)
        return final_summary

    def cascade_summary_on_summaries(self, texts, model, embedder, max_tokens=25000, llm="gpt4all", safety_margin=1000):
        """
        Condense de manière itérative une liste de textes (chunks ou résumés partiels)
        afin d'obtenir un résumé final qui tient dans la limite de tokens autorisée.
        """
        current_texts = texts
        if len(current_texts) == 1:
            return self.generate_synthesis_on_chunk(model, current_texts[0], llm=llm, max_tokens=4096, prompt_template=prompt4)
        while len(current_texts) > 1:
            print("Number of chunks left :", len(current_texts))
            new_texts = []
            batch = []
            batch_token_count = 0

            for txt in current_texts:
                token_count = len(embedder.tokenizer(txt)["input_ids"])
                print("Token count:", token_count)
                # Si le batch n'est pas vide et que l'ajout de ce texte dépasse la limite,
                # alors on résume le batch actuel
                if batch and (batch_token_count + token_count > max_tokens - safety_margin):
                    batch_text = "\n\n".join(batch)
                    summarized = self.generate_synthesis_on_chunk(model, batch_text, llm=llm, max_tokens=4096, prompt_template=prompt3)
                    new_texts.append(summarized)
                    batch = [txt]
                    batch_token_count = token_count
                else:
                    batch.append(txt)
                    batch_token_count += token_count

            # Résumé du dernier batch s'il n'est pas vide
            if batch:
                batch_text = "\n\n".join(batch)
                summarized = self.generate_synthesis_on_chunk(model, batch_text, llm=llm, max_tokens=4096, prompt_template=prompt4)
                new_texts.append(summarized)

            current_texts = new_texts
        return current_texts[0]


    def generate_synthesis_on_chunk(self, model, text, llm="gpt4all", max_tokens=None, temperature=0, top_p=0,
                                    top_k=50, stop_tokens=None, prompt_template=""):
        """
        Génère une synthèse à partir d'un chunk de texte en appelant le LLM.
        """
        # Utilisation de self.context_length si max_tokens n'est pas précisé
        if max_tokens is None:
            max_tokens = 4096

        prompt = format_prompt(prompt_template, text)

        if llm == "gpt4all":
            try:
                prompt = prompt_management.apply_prompt_template(self.model_path, user_prompt=prompt)
                answer = answers.run_query(prompt, model)
                return answer
            except Exception as e:
                return f"Error generating synthesis: {e}"

        if llm == "lmstudio":
            try:
                response = lmstudio.appel_lmstudio(prompt, self.model_path, max_tokens=max_tokens)
                return response
            except Exception as e:
                return f"Error generating synthesis: {e}"


def format_prompt(template: str, text: str) -> str:
    return template.format(text=text)

prompt1 = """### Contexte : Tu es un assistant de synthèse documentaire. Ton objectif est d'identifier et de lister les points essentiels d'un extrait de document envoyé par un User.


### Instructions :
- Lis le document qui suit.
- Liste les éléments essentiels sous la forme d'une liste avec des tirets.
- Répond dans la langue du document analysé.
- N'ajoute aucun commentaire à ta réponse.


### User : Voici un extrait de document.

{text}




### Assistant:"""

prompt2 = """### Contexte : Tu es un assistant de synthèse documentaire. Un User t'envoie une liste de tous les éléments essentiels contenus dans un document.

### Instructions :
- Lis la liste qui suit.
- Déduis de cette liste le résumé final du document complet.
- Rédige le résumé de façon structurée, en utilisant un format Markdown.
- N'ajoute aucun commentaire à ta réponse.


### User : Voici les éléments de mon document.

{text}



### Assistant :# Résumé du document"""


prompt3 = """### Contexte : Tu es un assistant de synthèse documentaire. Ton objectif est de résumer extrait de document envoyé par un User.


### Instructions :
- Lis l'extrait de document qui suit.
- Rédige un résumé du document.
- Répond dans la langue du document analysé.
- N'ajoute aucun commentaire à ta réponse.


### User : Voici un extrait de document.

{text}




### Assistant:# Résumé de l'extrait :"""

prompt4 = """### Contexte : Tu es un assistant de synthèse documentaire. Un User t'envoie un document qui a été résumé par parties. Ton objectif est de produire le résumé global.

### Instructions :
- Lis le texte qui suit.
- Déduis de ce texte le résumé final du document complet.
- Rédige le résumé de façon structurée, en utilisant un format Markdown.
- N'ajoute aucun commentaire à ta réponse.


### User : Voici le résumé par partie de mon document complet.

{text}



### Assistant :# Résumé du document"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWGenerateSynthesis()
    my_widget.show()
    app.exec_()

# local_store_path = get_local_store_path()
# model_name = "all-mpnet-base-v2"
# model_path = os.path.join(local_store_path, "Models", "NLP", model_name)
# model = SentenceTransformer(model_path)
# tokenizer = model.tokenizer
#
# T = "Une souris verte qui courait dans l'herbe"
# A = tokenizer(T, truncation=False)
# print(A)
# print(len(A["input_ids"]))