from oslo_versionedobjects import base as ovoo_base
from oslo_versionedobjects import fields as ovoo_fields

remotable_classmethod = ovoo_base.remotable_classmethod
remotable = ovoo_base.remotable

class DameraObjectRegistry(ovoo_base.VersionedObjectRegistry):
    pass


class DameraObject(ovoo_base.VersionedObject):
    OBJ_SERIAL_NAMESPACE = 'damera_object'
    OBJ_PROJECT_NAMESPACE = 'damera'

    def as_dict(self):
        return {k: getattr(self, k)
                for k in self.fields
                if self.obj_attr_is_set(k)}


class DameraObjectDictCompat(ovoo_base.VersionedObjectDictCompat):
    pass


class DameraPersistentObject(object):
    """Mixin class for Persistent objects.

    This adds the fields that we use in common for all persistent objects.
    """
    fields = {
        'created_at': ovoo_fields.DateTimeField(nullable=True),
        'updated_at': ovoo_fields.DateTimeField(nullable=True),
    }


class DameraObjectIndirectionAPI(ovoo_base.VersionedObjectIndirectionAPI):
    def __init__(self):
        super(DameraObjectIndirectionAPI, self).__init__()
        from damera.conductor import api as conductor_api
        self._conductor = conductor_api.API()

    def object_action(self, context, objinst, objmethod, args, kwargs):
        return self._conductor.object_action(context, objinst, objmethod,
                                             args, kwargs)

    def object_class_action(self, context, objname, objmethod, objver,
                            args, kwargs):
        return self._conductor.object_class_action(context, objname, objmethod,
                                                   objver, args, kwargs)

    def object_backport(self, context, objinst, target_version):
        return self._conductor.object_backport(context, objinst,
                                               target_version)


class DameraObjectSerializer(ovoo_base.VersionedObjectSerializer):
    # Base class to use for object hydration
    OBJ_BASE_CLASS = DameraObject