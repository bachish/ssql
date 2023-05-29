from ssql.tests.resources.core import execute, get_int

# error, column "x" doesn't exists
execute("select * from EMPLOYEE where x = $1", get_int())
