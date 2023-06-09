from ssql.ssql_plugin import SsqlPlugin

try:
    p = SsqlPlugin(options=None)
except TypeError:
    pass


print("'Ex.py': Ssql module checked.")
