#!/usr/bin/env python3
"""
PasarSemaka - Backend Web Server & REST API
Menyajikan REST API, Database SQLite3 Lokal, dan UI Web Responsif Pasar Digital Tanggamus.
Copyright © 2026 by Athi Cahyani R dan Dr. Erliyan Redy Susanto, M.Kom.
"""

import os
import sys
import json
import csv
import io
import datetime
import tornado.ioloop
import tornado.web
import database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Pastikan folder static dan templates ada
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "css"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "js"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "img"), exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Inisialisasi DB jika belum
database.init_db()
database.seed_data()

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Cache-Control", "no-cache, no-store, must-revalidate")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def get_json_body(self):
        try:
            return json.loads(self.request.body.decode("utf-8"))
        except Exception:
            return {}

    def write_json(self, data, status_code=200):
        self.set_status(status_code)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps(data, ensure_ascii=False))


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        index_file = os.path.join(TEMPLATES_DIR, "index.html")
        if os.path.exists(index_file):
            with open(index_file, "r", encoding="utf-8") as f:
                self.write(f.read())
        else:
            self.write("<h1>PasarSemaka Server Berjalan</h1><p>File template index.html sedang dimuat...</p>")


class PageHandler(tornado.web.RequestHandler):
    def get(self, page_name):
        # Support /beranda, /katalog, /keranjang, /pesanan, /umkm, /admin
        mapping = {
            "beranda": "beranda.html",
            "katalog": "katalog.html",
            "keranjang": "keranjang.html",
            "pesanan": "pesanan.html",
            "umkm": "umkm-dashboard.html",
            "umkm-katalog": "umkm-dashboard.html",
            "umkm-pesanan": "umkm-dashboard.html",
            "admin": "admin-dinas.html",
            "dinas-kurasi": "admin-dinas.html",
            "dinas-statistik": "admin-dinas.html"
        }
        target = mapping.get(page_name, "index.html")
        file_path = os.path.join(TEMPLATES_DIR, target)
        if not os.path.exists(file_path):
            file_path = os.path.join(TEMPLATES_DIR, "index.html")
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.write(f.read())
        else:
            self.send_error(404)


# ===================== REST API HANDLERS =====================

class ProductsHandler(BaseHandler):
    def get(self):
        category = self.get_query_argument("category", None)
        district = self.get_query_argument("district", None)
        search = self.get_query_argument("search", None)
        max_price = self.get_query_argument("max_price", None)
        verified = self.get_query_argument("verified", None) == "true"

        products = database.get_products(category, district, search, max_price, verified)
        self.write_json({
            "status": "success",
            "count": len(products),
            "data": products
        })

    def post(self):
        data = self.get_json_body()
        name = data.get("product_name")
        price = data.get("price")
        stock = data.get("stock", 0)
        category_id = data.get("category_id", 1)
        umkm_id = data.get("umkm_id", 1)
        description = data.get("description", "")
        image_url = data.get("image_url", "")
        badge = data.get("badge", "Produk Baru")

        if not name or price is None:
            self.write_json({"status": "error", "message": "Nama produk dan harga wajib diisi!"}, 400)
            return

        try:
            new_id = database.create_product(
                umkm_id=int(umkm_id),
                category_id=int(category_id),
                product_name=str(name),
                description=str(description),
                price=int(price),
                stock=int(stock),
                image_url=image_url,
                badge=badge
            )
            self.write_json({
                "status": "success",
                "message": "Produk berhasil ditambahkan ke etalase PasarSemaka!",
                "product_id": new_id
            }, 201)
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


class ProductDetailHandler(BaseHandler):
    def get(self, product_id):
        product = database.get_product_by_id(int(product_id))
        if product:
            self.write_json({"status": "success", "data": product})
        else:
            self.write_json({"status": "error", "message": "Produk tidak ditemukan"}, 404)

    def put(self, product_id):
        data = self.get_json_body()
        name = data.get("product_name")
        price = data.get("price")
        stock = data.get("stock")
        desc = data.get("description")
        cat_id = data.get("category_id")

        try:
            database.update_product(int(product_id), name, int(price), int(stock), desc, cat_id)
            self.write_json({"status": "success", "message": "Produk berhasil diperbarui!"})
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)

    def delete(self, product_id):
        try:
            database.delete_product(int(product_id))
            self.write_json({"status": "success", "message": "Produk berhasil dinonaktifkan dari etalase!"})
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


class CategoriesHandler(BaseHandler):
    def get(self):
        cats = database.get_categories()
        self.write_json({"status": "success", "count": len(cats), "data": cats})


class UmkmHandler(BaseHandler):
    def get(self):
        district = self.get_query_argument("district", None)
        status = self.get_query_argument("status", None)
        umkms = database.get_umkm_list(district, status)
        self.write_json({"status": "success", "count": len(umkms), "data": umkms})


class UmkmDetailHandler(BaseHandler):
    def get(self, umkm_id):
        umkm = database.get_umkm_by_id(int(umkm_id))
        if umkm:
            self.write_json({"status": "success", "data": umkm})
        else:
            self.write_json({"status": "error", "message": "UMKM tidak ditemukan"}, 404)


class UmkmVerificationHandler(BaseHandler):
    def patch(self, umkm_id):
        data = self.get_json_body()
        status = data.get("status")
        notes = data.get("notes", "")

        if status not in ['approved', 'rejected', 'pending']:
            self.write_json({"status": "error", "message": "Status verifikasi tidak valid"}, 400)
            return

        try:
            database.update_umkm_verification(int(umkm_id), status, notes)
            self.write_json({
                "status": "success", 
                "message": f"Verifikasi UMKM berhasil diperbarui menjadi {status}!"
            })
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


class OrdersHandler(BaseHandler):
    def get(self):
        status = self.get_query_argument("status", None)
        orders = database.get_orders(status)
        self.write_json({"status": "success", "count": len(orders), "data": orders})

    def post(self):
        data = self.get_json_body()
        buyer_name = data.get("buyer_name")
        buyer_phone = data.get("buyer_phone")
        shipping_address = data.get("shipping_address")
        district = data.get("district", "Kota Agung Timur")
        notes = data.get("notes", "")
        items = data.get("items", [])
        payment_method = data.get("payment_method", "COD")

        if not buyer_name or not buyer_phone or not shipping_address or not items:
            self.write_json({"status": "error", "message": "Data pembeli, alamat, dan produk wajib lengkap!"}, 400)
            return

        try:
            result = database.create_order(
                buyer_name=buyer_name,
                buyer_phone=buyer_phone,
                shipping_address=shipping_address,
                district=district,
                notes=notes,
                items=items,
                payment_method=payment_method
            )
            self.write_json({
                "status": "success",
                "message": "Pesanan berhasil dibuat dan diteruskan ke sistem distribusi!",
                "data": result
            }, 201)
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


class OrderStatusHandler(BaseHandler):
    def patch(self, order_id):
        data = self.get_json_body()
        new_status = data.get("status")
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'completed', 'cancelled']
        
        if new_status not in valid_statuses:
            self.write_json({"status": "error", "message": "Status pesanan tidak valid"}, 400)
            return

        try:
            database.update_order_status(int(order_id), new_status)
            self.write_json({"status": "success", "message": f"Status pesanan #{order_id} berhasil diubah ke {new_status}!"})
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


class OrderTrackingHandler(BaseHandler):
    def get(self, order_id):
        # Demo / Live Tracking details for Semaka Express
        tracking_info = {
            "order_number": "#PSM-2026-0891",
            "tracking_number": "SMK-TGM-202604-89102",
            "courier": "Semaka Express (Logistik Terpadu Tanggamus)",
            "driver": {
                "name": "Budi Santoso",
                "vehicle": "Supra X 125cc (BE 4182 ZG)",
                "rating": 4.9,
                "phone": "0821-8899-7711",
                "status": "Dalam Pengantaran"
            },
            "origin": "Pekon Ngarip, Kec. Ulubelu",
            "destination": "Pekon Kampung Baru, Kec. Kota Agung Timur",
            "estimated_delivery": "24 Menit Lagi (11:30 WIB)",
            "distance_remaining_km": 14.2,
            "current_speed_kmh": 38,
            "checkpoints": [
                {"title": "Pesanan Dikonfirmasi UMKM", "time": "10:14 WIB", "desc": "Kopi Berkah Jaya Ulubelu telah mengemas paket", "completed": True},
                {"title": "Paket Diserahkan ke Kurir", "time": "10:35 WIB", "desc": "Pick-up titik sentra Pekon Ngarip, Kec. Ulubelu", "completed": True},
                {"title": "Sedang Diantar ke Tujuan", "time": "11:02 WIB", "desc": "Melintasi Jalur Lintas Talang Padang menuju Kota Agung Timur", "completed": True, "current": True},
                {"title": "Estimasi Tiba di Penerima", "time": "11:30 WIB", "desc": "Pekon Kampung Baru, Kec. Kota Agung Timur", "completed": False}
            ]
        }
        self.write_json({"status": "success", "data": tracking_info})


class AdminDashboardHandler(BaseHandler):
    def get(self):
        stats = database.get_admin_dashboard_stats()
        self.write_json({"status": "success", "data": stats})


class AdminExportHandler(BaseHandler):
    def get(self):
        umkms = database.get_umkm_list()
        
        output = io.StringIO()
        # Add UTF-8 BOM so Excel opens it with proper encoding
        output.write('\ufeff')
        writer = csv.writer(output)
        
        writer.writerow(["ID", "Nama Usaha", "Nama Pemilik", "Kecamatan", "Pekon", "Status Verifikasi", "NIB", "P-IRT", "Sertifikasi Halal", "Rating", "Jumlah Produk", "No. Telepon"])
        for u in umkms:
            writer.writerow([
                u['id'],
                u['business_name'],
                u['owner_name'],
                u['district'],
                u.get('village', '-'),
                u['verification_status'].upper(),
                u.get('nib', '-'),
                u.get('pirt', '-'),
                u.get('halal_cert', '-'),
                u.get('rating', 5.0),
                u.get('product_count', 0),
                u.get('phone', '-')
            ])

        csv_content = output.getvalue()
        self.set_header("Content-Type", "text/csv; charset=utf-8")
        self.set_header("Content-Disposition", "attachment; filename=Laporan_UMKM_Tanggamus_2026.csv")
        self.write(csv_content)


class ResetDemoHandler(BaseHandler):
    def post(self):
        try:
            # Delete and reseed
            if os.path.exists(database.DB_PATH):
                os.remove(database.DB_PATH)
            database.init_db()
            database.seed_data()
            self.write_json({"status": "success", "message": "Database berhasil direset ke kondisi data demo awal!"})
        except Exception as e:
            self.write_json({"status": "error", "message": str(e)}, 500)


def make_app():
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/page/([^/]+)", PageHandler),
        (r"/api/products", ProductsHandler),
        (r"/api/products/([0-9]+)", ProductDetailHandler),
        (r"/api/categories", CategoriesHandler),
        (r"/api/umkm", UmkmHandler),
        (r"/api/umkm/([0-9]+)", UmkmDetailHandler),
        (r"/api/umkm/([0-9]+)/verification", UmkmVerificationHandler),
        (r"/api/orders", OrdersHandler),
        (r"/api/orders/([0-9]+)/status", OrderStatusHandler),
        (r"/api/orders/([0-9]+)/tracking", OrderTrackingHandler),
        (r"/api/admin/dashboard", AdminDashboardHandler),
        (r"/api/admin/export", AdminExportHandler),
        (r"/api/reset-demo", ResetDemoHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": STATIC_DIR}),
        (r"/(.*\.html)", tornado.web.StaticFileHandler, {"path": TEMPLATES_DIR}),
    ], debug=False, autoreload=False)

def main():
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    app = make_app()
    app.listen(port, address="0.0.0.0")
    print("=" * 65)
    print("   🌿 PASARSEMAKA - PASAR DIGITAL PRODUK LOKAL TANGGAMUS")
    print("=" * 65)
    print(f" [OK] Server aktif pada : http://localhost:{port}")
    print(f" [OK] Database SQLite  : {database.DB_PATH}")
    print(f" [OK] Mode Aplikasi    : Smart Economy MVP (3 Peran Terpadu)")
    print(" Tekan CTRL+C untuk menghentikan server.")
    print("=" * 65)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

