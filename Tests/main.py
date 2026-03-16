from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from typing import Optional, Annotated
import json
from sqlalchemy import Column, JSON
data = json.load(open("../savefile.json", "r"))
class savefiletest(SQLModel, table=True):
  username: str = Field(index=True, primary_key=True)
  password_hash: str = Field()
  save_blob: dict = Field(sa_column=Column(JSON))
  cash: float = Field()
  cash_exp: float = Field()
  multiplier: float = Field()
  multiplier_exp: float = Field()
  rebirths: float = Field()
  rebirths_exp: float = Field()
  #etc...
class Public(SQLModel):
  username: str
class Create(SQLModel):
  username: str
  password: str
class Update(SQLModel):
  save_blob: dict
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
def func(test):
  return {"message": f"Success! {test}"}
@app.get("/file/{file_path:path}")
def file_path(file_path: str):
  return {"file_path": file_path}
@app.get("/query_test/")
def query_test(index: int=0, instance: str="test"):
  return str(type(test[index])) == f"<class '{instance}'>"
@app.get("/db_test")
def db_test(username: str="Example", password:str="Example", savefile: str=data):
  pass
@app.patch("/update/{username}", response_model=Public)
def update(username: str, instance: Update, session: SessionDep, savefile_blob: dict=data):
  db = session.get(savefiletest, username)
  if not db:
    raise HTTPException(status_code=404, detail="User not found")
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