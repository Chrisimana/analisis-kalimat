# Membalikkan urutan karakter dalam kalimat
def balik_kalimat(kalimat: str) -> str:
    return kalimat[::-1]

# Menghitung jumlah huruf vokal dalam kalimat
def hitung_vokal(kalimat: str) -> int:
    vokal = "aiueoAIUEO"
    return sum(1 for huruf in kalimat if huruf in vokal)

# Menghitung jumlah huruf konsonan dalam kalimat
def hitung_konsonan(kalimat: str) -> int:
    vokal = "aiueoAIUEO"
    return sum(1 for huruf in kalimat if huruf.isalpha() and huruf not in vokal)

# Menghitung jumlah kata dalam kalimat
def hitung_kata(kalimat: str) -> int:
    return len(kalimat.split())

# Menghitung total karakter dalam kalimat
def hitung_karakter(kalimat: str) -> int:
    return len(kalimat)