from .is_admin import IsAdmin
from loader import dp


if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
