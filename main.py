from fastapi import FastAPI
from app import data
from app.rekomendasi import collaborative
import os
import pandas as pd

# inisialisasi web service
app = FastAPI()

# inisialisasi koneksi database
connect = data.create_connection(
    os.getenv("DB_HOST"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_NAME"),
    os.getenv("DB_PORT")
)

@app.post("/prediksi/{user_id}")
def prediksi(user_id):
    """Melakukan prediksi rekomendasi terhadap user x

    Method: POST
    Parameter: path parameter
    Content-Type: application/json
    """

    try:
        
        # ambil data transaksi
        transaksi = data.get_transaction(os.getenv("QUERY"), connect)

        # mengubah dictionary menjadi tabel ( pandas data frame )
        tabel = pd.DataFrame(transaksi)

        row = os.getenv("ROW_VALUE")
        column = os.getenv("COLUMN_VALUE")

        # membuat pivot tabel
        pivot = data.create_pivot_table(tabel, row, column)

        # prediksi konten collaborative filltering
        rekomendasi = collaborative(product_id=pivot.columns.tolist(),
                                    user_id=user_id,
                                    pivot_table=pivot)
        return {
            "data": rekomendasi,
            "pesan": "berhasil mendapatkan rekomendasi"
        }
    
    except Exception as err:
        return {
            "data": [],
            "pesan": str(err)
        }