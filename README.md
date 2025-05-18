# Kutubxona API

Ushbu API kitoblar, mualliflar, janrlar, nusxalar, qarzga berish, rezervatsiya va reytinglarni boshqarish uchun mo‘ljallangan.

---

## API Endpointlar

### 1. **Book Lending (Qarzga olish)**
`/booklending/`

- `GET /booklending/`  
  - Admin/operatorlar: barcha qarzlar  
  - Foydalanuvchilar: faqat o‘z qarzlari
- `POST /booklending/` — Yangi qarz yaratish (hozirgi foydalanuvchi qarz oluvchi sifatida saqlanadi)
- `GET /booklending/overdue/` — Kechiktirilgan qarzlarni ko‘rish (faqat admin/operatorlar)
- `POST /booklending/return/` — Qarzni qaytarish (faqat qarz oluvchi va faolligi tekshiriladi)

### 2. **Book Reservation (Rezervatsiya qilish)**
`/bookreservation/`

- `GET /bookreservation/` — Rezervatsiyalar ro‘yxati (permissionlarga bog‘liq)
- `POST /bookreservation/` — Yangi rezervatsiya yaratish (muddat 1 kun)
- `GET /bookreservation/overdue/` — Muddati o‘tgan faolligi qolgan rezervatsiyalar
- `GET /bookreservation/my/` — Foydalanuvchining faolligi bor rezervatsiyalari

### 3. **Rating (Reytinglar)**
`/ratings/`

- `GET /ratings/` — Admin barcha reytinglarni ko‘radi, foydalanuvchilar faqat o‘z reytinglarini
- `POST /ratings/` — Yangi reyting yaratish (foydalanuvchi avtomatik hozirgi foydalanuvchi)
- `PUT/PATCH/DELETE /ratings/{id}/` — Reytingni o‘zgartirish yoki o‘chirish (permissionlarga bog‘liq)

### 4. **Genres (Janrlar)**
`/genres/`

- `GET/POST/PUT/DELETE /genres/` — Janr CRUD operatsiyalari
- `GET /genres/{id}/books/` — Berilgan janrga tegishli kitoblar (pagination bilan)

### 5. **Book Copies (Kitob Nusxalari)**
`/bookcopies/`

- `GET/POST/PUT/DELETE /bookcopies/` — Nusxa CRUD
- `GET /bookcopies/available/` — Hozirda mavjud bo‘lgan nusxalar ro‘yxati

### 6. **Books (Kitoblar)**
`/books/`

- `GET/POST/PUT/DELETE /books/` — Kitob CRUD
- `POST /books/{id}/rate/` — Kitobga reyting va sharh qo‘yish yoki yangilash
- `POST /books/{id}/reserve/` — Kitobni rezervatsiya qilish (agar mavjud nusxa bo‘lsa)
- `GET /books/{id}/available_copies/` — Kitobning mavjud nusxalari

### 7. **Authors (Mualliflar)**
`/authors/`

- `GET/POST/PUT/DELETE /authors/` — Muallif CRUD
- `GET /authors/{id}/books/` — Berilgan muallifning kitoblari (pagination bilan)

---

## Ruxsatlar (Permissions)

- **Admin** va **operator** foydalanuvchilar barcha ma'lumotlarni ko‘rish va o‘zgartirish huquqiga ega.  
- Oddiy **user** faqat o‘z ma'lumotlari bilan ishlashi mumkin, ba'zi operatsiyalar (masalan, qarzni qaytarish) uchun maxsus ruxsat talab qilinadi.  
- Qo‘shimcha permission sinflari `core.permissions` modulida ta'riflangan.

---

## Pagination va Filtrlash

- Har bir ViewSet pagination bilan ishlaydi (masalan, `BookPagination`, `GenrePagination` va boshqalar).  
- DjangoFilterBackend yordamida kerakli joylarda filtrlar mavjud (masalan, kitoblar, mualliflar, reytinglar bo‘yicha).

---

## Texnologiyalar

- Django REST Framework  
- Django Filters  
- PostgreSQL (yoki boshqa DB)  
- Python 3.x

---

## Qo‘shimcha ma’lumotlar

- API autentifikatsiya talab qiladi (token yoki session asosida).  
- Ma'lumotlar JSON formatida yuboriladi va olinadi.  
- Har bir model uchun serializerlar va paginatsiya sinflari mavjud.

---

**Loyiha muallifi:** Rayxon Irisqulova

---
