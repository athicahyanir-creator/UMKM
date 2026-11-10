#!/usr/bin/env python3
"""
PasarSemaka - Database Management & Seeding Engine
Sistem Basis Data SQLite3 Terpadu untuk Pasar Digital Produk Lokal Tanggamus
Kolaborasi: Pemerintah Kabupaten Tanggamus & Universitas Teknokrat Indonesia
Copyright © 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.
"""

import os
import sqlite3
import datetime
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pasarsemaka.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Tabel users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('buyer', 'umkm', 'admin')),
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Tabel umkm_profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS umkm_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        business_name TEXT NOT NULL,
        owner_name TEXT NOT NULL,
        description TEXT,
        phone TEXT,
        address TEXT,
        district TEXT NOT NULL,
        village TEXT,
        verification_status TEXT DEFAULT 'pending' CHECK(verification_status IN ('pending', 'approved', 'rejected')),
        nib TEXT,
        pirt TEXT,
        halal_cert TEXT,
        rating REAL DEFAULT 5.0,
        reviews_count INTEGER DEFAULT 0,
        year_established INTEGER DEFAULT 2020,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # 3. Tabel categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        slug TEXT NOT NULL UNIQUE,
        description TEXT,
        icon TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    # 4. Tabel products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        umkm_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        image_url TEXT,
        badge TEXT,
        rating REAL DEFAULT 4.8,
        reviews_count INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(umkm_id) REFERENCES umkm_profiles(id),
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    """)

    # 5. Tabel orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        buyer_name TEXT NOT NULL,
        buyer_phone TEXT NOT NULL,
        shipping_address TEXT NOT NULL,
        district TEXT NOT NULL,
        notes TEXT,
        total_amount INTEGER NOT NULL,
        shipping_fee INTEGER DEFAULT 10000,
        payment_method TEXT DEFAULT 'COD',
        order_status TEXT DEFAULT 'pending' CHECK(order_status IN ('pending', 'confirmed', 'processing', 'shipped', 'completed', 'cancelled')),
        tracking_code TEXT,
        driver_name TEXT DEFAULT 'Budi Santoso',
        driver_phone TEXT DEFAULT '0821-8899-7711',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 6. Tabel order_items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price INTEGER NOT NULL,
        subtotal INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # 7. Tabel reviews
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        buyer_name TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        comment TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # 8. Tabel admin_logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_name TEXT NOT NULL,
        action TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_name TEXT,
        details TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Cek apakah data sudah ada
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    print("[DB] Seeding categories...")
    categories = [
        ("Kopi & Minuman", "kopi-minuman", "Robusta pegunungan Ulubelu, kopi wine, jahe merah aren", "coffee"),
        ("Makanan Ringan", "makanan-ringan", "Keripik pisang khas Semaka, sale pisang basah dan kering", "bakery_dining"),
        ("Hasil Bumi & Madu", "hasil-bumi", "Madu odeng lebah hutan liar Gisting, hasil kebun segar", "eco"),
        ("Olahan Ikan & Hasil Laut", "olahan-ikan", "Abon tongkol, terasi udang rebon asli Teluk Semaka", "phishing"),
        ("Kerajinan & Tapis", "kerajinan-tapis", "Tenun tapis khas pengrajin Talang Padang dan souvenir", "texture"),
        ("Herbal & Rempah", "herbal-rempah", "Olahan rimpang jahe merah, temulawak, dan rempah herbal", "local_pharmacy")
    ]
    cursor.executemany("INSERT INTO categories (name, slug, description, icon) VALUES (?, ?, ?, ?)", categories)

    print("[DB] Seeding users...")
    users = [
        ("Ahmad Subagyo", "subagyo@kopiulubelu.id", "0812-7890-1122", "umkm"),
        ("Ibu Rohani", "rohani@semakasnack.id", "0813-6655-3344", "umkm"),
        ("Hendra Kurniawan", "hendra@madugisting.id", "0821-7788-9900", "umkm"),
        ("Ibu Maryati", "maryati@putrilaut.id", "0852-6677-8899", "umkm"),
        ("Pak Slamet", "slamet@salewonosobo.id", "0812-3344-5566", "umkm"),
        ("Ny. Siti Zulaikha", "zulaikha@tapistangganus.id", "0813-4455-6677", "umkm"),
        ("Rian Hidayat", "rian.hidayat@gmail.com", "0812-7890-4321", "buyer"),
        ("Dinas Koperasi & UKM Tanggamus", "admin.koperasi@tanggamus.go.id", "0811-7200-112", "admin")
    ]
    cursor.executemany("INSERT INTO users (full_name, email, phone, role) VALUES (?, ?, ?, ?)", users)

    print("[DB] Seeding UMKM profiles...")
    umkms = [
        (1, "UMKM Kopi Berkah Jaya", "Ahmad Subagyo", "Spesialis pengolahan biji kopi Robusta lereng Gunung Ulubelu dengan metode petik merah alami dan fermentasi modern.", "0812-7890-1122", "Pekon Ngarip, RT 03/RW 01", "Ulubelu", "Pekon Ngarip", "approved", "1904230048123", "2101806010452-26", "ID181100004921", 4.9, 124, 2017),
        (2, "Semaka Snack Mandiri", "Ibu Rohani", "Memaksimalkan potensi pisang kepok dan muli lokal Tanggamus menjadi camilan aneka rasa modern berstandar higienis.", "0813-6655-3344", "Pekon Sukaraja No. 45", "Semaka", "Pekon Sukaraja", "approved", "1904230059124", "2151806010782-27", "ID181100005183", 4.8, 89, 2019),
        (3, "KTH Tanggamus Lestari", "Hendra Kurniawan", "Konsorsium pembudidaya lebah hutan alami di kawasan lindung Gunung Tanggamus yang memproduksi madu murni tanpa pasteurisasi.", "0821-7788-9900", "Jl. Raya Gisting Atas No. 12", "Gisting", "Pekon Gisting Bawah", "approved", "1904230061245", "2091806010341-26", "ID181100006241", 5.0, 65, 2015),
        (4, "Putri Laut Kota Agung", "Ibu Maryati", "Pengolahan aneka hasil tangkapan nelayan pesisir Teluk Semaka menjadi abon ikan gurih dan kerupuk ikan berkualitas ekspor.", "0852-6677-8899", "Dermaga Pelabuhan Kota Agung", "Kota Agung", "Pekon Pasar Madang", "approved", "1904230072356", "2021806010891-28", "ID181100007812", 4.7, 42, 2018),
        (5, "Berkah Tani Wonosobo", "Pak Slamet", "Pionir olahan sale pisang basah legit dan keripik renyah khas sentra agrikultur pisang Wonosobo Tanggamus.", "0812-3344-5566", "Pekon Karang Anyar", "Wonosobo", "Pekon Karang Anyar", "approved", "1904230083467", "2141806010654-27", "ID181100008321", 4.9, 78, 2016),
        (6, "Sanggar Tapis Tanggamus", "Ny. Siti Zulaikha", "Pusat pelestarian dan perajin tenun kain tapis tradisional Lampung dengan sulaman benang emas motif klasik khas adat Saibatin.", "0813-4455-6677", "Jl. Lintas Barat Talang Padang", "Talang Padang", "Pekon Banding", "approved", "1904230094578", "KRIYA-1806-TP24", "ID181100009210", 4.9, 31, 2012),
        (7, "Herbal Sehat Sumberejo", "Pak Darsono", "Pengolahan jahe merah organik, temu lawak, dan gula aren murni dari perkebunan perbukitan Sumberejo.", "0812-8877-6655", "Pekon Margodadi", "Sumberejo", "Pekon Margodadi", "approved", "1904230105689", "2131806010912-28", "ID181100009145", 4.8, 56, 2021),
        (8, "Dapur Pesisir Semaka", "Bu Nurlaila", "Spesialis sambal basah ikan jambal asin dan terasi rebon asli nelayan pesisir Semaka dengan racikan cabai pekon.", "0813-9988-7766", "Pekon Karang Anyar Laut", "Semaka", "Pekon Karang Anyar", "pending", "1904230116790", "2021806010998-28", "ID181100010214", 4.8, 94, 2022)
    ]
    cursor.executemany("""
    INSERT INTO umkm_profiles (
        user_id, business_name, owner_name, description, phone, address, district, village,
        verification_status, nib, pirt, halal_cert, rating, reviews_count, year_established
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, umkms)

    print("[DB] Seeding products...")
    products = [
        # 1. Kopi Robusta Organik Ulubelu
        (1, 1, "Kopi Robusta Organik Ulubelu 250g", 
         "Biji kopi pilihan dari perkebunan lereng Gunung Ulubelu dengan aroma cokelat karamel yang khas. Dipetik merah alami dari ketinggian 1.000 mdpl.",
         45000, 45, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDezOv4jeWUTjjleiI4W8OMxdljMQ0BIQXV1MMI7zyry0-2g_rLcsHxZuLjo0wnsyZoAJce32knUOtTAj5nkccTjSXh8SgrrrpzNT0H4dvSiKXnMzVdE7PLrB-1y33pMlG9kw_NGoPyqkTH2-AZlzslZR2naUuIA7234zrMEJKkfjtBgqhsfy1Gb6pJXeyxrRzQXekc4SH2BPey_zvXB50xS4uLH3pAitL9GKE6fGQQ",
         "Terlaris", 4.9, 124),

        # 2. Keripik Pisang Rasa Susu & Cokelat
        (2, 2, "Keripik Pisang Rasa Susu & Cokelat 250g", 
         "Irisan pisang kepok renyah khas Semaka dilumuri saus bubuk cokelat premium dan susu creamy, gurih manis pas.",
         20000, 110, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDe2ZCdt8Tb2VZWBT6Gfw3ad2zJl2njATinuYLmPb2oABWBPbmIPTl14nRq7Vk56shV27b8msGwiAD55xMXt35FhNZh4YjhZ4PZ7kxID62iai3VtfjwXMj0liEnrNgFA2haFh2hLQ1KgdNZ9PVoMbUoRH7sF8_NG0gVbk-5bGtTgePe3-IfiGZRNKQ9_yu16aBUZboEqq5svA9rjI7AyCi81pyitEtAcHx2PsI1tQc0",
         "Binaan Pemkab", 4.8, 89),

        # 3. Madu Odeng Gisting 600ml
        (3, 3, "Madu Odeng Gisting 600ml", 
         "Madu hutan murni hasil panen lebah liar Apis dorsata di kawasan hutan lindung Gisting Tanggamus tanpa campuran pemanis buatan.",
         110000, 18, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDrm_vWL1OpEAifhXQ8jAnsmw4SuDylms5QmOIZ74c1fjeXvuf-lIxZfQIy8V1DxT6nh_nNsbdyx8K14CLQcIrfdV3nUmQv9Ky1LlxMFeejLweQzEnTTpsarOQcajgP1YK_IAEDe4FCe-C8eLeAFQGX9byzSp8Q7lrpI9HBDRL919RCcTUNU1KmcoaTXtf9p3u2T5nUzV-jCopDfA50BzNNEIBKkoSPQatgV6ne45hL",
         "Organik", 5.0, 65),

        # 4. Abon Ikan Tongkol Karang Brak 100g
        (4, 4, "Abon Ikan Tongkol Karang Brak 100g", 
         "Abon gurih renyah dibuat dari ikan tongkol segar tangkapan nelayan Teluk Semaka dan rempah tradisional Kota Agung.",
         25000, 35, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuBw-ly2nxwpo7hd-Ml2P0fufcsOPkZReY4o83UdhUZHZKgOCxTZu1k-mE7l6lNbZ5WmVPE9O0CRhTDNtMnekXO4gQ9Ax9lHqnjaFTj-KdhNApXHF77Y8r-NMezHgLgDEP6ZprsDjBuTElvCLDD9A022rWZXVDgpn7HTvnARDijBfPEXV3E1UNq6JsZmT1UzcxA1dZITeorz2B673G5Yu_PtVGLTJ33FUn3qYzXZI9-d",
         "Favorit", 4.7, 42),

        # 5. Sale Pisang Basah Manis Legit 300g
        (5, 2, "Sale Pisang Basah Manis Legit 300g", 
         "Sale pisang ambon pilihan dengan pengasapan higienis menghasilkan rasa legit manis alami tanpa pemanis buatan khas Wonosobo.",
         23000, 50, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDqV9FRmrthiGCv_TPR_6dJgEU9zPN9GCLvBY33SnzzzyjEmbofyFza70OjSI7bj-h58TKmLJ6-nSOG7hnN4CmTH2-TIdsPoskjbt4XYytlnpPxylJuWMNGNpkrGgJnDQX0ZQJgGw4SOb_ol4qWh2ScVkw_cv0XyYQz48T5v3Q1bUi4ZO-ICZugBMih7GOx_h2ctcSs_kd9hMak8mTQ3jGmc7ynOfo_LvXA46dMC9C8",
         "Terlaris", 4.9, 78),

        # 6. Kain Tapis Selempang Motif Pucuk Rebung
        (6, 5, "Kain Tapis Selempang Motif Pucuk Rebung", 
         "Tenun tapis khas perajin wanita Talang Padang dengan sulaman benang emas motif pucuk rebung kemakmuran adat Lampung Saibatin.",
         185000, 8, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDR89mraZJueiyGErq_pDcSq3uW8BbSCRYqX86X-jhyuivlo47oIdXO4hu3joUVDLwiq9qYCsatzYlsSdMKX8bWr2gtnCyU9PEFye6axaMkb6K1KsElOJ__kTwgnMNdZxZdc1KR_iQWPmeAkbOHHNE-Re94M3iHcJunq-Rf0xXpLi023TCazK6MoCmQJo41goSMmjTo7ROlr2wFb8KdQZqsPggIQ5-_gvKbUjplCw2A",
         "Warisan Budaya", 4.9, 31),

        # 7. Bubuk Jahe Merah Gula Aren 200g
        (7, 6, "Bubuk Jahe Merah Gula Aren 200g", 
         "Minuman kesehatan rempah jahe merah organik berpadu keaslian gula aren lokal Sumberejo menghangatkan tubuh.",
         28000, 60, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuAjpO8utNg00bFtca8wIDNRRTQcGs8LEq53LvRlS-il_3BdvkCXaeHOFMPE_XsIJrXpc7Xsxm8GmYxu4_6PBMyyyNsZwgWxOwM-n5RqL3hcdcabgsLYk08c1Tb74FnR3GV-s3ct-6QLsKVERB24cOY6G2WknaNpAPJyQJ6-NLNRpQ6H1draQ3jOGND-xdUBBmpXZGkAyerLTKngweTMwBGvjbgG14V4nUlNuDPNwCSr",
         "Organik", 4.8, 56),

        # 8. Sambal Ikan Asin Jambal Roti 180g
        (8, 4, "Sambal Ikan Asin Jambal Roti 180g", 
         "Potongan ikan jambal roti empuk dengan racikan sambal bawang pedas gurih mantap khas nelayan pesisir Semaka.",
         30000, 40, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuCrTBK953lq5E_yiUhTAriCWu88aDICYZGTWOLefpPcY4iAK2U1I6KZ1jrvtC7BrSKSSqwLIPHHGSfuAwI2oAKkl6zbHmMJWU3laLwIu37NX-FaDF_otfXJ1KLpMrItQEBtVcN-lVZwrwpNdqw-_4MyXGNzAnvRT45K6RPcPuICOHMekqS1tqZmnmpQjO5I67jCCuwa7QbHs2_SEk1FmN7dnfQw3KfsFoC0SKbzNnMV",
         "Pedas Gurih", 4.8, 94),

        # 9. Kopi Robusta Wine Fermentasi 200gr
        (1, 1, "Kopi Robusta Wine Fermentasi 200gr", 
         "Aroma fruity wine alami hasil proses fermentasi anaerob ceri merah pilihan pekebun Ulubelu tanpa alkohol.",
         65000, 25, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuCX11vrBQ5YrSUVICcOTdv_v6lXEaBAbrH2z9JNrr8CIsI4yXMhy6BVuN7aRfNh7vXhTdNXxcbcHACIx0V0moObJY28NvEin0h7k6JIpXZG1idhWU6Bp3lgalZkqaPUg3wiD2YLBNW74C7J0tCF650UajgN0VVR3cZLsFNbJyZPBciJ_JJLrDJ-73CnZZYgTPpYYwv78pE7N74ynYlitUHaYTj6YB9auJHk7CDpJ4W7",
         "Premium Specialty", 4.9, 48),

        # 10. Keripik Pisang Muli Coklat Lumer 200gr
        (2, 2, "Keripik Pisang Muli Coklat Lumer 200gr", 
         "Pisang muli manis digoreng krispi dengan balutan cokelat lumer tebal khas Semaka.",
         18000, 120, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuDg4Qn_kPUrtW-PSBaoUYsZ8gOXs12da_PCfjuBcoyV3T0MrHnF3JLOrHCSa7qrd363un2aWRCpp5jBxRNrqwSsOpvZ1t0a6LZf4QQXRfmeyvWzXfj8RRZrsE2JksibmHHU6I5QvMfJU-C1zht2tbdCMbiAHtrGDTJHNmA0xLf6Tnsyh8RX7eBdZj9xtX2laM709XplzZ7HN33N1qW7oWqo84PieAUnbUGQ1U5megkp",
         "Favorit Anak Muda", 4.8, 105),

        # 11. Terasi Udang Rebon Asli Teluk Semaka 150gr
        (4, 4, "Terasi Udang Rebon Asli Teluk Semaka 150gr", 
         "Terasi merah harum alami dibuat dari udang rebon segar tangkapan nelayan tanpa pengawet atau pewarna buatan.",
         15000, 45, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuALgEvKBWI4Tt15hhCh-SLRRvvby1EaYf2aien2wRGgIrpY27J9XhiAM2RZD1jjmvJATO_45BYHlqN7sXGmFhLklQayXFQ_uwzr8zfSTEysAFyrE0eFQMwdQvsF0ept8JBq4r-9ljcaRnZyjrpyr0si2mWcjCuj0YirJ9KQswyfTjItBO97XFHyKddw6120N62EDnKiwbeklzUQJjZmvoI-YmrgbfkM5iAt-yp7Aj25",
         "Aroma Khas", 4.8, 62),

        # 12. Sale Pisang Crispy Karang Anyar 250gr
        (5, 2, "Sale Pisang Crispy Karang Anyar 250gr", 
         "Sale pisang renyah dibalut adonan tepung gurih khas Pekon Karang Anyar Wonosobo, camilan pas santai sore.",
         22000, 80, 
         "https://lh3.googleusercontent.com/aida-public/AB6AXuAnn7hVv1oI6lhsmm7znmZ6sjdir98kaI09NhibKQYZN3f4ckUrbTEe5MSkJXNwhhHWO4S0Z1LuVZ9T1i5uWifPviKy4z5WHzHzwPqmT92baB-FGwILdylJVTUG3nPw_LUj13nBPioqEzdrOVOJkYRtTg2ZYxHskUb5zG10FQs5YSThSImkxaJ4PKd4pR6p9BGpFJVlvSjACYorbwhnKQrxwk30Kw_EAN16FEHU0QBU",
         "Bestseller", 4.9, 87)
    ]
    cursor.executemany("""
    INSERT INTO products (
        umkm_id, category_id, product_name, description, price, stock, image_url, badge, rating, reviews_count
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products)

    print("[DB] Seeding demo order & items...")
    cursor.execute("""
    INSERT INTO orders (
        order_number, buyer_name, buyer_phone, shipping_address, district, notes, total_amount, shipping_fee, payment_method, order_status, tracking_code, driver_name, driver_phone, created_at
    ) VALUES (
        '#PSM-2026-0891', 'Rian Hidayat', '0812-7890-4321', 'Jl. Merdeka No. 14, RT 02 / RW 01, Pekon Kampung Baru', 'Kota Agung Timur', 'Mohon giling medium halus (bubuk sedang), terima kasih.', 165000, 10000, 'COD', 'shipped', 'SMK-TGM-202604-89102', 'Budi Santoso', '0821-8899-7711', '2026-11-10 10:14:00'
    )
    """)
    order_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, 1, "Kopi Robusta Organik Ulubelu 250g", 2, 45000, 90000))

    cursor.execute("""
    INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, 9, "Kopi Robusta Wine Fermentasi 200gr", 1, 65000, 65000))

    cursor.execute("""
    INSERT INTO admin_logs (admin_name, action, target_type, target_name, details)
    VALUES ('Budi Santoso (Admin Dinas)', 'VERIFIKASI_UMKM', 'umkm_profiles', 'UMKM Kopi Berkah Jaya', 'Verifikasi berkas NIB 1904230048123 dan P-IRT disetujui.')
    """)

    conn.commit()
    conn.close()
    print("[DB] Inisialisasi dan Seeding Database PasarSemaka Berhasil!")


# Public Helper Functions for REST API

def get_products(category=None, district=None, search=None, max_price=None, verified_only=False):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT p.*, u.business_name, u.district, u.verification_status, c.name as category_name
    FROM products p
    JOIN umkm_profiles u ON p.umkm_id = u.id
    JOIN categories c ON p.category_id = c.id
    WHERE p.is_active = 1
    """
    params = []

    if category and category != 'Semua':
        query += " AND c.name = ?"
        params.append(category)

    if district and district != 'Semua':
        query += " AND u.district = ?"
        params.append(district)

    if search:
        query += " AND (p.product_name LIKE ? OR p.description LIKE ? OR u.business_name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if max_price:
        try:
            val = int(max_price)
            if val < 200000:
                query += " AND p.price <= ?"
                params.append(val)
        except ValueError:
            pass

    if verified_only:
        query += " AND u.verification_status = 'approved'"

    query += " ORDER BY p.id ASC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_product_by_id(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.*, u.business_name, u.district, u.owner_name, u.phone as seller_phone, u.verification_status, c.name as category_name
    FROM products p
    JOIN umkm_profiles u ON p.umkm_id = u.id
    JOIN categories c ON p.category_id = c.id
    WHERE p.id = ?
    """, (product_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_product(umkm_id, category_id, product_name, description, price, stock, image_url=None, badge=None):
    conn = get_connection()
    cursor = conn.cursor()
    if not image_url:
        image_url = "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80"
    cursor.execute("""
    INSERT INTO products (umkm_id, category_id, product_name, description, price, stock, image_url, badge)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (umkm_id, category_id, product_name, description, price, stock, image_url, badge))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_product(product_id, product_name, price, stock, description=None, category_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE products SET product_name = ?, price = ?, stock = ?"
    params = [product_name, price, stock]
    if description:
        query += ", description = ?"
        params.append(description)
    if category_id:
        query += ", category_id = ?"
        params.append(category_id)
    query += " WHERE id = ?"
    params.append(product_id)
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return True

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET is_active = 0 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return True

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories WHERE is_active = 1")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_umkm_list(district=None, status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT u.*, COUNT(p.id) as product_count
    FROM umkm_profiles u
    LEFT JOIN products p ON u.id = p.umkm_id AND p.is_active = 1
    WHERE 1=1
    """
    params = []
    if district and district != 'Semua':
        query += " AND u.district = ?"
        params.append(district)
    if status and status != 'Semua':
        query += " AND u.verification_status = ?"
        params.append(status)
    query += " GROUP BY u.id ORDER BY u.id ASC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_umkm_by_id(umkm_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM umkm_profiles WHERE id = ?", (umkm_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_umkm_verification(umkm_id, status, notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE umkm_profiles 
    SET verification_status = ?, notes = ? 
    WHERE id = ?
    """, (status, notes, umkm_id))
    cursor.execute("""
    INSERT INTO admin_logs (admin_name, action, target_type, target_name, details)
    VALUES ('Budi Santoso (Admin Dinas)', 'UPDATE_STATUS_VERIFIKASI', 'umkm_profiles', 
            (SELECT business_name FROM umkm_profiles WHERE id = ?), ?)
    """, (umkm_id, f"Status diubah menjadi {status}. Catatan: {notes or '-'}"))
    conn.commit()
    conn.close()
    return True

def create_order(buyer_name, buyer_phone, shipping_address, district, notes, items, payment_method='COD'):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Hitung total
    subtotal = 0
    for it in items:
        subtotal += int(it['price']) * int(it['quantity'])
    shipping_fee = 10000
    total_amount = subtotal + shipping_fee

    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand_suffix = str(int(datetime.datetime.now().timestamp()))[-4:]
    order_number = f"#PSM-2026-{rand_suffix}"
    tracking_code = f"SMK-TGM-2026-{rand_suffix}"

    cursor.execute("""
    INSERT INTO orders (
        order_number, buyer_name, buyer_phone, shipping_address, district, notes,
        total_amount, shipping_fee, payment_method, order_status, tracking_code, driver_name, driver_phone
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, 'Budi Santoso', '0821-8899-7711')
    """, (order_number, buyer_name, buyer_phone, shipping_address, district, notes, total_amount, shipping_fee, payment_method, tracking_code))
    order_id = cursor.lastrowid

    # Insert items & potong stok
    for it in items:
        pid = it['product_id']
        qty = int(it['quantity'])
        uprice = int(it['price'])
        item_sub = qty * uprice
        pname = it.get('product_name', 'Produk Lokal')
        cursor.execute("""
        INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, subtotal)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, pid, pname, qty, uprice, item_sub))
        
        # update stok
        cursor.execute("UPDATE products SET stock = MAX(0, stock - ?) WHERE id = ?", (qty, pid))

    conn.commit()
    conn.close()
    return {
        "id": order_id,
        "order_number": order_number,
        "tracking_code": tracking_code,
        "total_amount": total_amount,
        "shipping_fee": shipping_fee,
        "status": "pending"
    }

def get_orders(status=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    if status and status != 'Semua':
        query += " AND order_status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    orders = [dict(row) for row in cursor.fetchall()]

    for o in orders:
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (o['id'],))
        o['items'] = [dict(item) for item in cursor.fetchall()]

    conn.close()
    return orders

def update_order_status(order_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET order_status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()
    return True

def get_admin_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM umkm_profiles")
    total_umkm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM umkm_profiles WHERE verification_status = 'approved'")
    approved_umkm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM umkm_profiles WHERE verification_status = 'pending'")
    pending_umkm = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders")
    total_revenue = cursor.fetchone()[0]

    # Distribusi per kecamatan
    cursor.execute("""
    SELECT district, COUNT(id) as count 
    FROM umkm_profiles 
    GROUP BY district 
    ORDER BY count DESC
    """)
    district_distribution = [dict(row) for row in cursor.fetchall()]

    # Distribusi per kategori
    cursor.execute("""
    SELECT c.name, COUNT(p.id) as count
    FROM categories c
    LEFT JOIN products p ON c.id = p.category_id AND p.is_active = 1
    GROUP BY c.id
    ORDER BY count DESC
    """)
    category_distribution = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "total_products": total_products,
        "total_umkm": total_umkm,
        "approved_umkm": approved_umkm,
        "pending_umkm": pending_umkm,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "district_distribution": district_distribution,
        "category_distribution": category_distribution
    }

if __name__ == "__main__":
    init_db()
    seed_data()

