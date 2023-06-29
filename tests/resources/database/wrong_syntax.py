from ssql.tests.resources.core import execute, get_int, get_str

execute(
    "select * from EMPLOYEE where empId = $1, dept = $2 ",
    get_int(),
    get_str(),
)
