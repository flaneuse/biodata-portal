'''
    Elasticsearch Document Object Model

    - The ES backend is a collection of these documents
    - There are two indexes for schemas and classes each

    Reference: https://schema.org/docs/datamodel.html

'''
import gzip
import hashlib
import json
import logging
from datetime import datetime

from discovery.api.adapters import ClassInfoDict

from elasticsearch_dsl import (Binary, Date, Document, InnerDoc, Keyword,
                               Nested, Object, Text, Boolean)

LOGGER = logging.getLogger(__name__)


class DocumentMeta(InnerDoc):
    '''
        The Metadata of a Schema or Dataset

        - Excluded from the default search fields.
        - Timestamp corresponds to ~raw processing time.

    '''
    url = Text()
    username = Keyword(required=True)
    timestamp = Date()

    def stamp(self):
        '''
        Record current datetime.
        '''
        self.timestamp = datetime.now()


class Schema(Document):
    '''
        A Top-Level Schema
        https://schema.org/docs/schemas.html
    '''
    _meta = Object(DocumentMeta, required=True)
    context = Object(enabled=False)
    locals()['~raw'] = Binary()

    # _id : schema namespace, provided by the front-end when registering
    #       accessible through constructor argument 'id' or schema.meta.id

    class Index:
        '''
        Associated ES Index
        '''
        name = 'discover_schema'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def gather_contexts(cls):

        contexts = dict()

        context_list = [
            schema.context.to_dict()
            for schema in cls.search()
        ]

        for context in context_list:
            contexts.update(context)

        contexts.update({
            "schema": "http://schema.org/",
        })

        return {k: v for k, v in contexts.items() if v}

    def encode_raw(self, text):
        '''
        Encode and save the original schema.
        Refresh timestamp in _meta field.
        Return the encoded binary.
        '''
        assert isinstance(text, str)
        _raw = gzip.compress(text.encode())
        self['~raw'] = _raw
        self._meta.stamp()
        return _raw

    def decode_raw(self):
        '''
        Decode the compressed raw definition.
        Return decoded json saved in _raw field.
        '''
        if '~raw' in self:
            return json.loads(gzip.decompress(self['~raw']).decode())
        return None

    def save(self, *args, **kwargs):
        assert self.meta.id
        return super().save(*args, **kwargs)


class SchemaClassProp(InnerDoc):
    '''
    A Class Property for SchemaClass
    '''
    uri = Text()
    curie = Text(required=True)
    label = Text()
    range = Text(multi=True)
    description = Text()


class SchemaClass(Document):
    '''
        A Class(Type) in a Schema
        https://schema.org/docs/full.html
    '''

    # _id : in the format of <namespace>::<prefix>:<label>, for example, schema:Thing
    #       accessible through constructor argument 'id' or cls.meta.id

    namespace = Text(required=True)  # the _id of the schema document defining the class
    prefix = Text(required=True)
    label = Text(required=True)
    uri = Text()
    description = Text()
    parent_classes = Text(multi=True)  # immediate ones only
    properties = Nested(SchemaClassProp)  # immediate ones only
    validation = Object(enabled=False)
    ref = Boolean()

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_class'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def delete_by_schema(cls, namespace):
        '''
        Delete all classes of the specified namespace.
        '''
        existing_classes = cls.search().query("match", namespace=namespace)
        existing_classes.delete()

        LOGGER.info("Deleted %s classes from namespace %s.",
                    existing_classes.count(), namespace)

    @classmethod
    def import_classes(cls, parser, namespace):

        defined_classes = parser.list_all_defined_classes()
        referenced_classes = (parser.list_all_referenced_classes()
                              + sum([klass.ancestor_classes for klass in defined_classes], []))

        defined_info = {ClassInfoDict(klass, ref=False, namespace=namespace)
                        for klass in defined_classes}
        referenced_info = {ClassInfoDict(klass, ref=True, namespace=namespace)
                           for klass in referenced_classes}

        LOGGER.info("Found %s defined classes: %s", len(defined_info), defined_info)
        LOGGER.info("Found %s referenced classes: %s", len(referenced_info), referenced_info)

        defined_list = [cls(**info) for info in defined_info]
        referenced_list = [cls(**info) for info in referenced_info]

        return defined_list + referenced_list

    def save(self, **kwargs):

        self.meta.id = f"{self.namespace}::{self.prefix}:{self.label}"
        return super().save(**kwargs)


class DatasetMetadata(Document):
    '''
        Documents of a certain Schema
    '''
    _meta = Object(DocumentMeta, required=True)
    identifier = Text(required=True)
    name = Text()
    description = Text()
    _raw = Object(enabled=False)

    class Index:
        '''
        Associated ES index
        '''
        name = 'discover_metadata'
        settings = {
            "number_of_replicas": 0
        }

    @classmethod
    def from_json(cls, doc, user):
        meta = cls()
        meta.identifier = doc['identifier']
        meta.name = doc['name']
        meta.description = doc['description']
        meta._meta.username = user
        meta._raw = doc
        return meta

    def to_json(self):
        assert self.meta.id
        json = {'_id': self.meta.id}
        json.update(self.to_dict()['_raw'])
        return json

    def save(self, **kwargs):
        '''
        Create _id basing on identifier
        '''
        self.meta.id = hashlib.blake2b(
            self.identifier.encode(), digest_size=8).hexdigest()
        return super().save(**kwargs)
