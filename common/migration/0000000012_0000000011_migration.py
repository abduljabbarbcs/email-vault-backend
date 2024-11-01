revision = "0000000012"
down_revision = "0000000011"



def upgrade(migration):
    table_name = 'payment_info_audit'
    columns = """
        entity_id VARCHAR(50) NOT NULL,
        version VARCHAR(50) NOT NULL,
        previous_version VARCHAR(50),
        active BOOLEAN DEFAULT TRUE,
        changed_by_id VARCHAR(50) NOT NULL,
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE,
        person VARCHAR(50) DEFAULT NULL,
        card_holder_name VARCHAR(255) DEFAULT NULL,
        card_number_masked VARCHAR(50) DEFAULT NULL,
        card_hash VARCHAR(255) DEFAULT NULL,
        FOREIGN KEY (person) REFERENCES person(entity_id) ON DELETE SET NULL
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('payment_info_audit')
    migration.update_version_table(version=down_revision)
