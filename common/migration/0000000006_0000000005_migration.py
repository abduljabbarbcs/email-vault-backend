revision = "0000000006"
down_revision = "0000000005"



def upgrade(migration):
    table_name = 'email_audit'
    columns = """
        entity_id varchar(50) NOT NULL,         
        version varchar(50) NOT NULL,                      
        previous_version varchar(50),                   
        active BOOLEAN DEFAULT TRUE,                
        changed_by_id varchar(50) NOT NULL,    
        changed_on DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_partial BOOLEAN DEFAULT FALSE, 
        person varchar(50),                
        email VARCHAR(255),
        is_verified BOOLEAN DEFAULT FALSE,
        is_default BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (person) REFERENCES person(entity_id) ON DELETE SET NULL
    """
    migration.create_table(table_name, columns)
    migration.update_version_table(version=revision)

def downgrade(migration):
    migration.drop_table('email_audit')
    migration.update_version_table(version=down_revision)

