# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from django.utils.translation import ugettext_lazy as _

from horizon import tables

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


class DeleteFlavors(tables.DeleteAction):
    data_type_singular = _("Flavor")
    data_type_plural = _("Flavors")

    def delete(self, request, obj_id):
        api.tuskar.FlavorTemplate.delete(request, obj_id)


class CreateFlavor(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Flavor")
    url = "horizon:infrastructure:resource_management:flavors:create"
    classes = ("ajax-modal", "btn-create")


class EditFlavor(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit Flavor")
    url = "horizon:infrastructure:resource_management:flavors:edit"
    classes = ("ajax-modal", "btn-edit")


class FlavorsFilterAction(tables.FilterAction):

    def filter(self, table, flavors, filter_string):
        """ Naive case-insensitive search. """
        q = filter_string.lower()
        return [flavor for flavor in flavors
                if q in flavor.name.lower()]


class FlavorsTable(tables.DataTable):
    name = tables.Column('name',
                         link=("horizon:infrastructure:"
                               "resource_management:flavors:detail"),
                         verbose_name=_('Flavor Name'))
    cpu = tables.Column(
        "cpu",
        verbose_name=_('VCPU'),
        filters=(lambda x: getattr(x, 'value', ''),)
    )
    memory = tables.Column(
        "memory",
        verbose_name=_('RAM (MB)'),
        filters=(lambda x: getattr(x, 'value', ''),)
    )
    storage = tables.Column(
        "storage",
        verbose_name=_('Root Disk (GB)'),
        filters=(lambda x: getattr(x, 'value', ''),)
    )
    ephemeral_disk = tables.Column(
        "ephemeral_disk",
        verbose_name=_('Ephemeral Disk (GB)'),
        filters=(lambda x: getattr(x, 'value', ''),)
    )
    swap_disk = tables.Column(
        "swap_disk",
        verbose_name=_('Swap Disk (MB)'),
        filters=(lambda x: getattr(x, 'value', ''),)
    )

    class Meta:
        name = "flavors"
        verbose_name = _("Flavors")
        table_actions = (CreateFlavor, DeleteFlavors, FlavorsFilterAction)
        row_actions = (EditFlavor, DeleteFlavors)
