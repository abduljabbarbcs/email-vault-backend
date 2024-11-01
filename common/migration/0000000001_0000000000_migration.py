revision = "0000000001"
down_revision = "0000000000"


def upgrade(migration):
    table_name = 'person'
    columns = """entity_id varchar(50) NOT NULL PRIMARY KEY,
    version varchar(50) NOT NULL,
    previous_version varchar(50),
    active BOOLEAN DEFAULT TRUE,
    changed_by_id varchar(50) NOT NULL,
    changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_partial BOOLEAN DEFAULT FALSE,
    first_name VARCHAR(255),
    last_name VARCHAR(255)"""
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('person')
    migration.update_version_table(version=down_revision)



