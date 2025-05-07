"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from . import user_group_pb2 as user__group__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n user-group-management-msgs.proto\x1a\x10user-group.proto"I\n\x12UserGroupCreateReq\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x10\n\x08joinable\x18\x03 \x01(\x08"0\n\x13UserGroupCreateResp\x12\x19\n\x05group\x18\x01 \x01(\x0b2\n.UserGroup"%\n\x12UserGroupDeleteReq\x12\x0f\n\x07groupId\x18\x01 \x01(\t"\x15\n\x13UserGroupDeleteResp"_\n\x17UserGroupEditDetailsReq\x12\x0f\n\x07groupId\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12\x10\n\x08joinable\x18\x04 \x01(\x08"5\n\x18UserGroupEditDetailsResp\x12\x19\n\x05group\x18\x01 \x01(\x0b2\n.UserGroupB\nZ\x08.;protosb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_group_management_msgs_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z\x08.;protos'
    _globals['_USERGROUPCREATEREQ']._serialized_start = 54
    _globals['_USERGROUPCREATEREQ']._serialized_end = 127
    _globals['_USERGROUPCREATERESP']._serialized_start = 129
    _globals['_USERGROUPCREATERESP']._serialized_end = 177
    _globals['_USERGROUPDELETEREQ']._serialized_start = 179
    _globals['_USERGROUPDELETEREQ']._serialized_end = 216
    _globals['_USERGROUPDELETERESP']._serialized_start = 218
    _globals['_USERGROUPDELETERESP']._serialized_end = 239
    _globals['_USERGROUPEDITDETAILSREQ']._serialized_start = 241
    _globals['_USERGROUPEDITDETAILSREQ']._serialized_end = 336
    _globals['_USERGROUPEDITDETAILSRESP']._serialized_start = 338
    _globals['_USERGROUPEDITDETAILSRESP']._serialized_end = 391