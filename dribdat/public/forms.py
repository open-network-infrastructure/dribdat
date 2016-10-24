# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (
    SubmitField, BooleanField,
    StringField, PasswordField,
    TextAreaField, TextField,
    SelectField
)
from wtforms.validators import DataRequired

from dribdat.user.models import User
from wtforms.validators import AnyOf, required, length
from ..user import projectProgressList

class LoginForm(Form):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('Unknown username')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        if not self.user.active:
            self.username.errors.append('User not activated')
            return False
        return True

class UserForm(Form):
    email = StringField(u'E-mail', [required(), length(max=80)])
    webpage_url = StringField(u'Online profile', [length(max=128)], description="URL to a GitHub/Twitter profile, or another personal website")
    password = PasswordField(u'New password', [length(max=128)])
    submit = SubmitField(u'Save')

class ProjectForm(Form):
    category_id = SelectField(u'Category / challenge', coerce=int)
    progress = SelectField(u'Progress', coerce=int, choices=projectProgressList())
    AUTOTEXT__HELP = u"Link to a GitHub or wiki page from which to update the following fields."
    autotext_url = StringField(u'Autofill link', [length(max=255)], description=AUTOTEXT__HELP)
    is_autoupdate = BooleanField(u'Autoupdate project data using this link')
    name = StringField(u'Title', [required(), length(max=80)], description="Required, you may change this any time")
    summary = StringField(u'Short summary', [length(max=120)], description="Optional, max. 120 characters")
    longtext = TextAreaField(u'Full description', description="Optional, Markdown formatting allowed")
    # tagwords = StringField(u'Tags', [length(max=255)], description="Optional, separated by spaces")
    webpage_url = StringField(u'Project home link', [length(max=255)], description="Optional")
    source_url = StringField(u'Source code link', [length(max=255)], description="Optional")
    image_url = StringField(u'Banner image link', [length(max=255)], description="Optional")
    logo_color = StringField(u'Custom color', [length(max=7)])
    logo_icon = StringField(u'<a target="_blank" href="http://fontawesome.io/icons/#search">Custom icon</a>', [length(max=20)])
    submit = SubmitField(u'Save')
