import functools

def login_required(permissions=["none"]):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(*args,**kwargs):
            print('Decorator call')
            print(permissions)
            return view(*args, **kwargs)
        return wrapped_view
    return decorator

@login_required(permissions='fooff')
def fun():
    print('Fun call')

print(fun.__name__)
fun()