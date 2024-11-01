revision = "0000000004"
down_revision = "0000000003"



def upgrade(migration):
    table_name = 'organization_audit'
    columns = """ 
        entity_id VARCHAR(50) NOT NULL,
        version VARCHAR(50) NOT NULL,
        previous_version VARCHAR(50),
        active BOOLEAN DEFAULT TRUE,
        changed_by_id VARCHAR(50) NOT NULL,
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE,
        name VARCHAR(255) NOT NULL,
        code VARCHAR(50) DEFAULT NULL,
        description VARCHAR(255) DEFAULT NULL
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('organization_audit')
    migration.update_version_table(version=down_revision)

