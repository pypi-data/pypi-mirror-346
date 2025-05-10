This might look like \
install postgresql
```bash
createdb campfin
export DATABASE_URL=postgres:///campfin
```

Once that's all done you can run the example:

```bash
python pgsql_big_dedupe_example_init_db.py 
python test.py
```