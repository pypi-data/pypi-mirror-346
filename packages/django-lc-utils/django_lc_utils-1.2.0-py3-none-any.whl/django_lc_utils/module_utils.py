def import_dotted(path: str):
    path_components = path.split(".")
    obj = path_components[-1]
    fromlist = [obj]
    mod = __import__(".".join(path_components[0:-1]), fromlist=fromlist)
    return getattr(mod, obj)
