from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from typing import Optional, Annotated
import json
data = json.load(open("../savefile.json", "r"))
leaderboard_stats = {"Cash": str, "Multiplier": str} #More will be added here later
class savefiletest(SQLModel, table=True):
  username: str = Field(index=True, primary_key=True)
  password: str = Field()
  save_blob: str = Field()
  cash: str = Field()
  multiplier: str = Field()
  rebirths: str = Field()
  #etc...
class Public(savefiletest):
  username: str
class Create(savefiletest):
  pass
class Update(SQLModel):
  save_blob: str
  cash: str
  multiplier: str
  rebirths: str
  #etc...
sqlite_file_name = "test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
model = savefiletest
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(lifespan=lifespan)
SessionDep = Annotated[Session, Depends(get_session)]

test = ["A", 1, True, 1.0]

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/test/{test}")
def func(test: complex):
  return {"message": f"Success! {test}"}
@app.get("/file/{file_path:path}")
def file_path(file_path: str):
  return {"file_path": file_path}
@app.get("/query_test/")
def query_test(index: int=0, instance: str="test"):
  return isinstance(test[index], type(instance))
@app.get("/db_test")
def db_test(username: str="Example", password:str="Example", savefile: str=data):
  pass
@app.patch("/update/{username}", response_model=Public)
def update(username: str, instance: Update, session: SessionDep):
  db = session.get(savefiletest, username)
  if not db:
    return HTTPException(status_code=404, detail="User not found")
  data = instance.model_dump(exclude_unset=True)
  db.sqlmodel_update(data)
  session.add(db)
  session.commit()
  session.refresh(db)
  return db
@app.post("/create/", response_model=Public)
def create_user(user: Create):
    with Session(engine) as session:
      db = savefiletest.model_validate(user)
      session.add(db)
      session.commit()
      session.refresh(db)
      return db