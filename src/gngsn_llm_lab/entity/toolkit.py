# SQLDatabaseToolkit 객체 생성
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import SqliteDatabase

from gngsn_llm_lab.domain.llm import llm

database = SqliteDatabase(":memory:")
toolkit = SQLDatabaseToolkit(db=database, llm=llm)
