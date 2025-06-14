# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator
from functools import reduce

import django_filters
from django.db.models import Q


class SearchFilter(django_filters.Filter):
    def __init__(self,names=[],*args,**kwargs):
        if len(args) == 0:
            kwargs['field_name'] = names[0]
        self.token_prefix = kwargs.pop('token_prefix','')
        self.token_suffix = kwargs.pop('token_suffix','')
        self.token_reducer = kwargs.pop('token_reducer',operator.and_)
        self.names = names
        django_filters.Filter.__init__(self,*args,**kwargs)


    def get_subquery_list(self, search_value):
        return [Q(**{'%s__isnull'%name:False}) & Q(**{'%s__icontains'%name:
                    (self.token_prefix+search_value+self.token_suffix)})
                        for name in self.names]

    def filter(self,qs,value):
        if value not in (None,''):
            tokens = value.split(',')
            return qs.filter(
                reduce(
                    self.token_reducer,
                    [
                        reduce(operator.or_, self.get_subquery_list(token))
                        for token in tokens]))
        return qs