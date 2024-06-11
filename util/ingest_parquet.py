from sqlalchemy import create_engine
import pyarrow.parquet as pq
import numpy as np

df = pq.read_table(source='LocMonth_Timestamp.parquet').to_pandas()
df['job_id'] = 1

str_df = df.select_dtypes([np.object])
str_df = str_df.stack().str.decode('utf-8').unstack()
for col in str_df:
    df[col] = str_df[col]

print("Inside IngestParque.py")
engine = create_engine(
    'postgresql://ghost:password@localhost:5433/sampledb'
)
print("ppost engine definition")
df.to_sql('api_calldetailrecord', engine, if_exists='append', index=False)
print("Post Equecution")
