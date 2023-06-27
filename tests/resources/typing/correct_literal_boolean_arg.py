from ssql.tests.resources.core import execute

execute("select * from employee where isFired = $1", True)
