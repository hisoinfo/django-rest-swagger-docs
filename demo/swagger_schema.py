import yaml

from rest_framework.compat import coreapi, urlparse
from rest_framework.schemas import SchemaGenerator
from rest_framework_swagger import renderers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.permissions import AllowAny


from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.schemas import SchemaGenerator
from urllib.parse import urljoin
import yaml
import coreapi

'''
class CustomSchemaGenerator(SchemaGenerator):
    def get_link(self, path, method, view):
        fields = self.get_path_fields(path, method, view)
        yaml_doc = None
        if view and view.__doc__:
            try:
                yaml_doc = yaml.load(view.__doc__)
            except:
                yaml_doc = None

        #Extract schema information from yaml

        if yaml_doc and type(yaml_doc) != str:
            _method_desc = yaml_doc.get('description', '')
            params = yaml_doc.get('parameters', [])

            for i in params:
                _name = i.get('name')
                _desc = i.get('description')
                _required = i.get('required', False)
                _type = i.get('type', 'string')
                _location = i.get('location', 'form')
                field = coreapi.Field(
                    name=_name,
                    location=_location,
                    required=_required,
                    description=_desc,
                    type=_type
                )
                fields.append(field)
        else:

            _method_desc = view.__doc__ if view and view.__doc__ else ''
            fields += self.get_serializer_fields(path, method, view)

        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=_method_desc
        )


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Return schema view which renders Swagger/OpenAPI.
    """
    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            renderers.JSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = CustomSchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()

'''

from django.contrib.admindocs.utils import trim_docstring
from rest_framework import exceptions, renderers, serializers
from rest_framework.schemas import (SchemaGenerator as BaseSchemaGenerator, 
    get_pk_name)
from rest_framework.compat import (coreapi, urlparse)
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework_swagger import renderers


class SchemaGenerator(BaseSchemaGenerator):
    '''
        自定义
    '''

    def coerce_path(self, path, method, view):
        """
        Coerce {pk} path arguments into the name of the model field,
        where possible. This is cleaner for an external representation.
        (Ie. "this is an identifier", not "this is a database primary key")
        """
        if not self.coerce_path_pk or '{pk}' not in path:
            return path

        model = getattr(getattr(view, 'queryset', None), 'model', None)
        if model:
            field_name = get_pk_name(model)
            path = path.replace('{pk}', '{%s}' % field_name)

        return path


    def get_link(self, path, method, view):
        """
        Return a `coreapi.Link` instance for the given endpoint.
        """
        fields = self.get_path_fields(path, method, view)
        fields += self.get_serializer_fields(path, method, view)
        fields += self.get_pagination_fields(path, method, view)
        fields += self.get_filter_fields(path, method, view)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method, view)
        else:
            encoding = None

        description = self.get_description(path, method, view)

        # bubble modify(add)
        if description and len(description) > 0:
            query_fields, description = self.get_docstring_fields(
                description)
            fields += query_fields
        # modify finish

        if self.url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(self.url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )


    def get_docstring_fields(self, description):
        # bubble modify(add) 
        fields = []
        split_lines = trim_docstring(description).split('\n')
        temp_lines = []

        for line in split_lines:
            param = line.split(' -- ')
            if len(param) == 2:
                fields.append(coreapi.Field(name=param[0].strip(),
                                            required=False,
                                            location='query',
                                            description=param[1].strip()))
            else:
                temp_lines.append(line)
                temp_lines.append('\n')

        description = ''.join(temp_lines)

        return fields, description


def get_swagger_view(title=None, url=None):
    """
    Returns schema view which renders Swagger/OpenAPI.

    (Replace with DRF get_schema_view shortcut in 3.5)
    """
    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            # bubble modify (SchemaGenerator->CustomerSchemaGenerator)
            generator = SchemaGenerator(title=title, url=url)
            # bubble modify end
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()