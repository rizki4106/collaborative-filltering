from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def collaborative(
        product_id: list,
        user_id : int,
        pivot_table: pd.DataFrame) -> list:
    """
    Memprediksi rekomendasi dengan menggunakan metode collaborative filltering user based

    Args:
        user_id: int -> id user yang akan diberikan rekomendasi
        pivot_table: pd.DataFrame -> pivot tabel yang berisi index user id, column product_id dan value one hot encoding

    Returns:
        rekomendasi : list -> rekomendasi produk yang akan diberikan kepada user
    """

    # ambil semua list user id
    user = pivot_table.index.tolist()

    # nilai pivot tabel user id 2
    pivot = pivot_table.iloc[user.index(user_id), :]

    # menghapus data di index ke n yang mana index n ini merupakan posisi index user id x
    # jika tidak dihapus maka nilai kesamaan akan sama dengan dirinya sendiri

    pivot_table = pivot_table.drop(user_id)

    # menghitung nilai kesamaan
    nilai_kesamaan = [ cosine_similarity(pivot.values.reshape(1, -1), pivot_all.reshape(1, -1)).squeeze().tolist() for pivot_all in pivot_table.values]

    # mengurutkan nilai kesamaan dari yang besar hingga kecil
    similarity = sorted(nilai_kesamaan, reverse=True)

    # ambil user yang mirip
    user_mirip = []

    # kesamaan yang nilainya > 0
    kesamaan_terpilih = []

    for sim in similarity:

        user_mirip.append(user[nilai_kesamaan.index(sim)])
        kesamaan_terpilih.append(sim)

    # menghilangkan data ganda
    user_mirip = list(set(user_mirip))
    kesamaan_terpilih = list(set(kesamaan_terpilih))

    # ambil data yang mirip dengan user x
    data_mirip = np.array([pivot_table.iloc[i].values.tolist() for i in user_mirip])

    produk = []

    for i, p in enumerate(pivot):

        # 1 pernah membeli
        # 0 belum pernah membeli
        # jadi jika nilai pivot = 0 simpan data tersebut sebagai data produk yang belum pernah dibeli
        if p > 0:
            pass
        else:
            produk.append(product_id[i])

    # prediksi rating
    rekomendasi = []

    for p in produk:

        # hitung rating
        rating = np.dot(kesamaan_terpilih, data_mirip[:, product_id.index(p)]) / np.sum(kesamaan_terpilih)

        context = {
            "item": p,
            "rating": round(rating, 4) if rating > 0 else 0,
        }

        rekomendasi.append(context)

    # urutkan nilai rating dari yang terbesar hingga kecil
    rekomendasi = sorted(rekomendasi, key=lambda x : x['rating'], reverse=True)

    return rekomendasi