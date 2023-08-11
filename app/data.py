from mysql.connector import connect
import pandas as pd

def create_connection(host: str,
                      user: str,
                      password: str,
                      database: str,
                      port: int):
    """Membuat koneksi database
    
    Args:
        host : string -> mysql host
        user : string -> mysql user
        passowrd: string -> mysql password
        database: string -> nama database yang akan digunakan
    Returns:
        db : mysql.connector.connect
    """

    # inisialisasi database
    db = connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    return db

def get_transaction(query: str, connection) -> list:
    """
    Ambil data transaksi dari database

    Args:
        query : string -> query untuk mendapatkan data
        connection: mysql.connector -> koneksi mysql 

    Returns:
        transaksi : list -> list data transaksi
    """

    cursor = connection.cursor(dictionary=True)

    # execute quer
    cursor.execute(query)

    # get result from query above
    result = cursor.fetchall()

    return result

def create_pivot_table(data : pd.DataFrame, index : str, column: str) -> pd.DataFrame:
    """Membuat pivot tabel dari data pandas data frame
    Args:
        data : pd.DataFrame -> data user dan item
    """

    # membuat pivot table
    # membuat one hot encoding
    one_hot = pd.get_dummies(data[column])

    # merge one hot encoding dengan data user
    merge = pd.concat([data[index], one_hot], axis=1)

    # final, generate pivot tabel
    pivot_tabel = pd.pivot_table(merge, index=index, aggfunc='max')

    return pivot_tabel