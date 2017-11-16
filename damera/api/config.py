from damera.api import hooks

# Pecan Application Configurations
app = {
    'root': 'damera.api.controllers.root.RootController',
    'modules': ['damera.api'],
    'debug': False,
    'hooks': [
        hooks.ContextHook(),
        hooks.RPCHook(),
        hooks.NoExceptionTracebackHook(),
    ],
    'acl_public_routes': [
        '/',
        '/v1',
    ],
}