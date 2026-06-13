def test_migrations_stairway(alembic_runner):
    alembic_runner.migrate_up_to("heads")
    
    alembic_runner.migrate_down_to("base")
    
    alembic_runner.migrate_up_to("heads")