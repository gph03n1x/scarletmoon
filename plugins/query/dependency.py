try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
except ImportError:
    SPACY_INSTALLED = False
else:
    SPACY_INSTALLED = True
from moon import plugins
from moon.queries.querying import AND_OPERATION




class DependencyFilter(plugins.PluginQuery):
    name = "Dependency filter"
    enabled = SPACY_INSTALLED

    @staticmethod
    def reconstruct_query(sent):
        allowed_dependencies = ["ROOT", "pcomp", "dobj", "nsubj"]

        doc = nlp(sent)
        sub_tokens = [str(tok) for tok in doc if (tok.dep_ in allowed_dependencies)]
        for position in range(len(sub_tokens), 0, -1):
            sub_tokens.insert(position, AND_OPERATION)

        return " ".join(sub_tokens)

    @staticmethod
    def can_handle(query):
        if ">" in query or "<" in query:
            return False
        return True
