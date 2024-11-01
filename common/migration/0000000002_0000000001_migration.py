revision = "0000000002"
down_revision = "0000000001"



def upgrade(migration):
    table_name = 'person_audit'
    columns = """
        entity_id varchar(50) NOT NULL,
        version varchar(50) NOT NULL,
        previous_version varchar(50),
        active BOOLEAN DEFAULT TRUE,
        changed_by_id varchar(50) NOT NULL,
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE,
        first_name VARCHAR(255),
        last_name VARCHAR(255)
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('person_audit')
    migration.update_version_table(version=down_revision)

