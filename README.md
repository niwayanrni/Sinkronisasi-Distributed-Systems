# Sinkronisasi-Distributed-Systems

Distributed Sync System adalah proyek simulasi sistem terdistribusi yang mencakup beberapa komponen penting:  
1. **Distributed Lock Manager** (Raft-based)  
2. **Distributed Queue System** (consistent hashing, message persistence)  
3. **Distributed Cache Coherence** (MESI/MOSI/MOESI stub)  
4. **Containerization** dengan Docker & docker-compose  

Proyek ini dirancang untuk mendemonstrasikan prinsip-prinsip sistem terdistribusi, termasuk konsistensi, fault tolerance, dan komunikasi antar-node.

## Features

### A. Distributed Lock Manager
- Implementasi Raft consensus
- Mendukung shared & exclusive locks
- Handle network partition scenarios
- Deadlock detection (stub)

### B. Distributed Queue System
- Distributed queue menggunakan consistent hashing
- Multiple producers & consumers
- Message persistence & recovery
- Handle node failure tanpa kehilangan data
- At-least-once delivery guarantee (stub)

### C. Distributed Cache Coherence
- Implementasi cache coherence protocol (MESI/MOSI/MOESI)
- Multiple cache nodes
- Cache invalidation & update propagation
- Cache replacement policy (LRU/LFU stub)
- Performance monitoring (stub)

### D. Containerization
- Dockerfile untuk setiap node
- docker-compose untuk orchestration
- Scaling nodes secara dinamis
- Environment configuration via `.env` file

## Teknologi yang Digunakan
- **Python 3.11**: bahasa pemrograman utama  
- **SQLite**: persistence sederhana untuk queue  
- **Threading & Queue (Python)**: simulasi multiple producers/consumers  
- **Docker & docker-compose**: containerization dan orchestration  
- **Pickle**: serialisasi pesan  
- **Hashlib**: consistent hashing untuk distribusi pesan  
- **OS & Env**: konfigurasi environment  

## Notes
- Semua modul saat ini berupa stub, siap untuk implementasi logika penuh.  
- Queue persistence menggunakan SQLite (stub).  
- Message passing mendukung simulasi network partition.  
- Raft & Cache modules masih stub, bisa diisi logika konsensus dan cache coherence.

## How to Run

1. **Install dependencies**
```bash
pip install -r requirements.txt

2. **Jalankan node**
```opsi 1 "Python individu"
python -m src.nodes.base_node
python -m src.nodes.queue_node
python -m src.nodes.lock_manager
python -m src.nodes.cache_node

```opsi 2 "Jalankan semua node dengan Docker"
docker-compose up --build