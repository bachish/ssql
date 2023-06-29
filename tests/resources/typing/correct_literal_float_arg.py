from ssql.tests.resources.core import execute

execute("select * from employee where bonus = $1", 1.231)
