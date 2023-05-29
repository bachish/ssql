from ssql.tests.resources.core import execute, query_generator

# warn: can't get query statement
execute(query_generator())
execute(query_generator(), 2)
