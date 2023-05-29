from ssql.tests.resources.core import execute, unknownRet

execute("select * from employee where dept = $1", unknownRet())
