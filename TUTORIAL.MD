FLASK
---------------

virtualenv envfo
envfo\Scripts\activate

REQUIREMENTS
---------------

pip install flask
pip install flask-login
pip install flask-openid
pip install flask-mail
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-whooshalchemy
pip install flask-wtf
pip install flask-babel
pip install guess_language
pip install flipflop
pip install coverage

DIRECTORY
---------------

|-flaskone
|-mirocblog
|--app
|---static
|---templates
|--tmp

//////////// HELLO WORLD

app\__init__.py

from flask import Flask

app = Flask(__name__)
from app import views

membuat objek Flask di variabel app, kemudian mengimport modul views.

`Views ini adalah program yang menangani request dari web browser. Setiap fungsi view bisa jadi satu atau lebih URL.

import diletakkan dibawah agar kita tidak terjebak dengan circular reference.

app/views.py

from app import app

@app.route('/')
@app.route('/index')
def index():
	return "hello, world"
	
Pada kode di atas, ada dua URL yang dipetakan dengan decorator route, yaitu / dan /index. 

Buat run.py pada folder root (microblog) untuk menjalankan web server. 

from app import app

app.run(debug=True)

python run.py

untuk menjalankan web server

127.0.0.1:5000/
127.0.0.1:5000/index

akan menampilkan pesan yang sama yaitu hello, world


//////////// HTML TEMPLATE

Membuat home page
membuat view kita me-return sebuah halaman HTML

app/views.py

from app import app
 
@app.route('/')
@app.route('/index')
def index():
    user = {"nickname": "uman"}  # temprorary
    return \
        """
        <html>
            <head>
                <title>Microblog Home Page</title>
            </head>
            <body>
                <h1>Hello, """ + user["nickname"] + """</h1>
            </body>
        </html>
        """

karena kita belum membuat modul untuk user, maka kita membuat sebuah user palsu / sementara. Cara ini sangat tidak dianjurkan karena akan sangat berantakan jika kita akan membuat sebuah aplikasi yang lengkap.

Menggunakan Template
file HTML akan disimpan pada folder lain (app/templates) secara independen, dengan memanggil beberapa variabel yang akan di-pass oleh view kita. Nanti, kita tinggal buat kode bisnis nya dengan python di view, kemudian memanggil template HTML dan mem-pass beberapa variabel yang akan digunakan oleh template. Dengan ini, kita bisa memisahkan pekerjaan desain dan bisnis.
		
app/templates/index.html

<html>
    <head>
        <title>Microblog - {{ title }}</title>
    </head>
    <body>
        <h1>Hello, {{ user.nickname }}!!</h1>
    </body>
</html>

Kita lihat di atas, bahwa pemanggilan variabel dilakukan dengan {{ ... }}. Di sana, ada variabel title dan user yang di-pass dari view nya. Sekarang, mari kita ubah views.py kita.

app/views.py

from flask import render_template
from app import app
 
@app.route('/')
@app.route('/index')
def index():
    user = {"nickname": "uman"}  # temprorary
    return render_template("index.html", title="Home", user=user)
	
Untuk melakukan render ini, digunakan sebuah fasilitas dari flask yaitu render_template. Fungsi ini akan mengambil parameter, yang pertama adalah nama dari file template yang kita buat, kemudian dilanjutkan dengan variabel apa yang ingin kita pass ke template tersebut. Di belakangnya, render_template menggunakan engine Jinja2, sehingga kita bisa memanggil variabel yang di pass dengan {{ ... }}.

Mengendalikan Template
Template Jinja2 juga menyediakan control statement, untuk melakukan kendali pada template. Kendali yang saya maksud seperti if, for, dll. Di sini, control statement akan dimasukkan ke dalam blok {% ... %}.

app/templates/index.html

<html>
    <head>
        {% if title %}
        <title>Microblog - {{ title }}</title>
        {% else %}
        <title>Microblog Home</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.nickname }}!!</h1>
    </body>
</html>

Dengan modifikasi ini, jika kita menghilangkan parameter title dari view kita, tidak apa-apa, template akan mengubah judulnya secara otomatis.

Di homepage, pengguna yang masuk tentu ingin melihat postingan dari akun-akun lain yang dia ikuti, atau mungkin dari akunnya sendiri juga. Di sini, kita akan menggunakan pengulangan dengan dtatement {% for %}. Pertama, kita akan masukkan post-post palsu ke dalam view kita.

app/views.py

from flask import render_template
from app import app
 
@app.route('/')
@app.route('/index')
def index():
    user = {"nickname": "uman"}  # user palsu
    posts = [
        {
            "author": {"nickname": "sarala"},
            "body": "Hari ini cerah!!"
        },
        {
            "author": {"nickname": "serele"},
            "body": "Kabut asap di mana-mana T-T"
        }
    ]
    return render_template("index.html",
                           title="Home",
                           user=user,
                           posts=posts)
						   
Jadi posts itu adalah sebuah array yang berisi postingan yang ingin ditampilkan. Isi sebuah postingan adalah author, yang berisi user yang membuatnya dan body yang berisi postingan dia saat itu.

bagaimana template akan mencetak postingan tadi? Karena template tidak tahu berapa postingan yang akan masuk, kita akan menampilkan postingan itu sebanyak yang diperlukan. Kita akan menggunakan {% for %} untuk menampilkannya.

app/templates/index.html

<html>
    <head>
        {% if title %}
        <title>Microblog - {{ title }}</title>
        {% else %}
        <title>Microblog Home</title>
        {% endif %}
    </head>
    <body>
        <h1>Hello, {{ user.nickname }}!!</h1>
        {% for post in posts %}
        <div>
            <p>{{ post.author.nickname }}: <b>{{ post.body }}</b></p>
        </div>
        {% endfor %}
    </body>
</html>

Template Inheritance
template yang kita buat, ternyata bisa kita panggil ke dalam template lain, kita sebut template inheritance, salah satu fitur dari Jinja2. Hal ini kita lakukan jika kita ingin menyediakan sebuah template yang berulang-ulang (misalnya seperti Facebook, di manapun kita berada, pasti ada navigation bar biru yang di atas kan? Daripada kita meng-copy seluruhnya ke sana, kita bisa melakukannya dengan menambahkan template dasar.

app/templates/base.html

<html>
    <head>
        {% if title %}
        <title>Microblog - {{ title }}</title>
        {% else %}
        <title>Microblog Home</title>
        {% endif %}
    </head>
    <body>
        {% block content %}{% endblock %}
    </body>
</html>

Di sana, kita lihat ada {% block content %}{% endblock %}, yang akan diisi oleh template yang ingin kita masukkan. Untuk memasukkannya, kita bisa mengubah index.html kita menjadi:

{% extends "base.html" %}
{% block content %}
    <h1>Hello, {{ user.nickname }}!! -- <a href="/index">Home</a></h1>
    {% for post in posts %}
    <div>
        <p>{{ post.author.nickname }}: <b>{{ post.body }}</b></p>
    </div>
    {% endfor %}
{% endblock %}

index.html ini akan memanggil base.html dan mendefinisikan blok content dengan statement {% block ... %}. Jinja2 akan langsung memanggil base.html dan memasangkan template kita ke dalamnya sesuai dengan bloknya. Untuk template lain kita juga akan memasangnya sebagai extension dari base.html. Hasil dari kode ini, pada dasarnya sama dengan kode sebelumnya, karena isinya memang sama, kita hanya mengubah strukturnya saja.

//////////// WEB FORMS

Konfigurasi
Web-Form akan menggunakan Flask-WTF extension, yaitu sebuah wrapper untuk WTForms di Flask. Banyak Flask extensions akan membutuhkan konfigurasi, dan kita akan mengumpulkannya dalam satu file konfigurasi yang bernama config.py. File ini akan kita simpan di folder root aplikasi kita (microblog/).

config.py

WTF_CSRF_ENABLED = True
SECRET_KEY = "rahasia"

Flask-WTF akan menerima dua pengaturan dari kita, yaitu WTF_CSRF_ENABLED yang akan mengaktifkan perlindungan terhadap cross-site request forgery dan membuat aplikasi kita lebih aman.

SECRET_KEY dibutuhkan jika CSRF dinyalakan, dan digunakan sebagai sebuah token kriptografi untuk memvalidasi form kita. Nilai dari setting ini bisa dimasukkan apa saja, dan jangan disebar luaskan ketika nanti kita membuat aplikasi kita sendiri.

memasukkan file config tersebut ke dalam Flask

app/init.py

from flask import Flask
 
app = Flask(__name__)
app.config.from_object('config')
 
from app import views

Form login
Web Form pada Flask-WTF direpresentasikan sebagai sebuah kelas, diturunkan dari kelas Form di Flask-WTF. Sub-class yang akan kita buat ini akan mendifinisikan field dari form sebagai variabel. Untuk form login nya sendiri, kita akan memanfaatkan OpenID, jadi kita tidak akan menampung data user dalam database kita. Mari kita buat form kita di app/forms.py.

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
 
 
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
	
kita telah membuat sebuah login form yang di-extend dari kelas Form yang ada di flask_wtf. di sana, kita mendefinisikan dua buah field, yaitu openid yang bertipe String (nantinya diisi oleh ID open ID kita, dan remember_me yang bertipe boolean, menandakan apakah akun kita akan diingat oleh aplikasi atau tidak.

DataRequired adalah sebuah validator yang mengecek apakah field tersebut diisi oleh user. Masih banyak validator di Flask-WTF, yang nanti akan kita gunakan juga.

Form View
Kita akan membuat sebuah view untuk me-render template login yang akan kita buat selanjutnya. intinya, kita akan mem-pass objek form kita ke template yang akan kita buat nanti. Ini adalah tambahan untuk file view kita (app/views.py)

app/views.py

from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
 
#functions....
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template("login.html",
                           title="Sign In",
                           form=form)
						   
Di sana ada beberapa import baru, seperti flash dan redirect yang akan kita bahas nanti. Ada import juga untuk LoginForm yang telah kita buat tadi. Nah jika kita lihat di route nya ada argument baru yaitu methods. Mengeset argument ini adalah agar fungsi view ini menerima request POST, selain GET sebagai default nya.

Template untuk Form
Setelah mendefinisikan field apa saja yang ada di form, sekarang saatnya kita menuliskan HTML untuk menulis form nya. Untungnya, kelas yang kita buat sebelumnya, LoginForm, akan mengurusi render dari field menjadi HTML, sehingga kita hanya akan berkonsentrasi pada layout. Sekarang kita buat template login pada app/templates/login.html

<!-- include base layout -->
{% extends "base.html" %}
 
{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" name="login">
        {{ form.hidden_tag() }}
        <p>
            Please enter your OpenID:<br />
            {{ form.openid(size=80) }}<br />
        </p>
        <p>{{ form.remember_me }} Remember Me</p>
        <p><input type="submit" value="Sign In"></p>
    </form>
{% endblock %}

Menerima data form
Kita akan lagi-lagi menggunakan Flask-WTF untuk mengolah data form yang sudah dimasukkan pengguna. Kita akan memvalidasi dan menerima data form di fungsi login() pada file app/views.py:

app/views.py

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login requested for openID: '%s', remember me: %s" %
              (form.openid.data, str(form.remember_me.data)))
        return redirect("/index")
    return render_template("login.html",
                           title="Sign In",
                           form=form)
						   
Di kode ini, ada sebuah method validate_on_submit() yang berfungsi mem-validasi masukan dari pengguna. Method ini akan mengembalikan False jika masukan pengguna tidak memenuhi syarat. Syarat yang akan divalidasi bergantung pada field yang memiliki validator. Pada kode ini, jika pengguna memasukkan dengan benar, maka akan di-redirect dengan fungsi redirect ke halaman /index, sedangkan jika gagal validasi, ia akan dikembalikan ke halaman yang sama.

Fungsi flash berfungsi untuk menampilkan pesan kepada pengguna. Fungsi ini dapat digunakan untuk melakukan debugging (seperti yang akan kita lakukan sekarang), atau memberikan feedback kepada pengguna setelah aksi yang dia lakukan. Nah pesan flash ini tidak akan muncul begitu saja pada halaman kita, harus kita tampilkan. Sekarang kita akan memasukkan pesan flash ini ke dalam app/templates/base.html.

<html>
    <head>
        {% if title %}
        <title>Microblog - {{ title }}</title>
        {% else %}
        <title>Microblog Home</title>
        {% endif %}
    </head>
    <body>
        <div>Microblog</div>
        <hr />
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <ul>
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </body>
</html>

Jadi, kita bisa mendapatkan pesan flash yang kita berikan pada view dengan fungsi get_flashed_messages(). Hal yang menarik dari pesan-pesan flash ini adalah mereka hanya akan muncul sekali dengan get_flashed_messages(). Artinya, sebelum fungsi tersebut dipanggil, pesan tidak akan muncul namun tetap tersimpan. Jika sudah dipanggil, dia hanya akan terpanggil sekali saja, dan tidak dipanggil lagi di tempat lain.

Meningkatkan Validasi
Tentu, kita sudah melakukan validasi pada form yang telah kita buat tadi. Dan jika data yang kita masukkan tidak memenuhi validasi, maka kita akan dikembalikan ke halaman login. Tapi bagaimana kita tahu bahwa kita salah memasukkan? Kita akan memasukkannya ke dalam halaman app/templates/login.html

<!-- include base layout -->
{% extends "base.html" %}
 
{% block content %}
    <h1>Sign In</h1>
    <form action="" method="post" name="login">
        {{ form.hidden_tag() }}
        <p>
            Please enter your OpenID:<br />
            {{ form.openid(size=80) }}<br />
            {% for error in form.openid.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}<br />
        </p>
        <p>{{ form.remember_me }} Remember Me</p>
        <p><input type="submit" value="Sign In"></p>
    </form>
{% endblock %}

Error yang kita buat akan muncul pada looping setelah pemanggilan field openid. Cara memanggilnya adalah form.nama_field.errors, contohnya seperti di atas form.openid.errors. Setelah form dibuat

Berurusan dengan OpenID
Nah sekarang kita akan menambahkan link untuk melakukan login ke open ID. Hanya link, kita belum menambahkan proses untuk login. Pertama, kita akan mendaftarkan akun-akun open ID apa saja yang bisa kita akses. Untuk saat ini kita gunakan Google, Yahoo, AOL, Flicker, dan lain-lain (Catatan: Google sudah menutup layanan open ID pada April 2015). Kita masukkan daftar tersebut ke dalam file config.py.

WTF_CSRF_ENABLED = True
SECRET_KEY = "ayo-tebak"
 
OPENID_PROVIDERS = [
    {"name":"Google", "url":"https://www.google.com/accounts/08/id"},
    {"name":"Yahoo", "url":"https://me.yahoo.com"},
    {"name":"AOL", "url":"http://openid.aol.com/<username>"},
    {"name":"Flickr", "url":"http://www.flickr.com/<username>"},
    {"name":"MyOpenID", "url":"https://www.myopenid.com"}
]

Kemudian kita masukkan ke dalam fungsi view kita di app/views.py (lihat parameter terakhir — providers — kita masukkan list provider yang ada di file config dengan memanggil app.config[“OPENID_PROVIDERS”] ).

app/views.py

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("login requested for openID: '%s', remember me: %s" %
              (form.openid.data, str(form.remember_me.data)))
        return redirect("/index")
    return render_template("login.html",
                           title="Sign In",
                           form=form,
                           providers=app.config["OPENID_PROVIDERS"])
						   
						   
Nah sekarang kita akan menampilkan link-link provider tersebut di app/templates/login.html. Tambahan yang dilakukan termasuk daftar link dan script untuk menangani ketika link tersebut diklik.

app/templates/login.html

<!-- include base layout -->
{% extends "base.html" %}
 
{% block content %}
<script type="text/javascript">
    function set_openid(openid, pr) {
        u = openid.search("<username>");
        if(u != -1) {
            // openid requires username
            user = prompt("Enter your " + pr + " username:");
            openid = openid.substr(0, u) + user;
        }
        form = document.forms['login'];
        form.elements['openid'].value = openid;
    }
</script>
    <h1>Sign In</h1>
    <form action="" method="post" name="login">
        {{ form.hidden_tag() }}
        <p>
            Please enter your OpenID:<br />
            {{ form.openid(size=80) }}<br />
            {% for error in form.openid.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}<br />
            |
            {% for pr in providers %}
                <a href="javascript:set_openid('{{ pr.url }}', '{{ pr.name }}')">{{ pr.name }}</a> |
            {% endfor %}
        </p>
        <p>{{ form.remember_me }} Remember Me</p>
        <p><input type="submit" value="Sign In"></p>
    </form>
{% endblock %}

//////////// DATABASES

Database di Flask
Kita akan menggunakan extension Flask-SQLAlchemy untuk aplikasi kita. Extension ini adalah sebuah wrapper untuk SQLAlchemy, sebuah Object Relational Mapper (ORM) untuk python.

ORM akan menyajikan database sebagai objek pada kita, sehingga kita tidak perlu berinteraksi dengan tabel dan SQL. Tentu saja dengan mengetahui SQL akan lebih baik, namun sekarang kita tidak akan belajar SQL. Untuk saat ini, kita manfaatkan saja SQLAlchemy untuk berbicara dengan database.

Salah satu fitur SQLAlchemy yang sangat menguntungkan adalah SQLAlchemy-migrate, yang dapat melacak update pada database kita, sehingga kita bisa mengupdate database jika ada perubahan, tidak dengan menghapus database lama kemudian membuatnya lagi dengan database yang terupdate — yang akan menjadi sulit ketika di database sudah ada data.

Konfigurasi
Untuk tutorial ini, kita akan menggunakan database SQLite. Database ini tidak membutuhkan kita menyalakan database server, dan setiap database akan disimpan dalam satu file. SQLAlchemy, tentu saja men-support database lain, seperti Postgresql, MySQL, Oracle, MS-SQL, Firebird, Sybase, dan lainnya. Kita menggunakan SQLite untuk kenyamanan kita saja saat ini.

Untuk menghubungkan aplikasi Flask kita ke database,

config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
 
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")

SQLALCHEMY_DATABASE_URI adalah path yang menuju ke file database kita. Ini diperlukan oleh Flask-SQLAlchemy.
SQLALCHEMY_MIGRATE_REPO adalah folder untuk menyimpan data migrasi database oleh SQLAlchemy-migrate.

kita butuh menginisialisasi database ketika menginisalisasi aplikasi. Hal ini dilakukan pada app/__init__.py, dengan menambah sebuah objek db yang menjadi database kita dan sebuah modul models yang akan kita tambahkan nanti:

app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
 
from app import views, models

Database model
Jadi seperti yang telah dikatakan sebelumnya, struktur data yang akan disimpan ke database merupakan sekumpulan kelas yang disebut database model. ORM akan mentranslasikan model ini ke dalam tabel database.

Pertama mari kita buat sebuah model untuk merepresentasikan pengguna kita:

++++++++++++++++++++++++++++++
+            users           +
++++++++++++++++++++++++++++++
+  id        +  integer      +
+  nickname  +  varchar(64)  +
+  email     +  varchar(120) +
++++++++++++++++++++++++++++++

Tabel tersebut adalah users, yang menyimpan beberapa field, yaitu id sebagai primary key yang akan berbeda pada setiap entri di tabel, nickname dan email berupa string (VARCHAR) dengan panjang maksimal masing-masing 64 dan 120.

Setelah menentukan struktur tabel yang diinginkan, kita terjemahkan sebagai database model

app/models.py

from app import db
 
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
 
    def __repr__(self):
        return "<User %r>" % self.nickname
		
Kelas User yang kita buat adalah model, yang merupakan subclass dari kelas db.Model untuk tabel yang kita buat tadi, dengan atribut di dalamnya sebagai field, dengan membuat instance dari kelas db.Column dengan argument tipe field dan argument lain. Method __repr__ digunakan untuk mem-print kelas ini, bisa digunakan untuk debugging.

Membuat database
Dengan konfigurasi dan model yang telah dibuat, sekarang kita siap untuk membuat database kita. Package SQLAlchemy-migrate menyediakan command line tools dan API untuk membuat database dengan cara yang memudahkan kita melakukan update nantinya. Untuk memudahkan, kita bisa menulis script python untuk memanggil API tersebut.

db_create.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os
 
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, "database repository")
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
	
Script ini nantinya bisa digunakan setiap kali kita membuat project Flask, karena di sini semua parameter diambil dari file konfigurasi yang telah kita buat. Untuk membuat database, kita cukup mengeksekusi script tersebut

Setelah kita mengeksekusi script tadi, maka akan dibuat file app.db yang berisi database kita, serta folder db_repository yang menyimpan data file dari SQLAlchemy-migrate. Jika kita sudah punya folder tersebut, maka tidak akan dibuat ulang. Artinya, kita dapat membuat database baru dengan mengamankan repository database yang kita punya.

Migrasi database
Karena kita sudah punya model yang dibuat, maka kita akan memindahkan ke dalam database. Kita sebut perpindahan struktur dari model ke database ini sebagai migration. Untuk melakukan migrasi, kita buat satu lagi script python untuk membantu

db_migrate.py

import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
 
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ("/versions/%03d_migration.py" % (v+1))
tmp_module = imp.new_module("old_model")
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
 
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
 
print "New migration saved as" + migration
print "Current database version: " + str(v)

Pada script ini, SQLAlchemy-migrate membuat sebuah migration dengan membandingkan struktur database dengan struktur model kita. Setelah itu, perbedaan tersebut disimpan sebagai script migrasi dalam repository kita. Script ini bisa digunakan untuk meng-upgrade atau downgrade format database kita.

Yang penting diingat adalah walaupun seharusnya script ini bisa berjalan dengan baik, tetap kita harus menyediakan backup database kita setiap sebelum melakukan migrasi. Selain itu, selalu tes migration kita terlebih dahulu di server development sebelum masuk server production.

Kenapa kita menyimpan migrasi database kita setiap saat? Bayangkan kita punya dua buah mesin, satu untuk development satunya lagi untuk produksi. Ketika kita mengubah struktur database di development, otomatis kita harus mengubah juga di produksi. Mengubah struktur database satu persatu tentu saja akan sangat banyak memakan waktu.

Dengan migration, jika dalam pengembangan kita ada perubahan struktur tabel dan database, di server production kita tinggal meng-copy kan saja script migrasi yang telah dibuat (di db_repository) kemudian dimasukkan ke sana. Setelah itu, kita tinggal panggil script tersebut dengan script upgrade dan downgrade. Upgrade dapat dilakukan dengan script berikut 

db_upgrade.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
 
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print "Current database version: " + str(v)

Script di atas adalah untuk meng-upgrade database kita menjadi versi terakhir yang ada di dalam repository kita. Untuk meng-downgrade database kita menjadi versi sebelumnya, kita dapat menjalankan script berikut

db_downgrade.py

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v-1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print "Current database version: " + str(v)

Relasi database
Database relasional dapat menyimpan relasi antar data item dengan baik. Misalnya kasusnya adalah postingan yang dibuat oleh user. Untuk menyimpan siapa yang membuat posting, paling efisien adalah membuat link antara dua tabel tersebut.

Begitu link dibuat, maka akan ada dua operasi yang kita ingin lakukan. Yang pertama adalah mengetahui oleh siapa sebuah posting dibuat, atau mengetahui posting apa saja yang telah dibuat oleh seorang pengguna. Flask-SQLAlchemy akan membantu kita dalam dua operasi tersebut.

Kira-kira begini desain database yang akan kita buat:

++++++++++++++++++++++++++++++                 +++++++++++++++++++++++++++++++
+            users           + +++++           +            posts            +
++++++++++++++++++++++++++++++      +          +++++++++++++++++++++++++++++++
+  id        +  integer      +       +         +  id         +  integer      + 
+  nickname  +  varchar(64)  +        +        +  body       +  varchar(140) +
+  email     +  varchar(120) +         +       +  timestamp  +  datetime     +
++++++++++++++++++++++++++++++          ++++++ +  user_id    +  integer      +
                                               +++++++++++++++++++++++++++++++
											   
Field user_id adalah sebuah link yang menghubungkan antara tabel users dan posts. Field ini akan berisi id dari pengguna yang membuat sebuah postingan. Jenis link ini adalah one to many relationship.

Sekarang kita perbaharui app/models.py untuk menampung perubahan pada database tersebut.

app/models.py

from app import db
 
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
 
    def __repr__(self):
        return "<User %r>" % self.nickname
 
 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
 
    def __repr__(self):
        return "<Post %r>" % self.body
		
Sekarang kita telah menambahkan kelas Post, yang merepresentasikan posting dari user. Field user_id menyertakan db.ForeignKey, yang menandakan bahwa field ini terkait dengan field id pada kelas User.

Kemudian di kelas User kita menambahkan field posts. Field ini merupakan db.relationship, tidak ada dalam tabel asli, namun lebih merupakan sebuah penanda untuk Flask-SQLAlchemy bahwa dengan field itu ada hubungan dengan tabel lainnya. Sehingga, kita dapat memanggil user.posts untuk memanggil posting yang dibuat seorang pengguna dan post.author untuk memanggil user yang membuat sebuah posting.

Setelah dilakukan perubahan model, kita lakukan migrasi seperti yang telah dijelaskan di atas. Versi database sekarang seharusnya adalah 2.

Mencoba model dan database
Jadi, bagaimana sebenarnya model dan database ini bekerja? Mari kita coba di Python interpreter, berhubung aplikasi kita belum terhubung ke database.

Pertama, jalankan interpreter Python, Begitu kita masuk python, kita import database dan model dari aplikasi kita.

>>> from app import db, models

Setelah itu mari kita membuat sebuah user:

>>> u1 = models.User(nickname="peter", email="peter@email.com")
>>> db.session.add(u1)
>>> db.session.commit()

Perubahan database akan disimpan pada session. Perubahan dapat dilakukan namun baru akan ter-register jika kita memanggil db.session.commit(). Jika kita terkena error atau ingin membatalkan perubahan, kita dapat memanggil db.session.callback(). Session ini menjamin database selalu konsisten.

Sekarang kita tambahkan user lain:

>>> u2 = models.User(nickname="rachel", email="rachel@email.com")
>>> db.session.add(u2)
>>> db.session.commit()

Sekarang kita dapat meng-query user yang telah kita masukkan:

>>> users = models.User.query.all()
>>> users
[<User u'peter'>, <User u'rachel'>]
>>> for u in users:
...     print(u.id, u.nickname)
...
(1, u'peter')
(2, u'rachel')
>>>

query dapat dilakukan pada semua kelas model. Contoh di atas adalah meng-query semua baris user yang ada dalam tabel. Kita juga dapat meng-query satu baris, jika kita sudah mengetahui id-nya:

>>> u = models.User.query.get(1)
>>> u
<User u'peter'>
>>>

Sekarang kita coba masukkan sebuah post:

>>> import datetime
>>> u = models.User.query.get(2)
>>> p = models.Post(body="rachel's first post!", timestamp=datetime.datetime.utcnow(), author=u)
>>> db.session.add(p)
>>> u2 = models.User.query.get(1)
>>> p2 = models.Post(body="hi rachel, i'm peter", timestamp=datetime.datetime.utcnow(), author=u2)
>>> db.session.add(p2)
>>> db.session.commit()

Script di atas adalah untuk menambahkan dua buah post, yaitu post dari rachel dan peter, dua user yang telah kita masukkan tadi. Untuk timestamp, kita menggunakan UTC, agar seragam jika diisi dari berbagai belahan dunia.

Untuk kelas Post, seperti yang dilihat, kita tidak memasukkan field user_id, melainkan memasukkan author. Flask-SQLAlchemy akan menerjemahkan informasi tersebut sehingga menjadi field user_id di database.

Mari kita lanjutkan dengan beberapa query,
Ambil semua post dari satu user:

>>> u = models.User.query.get(1)
>>> u
<User u'peter'>
>>> posts = u.posts.all()
>>> posts
[<Post u"hi rachel, i'm peter">]

Ambil penulis dari masing-masing post:

>>> all_posts = models.User.query.all()
>>> all_posts = models.Post.query.all()
>>> for post in all_posts:
...     print(post.id, post.author.nickname, post.body)
...
(1, u'rachel', u"rachel's first post!")
(2, u'peter', u"hi rachel, i'm peter")

Ambil user dengan pengurutan:

>>> models.User.query.order_by("nickname desc").all()
[<User u'rachel'>, <User u'peter'>]
>>>

Kita masih bisa banyak bermain-main dengan query database dengan mengacu pada dokumentasi Flask-SQLAlchemy. Sebelum mengakhiri tutorial ini, kita hapus dulu data yang tadi kita masukkan, agar di bagian selanjutnya kita memulai dari awal.

>>> users = models.User.query.all()
>>> for u in users:
...     db.session.delete(u)
...
>>> posts = models.Post.query.all()
>>> for p in posts:
...     db.session.delete(p)
...
>>> db.session.commit()

//////////// USER LOGIN



//////////// PROFILE PAGE AND AVATAR

Halaman Profil
Sekarang, kita akan membuat halaman profil. Sesungguhnya untuk membuat halaman profil, tidak ada konsep yang baru. Pertama, kita akan membuat view untuk profil di app/views.py:

app/views.py

@app.route("/user/<nickname>")
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash("User %s not found" % nickname)
        return redirect(url_for("index"))
    posts = [
        {"author": user, "body": "Test post 1"},
        {"author": user, "body": "Test post 2"}
    ]
    return render_template("user.html",
                           user=user,
                           posts=posts)
						   
Pada decorator, kita dapat melihat bahwa route kita menerima satu argument yaitu nickname. Jadi, ketika nanti kita memanggil dengan argument tersebut, dia akan masuk ke dalam fungsi yang ditunjuk oleh route. Jadi misalnya kita memanggil /user/uman, maka fungsi ini akan menerima nickname dengan nilai uman.

Untuk fungsinya sendiri tidak ada hal yang aneh. Pertama, kita mencoba me-load user dengan nickname yang diberikan, jika tidak ada maka kita redirect ke index. Jika ada, maka kita load post dari pengguna tersebut (disini masih kita masukkan data palsu), dan me-render template app/templates/user.html:

app/templates/user.html

{% extends "base.html" %}
 
{% block content %}
    <h1>User: {{ user.nickname }}</h1>
    <hr />
    {% for post in posts %}
    <p>
        {{ post.author.nickname }} said: <b>{{ post.body }}</b>
    </p>
    {% endfor %}
{% endblock %}

Sekarang halaman user kita sudah selesai, namun masih belum ada link untuk masuk ke halaman tersebut. Maka kita masukkan ke dalam base.html kita, link untuk masuk ke dalam profil masing-masing. Kita edit app/templates/base.html, pada bagian div pertama di atas:

<div>
    Microblog: <a href="{{ url_for('index') }}">Home</a>
    {% if g.user.is_authenticated %}
    | <a href="{{ url_for('user', nickname=g.user.nickname) }}">Your Profile</a>
    | <a href="{{ url_for('logout') }}">Logout</a>
    {% endif %}
</div>

Nah sekarang kita punya link untuk masuk ke dalam halaman profil, tentu saja dengan argument nickname. Untuk masuk ke profil orang lain, kita harus mengetik nama user nya sendiri.

Avatar
mewarnai halaman profil kita, mari kita tambahkan Avatar di halaman profil kita. Kita akan menggunakan service Gravatar untuk menyediakan avatar pengguna di aplikasi kita.

Pertama, kita akan memasukkan avatar tersebut ke kelas User di model (app/models.py).

app/models.py

from hashlib import md5
#....
 
class User(db.Model):
    #....
    def avatar(self, size):
        return "http://www.gravatar.com/avatar/%s?d=mm&s=%d" % (md5(self.email.encode("utf8")).hexdigest(), size)

Method avatar pada kelas User akan mengembalikan link ke avatar pengguna. Service gravatar cukup membutuhkan hash md5 dari alamat email. Parameter lainnya menunjukkan beberapa fungsi lain dalam memanggil service Gravatar. d=mm akan mengembalikan gambar mystery man jika pada layanan tidak ditemukan alamat email yang dimaksud. s=N akan mengubah gambar menjadi skala tertentu.

app/templates/user.html

{% extends "base.html" %}
 
{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}" /></td>
            <td><h1>User: {{ user.nickname }}</h1></td>
        </tr>
    </table>
 
    <hr />
    {% for post in posts %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(50) }}" /></td>
            <td><i>{{ post.author.nickname }} said:</i>
<b>{{ post.body }}</b></td>
        </tr>
    </table>
    {% endfor %}
{% endblock %}

Kita menambahkan method avatar pada beberapa titik di template, yaitu di header dan masing-masing post. Pada method tersebut, kita menambahkan parameter berupa ukuran avatar yang diinginkan, dengan ukuran pada header lebih besar dari ukuran pada masing-masing post. 

Menggunakan sub-template
Kita lihat kita melakukan hal yang sama pada dua buah bagian pada aplikasi ini, yaitu menampilkan post pada index dan halaman user. Agar tidak mengulang-ulang hal tersebut, kita dapat menggunakan sub-template. Sebenarnya, sub-template sama saja dengan template biasa. Kita buat app/templates/post.html:

app/templates/post.html

<table>
    <tr valign="top">
        <td><img src="{{ user.avatar(50) }}" /></td>
        <td><i>{{ post.author.nickname }} said:</i>
<b>{{ post.body }}</b></td>
    </tr>
</table>

Lalu kita masukkan sub-template tersebut ke dalam template app/templates/user.html dengan menggunakan fungsi Jinja2 include

app/templates/user.html

{% extends "base.html" %}
 
{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}" /></td>
            <td><h1>User: {{ user.nickname }}</h1></td>
        </tr>
    </table>
 
    <hr />
    {% for post in posts %}
        {% include 'post.html' %}
    {% endfor %}
{% endblock %}

Menambahkan profil pengguna
Nah meskipun sekarang kita sudah punya halaman profil, tetapi dilihat-lihat garing juga ternyata. Mari kita tambahkan sebuah field untuk menampung apa yang ingin diceritakan oleh pengguna pada halaman profil nya. Kita akan tambahkan juga kapan si pengguna main ke website ini. Kita akan tambahkan pada kelas User di model app/models.py.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
	
Perlu diingat, setelah kita melakukan perubahan pada model, kita perlu melakukan perubahan pula pada database. Untungnya, pada waktu yang lalu kita sudah membuat sebuah prosedur untuk memudahkan hal itu. Sekarang kita jalankan script migrate.py:

python db_migrate.py

Sekarang field tersebut sudah muncul di database kita. Jika kita tidak punya script untuk mendukung migrasi database, kita harus mengubah secara manual database kita, atau lebih parah harus menghapus dan membuat ulang database kita.

Selanjutnya, kita akan menampilkan field-field baru ini di template kita app/templates/user.html

{% extends "base.html" %}
 
{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}" /></td>
            <td>
                <h1>User: {{ user.nickname }}</h1>
                {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
                {% if user.last_seen %}<p><i>last seen on: {{ user.last_seen }}</i></p>{% endif %}
            </td>
        </tr>
    </table>
 
    <hr />
    {% for post in posts %}
        {% include 'post.html' %}
    {% endfor %}
{% endblock %}

Pada template di atas, saat kita ingin menampilkan about me dan last seen, kita menggunakan if, artinya sebelum menampilkan kita mengecek apakah field tersebut terisi atau tidak. Jika tidak terisi, maka kita tidak akan menuliskannya.

Pertanyaan selanjutnya adalah, bagaimana kita memasukkan data untuk kedua field tersebut. Untuk field last_seen kita akan memasukkannya pada before_request saat kita mendaftarkan user pada variabel global flask.g. Kita akan masukkan ke dalam app/views.py:

from datetime import datetime
#....
 
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
		
Seperti bagian sebelumnya, kita menggunakan datetime.utcnow() untuk memasukkan nilai waktu saat ini (dalam UTC). UTC digunakan untuk menjaga konsistensi, untuk menampilkan waktu secara lebih nyaman nantinya (menurut zona waktu masing-masing), kita akan membahas dalam bagian terpisah nanti.

Untuk mengubah data pada about_me, kita harus membuat sebuah form untuk mengedit profil.

Mengedit profil
Untuk membuat sebuah form ternyata tidak begitu sulit. Pertama, kita mulai dengan membuat form di file app/forms.py:

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
 
#....
 
class EditForm(Form):
    nickname = StringField("nickname", validators=[DataRequired()])
    about_me = TextAreaField("about_me", validators=[Length(min=0, max=140)])
	
Selanjutnya, kita membuat template di app/templates/edit.html:

{% extends "base.html" %}
 
{% block content %}
    <h1>Edit your profile</h1>
    <form action="" method="post" name="edit">
        {{ form.hidden_tag() }}
        <table>
            <tr>
                <td>Nickname:</td>
                <td>{{ form.nickname(size=24) }}</td>
            </tr>
            <tr>
                <td>About yourself:</td>
                <td>{{ form.about_me(cols=32, rows=4) }}</td>
            </tr>
            <tr>
                <td></td>
                <td><input type="submit" value="Save" /></td>
            </tr>
        </table>
    </form>
{% endblock %}

Setelah itu, kita buat fungsi pada view (app/views.py):

from .forms import LoginForm, EditForm
#...
 
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash("your changes have been saved")
        return redirect(url_for("edit"))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return  render_template("edit.html", form=form)
	
Agar halaman ini bisa diakses dengan mudah, kita tambahkan link pada halaman profil app/templates/user.html, dengan catatan link ini hanya bisa diakses jika kita login sebagai user tersebut:

{% extends "base.html" %}
 
{% block content %}
    <table>
        <tr valign="top">
            <td><img src="{{ user.avatar(128) }}" /></td>
            <td>
                <h1>User: {{ user.nickname }}</h1>
                {% if user.about_me %}<p>{{ user.about_me }}</p>{% endif %}
                {% if user.last_seen %}<p><i>last seen on: {{ user.last_seen }}</i></p>{% endif %}
                {% if user.id == g.user.id %}<p><a href="{{ url_for('edit') }}">Edit</a></p>{% endif %}
            </td>
        </tr>
    </table>
 
    <hr />
    {% for post in posts %}
        {% include 'post.html' %}
    {% endfor %}
{% endblock %}

//////////// UNIT TESTING



//////////// 
//////////// 
//////////// 
Reference
https://umanium.wordpress.com/2015/09/29/python-flask-tutorial-1-instalasi-dan-hello-world/

