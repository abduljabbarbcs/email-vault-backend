revision = "0000000009"
down_revision = "0000000008"



def upgrade(migration):
    table_name = 'referral_code'
    columns = """
        entity_id VARCHAR(50) NOT NULL PRIMARY KEY,
        version VARCHAR(50) NOT NULL,
        previous_version VARCHAR(50),
        active BOOLEAN DEFAULT TRUE,
        changed_by_id VARCHAR(50) NOT NULL,
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE,
        code VARCHAR(50) DEFAULT NULL,
        referrer_person_id VARCHAR(50) DEFAULT NULL,
        referred_person_id VARCHAR(50) DEFAULT NULL,
        FOREIGN KEY (referrer_person_id) REFERENCES person(entity_id) ON DELETE SET NULL,
        FOREIGN KEY (referred_person_id) REFERENCES person(entity_id) ON DELETE SET NULL
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)


def downgrade(migration):
    migration.drop_table('referral_code')
    migration.update_version_table(version=down_revision)

