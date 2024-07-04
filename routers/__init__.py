from .user import user
from .device import device

routes = [
    user.user_router,
    device.device_router
]
