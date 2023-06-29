import time

import psycopg2
import pytest
from docker import DockerClient
from docker.models.containers import Container


@pytest.fixture(scope="session", autouse=True)
def postgres_container() -> Container:
    print("CONTAINER WAS CREATED")
    client = DockerClient()
    user = "postgres"
    password = "123"
    db = "postgres"

    container: Container = client.containers.run(
        "postgres",
        detach=True,
        name="test-postgres",
        ports={5432: 5432},
        environment={
            "POSTGRES_USER": user,
            "POSTGRES_PASSWORD": password,
            "POSTGRES_DB": db,
        },
    )

    time.sleep(5)
    conn = psycopg2.connect(
        host="172.17.0.2",
        database="postgres",
        user="postgres",
        password="123",
    )
    cur = conn.cursor()
    cur.execute(q)
    conn.commit()
    rows = cur.fetchall()

    for row in rows:
        print(row)
    yield container

    container.stop()
    container.remove()


q = """
        -- create
        CREATE TABLE IF NOT EXISTS EMPLOYEE (
        empId INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        dept TEXT NOT NULL,
        bonus REAL,
        isFired BOOLEAN NOT NULL DEFAULT False
        );
        -- insert
        --INSERT INTO EMPLOYEE VALUES (0001, 'Clark', 'Sales');
        --INSERT INTO EMPLOYEE VALUES (0002, 'Dave', 'Accountin');
        SELECT * FROM EMPLOYEE;

        """
