#
# ddSMT: A delta debugger for SMT benchmarks in SMT-Lib v2 format.
#
# This file is part of ddSMT.
#
# Copyright (C) 2013-2021 by the authors listed in AUTHORS file.
#
# ddSMT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ddSMT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ddSMT.  If not, see <https://www.gnu.org/licenses/>.

from .smtlib import *
from .mutator_utils import Simplification


class RemoveConstructor:
    """Remove a single datatype constructor."""
    def filter(self, node):
        return is_operator_app(node, 'declare-datatype') or is_operator_app(
            node, 'declare-datatypes')

    def mutations(self, node):
        if is_operator_app(node, 'declare-datatype'):
            if len(node) != 3:
                return
            for cons in node[2]:
                yield Simplification({cons.id: None}, [])
        elif is_operator_app(node, 'declare-datatypes'):
            if len(node) != 3:
                return
            for type in node[2]:
                for cons in type:
                    yield Simplification({cons.id: None}, [])

    def __str__(self):
        return 'remove datatype constructor'


class RemoveDatatype:
    """Remove a datatype from a recursive datatype declaration."""
    def filter(self, node):
        return is_operator_app(node, 'declare-datatypes')

    def mutations(self, node):
        if len(node) != 3 or len(node[1]) != len(node[2]):
            return
        for i in range(len(node[1])):
            yield Simplification({
                node[1][i].id: None,
                node[2][i].id: None
            }, [])

    def __str__(self):
        return 'remove datatype'


def get_mutators():
    """Returns a mapping from mutator class names to the name of their config
    options."""
    return {
        'RemoveConstructor': 'dt-rm-constructor',
        'RemoveDatatype': 'dt-rm-datatype',
    }