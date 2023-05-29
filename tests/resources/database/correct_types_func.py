from ssql.tests.resources.core import execute, get_bool, get_int, get_str

# correct query and types, no errors, no warnings
# arguments gets from other function
execute(
    "select * from EMPLOYEE where empId = $1 and dept = $2 and isFired = $3 ",
    get_int(),
    get_str(),
    get_bool(),
)
