import jsonpickle
from google.cloud import ndb
from storage.db import OptionsEntity, RetrievalConfigEntity, TemplateEntity
from data import Options, RetrievalConfig, TemplateInstance


# TODO: support per-user options
USER_ID = 'test'
ndb_client = ndb.Client()


def store_options(options: Options):
    with ndb_client.context():
        entity = OptionsEntity.get_by_user_id(USER_ID)
        if entity is None:
            entity = OptionsEntity(
                user_id=USER_ID,
                google_model=options.google_model,
                openai_model=options.openai_model,
                cohere_model=options.cohere_model,
                temperature=options.temperature,
                token_limit=options.token_limit,
                top_k=options.top_k,
                top_p=options.top_p)
        else:
            entity.google_model = options.google_model
            entity.openai_model = options.openai_model
            entity.cohere_model = options.cohere_model
            entity.temperature = options.temperature
            entity.token_limit = options.token_limit
            entity.top_k = options.top_k
            entity.top_p = options.top_p
        entity.put()


def fetch_options():
    options = Options()
    with ndb_client.context():
        entity = OptionsEntity.get_by_user_id(USER_ID)
        if entity is not None:
            options.google_model = entity.google_model
            options.openai_model = entity.openai_model
            options.cohere_model = entity.cohere_model
            options.temperature = entity.temperature
            options.token_limit = entity.token_limit
            options.top_k = entity.top_k
            options.top_p = entity.top_p
        return options


def add_template(template: TemplateInstance):
    if not template.name:
        raise Exception("Template name is required.")
    with ndb_client.context():
        entity = TemplateEntity.get_by_name(template.name)
        if entity is not None:
            raise Exception("Duplicate template name.")
        examples = None
        if template.examples:
            examples = jsonpickle.encode(template.examples)
        entity = TemplateEntity(
                name=template.name,
                instruction=template.instruction,
                context=template.context,
                examples=examples)
        entity.put()


def update_template(template: TemplateInstance):
    if not template.name:
        raise Exception("Template name is required.")
    with ndb_client.context():
        entity = TemplateEntity.get_by_name(template.name)
        if entity is None:
            raise Exception("Cannot find template. You need to delete "
                            "the old one if you want to update name")
        examples = None
        if template.examples:
            examples = jsonpickle.encode(template.examples)
        entity.instruction = template.instruction
        entity.context = template.context
        entity.examples = examples
        entity.put()


def fetch_template(name: str):
    template = TemplateInstance('', '', '', None)
    with ndb_client.context():
        entity = TemplateEntity.get_by_name(name)
        if entity is not None:
            template.name = entity.name
            template.instruction = entity.instruction
            template.context = entity.context
            if entity.examples:
                template.examples = jsonpickle.decode(entity.examples)
        return template


def delete_template(name):
    if not name:
        raise Exception("Template name is required.")
    with ndb_client.context():
        entity = TemplateEntity.get_by_name(name)
        if entity is None:
            raise Exception("Cannot find template.")
        entity.key.delete()


def list_templates():
    with ndb_client.context():
        names = map(lambda tmpl: tmpl.name, TemplateEntity.query().fetch())
        return names


def add_retrieval(retrieval: RetrievalConfig):
    if not retrieval.name:
        raise Exception("RetrievalConfig name is required.")
    with ndb_client.context():
        entity = RetrievalConfigEntity.get_by_name(retrieval.name)
        if entity is not None:
            raise Exception("Duplicate retrieval config name.")
        urls = jsonpickle.encode(retrieval.urls)
        entity = RetrievalConfigEntity(
            name=retrieval.name,
            urls=urls)
        entity.put()


def update_retrieval(retrieval: RetrievalConfig):
    if not retrieval.name:
        raise Exception("RetrievalConfig name is required.")
    with ndb_client.context():
        entity = RetrievalConfigEntity.get_by_name(retrieval.name)
        if entity is None:
            raise Exception("Cannot find the retrieval. You need to delete "
                            "the old one if you want to update name")
        entity.urls = jsonpickle.encode(retrieval.urls)
        entity.put()


def fetch_retrieval(name: str):
    retrieval = RetrievalConfig('', None)
    with ndb_client.context():
        entity = RetrievalConfigEntity.get_by_name(name)
        if entity is not None:
            retrieval.name = entity.name
            if entity.urls:
                retrieval.urls = jsonpickle.decode(entity.urls)
        return retrieval


def delete_retrieval(name):
    if not name:
        raise Exception("Retrieval name is required.")
    with ndb_client.context():
        entity = RetrievalConfigEntity.get_by_name(name)
        if entity is None:
            raise Exception("Cannot find retrieval.")
        entity.key.delete()


def list_retrievals():
    with ndb_client.context():
        names = map(lambda r: r.name, RetrievalConfigEntity.query().fetch())
        return names
