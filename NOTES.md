## installations
pip install fastapi[all]
pip install psycopg[binary,pool]


### Auth Setting and Variables
secret_key: str
jwt_secret_key: str
jwt_refresh_secret_key: str
algorithm: str
REFRESH_TOKEN_EXPIRE_TIME: int 

## exporting new requirements.txt from poetry
poetry export -f requirements.txt --output requirements.txt


### building & running docker-compose
docker-compose up --build

### shuting down docker-compose
```bash
docker-compose down -v
```

Ctrl+p, Ctrl+q will now turn interactive mode into daemon mode.  
Ctrl+C (or Ctrl+\) should detach you from the container but it will kill the container because your main process is a bash.
see this issue [here](https://stackoverflow.com/questions/25267372/correct-way-to-detach-from-a-container-without-stopping-it)


### if you want run deatched docker containers
```bash
# show all existing Containers with there STATUS Created | UP
docker ps -a

## RE-Attach or Listen to logs
docker-compose up
# OR
docker-compose logs 

```

## Generate powerful secrets
openssl rand -hex 32

### SQLAlchemy Knowladge
 - `session.refresh` is set to expire the data then immediately get the latest data 

## Alembic Setup
Remove the startup event from project/app/main.py since we no longer want the tables created at startup:


## API Limiter
```py
## In app/__init__.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address) 


from app.logs.logconfig import init_loggers

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# init our logger
init_loggers(logger_name="app-logs")
log = logging.getLogger("app-logs")



app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get('/health-check')
@limiter.limit("5/minute")
def health_check(request: Request) -> dict:
    return {'status': r'100% good'}

```   

```py
@app.on_event("startup")
async def on_startup():
    await init_db()
```
Again, bring down the existing containers and volumes:

```bash
$ docker-compose down -v
```
Take a quick look at Using Asyncio with Alembic while the new images are building.

Once the containers are back up, initialize Alembic with the async template:

```bash
$ docker-compose exec web alembic init -t async migrations
```

Within the generated "project/migrations" folder, import SQLModel into script.py.mako, a Mako template file:
```py
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```
Now, when a new migration file is generated it will include import sqlmodel.

Next, we need to update the top of `project/migrations/env.py` like so:
```py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel                       # NEW

from alembic import context

from app.models import Song                         # NEW

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata             # UPDATED

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

...
```
Here, we imported SQLModel and our song model. We then set target_metadata to our model's MetaData, SQLModel.metadata. For more on the target_metadata argument, check out Auto Generating Migrations from the official Alembic docs.

Update sqlalchemy.url in project/alembic.ini:

```py
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@db:5432/foo
```
To generate the first migration file, run:

```bash
$ docker-compose exec web alembic revision --autogenerate -m "init"
```

If all went well, you should see a new migration file in "project/migrations/versions" that looks something like this:
```py
"""init

Revision ID: 842abcd80d3e
Revises:
Create Date: 2023-07-10 17:10:45.380832

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '842abcd80d3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('song',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('artist', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('song')
    # ### end Alembic commands ###
```
Apply the migration:

```bash
$ docker-compose exec web alembic upgrade head
```

Create a new migration file:
```bash
$ docker-compose exec web alembic revision --autogenerate -m "add year"
```

Update the route handlers:

```py
@app.get("/songs/", response_model=list[Song])
async def read_songs(session: AsyncSession = Depends(get_session)):
    # heroes = await session.exec(select(Hero)).all()
    result = await session.exec(select(Song))
    songs = result.scalars().all()
    return songs


@app.post("/songs/")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
```



<!-- TODOS -->
- [X] Update migration email field should now be unqie
- [X] Update migration products & categories
- [ ] Update migration cart & cartItems
- [ ] Update migration order & orderDetail
- [X] install pyjwt[crypto], python-multipart
- [X] poetry export -f requirements.txt --output requirements.txt
- [ ] set some constrains on the password field 