from ssql.tests.resources.core import execute

execute("select * from employee where dept = $1", "Sales")
