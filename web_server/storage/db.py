from google.cloud import ndb


class OptionsEntity(ndb.Model):
    """Models the prompt options of a user in the storage layer."""
    user_id = ndb.StringProperty()
    google_model = ndb.StringProperty()
    openai_model = ndb.StringProperty()
    cohere_model = ndb.StringProperty()
    temperature = ndb.FloatProperty()
    token_limit = ndb.IntegerProperty()
    top_k = ndb.IntegerProperty()
    top_p = ndb.FloatProperty()

    @classmethod
    def get_by_user_id(cls, userid):
        return cls.query(cls.user_id == userid).get()


class TemplateEntity(ndb.Model):
    """Class for prompt template in the storage layer."""
    name = ndb.StringProperty()
    instruction = ndb.StringProperty()
    context = ndb.StringProperty()
    examples = ndb.JsonProperty()

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name == name).get()


class RetrievalConfigEntity(ndb.Model):
    """Class for retrieval configuration in the storage layer."""
    name = ndb.StringProperty()
    urls = ndb.JsonProperty()

    @classmethod
    def get_by_name(cls, name):
        return cls.query(cls.name == name).get()
