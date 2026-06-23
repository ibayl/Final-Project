"""
Implementasi struktur data & algoritma (dibuat manual) untuk Sistem Parkir.

1. HashMap   -> akses data kendaraan berdasarkan plat nomor, O(1) rata-rata
2. Stack     -> tumpukan slot parkir (garasi 1 jalur, LIFO)
3. Queue     -> antrian kendaraan saat parkir penuh (FIFO)

Algoritma:
- Merge Sort    -> mengurutkan data kendaraan
- Binary Search -> mencari kendaraan pada data terurut (berdasarkan plat)
- Linear Search -> mencari kendaraan berdasarkan kata kunci
"""

# 1. HASH MAP (Separate Chaining)
class _NodeHash:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    #HashMap sederhana dengan teknik separate chaining
    def __init__(self, kapasitas=16):
        self.kapasitas = kapasitas
        self.jumlah = 0
        self.buckets = [None] * self.kapasitas

    def _hash(self, key):
        total = 0
        for ch in str(key):
            total = (total * 31 + ord(ch)) % self.kapasitas
        return total

    def _resize(self):
        lama = self.buckets
        self.kapasitas *= 2
        self.buckets = [None] * self.kapasitas
        self.jumlah = 0
        for head in lama:
            current = head
            while current:
                self.put(current.key, current.value)
                current = current.next

    def put(self, key, value):
        if self.jumlah / self.kapasitas > 0.7:
            self._resize()
        idx = self._hash(key)
        current = self.buckets[idx]
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        node = _NodeHash(key, value)
        node.next = self.buckets[idx]
        self.buckets[idx] = node
        self.jumlah += 1

    def get(self, key):
        idx = self._hash(key)
        current = self.buckets[idx]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key):
        idx = self._hash(key)
        current = self.buckets[idx]
        prev = None
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[idx] = current.next
                self.jumlah -= 1
                return True
            prev = current
            current = current.next
        return False

    def contains(self, key):
        return self.get(key) is not None

    def values(self):
        hasil = []
        for head in self.buckets:
            current = head
            while current:
                hasil.append(current.value)
                current = current.next
        return hasil

    def __len__(self):
        return self.jumlah

# 2. STACK (LIFO) - tumpukan slot parkir garasi 1 jalur
class Stack:
    def __init__(self):
        self._data = []

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def to_list(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)

# 3. QUEUE (FIFO) - antrian saat parkir penuh
class _NodeQueue:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.ukuran = 0

    def enqueue(self, value):
        node = _NodeQueue(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.ukuran += 1

    def dequeue(self):
        if self.head is None:
            return None
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.ukuran -= 1
        return node.value

    def is_empty(self):
        return self.ukuran == 0

    def to_list(self):
        hasil = []
        current = self.head
        while current:
            hasil.append(current.value)
            current = current.next
        return hasil

    def __len__(self):
        return self.ukuran

# ALGORITMA SORTING - MERGE SORT (O(n log n))
def merge_sort(data, key_func, menaik=True):
    if len(data) <= 1:
        return data
    tengah = len(data) // 2
    kiri = merge_sort(data[:tengah], key_func, menaik)
    kanan = merge_sort(data[tengah:], key_func, menaik)
    return _merge(kiri, kanan, key_func, menaik)

def _merge(kiri, kanan, key_func, menaik):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        a = key_func(kiri[i])
        b = key_func(kanan[j])
        kondisi = a <= b if menaik else a >= b
        if kondisi:
            hasil.append(kiri[i]); i += 1
        else:
            hasil.append(kanan[j]); j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil

# ALGORITMA SEARCHING
def binary_search(data_terurut, target, key_func):
    #Binary search pada data terurut. Mengembalikan index atau -1. O(log n)
    low, high = 0, len(data_terurut) - 1
    while low <= high:
        mid = (low + high) // 2
        nilai = key_func(data_terurut[mid])
        if nilai == target:
            return mid
        elif nilai < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def linear_search(data, kata_kunci):
    #Linear search berdasarkan plat/pemilik/jenis (partial, case-insensitive). O(n)
    kata_kunci = kata_kunci.lower()
    hasil = []
    for k in data:
        if (kata_kunci in k.plat.lower()
                or kata_kunci in k.pemilik.lower()
                or kata_kunci in k.jenis.lower()):
            hasil.append(k)
    return hasil
