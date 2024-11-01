revision = "0000000008"
down_revision = "0000000007"



def upgrade(migration):
    table_name = 'login_method_audit'
    columns = """
        entity_id VARCHAR(50) NOT NULL,
        version VARCHAR(50) NOT NULL,
        previous_version VARCHAR(50),
        active BOOLEAN DEFAULT TRUE,
        changed_by_id VARCHAR(50) NOT NULL,
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE,
        person VARCHAR(50) DEFAULT NULL,
        method_type VARCHAR(50) DEFAULT NULL,
        method_data JSON DEFAULT NULL,
        email VARCHAR(50) DEFAULT NULL,
        password VARCHAR(255) DEFAULT NULL,
        FOREIGN KEY (person) REFERENCES person(entity_id) ON DELETE SET NULL,
        FOREIGN KEY (email) REFERENCES email(entity_id) ON DELETE SET NULL 
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('login_method_audit')
    migration.update_version_table(version=down_revision)

