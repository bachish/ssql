from ssql.tests.resources.core import execute

execute("select * from employee where empId = $1", 12)
