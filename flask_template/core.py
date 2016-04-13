# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division, unicode_literals

from flask import request, redirect
from flask_admin.contrib import sqla
from flask_admin.form import SecureForm
from flask_admin.model import typefmt
from flask_login import current_user
from flask_mail import Mail
from flask_security import url_for_security
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry

#: Flask :class:`~flask_sqlalchemy.SQLAlchemy` extension instance.
db = SQLAlchemy()

#: Flask :class:`~flask_mail.Mail` extension instance.
mail = Mail()

#: :class:`~raven.contrib.flask.Sentry` logging instance.
sentry = Sentry()


class Service(object):
    """A :class:`.Service` instance encapsulates common :class:`~flask_sqlalchemy.SQLAlchemy` model operations in the
    context of a :class:`~flask.Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model. By default this method will raise a
        :class:`ValueError` if the model is not the expected type.

        :param model: The model instance to check.
        :type model: flask_sqlalchemy.Model
        :param raise_error: Flag to raise an error on a mismatch.
        :type raise_error: bool
        :return: ``True`` if ``model`` matches the service's model type. ``False`` otherwise.
        :raises ValueError: If ``raise_error=True`` and ``model`` does not match the service's model type.
        :rtype: bool
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    @staticmethod
    def _preprocess_params(kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default before creating a new instance or updating
        an existing instance.

        :param kwargs: a dictionary of parameters
        :type kwargs:dict
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.query.all()

    def get(self, id_):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id_: the instance id
        """
        return self.__model__.query.get(id_)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.query.filter_by(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.find(**kwargs).first()

    def get_or_404(self, id_):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id_: the instance id
        """
        return self.__model__.query.get_or_404(id_)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**self._preprocess_params(kwargs))  # pylint: disable=not-callable

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.save(self.new(**kwargs))

    def count(self):
        """Returns the row count of the service's model class."""
        return self.__model__.query.count()

    def update(self, model, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        self._isinstance(model)
        for key, value in self._preprocess_params(kwargs).items():
            setattr(model, key, value)
        self.save(model)
        return model

    def delete(self, model):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()

    def create_or_update(self, **kwargs):
        """Returns a new, saved instance of the service's model class if ``kwargs['id']`` does not exist in the db.
        Otherwise, the existing entry is updated with the values in ``kwargs``.

        :param **kwargs: instance parameters
        """
        model = self.get(kwargs.get('id', ''))
        if model:
            self.update(model, **kwargs)
        else:
            self.create(**kwargs)


class UserRoleViewMixin(object):
    __role__ = 'user'

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role(self.__role__)

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                # send 403 permission denied
                return self.inaccessible_callback(name, **kwargs)
            else:
                # redirect to login
                return redirect(url_for_security('login', next=request.path))


class BaseModelView(sqla.ModelView):
    form_base_class = SecureForm
    can_view_details = True
    column_display_pk = True
    column_default_sort = 'id'
    column_type_formatters = dict(typefmt.BASE_FORMATTERS.items() + [(type(None), typefmt.null_formatter), ])
    create_modal = False
    details_modal = True
    edit_modal = False
    can_export = True
    named_filter_urls = True


class UserRoleModelView(UserRoleViewMixin, BaseModelView):
    __role__ = 'user'


class AdminRoleModelView(UserRoleViewMixin, BaseModelView):
    __role__ = 'admin'


class SuperuserRoleModelView(UserRoleViewMixin, BaseModelView):
    __role__ = 'superuser'
