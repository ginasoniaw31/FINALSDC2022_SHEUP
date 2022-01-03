from flask import render_template, redirect, url_for, request, flash, session
import os
from app import app
import re
import random

R_ABOUT = "Virasschool (Virtual Assisten Educational Institution in Tegal) adalah asisten virtual untuk mencari informasi lembaga pendidikan khususnya untuk jenjang pendidikan SD, SMP, dan SMA/SMK yang ingin diketahui oleh masyarakat, serta calon siswa yang akan mendaftarkan diri ke lembaga pendidikan terkait yang ada di Kota Tegal."
R_D4 = "Mempermudah masyarakat dan calon siswa khususnya yang ada di sekitar wilayah Kota Tegal untuk mendapatkan informasi umum seputar lembaga pendidikan yang ada melalui sebuah website yang dilengkapi dengan chatbot"
def unknown():
    response = ["Maaf bisa ketikan dengan jelas? ",
                "...",
                "Maaf Vira tidak mengerti pertanyaanmu",][
        random.randrange(4)]
    return response

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Greeting-------------------------------------------------------------------------------------------------------
    response('Hello!', ['helo', 'hai', 'hi','halo','hallo'], single_response=True)
    response('Pagi juga!', ['pagi', 'selamat pagi'], single_response=True)
    response('Siang juga!', ['siang', 'selamat siang'], single_response=True)
    response('Sore juga!', ['sore', 'selamat sore'], single_response=True)
    response('Malam juga!', ['malam', 'selamat malam'], single_response=True)
    response('Semoga membantu!', ['oke', 'terimakasih','oke','makasih'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('Semester','Prodi TI', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    
    #Rekomend---------------------------------------------------------------------------
    response('SD N MANGKUKUSUMAN 8, SD N MANGKUKUSUMAN 1', ['sd', 'sekolah dasar','terbaik'], single_response=True)
    response('SMP N 1 TEGAL, SMP N 2 TEGAL, SMP N 7 TEGAL', ['smp', 'sekolah menengah pertama', 'terbaik'], single_response=True)
    response('SMA N 1 TEGAL, SMA N 4 TEGAL, SMA N 3 TEGAL', ['sma', 'sekolah menengah atas','terbaik'], single_response=True)
    response('SMK N 1 TEGAL, SMK N 3 TEGAL', ['smk', 'sekolah menengah kejuruan','terbaik'], single_response=True)


    #SD KOTA TEGAL-------------------------------------------------------------------------------------------------------
    #data sd
    response('pada website ini terdapat informasi tentang 35 lembaga pendidikan sd yang ada di kota tegal',['jumlah','sd','tegal'], single_response=True)
    response('pada website ini terdapat beberapa sd yang ada di kota tegal yaitu : sd negeri randugunting 5, sd negeri randugunting 6, sd negeri randugunting 7, sd negeri tunon 1, sd negeri tunon 2, sd aisyiyah cahaya insan, sd ihsaniyah 1 tegal, sd it usamah, sd muhammadiyah 1, sd muhammadiyah 2, sd negeri kejambon 8, sd negeri kejambon 7, sd negeri kejambon 6, sd negeri kejambon 5, sd negeri kejambon 4, sd negeri kejambon 3, sd negeri kejambon 2, sd negeri kejambon 1, sd negeri kejambon 10, sd negeri mangkukusuman 1, sd negeri mangkukusuman 2, sd negeri mangkukusuman 3, sd negeri kalinyamat wetan 3. sd negeri kalinyamat wetan 2, sd negeri kalinyamat wetan 1, sd negeri debong tengah 3, sd negeri debong tengah 2, sd negeri debong tengah 1,sd negeri debong kulon 1, sd negeri debong kidul 1,sd negeri bandung 3,sd negeri bandung 2, sd negeri bandung 1,sd muhammadiyah 3,sd it bina iman dan amal shaleh assalam',['data','sd','yang', 'ada'], single_response=True)

    #sd it bina iman dan amal shaleh assalam
    response('sd it bina iman dan amal shaleh assalam beralamat di jl dadali no.12, randugunting, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52131.',['alamat','sd', 'it', 'bina', 'iman', 'dan', 'amal', 'shaleh', 'assalam'], single_response=True)
    response('url website : http://biasassalam.sch.id. email : assalambias@gmail.com. nomor fax sekolah : 62283343090.',['kontak','sd', 'it', 'bina', 'iman', 'dan', 'amal', 'shaleh', 'assalam'], single_response=True)
    response('sd it bina iman dan amal shaleh assalam menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'it', 'bina', 'iman', 'dan', 'amal', 'shaleh', 'assalam'], single_response=True)
    response('pembelajaran di sd it bina iman dan amal shaleh assalam dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',['waktu', 'pembelajaran','sd', 'it', 'bina', 'iman', 'dan', 'amal', 'shaleh', 'assalam' ], single_response=True)
    response('sd it bina iman dan amal shaleh assalam memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'it', 'bina', 'iman', 'dan', 'amal', 'shaleh', 'assalam',], single_response=True)

    #sd muhammadiyah 3
    response('sd muhammadiyah 3 beralamat di jl. banyumas no. 8, debong tengah, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52132.',['alamat','sd','muhammadiyah','3'], single_response=True)
    response('email : sdmugaceri@ymail.com.',['kontak','sd','muhammadiyah','3'], single_response=True)
    response('sd muhammadiyah 3 menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd','muhammadiyah','3'], single_response=True)
    response('pembelajaran di sd muhammadiyah 3 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd','muhammadiyah','3'], single_response=True)
    response('sd muhammadiyah 3 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd','muhammadiyah','3'], single_response=True)

    #sd negeri bandung 1
    response('sd negeri bandung 1 beralamat di jl teuku cik ditiro no.153, bandung, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52137.',[ 'alamat','sd', 'negeri', 'bandung', '1'], single_response=True)
    response('email : sdnbandung1@gmail.com. nomor fax sekolah : 0283358033.',['kontak','sd', 'negeri', 'bandung', '1'], single_response=True)
    response('sd negeri bandung 1 menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd', 'negeri', 'bandung', '1'], single_response=True)
    response('pembelajaran di sd negeri bandung 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'bandung', '1'], single_response=True)
    response('sd negeri bandung 1 memiliki akreditasi b, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'bandung', '1'], single_response=True)

    #sd negeri bandung 2
    response('sd negeri bandung 2 beralamat di jl. teuku cik ditiro no. 155 bandung tegal, bandung, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52137.',[ 'alamat','sd', 'negeri', 'bandung', '2'], single_response=True)
    response('email : sdn_bandung2@yahoo.com.',['kontak','sd', 'negeri', 'bandung', '2'], single_response=True)
    response('sd negeri bandung 2 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'bandung', '2'], single_response=True)
    response('pembelajaran di sd negeri bandung 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'bandung', '2'], single_response=True)
    response('sd negeri bandung 2 memiliki akreditasi b, berdasarkan sertifikat 137/bap-sm/x/2014.',['akreditasi','sd', 'negeri', 'bandung', '2'], single_response=True)

    #sd negeri bandung 3
    response('sd negeri bandung 3 beralamat di jl. teuku cik ditiro no. 87, bandung, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52137.',[ 'alamat','sd', 'negeri', 'bandung', '3'], single_response=True)
    response('email : sdnbandung3@gmail.com.',['kontak','sd', 'negeri', 'bandung', '3'], single_response=True)
    response('sd negeri bandung 3 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'bandung', '3'], single_response=True)
    response('pembelajaran di sd negeri bandung 3 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'bandung', '3'], single_response=True)
    response('sd negeri bandung 3 memiliki akreditasi a, berdasarkan sertifikat 220/bap-sm/x/2016.',['akreditasi','sd', 'negeri', 'bandung', '3'], single_response=True)

    #sd negeri debong kidul 1
    response('sd negeri debong kidul 1 beralamat di tegal, debong kidul, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52138.',[ 'alamat','sd', 'negeri', 'debong', 'kidul', '1'], single_response=True)
    response('url website : http://sddebongkidul.blogspot.com. email :  debkid1@gmail.com. ',['kontak','sd', 'negeri', 'debong', 'kidul', '1'], single_response=True)
    response('sd negeri debong kidul 1 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'debong', 'kidul', '1'], single_response=True)
    response('pembelajaran di sd negeri debong kidul 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'debong', 'kidul', '1'], single_response=True)
    response('sd negeri debong kidul 1 memiliki akreditasi b, berdasarkan sertifikat 220/bap-sm/x/2016.',['akreditasi','sd', 'negeri', 'debong', 'kidul', '1'], single_response=True)

    #sd negeri debong kulon 1
    response('sd negeri debong kulon 1 beralamat di jl. samadikun no. 46 tegal, debong kulon, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52133.',[ 'alamat','sd', 'negeri', 'debong', 'kulon', '1'], single_response=True)
    response('url website :http://sddebongkulon1tegal.sch.id. email : debongkulon@yahoo.com. ',[ 'kontak','sd', 'negeri', 'debong', 'kulon', '1'], single_response=True)
    response('sd negeri debong kulon 1 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'debong', 'kulon', '1'], single_response=True)
    response('pembelajaran di sd negeri debong kulon 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'debong', 'kulon', '1'], single_response=True)
    response('sd negeri debong kulon 1 memiliki akreditasi b, berdasarkan sertifikat 147/bap-sm/x/2015.',['akreditasi','sd', 'negeri', 'debong', 'kulon', '1'], single_response=True)

    #sd negeri debong tengah 1
    response('sd negeri debong tengah 1 beralamat di jalan teuku umar no. 2 tegal, debong tengah, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52132.',[ 'alamat','sd', 'negeri', 'debong', 'tengah', '1'], single_response=True)
    response('email :  sd_dt01@yahoo.com.',['kontak','sd', 'negeri', 'debong', 'tengah', '1'], single_response=True)
    response('sd negeri debong tengah 1 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'debong', 'tengah', '1'], single_response=True)
    response('pembelajaran di sd negeri debong tengah 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'debong', 'tengah', '1'], single_response=True)
    response('sd negeri debong tengah 1 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'debong', 'tengah', '1'], single_response=True)

    #sd negeri debong tengah 2
    response('sd negeri debong tengah 2 beralamat di jalan teuku umar no.1, debong tengah, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52132.',[ 'alamat','sd', 'negeri', 'debong', 'tengah', '2'], single_response=True)
    response('email : sdn_debongtengah2@yahoo.co.id.',['kontak','sd', 'negeri', 'debong', 'tengah', '2'], single_response=True)
    response('sd negeri debong tengah 2 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'debong', 'tengah', '2'], single_response=True)
    response('pembelajaran di sd negeri debong tengah 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'debong', 'tengah', '2'], single_response=True)
    response('sd negeri debong tengah 2 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'debong', 'tengah', '2'], single_response=True)

    #sd negeri debong tengah 3
    response('sd negeri debong tengah 3 tegal beralamat di jalan teuku umar 1 tegal, debong tengah, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52132.',[ 'alamat','sd', 'negeri', 'debong', 'tengah', '3'], single_response=True)
    response('url website : http://www.sddebteng3.com. email : uchokcoki@gmail.com.',[ 'kontak','sd', 'negeri', 'debong', 'tengah', '3'], single_response=True)
    response('sd negeri debong tengah 3 tegal menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'debong', 'tengah', '3'], single_response=True)
    response('pembelajaran di sd negeri debong tengah 3 tegal dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'debong', 'tengah', '3'], single_response=True)
    response('sd negeri debong tengah 3 tegal memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'debong', 'tengah', '3'], single_response=True)

    #sd negeri kalinyamat wetan 1 
    response('sd negeri kalinyamat wetan 1 beralamat di jl. ir. juanda no. 128 rt. 01 rw. 03, kalinyamat wetan, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52136.',[ 'alamat','sd', 'negeri', 'kalinyamat', 'wetan', '1'], single_response=True)
    response('url website : http://sdnkalwet1.blogspot.co.id. email : sdnkalwetsatu@gmail.com.',[ 'kontak','sd', 'negeri', 'kalinyamat', 'wetan', '1'], single_response=True)
    response('sd negeri kalinyamat wetan 1 menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd', 'negeri', 'kalinyamat', 'wetan', '1'], single_response=True)
    response('pembelajaran di sd negeri kalinyamat wetan 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kalinyamat', 'wetan', '1'], single_response=True)
    response('sd negeri kalinyamat wetan 1 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'kalinyamat', 'wetan', '1'], single_response=True)

    #sd negeri kalinyamat wetan 2
    response('sd negeri kalinyamat wetan 2 beralamat di jl. sultan hasanudin, kalinyamat wetan, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52136.',[ 'alamat','sd', 'negeri', 'kalinyamat', 'wetan', '2'], single_response=True)
    response('email : sdkalinyamatwetan2tegal@gmail.com. ',['kontak','sd', 'negeri', 'kalinyamat', 'wetan', '2'], single_response=True)
    response('sd negeri kalinyamat wetan 2 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'kalinyamat', 'wetan', '2'], single_response=True)
    response('pembelajaran di sd negeri kalinyamat wetan 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kalinyamat', 'wetan', '2'], single_response=True)
    response('sd negeri kalinyamat wetan 2 memiliki akreditasi b, berdasarkan sertifikat 137/bap-sm/x/2014.',['akreditasi','sd', 'negeri', 'kalinyamat', 'wetan', '2'], single_response=True)

    #sd negeri kalinyamat wetan 3
    response('sd negeri kalinyamat wetan 3 tegal beralamat di jalan ir juanda kalinyamat wetan tegal, kalinyamat wetan, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52136.',[ 'alamat','sd', 'negeri', 'kalinyamat', 'wetan', '3'], single_response=True)
    response('email : sdnkalinyamatwetan3@gmail.com.',['kontak','sd', 'negeri', 'kalinyamat', 'wetan', '3'], single_response=True)
    response('sd negeri kalinyamat wetan 3 tegal menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'kalinyamat', 'wetan', '3'], single_response=True)
    response('pembelajaran di sd negeri kalinyamat wetan 3 tegal dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kalinyamat', 'wetan', '3'], single_response=True)
    response('sd negeri kalinyamat wetan 3 tegal memiliki akreditasi b, berdasarkan sertifikat .',['akreditasi','sd', 'negeri', 'kalinyamat', 'wetan', '3'], single_response=True)

    #sd negeri mangkukusuman 3 
    response('sd negeri mangkukusuman 3 beralamat di jl. kh mansyur no. 6, mangkukusuman, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52123.',[ 'alamat','sd', 'negeri', 'mangkukusuman', '3'], single_response=True)
    response('email : mkk3tegal@gmail.com.',['kontak','sd', 'negeri', 'mangkukusuman', '3'], single_response=True)
    response('sd negeri mangkukusuman 3 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'mangkukusuman', '3'], single_response=True)
    response('pembelajaran di sd negeri mangkukusuman 3 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'mangkukusuman', '3'], single_response=True)
    response('sd negeri mangkukusuman 3 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'mangkukusuman', '3'], single_response=True)

    #sd negeri mangkukusuman 2
    response('sd negeri mangkukusuman 2 beralamat di jl. kh. ahmad dahlan no. 14 tegal, mangkukusuman, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52123.',[ 'alamat','sd', 'negeri', 'mangkukusuman', '2'], single_response=True)
    response('email : sdnmangkukusuman2@yahoo.com.',['kontak','sd', 'negeri', 'mangkukusuman', '2'], single_response=True)
    response('sd negeri mangkukusuman 2 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'mangkukusuman', '2'], single_response=True)
    response('pembelajaran di sd negeri mangkukusuman 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'mangkukusuman', '2'], single_response=True)
    response('sd negeri mangkukusuman 2 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'mangkukusuman', '2'], single_response=True)

    #sd negeri mangkukusuman 1
    response('sd negeri mangkukusuman 1 beralamat di jl. kh. ahmad dahlan no. 24, mangkukusuman, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52123.',[ 'alamat','sd', 'negeri', 'mangkukusuman', '1'], single_response=True)
    response('email  : sdnmkk1@gmail.com.',['kontak','sd', 'negeri', 'mangkukusuman', '1'], single_response=True)
    response('sd negeri mangkukusuman 1 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. ',['fasilitas' ,'sd', 'negeri', 'mangkukusuman', '1'], single_response=True)
    response('pembelajaran di sd negeri mangkukusuman 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'mangkukusuman', '1'], single_response=True)
    response('sd negeri mangkukusuman 1 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'mangkukusuman', '1'], single_response=True)

    #sd negeri kejambon 8 
    response('sd negeri kejambon 8 beralamat di jl.kemuning no.47, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '8'], single_response=True)
    response('email : sdnegerikejambon8tegal@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '8'], single_response=True)
    response('sd negeri kejambon 8 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'kejambon', '8'], single_response=True)
    response('pembelajaran di sd negeri kejambon 8 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '8'], single_response=True)
    response('sd negeri kejambon 8 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'kejambon', '8'], single_response=True)

    #sd negeri kejambon 7 
    response('sd negeri kejambon 7 beralamat di jl. nakula utara, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '7'], single_response=True)
    response('email : ssdnegerikejambon7@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '7'], single_response=True)
    response('sd negeri kejambon 7 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'kejambon', '7'], single_response=True)
    response('pembelajaran di sd negeri kejambon 7 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '7'], single_response=True)
    response('sd negeri kejambon 7 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'kejambon', '7'], single_response=True)

    #sd negeri kejambon 6
    response('sd negeri kejambon 6 beralamat di jl.abimanyu no.14, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '6'], single_response=True)
    response('email : sdkejambon6@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '6'], single_response=True)
    response('sd negeri kejambon 6 menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd', 'negeri', 'kejambon', '6'], single_response=True)
    response('pembelajaran di sd negeri kejambon 6 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '6'], single_response=True)
    response('sd negeri kejambon 6 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'kejambon', '6'], single_response=True)

    #sd negeri kejambon 5
    response('sd negeri kejambon 5 beralamat di jl.abimanyu n0.14 tegal, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '5'], single_response=True)
    response('email : sdn.kejambon5@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '5'], single_response=True)
    response('sd negeri kejambon 5 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'kejambon', '5'], single_response=True)
    response('pembelajaran di sd negeri kejambon 5 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '5'], single_response=True)
    response('sd negeri kejambon 5 memiliki akreditasi a, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'kejambon', '5'], single_response=True)

    #sd negeri kejambon 4
    response('sd negeri kejambon 4 beralamat di jl. nakula utara no. 50, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '4'], single_response=True)
    response('url webaite : http://https://m.facebook.com/kejambon.papat. email : sdnkejambon04@gmail.com.',[ 'kontak','sd', 'negeri', 'kejambon', '4'], single_response=True)
    response('sd negeri kejambon 4 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'kejambon', '4'], single_response=True)
    response('pembelajaran di sd negeri kejambon 4 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '4'], single_response=True)
    response('sd negeri kejambon 4 memiliki akreditasi b, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'kejambon', '4'], single_response=True)

    #sd negeri kejambon 3
    response('sd negeri kejambon 3 beralamat di jl.nakula utara no.50 tegal, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '3'], single_response=True)
    response('email : sdn.kejambon3@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '3'], single_response=True)
    response('sd negeri kejambon 3 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'kejambon', '3'], single_response=True)
    response('pembelajaran di sd negeri kejambon 3 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '3'], single_response=True)
    response('sd negeri kejambon 3 memiliki akreditasi b, berdasarkan sertifikat 220/bap-sm/x/2016.',['akreditasi','sd', 'negeri', 'kejambon', '3'],single_response=True)

    #sd negeri kejambon 2
    response('sd negeri kejambon 2 beralamat di jl. menteri supeno no. 2, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '2'], single_response=True)
    response('email : sdnkejambon2tegal@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '2'], single_response=True)
    response('sd negeri kejambon 2 menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd', 'negeri', 'kejambon', '2'], single_response=True)
    response('pembelajaran di sd negeri kejambon 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '2'], single_response=True)
    response('sd negeri kejambon 2 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'kejambon', '2'], single_response=True)

    #sd negeri kejambon 10
    response('sd negeri kejambon 10 beralamat di jl.nakula utara no.50, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '10'], single_response=True)
    response('email : sdkejambon10@gmail.com.',['kontak','sd', 'negeri', 'kejambon', '10'], single_response=True)
    response('sd negeri kejambon 10 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'kejambon', '10'], single_response=True)
    response('pembelajaran di sd negeri kejambon 10 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '10'], single_response=True)
    response('sd negeri kejambon 10 memiliki akreditasi a, berdasarkan sertifikat 137/bap-sm/x/2014.',['akreditasi','sd', 'negeri', 'kejambon', '10'], single_response=True)

    #sd negeri kejambon 1
    response('sd negeri kejambon 1 beralamat di jl. kemuning no.49, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'negeri', 'kejambon', '1'], single_response=True)
    response('email : kejambonsatu@ymail.com. nomor fax sekolah : 0283342415.',['kontak','sd', 'negeri', 'kejambon', '1'], single_response=True)
    response('sd negeri kejambon 1 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'kejambon', '1'], single_response=True)
    response('pembelajaran di sd negeri kejambon 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'kejambon', '1'], single_response=True)
    response('sd negeri kejambon 1 memiliki akreditasi b, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'kejambon', '1'], single_response=True)

    #sd muhammadiyah 2
    response('sd muhammadiyah 2 beralamat di jl. melati no. 14, kejambon, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52124.',[ 'alamat','sd', 'muhammadiyah', '2'], single_response=True)
    response('email : esdemuhammadiyah@yahoo.co.id.',[ 'kontak','sd', 'muhammadiyah', '2'], single_response=True)
    response('sd muhammadiyah 2 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'muhammadiyah', '2'], single_response=True)
    response('pembelajaran di sd muhammadiyah 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'muhammadiyah', '2'], single_response=True)
    response('sd muhammadiyah 2 memiliki akreditasi b, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'muhammadiyah', '2'], single_response=True)

    #sd muhammadiyah 1
    response('sd muhammadiyah 1 beralamat di jl. cempaka no. 67, mangkukusuman, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52123.',[ 'alamat','sd', 'muhammadiyah', '1'], single_response=True)
    response('url website : http://www.sdmututegal.sch.id. email : sdmutugal@gmail.com.',[ 'kontak','sd', 'muhammadiyah', '1'], single_response=True)
    response('sd muhammadiyah 1 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'muhammadiyah', '1'], single_response=True)
    response('pembelajaran di sd muhammadiyah 1 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'muhammadiyah', '1'], single_response=True)
    response('sd muhammadiyah 1 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'muhammadiyah', '1'], single_response=True)

    #sd it usamah
    response('sd it usamah beralamat di jl surabayan, panggung, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52122.',[ 'alamat','sd', 'it', 'usamah'], single_response=True)
    response('url website : http://www.yru.or.id. email : datasditusamah@gmail.com.',[ 'kontak','sd', 'it', 'usamah'], single_response=True)
    response('sd it usamah menyediakan listrik untuk membantu kegiatan belajar mengajar.sd it usamah menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'it', 'usamah'], single_response=True)
    response('pembelajaran di sd it usamah dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'it', 'usamah'], single_response=True)
    response('sd it usamah memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'it', 'usamah'], single_response=True)

    #sd ihsaniyah 1 tegal
    response('sd ihsaniyah 1 tegal beralamat di jalan waringin no. 27 tegal, mintaragen, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52121.',[ 'alamat','sd', 'ihsaniyah', '1', 'tegal'], single_response=True)
    response('url website : http://www.sdihsaniyah1pusakategal.com. email : webihsaniyah1@gmail.com.',[ 'kontak','sd', 'ihsaniyah', '1', 'tegal'], single_response=True)
    response('sd ihsaniyah 1 tegal menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. ',['fasilitas' ,'sd', 'ihsaniyah', '1', 'tegal'], single_response=True)
    response('pembelajaran di sd ihsaniyah 1 tegal dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'ihsaniyah', '1', 'tegal'], single_response=True)
    response('sd ihsaniyah 1 tegal memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'ihsaniyah', '1', 'tegal'], single_response=True)

    #sd aisyiyah cahaya insan
    response('sd aisyiyah cahaya insan beralamat di jalan werkudoro no. 2, slerok, kec. tegal timur, kota tegal, jawa tengah, dengan kode pos 52125.',[ 'alamat','sd', 'aisyiyah', 'cahaya', 'insan'], single_response=True)
    response('email : sdaisyiyah_ci@yahoo.com.',['kontak','sd', 'aisyiyah', 'cahaya', 'insan'], single_response=True)
    response('sd aisyiyah cahaya insan menyediakan listrik untuk membantu kegiatan belajar mengajar. ',['fasilitas' ,'sd', 'aisyiyah', 'cahaya', 'insan'], single_response=True)
    response('pembelajaran di sd aisyiyah cahaya insan dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'aisyiyah', 'cahaya', 'insan'], single_response=True)
    response('sd aisyiyah cahaya insan memiliki akreditasi b, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'aisyiyah', 'cahaya', 'insan'], single_response=True)

    #sd negeri tunon 2
    response('sd negeri tunon 2 beralamat di tegal, tunon, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52135.',[ 'alamat','sd', 'negeri', 'tunon', '2'], single_response=True)
    response('email :  sdntunon2tegal@gmail.com.',['kontak','sd', 'negeri', 'tunon', '2'], single_response=True)
    response('sd negeri tunon 2 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. ',['fasilitas' ,'sd', 'negeri', 'tunon', '2'], single_response=True)
    response('pembelajaran di sd negeri tunon 2 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'tunon', '2'], single_response=True)
    response('sd negeri tunon 2 memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'tunon', '2'], single_response=True)

    #sd negeri tunon 1
    response('sd negeri tunon 1 tegal beralamat di jalan sutan syahrir no. 1 tegal, tunon, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52135.',[ 'alamat','sd', 'negeri', 'tunon', '1'], single_response=True)
    response('email : tunonsatu@gmail.com.',['kontak','sd', 'negeri', 'tunon', '1'], single_response=True)
    response('sd negeri tunon 1 tegal menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'tunon', '1'], single_response=True)
    response('pembelajaran di sd negeri tunon 1 tegal dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'tunon', '1'], single_response=True)
    response('sd negeri tunon 1 tegal memiliki akreditasi a, berdasarkan sertifikat 044/bansm-jtg/sk/x/2018.',['akreditasi','sd', 'negeri', 'tunon', '1'], single_response=True)

    #sd negeri randugunting 7
    response('sd negeri randugunting 7 beralamat di jl. ketilang no. 59, randugunting, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52131.',[ 'alamat','sd', 'negeri', 'randugunting','7'], single_response=True)
    response('nomor fax sekolah : 0283359243.',[ 'kontak','sd', 'negeri', 'randugunting','7'], single_response=True)
    response('sd negeri randugunting 7 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'randugunting','7'], single_response=True)
    response('pembelajaran di sd negeri randugunting 7 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'randugunting','7'], single_response=True)
    response('sd negeri randugunting 7 memiliki akreditasi a, berdasarkan sertifikat 1012/ban-sm/sk/2019.',['akreditasi','sd', 'negeri', 'randugunting','7'], single_response=True)

    #sd negeri randugunting 6
    response('sd negeri randugunting 6 beralamat di jl. merpati gg. kenari no. 13, randugunting, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52131.',[ 'alamat','sd', 'negeri', 'randugunting','6'], single_response=True)
    response('email : sdn.randugunting6@gmail.com.',['kontak','sd', 'negeri', 'randugunting','6'], single_response=True)
    response('sd negeri randugunting 6 menyediakan listrik untuk membantu kegiatan belajar mengajar.',['fasilitas' ,'sd', 'negeri', 'randugunting','6'], single_response=True)
    response('pembelajaran di sd negeri randugunting 6 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'randugunting','6'], single_response=True)
    response('sd negeri randugunting 6 memiliki akreditasi a, berdasarkan sertifikat 1012/ban-sm/sk/2019.',['akreditasi','sd', 'negeri', 'randugunting','6'], single_response=True)

    #sd negeri randugunting 5
    response('sd negeri randugunting 5 beralamat di jl. arum no. 45, randugunting, kec. tegal selatan, kota tegal, jawa tengah, dengan kode pos 52131.',[ 'alamat','sd', 'negeri', 'randugunting','5'], single_response=True)
    response('email : sdnrandugunting05@gmail.com.',['kontak','sd', 'negeri', 'randugunting','5'], single_response=True)
    response('sd negeri randugunting 5 menyediakan listrik untuk membantu kegiatan belajar mengajar dan juga menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah.',['fasilitas' ,'sd', 'negeri', 'randugunting','5'], single_response=True)
    response('pembelajaran di sd negeri randugunting 5 dilakukan pada pagi. dalam seminggu, pembelajaran dilakukan selama 6 hari.',[ 'waktu', 'pembelajaran','sd', 'negeri', 'randugunting','5'], single_response=True)
    response('sd negeri randugunting 5 memiliki akreditasi a, berdasarkan sertifikat 165/bap-sm/xi/2017.',['akreditasi','sd', 'negeri', 'randugunting','5'], single_response=True)
  
    #SMP KOTA TEGAL-------------------------------------------------------------------------------------------------------
    #SMP
    response('Jumlah SMP yang ada di Kota Tegal ada 34 sekolah.', ['jumlah','smp','smp n','tegal'], single_response=True)
    response('1.SMP NEGERI 1 2.TEGAL SMP NEGERI 2 TEGAL 3.SMP NEGERI 3 TEGAL 4.SMP NEGERI 4 TEGAL 5.SMP NEGERI 5 TEGAL 6.SMP NEGERI 6 TEGAL 7.SMP NEGERI 7 TEGAL 8.SMP NEGERI 8 TEGAL 9.SMP NEGERI 9 TEGAL 10.SMP NEGERI 10 TEGAL 11.SMP NEGERI 11 TEGAL 12.SMP NEGERI 12  TEGAL 13.SMP NEGERI 14 TEGAL 15.SMP NEGERI 15 TEGAL 16.SMP NEGERI 17 TEGAL 17.SMP NEGERI 18 TEGAL 19.SMP MAARIF NU 20.SMP IHSANIYAH 21.SMP ISLAM TERPADU USAMAH 22.SMP MUHAMMADIYAH 1 KOTA TEGAL 23.SMP MUHAMMADIYAH 2 KOTA TEGAL 24.SMP MUHAMMADIYAH 3 KOTA TEGAL 25.SMP AL KHAIRIYYAH 26.SMP AL IRSYAD 27.SMP ATMAJA WACANA 28.SMP GLOBAL INBYRA 29.SMP PELITA HARAPAN BANGSA 30.SMP PIUS 31.SMP TUNAS HIDUP HARAPAN KITA 32.SMP BHAKTI PRAJA 33.SMP IC BIAS ASSALAM  34.SMP PURNAMA', ['daftar','sekolah','nama','smp','tegal'], single_response=True)
    
    #SMP N 1
    response('SMP NEGERI 1 adalah salah satu satuan pendidikan dengan jenjang SMP di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 1 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','1','tegal'], single_response=True)
    response('Jl. Tentara Pelajar No. 32 Kota Tegal, Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat','smp','smpn','smp n','1','tegal','negri','negeri'], single_response=True)
    response('URL website : http://www.smp1-tegal.sch.id. Email : smp1tegal@yahoo.com. Nomor Fax sekolah : 0283351578.', ['kontak','smp n','smpn','1','tegal','negri','negeri'], single_response=True)
    response('SMP NEGERI 1 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 1 berasal dari PLN.', ['fasilitas','smp','smp n','1','smpn','negri','negeri','tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 1 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','1','tegal','smpn','negri','negeri'], single_response=True)
    response('SMP NEGERI 1 memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi','akreditas','smp n','smp','1','negri','negeri'], single_response=True)
	
    #SMP N 2
    response('SMP NEGERI 2 adalah salah satu satuan pendidikan dengan jenjang SMP di KEJAMBON, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 2 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','2','tegal'], single_response=True)
    response('Jl. Menteri Supeno No 3 Tegal, KEJAMBON, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52124.', ['alamat','negri','negeri','smp','smp n','2','tegal','smpn'], single_response=True)
    response('URL website : http://www.smpn2tegal.sch.id. Email : smpn2tegal@yahoo.com. Nomor Fax sekolah : 0283324963.', ['kontak','smp n','2','smp','smpn','negri','negeri','tegal'], single_response=True)
    response('SMP NEGERI 2 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 2 berasal dari PLN. SMP NEGERI 2 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 2 untuk sambungan internetnya adalah Biznet (Serat Optik).', ['fasilitas','smp','smp n','smpn','negri','negeri','tegal','2'], single_response=True)
    response('Pembelajaran di SMP NEGERI 2 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','tegal','negri','negeri','2'], single_response=True)
    response('SMP NEGERI 2 memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'akreditas', 'smp','smp n','smpn','negri','negeri','tegal','2'], single_response=True)
	
    #SMP N 3
    response('SMP NEGERI 3 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 3 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan. ', ['smp','n','3','tegal'], single_response=True)
    response('Jl. Yos Sudarso, Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52111.', ['alamat','smp','smp n','smpn','smp','3','tegal'], single_response=True)
    response('URL website : http://www.smpn3tegal.sch.id. Email : smp3tegal_yess@yahoo.com. Nomor Fax sekolah : 0283351368.', ['kontak','smp','smp n','smpn','3','tegal'], single_response=True)
    response('SMP NEGERI 3 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 3 TEGAL berasal dari PLN. SMP NEGERI 3 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 3 TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp','n', '3', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 3 TEGAL dilakukan pada Sehari Penuh. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','3','tegal'], single_response=True)
    response('SMP NEGERI 3 TEGAL memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi','akreditas','smp n','smp','smpn','3','tegal'], single_response=True)
	
    #SMP N 4
    response('SMP NEGERI 4 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 4 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','4','tegal'], single_response=True)
    response('Jl Setia Budi No. 163A Tegal, Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat','smp','smp n','smpn','4','tegal'], single_response=True)
    response('URL website : http://www.smpn4tegal.sch.id. Email : smpn4tegal@gmail.com. Nomor Fax sekolah : 0283351603.', ['kontak','4','tegal','smp','smp n','smp'], single_response=True)
    response('SMP NEGERI 4 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 4 TEGAL berasal dari PLN.', ['fasilitas','smp','smp n','smpn','tegal','4'], single_response=True)
    response('Pembelajaran di SMP NEGERI 4 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smpn','smp n','4','tegal'], single_response=True)
    response('SMP NEGERI 4 TEGAL memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi','akreditas','smp n','smp','smpn','4','tegal'], single_response=True)

    #SMP N 5
    response('SMP NEGERI 5 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Debong Kulon, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 5 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','5','tegal'], single_response=True)
    response('Jl. Gatot Subroto Tegal Selatan, Debong Kulon, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52133.', ['alamat','smp','smp n','smpn','5','tegal','negri','negeri'], single_response=True)
    response('URL website : http://smpn5kotategal.sch.id. Email : smp5tegal@gmail.com. Nomor Fax sekolah : - .', ['kontak','smp n','smpn','negeri','negri','5','tegal'], single_response=True)
    response('SMP NEGERI 5 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 5 TEGAL berasal dari PLN.', ['fasilitas','smp','smp n','smpn','5','negri','negeri','tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 5 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','5','tegal','negeri','negri'], single_response=True)
    response('SMP NEGERI 5 TEGAL memiliki akreditasi B, berdasarkan sertifikat 147/BAP-SM/X/2015.', ['akreditasi','akreditas','smp n','smp','5','smp n','smpn','tegal','negri','negeri'], single_response=True)
    
    #SMP N 6
    response('SMP NEGERI 6 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 6 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','6','tegal'], single_response=True)
    response('Jl. Cinde Kencana No. 1, Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52111.', ['alamat','smp','smp n','smpn','6','negri','negeri','tegal'], single_response=True)
    response('URL website : http://www.smpn6tegal.sch.id. Email : uptdsmpn6kotategal@gmail.com. Nomor Fax sekolah : - .', ['kontak','smp n','smpn', 'smp','6','tegal','negri','negeri'], single_response=True)
    response('SMP NEGERI 6 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 6 TEGAL berasal dari PLN. SMP NEGERI 6 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 6 TEGAL untuk sambungan internetnya adalah Telkomsel Flash. ', ['fasilitas','smp','smp n','smpn','6','tegal','negeri','negri'], single_response=True)
    response('Pembelajaran di SMP NEGERI 6 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','6','tegal','negri','negeri'], single_response=True)
    response('SMP NEGERI 6 TEGAL memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi','akreditas','smp n','smp','smpn','6', 'tegal'], single_response=True)
	
    #SMP N 7
    response('SMP NEGERI 7 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 7 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','7','tegal'], single_response=True)
    response('SMP NEGERI 7 TEGAL beralamat di Jl. Kapt. Sudibyo No.117, Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52131.', ['alamat','smp','smpn','smp n','tegal','7','negri','negeri'], single_response=True)
    response('URL website : http://www.smpn7tegal.sch.id. Email : smpntujuhtegal@yahoo.com. Nomor Fax sekolah : 028335659.', ['kontak', 'informasi','smp','smpn','smp n','7','negeri','negri','tegal'], single_response=True)
    response('SMP NEGERI 7 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 7 TEGAL berasal dari PLN. SMP NEGERI 7 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 7 TEGAL untuk sambungan internetnya adalah Biznet (Kabel).', ['fasilitas','smp','smp n','smpn','7','tegal','negeri','negri'], single_response=True)
    response('Pembelajaran di SMP NEGERI 7 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','7','tegal','negeri','negri'], single_response=True)
    response('SMP NEGERI 7 TEGAL memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi','akreditas','smp','smp n','smpn','7','tegal','negeri','negri'], single_response=True)
	

    #SMP N 8
    response('SMP NEGERI 8 adalah salah satu satuan pendidikan dengan jenjang SMP di TEGAL SARI, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 8 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','8','tegal'], single_response=True)
    response('Jl. Proklamasi No 14, TEGAL SARI, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52111.', ['alamat','smp','smp n','smpn','8','negri','negeri','tegal'], single_response=True)
    response('URL website : http://smpn8tegal.sch.id. Email : smpn8kotategal@gmail.com. Nomor Fax sekolah : 0283351246.', ['kontak','informasi','smp','8','smpn','smp n','negeri','negri','tegal'], single_response=True)
    response('SMP NEGERI 8 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 8 berasal dari PLN. SMP NEGERI 8 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 8 untuk sambungan internetnya adalah Telkomsel Flash.', ['fasilitas','smp','smp n','smpn','8','tegal','negeri','negri'], single_response=True)
    response('Pembelajaran di SMP NEGERI 6 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran','smp','smp n','smpn','8','tegal','negeri','negri'], single_response=True)
    response('SMP NEGERI 8 memiliki akreditasi B, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi','akreditas','smp','smp n','smpn','8','tegal','negri','negeri'], single_response=True)
	
    #SMP N 9
    response('SMP NEGERI 9 adalah salah satu satuan pendidikan dengan jenjang SMP di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 9 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','9','tegal'], single_response=True)
    response('Jl. Martoloyo No. 62 Tegal, Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat','9', 'smp negeri 9', 'smpn 9', 'smp 9', '9'], single_response=True)
    response('URL website : http://www.smp9tegal.sch.id. Email : smpn9tegal@gmail.com. Nomor Fax sekolah : 0283356681.', ['kontak','informasi','smp','contact','smpn','smp n','9','negeri','negri', 'tegal'], single_response=True)
    response('SMP NEGERI 9 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 9 berasal dari PLN. SMP NEGERI 9 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 9 untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'smp n', '9', 'smpn','tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 9 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'smp n', 'smpn', '9','tegal', 'negeri', 'negri'], single_response=True)
    response('SMP NEGERI 9 memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'akreditas', 'smp','smp n','smp n', '9', 'tegal'], single_response=True)
	
    #SMP N 10
    response('SMP NEGERI 10 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di MANGKUKUSUMAN, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 10 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','10','tegal'], single_response=True)
    response('Jln. Kartini, MANGKUKUSUMAN, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52123.', ['alamat', '10', 'smp', 'smpn', 'smp n', 'tegal'], single_response=True)
    response('URL website : - . Email : smp10tegal@yahoo.co.id. Nomor Fax sekolah : 0283351355.', ['kontak', 'smp', '10', 'tegal', 'informasi'], single_response=True)
    response('SMP NEGERI 10 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 10 TEGAL berasal dari PLN.', ['fasilitas smpn 10 tegal', 'fasilitas smp 10', 'fasilitas smp n 10', 'fasilitas', 'fasilitas smp 10','fasilitas smpn 10', 'fasilitas smp negeri 10', 'fasilitas smp 10', 'fasilitas yang disediakan'], single_response=True)
    response('Pembelajaran di SMP NEGERI 10 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', '10', 'tegal'], single_response=True)
    response('SMP NEGERI 10 TEGAL memiliki akreditasi A, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi', 'smp', '10', 'tegal', 'akreditas','n'], single_response=True)
	
    #SMP N 11
    response('SMP NEGERI 11 adalah salah satu satuan pendidikan dengan jenjang SMP di PANGGUNG, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 11 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','11','tegal'], single_response=True)
    response('Jl. Mejabung No. 18, PANGGUNG, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat', 'smp', '11', 'tegal', 'n'], single_response=True)
    response('URL website : - . Email : smpn11tegal@gmail.com. Nomor Fax sekolah : - .', ['kontak', 'smp','n', '11', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 11 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 11 berasal dari PLN.', ['fasilitas', 'smp','n', '11', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 11 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '11', 'tegal'], single_response=True)
    response('SMP NEGERI 11 memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', '11', 'tegal', 'akreditas'], single_response=True)
	
    #SMP N 12
    response('SMP NEGERI 12 adalah salah satu satuan pendidikan dengan jenjang SMP di MINTARAGEN, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 12 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','12','tegal'], single_response=True)
    response('Jl. Halmahera No.57, MINTARAGEN, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52121.', ['alamat', 'smp','n', '12', 'tegal'], single_response=True)
    response('URL website : https://smpn12tegal.blogspot.com . Email : smpn12tegal@yahoo.co.id. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '12', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 12 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 12 berasal dari PLN. SMP NEGERI 12 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 12 untuk sambungan internetnya adalah Lainnya (Serat Optik).', ['fasilitas', 'smp','n', '12', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 12 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '12', 'tegal'], single_response=True)
    response('SMP NEGERI 12 memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', '12', 'tegal', 'akreditas'], single_response=True)
	
    #SMP N 13
    response('SMP NEGERI 13 adalah salah satu satuan pendidikan dengan jenjang SMP di KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 13 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','13','tegal'], single_response=True)
    response('Jl. Rambutan No. 27, KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp','n', '13', 'tegal'], single_response=True)
    response('URL website : http://www.smpn13tegal.sch.id. Email :  smpn13tegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '13', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 13 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 13 berasal dari PLN.', ['fasilitas', 'smp','n', '13', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 13 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '13', 'tegal'], single_response=True)
    response('SMP NEGERI 13 memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', '13', 'tegal', 'akreditas'], single_response=True)
	
    #SMP N 14
    response('SMP NEGERI 14 adalah salah satu satuan pendidikan dengan jenjang SMP di Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 14 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','14','tegal'], single_response=True)
    response('Jl.Wisanggeni No. 5 Tegal, Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52124.', ['alamat', 'smp','n', '14', 'tegal'], single_response=True)
    response('URL website : http://smpn14tegal.mysch.id . Email : smpn14tegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '14', 'tegal','informasi','contact'], single_response=True)
    response('SMP NEGERI 14 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 14 berasal dari PLN.', ['fasilitas', 'smp','n', '14', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 14 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '14', 'tegal'], single_response=True)
    response('SMP NEGERI 14 memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017', ['akreditasi', 'smp', '14', 'tegal', 'akreditas'], single_response=True)

    #SMP N 15
    response('SMP NEGERI 15 adalah salah satu satuan pendidikan dengan jenjang SMP di SLEROK, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 15 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','15','tegal'], single_response=True)
    response('Jl. Sumbodro No. 60 Tegal, SLEROK, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52125.', ['alamat', 'smp','n', '15', 'tegal'], single_response=True)
    response('URL website : http://smpn15kotategal.sch.id. Email : smpn15tegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '15', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 15 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 15 berasal dari PLN. SMP NEGERI 15 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 15 untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp','n', '15', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 15 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran smpn 15 tegal', 'pembelajaran smp 15', 'pembelajaran smp n 15', 'pembelajaran', 'pembelajaran smp 15','pembelajaran smpn 15', 'pembelajaran smp negeri 15', 'pembelajaran smp 15', 'jam pembelajaran smp 15'], single_response=True)
    response('SMP NEGERI 15 memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', '15', 'tegal', 'akreditas', 'n'], single_response=True)
    
    #SMP N 17
    response('SMP NEGERI 17 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 17 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan. ', ['smp','n','17','tegal'], single_response=True)
    response('Jl. Sibandaran No.13 Tegal, Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52141.', ['alamat', 'smp','n', '17', 'tegal'], single_response=True)
    response('URL website : http://www.smp17tegal.sch.id. Email : smpjitutegal@yahoo.co.id. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '17', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 17 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 17 TEGAL berasal dari PLN. SMP NEGERI 17 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 17 TEGAL untuk sambungan internetnya adalah Lainnya.', ['fasilitas', 'smp','n', '17', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 17 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '17', 'tegal'], single_response=True)
    response('SMP NEGERI 17 TEGAL memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', '17', 'tegal', 'akreditas','n'], single_response=True)
    
    #SMP N 18
    response('SMP NEGERI 18 adalah salah satu satuan pendidikan dengan jenjang SMP di MARGADANA, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP NEGERI 18 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp','n','18','tegal'], single_response=True)
    response('Jl. Kh. Abdul Syukur No.45 A, MARGADANA, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52143.', ['alamat', 'smp','n', '18', 'tegal'], single_response=True)
    response('URL website : http://www.smpn18tegal.sch.id. Email : smpn18_tegal@yahoo.co.id. Nomor Fax sekolah : - ', ['kontak', 'smp','n', '18', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP NEGERI 18 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP NEGERI 18 berasal dari PLN. SMP NEGERI 18 menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP NEGERI 18 untuk sambungan internetnya adalah XL (GSM).', ['fasilitas', 'smp','n', '18', 'tegal'], single_response=True)
    response('Pembelajaran di SMP NEGERI 18 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp','n', '18', 'tegal'], single_response=True)
    response('SMP NEGERI 18 memiliki akreditasi B, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', '18', 'tegal', 'akreditas','n'], single_response=True)
    
    #SMP MAARIF NU
    response('SMP MAARIF NU adalah salah satu satuan pendidikan dengan jenjang SMP di KETUREN, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP MAARIF NU berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'nu', 'tegal', 'maarif'], single_response=True)
    response('Beralamat di Keturen, KETUREN, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52134.', ['alamat', 'smp', 'maarif', 'nu', 'tegal'], single_response=True)
    response('URL website : - . Email : solichinsadewa64@gmail.com. Nomor Fax sekolah : 0283322973. ', ['kontak', 'smp', 'maarif', 'nu', 'tegal','contact'], single_response=True)
    response('SMP MAARIF NU menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP MAARIF NU berasal dari PLN. SMP MAARIF NU menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP MAARIF NU untuk sambungan internetnya adalah Telkomsel Flash.', ['fasilitas', 'smp', 'maarif', 'nu', 'tegal'], single_response=True)
    response('Pembelajaran di SMP MAARIF NU dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'maarif', 'nu', 'tegal'], single_response=True)
    response('SMP MAARIF NU memiliki akreditasi B, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', 'maarif', 'nu', 'tegal', 'akreditas'], single_response=True)
    
    #SMP IHSANIYAH
    response('SMP IHSANIYAH adalah salah satu satuan pendidikan dengan jenjang SMP di SLEROK, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP IHSANIYAH berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'ihsaniyah', 'tegal'], single_response=True)
    response('SMP IHSANIYAH beralamat di Jl. Sumbodro No.14 Tegal, SLEROK, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52125.', ['alamat', 'smp', 'ihsaniyah', 'tegal'], single_response=True)
    response('URL website : http://www.smpihsaniyahtegal.hol.es. Email : smpihsaniyahtegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'ihsaniyah', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP IHSANIYAH menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP IHSANIYAH berasal dari PLN. SMP IHSANIYAH menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP IHSANIYAH untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'ihsaniyah', 'tegal'], single_response=True)
    response('Pembelajaran di SMP IHSANIYAH dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'ihsaniyah', 'tegal'], single_response=True)
    response('SMP IHSANIYAH memiliki akreditasi A, berdasarkan sertifikat 137/BAP-SM/X/2014.', ['akreditasi', 'smp', 'ihsaniyah', 'tegal','akreditas'], single_response=True)
    
    #SMP ISLAM TERPADU USAMAH
    response('SMP ISLAM TERPADU USAMAH adalah salah satu satuan pendidikan dengan jenjang SMP di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP ISLAM TERPADU USAMAH berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'islam', 'terpadu', 'usamah', 'it', 'tegal'], single_response=True)
    response('SMP ISLAM TERPADU USAMAH beralamat di JL. INDUSTRI RT.01/14, Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat', 'smp', 'islam', 'terpadu', 'usamah', 'tegal','it'], single_response=True)
    response('URL website : http://www.yru.or.id. Email : smpitusamah@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'islam', 'terpadu', 'usamah', 'tegal', 'informasi','contact','it'], single_response=True)
    response('SMP ISLAM TERPADU USAMAH menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP ISLAM TERPADU USAMAH berasal dari PLN. SMP ISLAM TERPADU USAMAH menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP ISLAM TERPADU USAMAH untuk sambungan internetnya adalah Lainnya (Kabel).', ['fasilitas', 'smp', 'islam', 'terpadu', 'usamah', 'tegal','it'], single_response=True)
    response('Pembelajaran di SMP ISLAM TERPADU USAMAH dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'islam', 'terpadu', 'usamah', 'tegal'], single_response=True)
    response('SMP ISLAM TERPADU USAMAH memiliki akreditasi C, berdasarkan sertifikat 044/BANSM-JTG/SK/X/2018.', ['akreditasi', 'smp', 'islam', 'terpadu', 'usamah', 'tegal','akreditas'], single_response=True)
    
    #SMP MUHAMMADIYAH 1 KOTA TEGAL
    response('SMP MUHAMMADIYAH 1 KOTA TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP MUHAMMADIYAH 1 KOTA TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'muhammadiyah', '1', 'kota', 'tegal'], single_response=True)
    response('Jl. Perintis Kemerdekaan No. 95, Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52125.', ['alamat', 'smp', 'muhammadiyah', '1', 'tegal'], single_response=True)
    response('URL website : http://smpmuhitegal.sch.id. Email : smp_muh1.tegal@yahoo.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'muhammadiyah', '1', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP MUHAMMADIYAH 1 KOTA TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP MUHAMMADIYAH 1 KOTA TEGAL berasal dari PLN. SMP MUHAMMADIYAH 1 KOTA TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP MUHAMMADIYAH 1 KOTA TEGAL untuk sambungan internetnya adalah Telkomsel Flash.', ['fasilitas', 'smp', 'muhammadiyah', '1', 'tegal'], single_response=True)
    response('Pembelajaran di SMP MUHAMMADIYAH 1 KOTA TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'muhammadiyah', '1', 'tegal'], single_response=True)
    response('SMP MUHAMMADIYAH 1 KOTA TEGAL memiliki akreditasi A, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi', 'smp', 'muhammadiyah', '1', 'tegal','akreditas'], single_response=True)
    
    #SMP MUHAMMADIYAH 2 KOTA TEGAL
    response('SMP MUHAMMADIYAH 2 adalah salah satu satuan pendidikan dengan jenjang SMP di MARGADANA, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP MUHAMMADIYAH 2 berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'muhammadiyah', '2', 'kota', 'tegal'], single_response=True)
    response('Jl. Demak 1 No 14, MARGADANA, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52143.', ['alamat', 'smp', 'muhammadiyah', '2', 'tegal'], single_response=True)
    response('URL website : http://www.smpmudamargadana@sch.id. Email : smp.muda@yahoo.com.', ['kontak', 'smp', 'muhammadiyah', '2', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP MUHAMMADIYAH 2 menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP MUHAMMADIYAH 2 berasal dari PLN.', ['fasilitas', 'smp', 'muhammadiyah', '2', 'tegal'], single_response=True)
    response('Pembelajaran di SMP MUHAMMADIYAH 2 dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'muhammadiyah', '2', 'tegal'], single_response=True)
    response('SMP MUHAMMADIYAH 2 memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', 'muhammadiyah', '2', 'tegal','akreditas'], single_response=True)
    
    #SMP MUHAMMADIYAH 3 KOTA TEGAL
    response('SMP MUHAMMADIYAH 3 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMP di Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP MUHAMMADIYAH 3 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'muhammadiyah', '3', 'kota', 'tegal'], single_response=True)
    response('Jl. Asemtiga Gg. V No. 27 B, Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp', 'muhammadiyah', '3', 'tegal'], single_response=True)
    response('URL website : http://muga.com. Email : smpmuh3tegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'muhammadiyah', '3', 'tegal', 'informasi', 'contact'], single_response=True)
    response('SMP MUHAMMADIYAH 3 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP MUHAMMADIYAH 3 TEGAL berasal dari PLN. SMP MUHAMMADIYAH 3 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP MUHAMMADIYAH 3 TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'muhammadiyah', '3', 'tegal'], single_response=True)
    response('Pembelajaran di SMP MUHAMMADIYAH 3 TEGAL dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'muhammadiyah', '3', 'tegal'], single_response=True)
    response('SMP MUHAMMADIYAH 3 TEGAL memiliki akreditasi B, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', 'muhammadiyah', '3', 'tegal','akreditas'], single_response=True)
    

    #SMP AL KHAIRIYYAH
    response('SMP AL KHAIRIYYAH adalah salah satu satuan pendidikan dengan jenjang SMP di KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP AL KHAIRIYYAH berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'al', 'khairiyyah', 'tegal'], single_response=True)
    response('Jl. Durian No. 48, KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp', 'al', 'khairiyyah', 'tegal'], single_response=True)
    response('URL website : - . Email : smp_alkhairiyyah@yahoo.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'al', 'khairiyyah', 'tegal'], single_response=True)
    response('SMP AL KHAIRIYYAH menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP AL KHAIRIYYAH berasal dari PLN.', ['fasilitas smp al khairiyyah tegal', 'fasilitas smp al khairiyyah', 'fasilitas al khairiyyah'], single_response=True)
    response('Pembelajaran di SMP AL KHAIRIYYAH dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'al', 'khairiyyah', 'tegal'], single_response=True)
    response('SMP AL KHAIRIYYAH memiliki akreditasi B, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', 'al', 'khairiyyah', 'tegal','akreditas'], single_response=True)
    
    #SMP AL IRSYAD
    response('SMP ALIRSYAD adalah salah satu satuan pendidikan dengan jenjang SMP di Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP ALIRSYAD berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'al', 'irsyad', 'tegal'], single_response=True)
    response('Jl. May.Jend. Sutoyo No.7 Tegal, Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52113.', ['alamat', 'smp', 'al', 'irsyad', 'tegal'], single_response=True)
    response('URL website : http://www.smp-alirsyadtegal.com. Email : smp_alirsyadtegal@yahoo.co.id. Nomor Fax sekolah : 0283350618.', ['kontak', 'smp', 'al', 'irsyad', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP ALIRSYAD menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP ALIRSYAD berasal dari PLN. SMP ALIRSYAD menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP ALIRSYAD untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'al', 'irsyad', 'tegal'], single_response=True)
    response('Pembelajaran di SMP ALIRSYAD dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'al', 'irsyad', 'tegal'], single_response=True)
    response('SMP ALIRSYAD memiliki akreditasi A, berdasarkan sertifikat 147/BAP-SM/X/2015.', ['akreditasi', 'smp', 'al', 'irsyad', 'tegal','akreditas'], single_response=True)
    
    #SMP ATMAJA WACANA
    response('SMP ATMAJA WACANA adalah salah satu satuan pendidikan dengan jenjang SMP di Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP ATMAJA WACANA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'atmaja', 'wacana','tegal'], single_response=True)
    response('Jl. Kapten Ismail 92- 94, Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp', 'atmaja', 'wacana', 'tegal'], single_response=True)
    response('URL website : http://https//www.facebook.com/atmajawacanategal. Email : atmaja.wacana@yahoo.com. Nomor Fax sekolah : 0283321501.', ['kontak', 'smp', 'atmaja', 'wacana', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP ATMAJA WACANA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP ATMAJA WACANA berasal dari PLN. SMP ATMAJA WACANA menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP ATMAJA WACANA untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'atmaja', 'wacana', 'tegal'], single_response=True)
    response('Pembelajaran di SMP ATMAJA WACANA dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'atmaja', 'wacana', 'tegal'], single_response=True)
    response('SMP ATMAJA WACANA memiliki akreditasi B, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', 'atmaja', 'wacana', 'tegal','akreditas'], single_response=True)
    
    #SMP GLOBAL INBYRA
    response('SMP GLOBAL INBYRA adalah salah satu satuan pendidikan dengan jenjang SMP di Kemandungan, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP GLOBAL INBYRA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'global', 'inbyra', 'tegal'], single_response=True)
    response('SMP GLOBAL INBYRA beralamat di JL. KOMPOL SUPRAPTO NO. 8, Kemandungan, Kec. Tegal Barat, Kota Tegal, Jawa Tengah.', ['alamat', 'smp', 'global', 'inbyra', 'tegal'], single_response=True)
    response('URL website : - . Email : - . Nomor Fax sekolah : - ', ['kontak', 'smp', 'global', 'inbyra', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP GLOBAL INBYRA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP GLOBAL INBYRA berasal dari PLN. SMP GLOBAL INBYRA menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP GLOBAL INBYRA untuk sambungan internetnya adalah Biznet (Kabel).', ['fasilitas', 'smp', 'global', 'inbyra', 'tegal'], single_response=True)
    response('Pembelajaran di SMP GLOBAL INBYRA dilakukan pada Sehari Penuh. Dalam seminggu, pembelajaran dilakukan selama 5 hari.', ['pembelajaran', 'smp', 'global', 'inbyra', 'tegal'], single_response=True)
    response('-', ['akreditasi', 'smp', 'global', 'inbyra', 'tegal','akreditas'], single_response=True)
    
    #SMP PELITA HARAPAN BANGSA 
    response('SMP PELITA HARAPAN BANGSA adalah salah satu satuan pendidikan dengan jenjang SMP di Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP PELITA HARAPAN BANGSA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'pelita', 'harapan', 'bangsa', 'tegal'], single_response=True)
    response('JL. SIPELEM NO. 24, Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp', 'pelita', 'harapan', 'bangsa', 'tegal'], single_response=True)
    response('URL website : http://www.smppelitaharapanbangsa.com. Email : pelitaharapabangsa@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'pelita', 'harapan', 'bangsa', 'tegal', 'informasi', 'contact'], single_response=True)
    response('SMP PELITA HARAPAN BANGSA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP PELITA HARAPAN BANGSA berasal dari PLN. SMP PELITA HARAPAN BANGSA menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP PELITA HARAPAN BANGSA untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas', 'smp', 'pelita', 'harapan', 'bangsa', 'tegal'], single_response=True)
    response('Pembelajaran di SMP PELITA HARAPAN BANGSA dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'pelita', 'harapan', 'bangsa', 'tegal'], single_response=True)
    response('SMP PELITA HARAPAN BANGSA memiliki akreditasi B, berdasarkan sertifikat 044/BANSM-JTG/SK/X/2018.', ['akreditasi', 'smp', 'pelita', 'harapan', 'bangsa', 'tegal','akreditas'], single_response=True)
    
    #SMP PIUS 
    response('SMP PIUS adalah salah satu satuan pendidikan dengan jenjang SMP di KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP PIUS berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'pius', 'tegal'], single_response=True)
    response('Jl. Dr. Sutomo 52 Tegal, KRATON, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat', 'smp', 'pius', 'tegal'], single_response=True)
    response('URL website : - . Email : smp_piustegal@yahoo.co.id. Nomor Fax sekolah : - ', ['kontak', 'smp', 'pius', 'tegal', 'informasi','contact'], single_response=True)
    response('SMP PIUS menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP PIUS berasal dari PLN.', ['fasilitas', 'smp', 'pius', 'tegal'], single_response=True)
    response('Pembelajaran di SMP PIUS dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'pius', 'tegal'], single_response=True)
    response('SMP PIUS memiliki akreditasi A, berdasarkan sertifikat 905/BAN-SM/SK/2019.', ['akreditasi', 'smp', 'pius', 'tegal','akreditas'], single_response=True)
    
    #SMP TUNAS HIDUP HARAPAN KITA  
    response('SMP TUNAS HIDUP HARAPAN KITA adalah salah satu satuan pendidikan dengan jenjang SMP di Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP TUNAS HIDUP HARAPAN KITA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'tunas', 'hidup', 'harapan', 'kita', 'tegal'], single_response=True)
    response('JL. GURAMI 6 KOTA TEGAL, Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52111.', ['alamat', 'smp', 'tunas', 'hidup', 'harapan', 'kita', 'tegal'], single_response=True)
    response('URL website : http://smpthhk.tridharmategal.or.id. Email : smpthhk.tegal@gmail.com. Nomor Fax sekolah : - ', ['kontak', 'smp', 'tunas', 'hidup', 'harapan', 'kita', 'tegal', 'informasi', 'contact'], single_response=True)
    response('SMP TUNAS HIDUP HARAPAN KITA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP TUNAS HIDUP HARAPAN KITA berasal dari PLN.', ['fasilitas', 'smp', 'tunas', 'hidup', 'harapan', 'kita', 'tegal'], single_response=True)
    response('Pembelajaran di SMP TUNAS HIDUP HARAPAN KITA dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'tunas', 'hidup', 'harapan', 'kita', 'tegal'], single_response=True)
    response('SMP TUNAS HIDUP HARAPAN KITA memiliki akreditasi B, berdasarkan sertifikat 817/BAN-SM/SK/2019.', ['akreditasi', 'smp', 'tunas', 'hidup', 'harapan','kita', 'tegal'], single_response=True)
    
    #SMP BHAKTI PRAJA 
    response('SMP BHAKTI PRAJA adalah salah satu satuan pendidikan dengan jenjang SMP di Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP BHAKTI PRAJA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'bhakti', 'praja', 'tegal'], single_response=True)
    response('Jl. Ki Hajar Dewantoro No. 59 Tegal, Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52141.', ['alamat', 'smp', 'bhakti', 'praja', 'tegal'], single_response=True)
    response('URL website : - . Email : smpbhaktipraja59@gmail.com. Nomor Fax sekolah : - ', ['kontak smp bhakti praja tegal', 'informasi smp bhakti praja', 'kontak smp bhakti praja', 'kontak bhakti praja'], single_response=True)
    response('SMP BHAKTI PRAJA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP BHAKTI PRAJA berasal dari PLN.', ['fasilitas smp bhakti praja tegal', 'fasilitas smp bhakti praja', 'fasilitas bhakti praja'], single_response=True)
    response('Pembelajaran di SMP BHAKTI PRAJA dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'bhakti', 'praja', 'tegal'], single_response=True)
    response('SMP BHAKTI PRAJA memiliki akreditasi B, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', 'bhakti', 'praja', 'tegal','akreditas'], single_response=True)
    
    #SMP IC BIAS ASSALAM 
    response('SMP IC BIAS ASSALAM adalah salah satu satuan pendidikan dengan jenjang SMP di Kaligangsa, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP IC BIAS ASSALAM berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'ic', 'bias', 'asssalam', 'tegal'], single_response=True)
    response('JL. KALIGANGSA ASRI TIMUR RT. 01/07 KEL. KALIGANGSA KEC. MARGADANA KOTA TEGAL, Kaligangsa, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52147.', ['alamat', 'smp', 'ic', 'bias', 'asssalam', 'tegal'], single_response=True)
    response('URL website : http://smpicbiasassalam.sch.id. Email : smpinsancendekiabiasassalam@gmail.com. Nomor Fax sekolah : -', ['kontak', 'smp', 'ic', 'bias', 'asssalam', 'tegal'], single_response=True)
    response('SMP IC BIAS ASSALAM menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP IC BIAS ASSALAM berasal dari PLN. SMP IC BIAS ASSALAM menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMP IC BIAS ASSALAM untuk sambungan internetnya adalah 3 (Tri).', ['fasilitas', 'smp', 'atmaja', 'wacana', 'tegal'], single_response=True)
    response('Pembelajaran di SMP IC BIAS ASSALAM dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'ic', 'bias', 'asssalam', 'tegal'], single_response=True)
    response('SMP IC BIAS ASSALAM memiliki akreditasi C, berdasarkan sertifikat 044/BANSM-JTG/SK/X/2018.', ['akreditasi', 'smp', 'ic', 'bias', 'asssalam', 'tegal','akreditas'], single_response=True)
    
    #SMP PURNAMA 
    response('SMP PURNAMA adalah salah satu satuan pendidikan dengan jenjang SMP di Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMP PURNAMA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smp', 'purnama', 'tegal'], single_response=True)
    response('Jl. Gatot Subroto, Sumurpanggang, Kec. Margadana, Kota Tegal, Jawa Tengah, dengan kode pos 52141.', ['alamat', 'smp', 'purnama', 'tegal'], single_response=True)
    response('URL website : -. Email : smpprntegal@gmail.com. Nomor Fax sekolah : -', ['kontak', 'smp', 'purnama', 'tegal', 'informasi', 'contact'], single_response=True)
    response('SMP PURNAMA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMP PURNAMA berasal dari PLN.', ['fasilitas smp purnama tegal', 'fasilitas smp purnama', 'fasilitas purnama'], single_response=True)
    response('Pembelajaran di SMP PURNAMA dilakukan pada Pagi. Dalam seminggu, pembelajaran dilakukan selama 6 hari.', ['pembelajaran', 'smp', 'atmaja', 'wacana', 'tegal'], single_response=True)
    response('SMP PURNAMA memiliki akreditasi C, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi', 'smp', 'purnama', 'tegal','akreditas'], single_response=True)
    
    
    # SMA/SMK KOTA TEGAL-------------------------------------------------------------------------------------------------------
    #SMAN 1 TEGAL
    response('SMAN 1 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAN 1 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','sman','1','tegal'], single_response=True)
    response('jl.menteri supeno no.16', ['alamat','sma','sman','1','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://sman1tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sman1_kotategal@yahoo.ccom. Nomor Fax sekolah adalah 0283323955.', ['kontak','sma','sman','1','tegal'], single_response=True)
    response('SMAN 1 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAN 1 TEGAL untuk sambungan internetnya adalah Biznet (Serat Optik).', ['fasilitas','sma','sman','1','tegal'], single_response=True)
    response('SMAN 1 TEGAL memiliki akreditasi A, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi','sma','sman','1','tegal'], single_response=True)
    
    #SMAN 2 TEGAL
    response('SMAN 2 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Tegalsari, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAN 2 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','sman','2','tegal'], single_response=True)
    response('jl.lumba-lumba no.24', ['alamat','sma','sman','2','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://sman2-tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sman2_kotategal@yahoo.com. Nomor Fax sekolah adalah 356816.', ['kontak','sma','sman','2','tegal'], single_response=True)
    response('Sumber listrik yang digunakan oleh SMAN 2 TEGAL berasal dari PLN. SMAN 2 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAN 2 TEGAL untuk sambungan internetnya adalah Telkom Astinet.', ['fasilitas','sma','sman','2','tegal'], single_response=True)
    response('SMAN 2 TEGAL memiliki akreditasi A, berdasarkan sertifikat 044/BANSM-JTG/SK/X/2018.', ['akreditasi','sma','sman','2','tegal'], single_response=True)

    #SMAN 3 TEGAL
    response('SMAN 3 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAN 3 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','sman','3','tegal'], single_response=True)
    response('jl.sumbodro no.81', ['alamat','sma','sman','3','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.sman3kotategal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sman3kotategal@gmail.com. Nomor Fax sekolah adalah 341747.', ['kontak','hubungi','sma','sman','3','tegal'], single_response=True)
    response('Sumber listrik yang digunakan oleh SMAN 3 TEGAL berasal dari PLN. SMAN 3 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAN 3 TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas','sma','sman','3','tegal'], single_response=True)
    response('SMAN 3 TEGAL memiliki akreditasi A, berdasarkan sertifikat 817/BAN-SM/SK/2019.', ['akreditasi','sma','sman','3','tegal'], single_response=True)
    
    #SMAN 4 TEGAL
    response('SMAN 4 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAN 4 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','sman','4','tegal'], single_response=True)
    response('jl.dr.setiabudi no.32', ['alamat','sma','sman','4','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.sman4tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sma4tegal@gmail.com. Nomor Fax sekolah adalah 0283351766.', ['kontak','sma','sman','4','tegal'], single_response=True)
    response('Sumber listrik yang digunakan oleh SMAN 4 TEGAL berasal dari PLN. SMAN 4 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAN 4 TEGAL untuk sambungan internetnya adalah Biznet (Serat Optik).', ['fasilitas','sma','sman','4','tegal'], single_response=True)
    response('SMAN 4 TEGAL memiliki akreditasi A, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi','sma','sman','4','tegal'], single_response=True)

    #SMAN 5 TEGAL
    response('SMAN 5 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Margadana, Kec. Margadana, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAN 5 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','sman','5','tegal'], single_response=True)
    response('jl.kali kemiri II', ['alamat','sma','sman','5','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.sma-alirsyadtegal.com. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sma.alirsyadtegal@gmail.com. Nomor Fax sekolah adalah 0283356869.', ['kontak','sma','sman','5','tegal'], single_response=True)
    response('SMAN 5 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAN 5 TEGAL berasal dari PLN & Diesel. SMAN 5 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAN 5 TEGAL untuk sambungan internetnya adalah Lainnya (Serat Optik).', ['fasilitas','sma','sman','5','tegal'], single_response=True)
    response('SMAN 5 TEGAL memiliki akreditasi A, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi','sma','sman','5','tegal'], single_response=True)

    #SMAS AL IRSYAD
    response('SMAS AL IRSYAD TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAS AL IRSYAD TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','smas','5','tegal'], single_response=True)
    response('jl.gajah mada no. 128', ['alamat','sma','smas','al irsyad','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.sman5kotategal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke sman5_tegal@yahoo.co.id.', ['kontak','sma','smas','al irsyad','tegal'], single_response=True)
    response('SMAS AL IRSYAD TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAS AL IRSYAD TEGAL berasal dari PLN. SMAS AL IRSYAD TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAS AL IRSYAD TEGAL untuk sambungan internetnya adalah Lainnya (Serat Optik).', ['fasilitas','sma','smas','al irsyad','tegal'], single_response=True)
    response('SMAS AL IRSYAD TEGAL memiliki akreditasi A, berdasarkan sertifikat 165/BAP-SM/XI/2017.', ['akreditasi','sma','smas','al irsyad','tegal'], single_response=True)

    #SMAS IHSANIYAH
    response('SMAS IHSANIYAH TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAS IHSANIYAH TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','smas','ihsaniyah','tegal'], single_response=True)
    response('jl.jalak barat no. 16', ['alamat','sma','smas','ihsaniyah','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smaihsaniyahtegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke mail@smaihsaniyahtegal.sch.id.', ['kontak','sma','smas','ihsaniyah','tegal'], single_response=True)
    response('SMAS IHSANIYAH TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAS IHSANIYAH TEGAL berasal dari PLN. SMAS IHSANIYAH TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAS IHSANIYAH TEGAL untuk sambungan internetnya adalah Indosat IM3.', ['fasilitas','sma','smas','ihsaniyah','tegal'], single_response=True)
    response('SMAS IHSANIYAH TEGAL memiliki akreditasi A, berdasarkan sertifikat 817/BAN-SM/SK/2019', ['akreditasi','sma','smas','ihsaniyah','tegal'], single_response=True)

    #SMAS MUHAMMADIYAH TEGAL
    response('SMAS MUHAMMADIYAH adalah salah satu satuan pendidikan dengan jenjang SMA di Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAS MUHAMMADIYAH berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','smas','muhammadiyah','tegal'], single_response=True)
    response('JL. KARTINI NO. 47, Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52123.', ['alamat','sma','smas','muhammadiyah','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smamuhatategal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smamuhata@gmail.com.', ['kontak','sma','smas','muhammadiyah','tegal'], single_response=True)
    response('SMAS MUHAMMADIYAH menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAS MUHAMMADIYAH berasal dari PLN. SMAS MUHAMMADIYAH menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAS MUHAMMADIYAH untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas','sma','smas','muhammadiyah','tegal'], single_response=True)
    response('SMAS MUHAMMADIYAH memiliki akreditasi B, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi','sma','smas','muhammadiyah','tegal'], single_response=True)

    #SMAS NU TEGAL
    response('SMAS NAHDLATUL ULAMA adalah salah satu satuan pendidikan dengan jenjang SMA di Pesurungan Kidul, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAS NAHDLATUL ULAMA berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','smas','nahdlatul ulama','tegal'], single_response=True)
    response('JL. DR. WAHIDIN SUDIROHUSODO NO. 4, Pesurungan Kidul, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52116.', ['alamat','sma','smas','nahdlatul ulama','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://sma-nukotategal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke lebsmanutik@yahoo.co.id. Nomor Fax sekolah adalah 0283358640.', ['kontak','sma','smas','nahdlatul ulama','tegal'], single_response=True)
    response('SMAS NAHDLATUL ULAMA menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAS NAHDLATUL ULAMA berasal dari PLN. SMAS NAHDLATUL ULAMA menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAS NAHDLATUL ULAMA untuk sambungan internetnya adalah Lainnya (Kabel).', ['fasilitas','sma','smas','nahdlatul ulama','tegal'], single_response=True)
    response('SMAS NAHDLATUL ULAMA memiliki akreditasi B, berdasarkan sertifikat 220/BAP-SM/X/2016.', ['akreditasi','sma','smas','nahdlatul ulama','tegal'], single_response=True)

    #SMAS PIUS TEGAL
    response('SMAS PIUS TEGAL adalah salah satu satuan pendidikan dengan jenjang SMA di Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMAS PIUS TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['sma','smas','pius','tegal'], single_response=True)
    response('JL. KAPTEN ISMAIL NO. 120, Kraton, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52112.', ['alamat','sma','smas','pius','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.astidharma.sch.id/. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smapius_tegal@ymail.com. Nomor Fax sekolah adalah 0283343882.', ['kontak','sma','smas','pius','tegal'], single_response=True)
    response('SMAS PIUS TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMAS PIUS TEGAL berasal dari PLN. SMAS PIUS TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMAS PIUS TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas','sma','smas','pius','tegal'], single_response=True)
    response('SMAS PIUS TEGAL memiliki akreditasi A, berdasarkan sertifikat 817/BAN-SM/SK/2019.', ['akreditasi','sma','smas','pius','tegal'], single_response=True)

    #SMKN 1 TEGAL
    response('SMKN 1 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKN 1 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smkn','1','tegal'], single_response=True)
    response('SMKN 1 TEGAL beralamat di JL. DR.SUTOMO NO.68, Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52113.', ['alamat','smk','smkn','1','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.smkn1tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smkn1kotategal@yahoo.com. Nomor Fax sekolah adalah 0283353302.', ['kontak','smk','smkn','1','tegal'], single_response=True)
    response('SMKN 1 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKN 1 TEGAL berasal dari PLN.', ['fasilitas','smk','smkn','1','tegal'], single_response=True)
    response('SMKN 1 TEGAL memiliki akreditasi B, berdasarkan sertifikat 032/BAN-SM/SK/2019.', ['akreditasi','smk','smkn','1','tegal'], single_response=True)

    #SMKN 2 TEGAL
    response('SMKN 2 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKN 2 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smkn','2','tegal','negeri','negri'], single_response=True)
    response('SMKN 2 TEGAL beralamat di JL. WISANGGENI NO. 1, Kejambon, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52124.', ['alamat','smk','smkn','2','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.smk2tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke email@smk2tegal.sch.id. Nomor Fax sekolah adalah 0283350430.', ['kontak','smk','smkn','2','tegal','negeri','negri'], single_response=True)
    response('SMKN 2 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKN 2 TEGAL berasal dari PLN.', ['fasilitas','smk','smkn','2','tegal','negeri','negri'], single_response=True)
    response('SMKN 2 TEGAL memiliki akreditasi A, berdasarkan sertifikat 032/BAN-SM/SK/2019.', ['akreditasi','smk','smkn','2','tegal','negeri','negri'], single_response=True)

    #SMKN 3 TEGAL
    response('SMKN 3 TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKN 3 TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smkn','3','tegal','negeri','negri'], single_response=True)
    response('SMKN 3 TEGAL beralamat di JL. GAJAHMADA 72 D, Pekauman, Kec. Tegal Barat, Kota Tegal, Jawa Tengah, dengan kode pos 52113.', ['alamat','smk','smkn','3','tegal',], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.smkn3tegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smkn03tegal@yahoo.com. Nomor Fax sekolah adalah 0283357718.', ['kontak','smk','smkn','3','tegal','negeri','negri'], single_response=True)
    response('SMKN 3 TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKN 3 TEGAL berasal dari PLN. SMKN 3 TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMKN 3 TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas','smk','smkn','3','tegal','negeri','negri'], single_response=True)
    response('SMKN 3 TEGAL memiliki akreditasi A, berdasarkan sertifikat 032/BAN-SM/SK/2019.', ['akreditasi','smk','smkn','3','tegal','negeri','negri'], single_response=True)

    #SMKs Al irsyad TEGAL
    response('SMKS AL IRSYAD adalah salah satu satuan pendidikan dengan jenjang SMK di Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS AL IRSYAD berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','al irsyad','tegal'], single_response=True)
    response('SMKS AL IRSYAD beralamat di JALAN GLATIK NO. 3, Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52131.', ['alamat','smk','smks','al irsyad','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smkalirsyadtegal.sch.id/. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smkalirsyadtgl@gmail.com.', ['kontak','smk','smks','al irsyad','tegal'], single_response=True)
    response('SMKS AL IRSYAD menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS AL IRSYAD berasal dari PLN.', ['fasilitas','smk','smks','al irsyad','tegal'], single_response=True)
    response('SMKS AL IRSYAD memiliki akreditasi B, berdasarkan sertifikat 817/BAN-SM/SK/2019.', ['akreditasi','smk','smks','al irsyad','tegal'], single_response=True)

    #SMKS ASSALAFIYAH TEGAL
    response('SMKS ASSALAFIYAH adalah salah satu satuan pendidikan dengan jenjang SMK di Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS ASSALAFIYAH berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','assalafiyah','tegal'], single_response=True)
    response('SMKS ASSALAFIYAH beralamat di JL. AR HAKIM NO. 10, Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52113.', ['alamat','smk','smks','assalafiyah','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smkassalafiyahtegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke amarsy1202@gmail.com.', ['kontak','smk','smks','assalafiyah','tegal'], single_response=True)
    response('SMKS ASSALAFIYAH menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS ASSALAFIYAH berasal dari PLN. SMKS ASSALAFIYAH menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMKS ASSALAFIYAH untuk sambungan internetnya adalah Smartfren.', ['fasilitas','smk','smks','assalafiyah','tegal'], single_response=True)
    response('SMKS ASSALAFIYAH memiliki akreditasi C, berdasarkan sertifikat 047/BANSM-JTG/SK/XII/2018', ['akreditasi','smk','smks','assalafiyah','tegal'], single_response=True)

    #SMKs DINAMIKA TEGAL
    response('SMKS DINAMIKA TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS DINAMIKA TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','dinamika','tegal'], single_response=True)
    response('SMKS DINAMIKA TEGAL beralamat di JL. GLATIK NO.68, Randugunting, Kec. Tegal Selatan, Kota Tegal, Jawa Tengah, dengan kode pos 52131.', ['alamat','smk','smks','dinamika','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smkdinamika.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smk_dinamika@yahoo.com. Nomor Fax sekolah adalah 0283320862.', ['kontak','smk','smks','al ikhlas','tegal'], single_response=True)
    response('SMKS DINAMIKA TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS DINAMIKA TEGAL berasal dari PLN. SMKS DINAMIKA TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMKS DINAMIKA TEGAL untuk sambungan internetnya adalah Telkom Speedy.', ['fasilitas','smk','smks','dinamika','tegal'], single_response=True)
    response('akreditasi B, berdasarkan sertifikat 032/BAN-SM/SK/2019.', ['akreditasi','smk','smks','dinamika','tegal'], single_response=True)

    #SMKs BAHARI TEGAL
    response('SMKS BAHARI TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Mintaragen, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS BAHARI TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','bahari','tegal'], single_response=True)
    response('SMKS BAHARI TEGAL beralamat di JL. SANGIR NO.15 (PAI) TEGAL, Mintaragen, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52121.', ['alamat','smk','smks','bahari','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://www.smkpelayaranbaharitegal.com. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smkpbaharitegal@gmail.com. Nomor Fax sekolah adalah 0283323631.', ['kontak','smk','smks','bahari','tegal'], single_response=True)
    response('SMKS BAHARI TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS BAHARI TEGAL berasal dari PLN.', ['fasilitas','smk','smks','bahari','tegal'], single_response=True)
    response('SMKS BAHARI TEGAL memiliki akreditasi B, berdasarkan sertifikat 1214/BAN-SM/SK/2018.', ['akreditasi','smk','smks','bahari','tegal'], single_response=True)

    #SMKs IHSANIYAH TEGAL
    response('SMKS IHSANIYAH TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS IHSANIYAH TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','ihsaniyah','tegal'], single_response=True)
    response('SMKS IHSANIYAH TEGAL beralamat di SUMBODRO NO. 14, Slerok, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52125.', ['alamat','smk','smks','ihsaniyah','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smkihsaniyahtegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke smkihsaniyah@gmail.com..', ['kontak','smk','smks','ihsaniyah','tegal'], single_response=True)
    response('SMKS IHSANIYAH TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS IHSANIYAH TEGAL berasal dari PLN. SMKS IHSANIYAH TEGAL menyediakan akses internet yang dapat digunakan untuk mendukung kegiatan belajar mengajar menjadi lebih mudah. Provider yang digunakan SMKS IHSANIYAH TEGAL untuk sambungan internetnya adalah Indosat IM3.', ['fasilitas','smk','smks','ihsaniyah','tegal'], single_response=True)
    response('SMKS IHSANIYAH TEGAL memiliki akreditasi C, berdasarkan sertifikat 1523/BANSM/SK/XII/2019.', ['akreditasi','smk','smks','ihsaniyah','tegal'], single_response=True)

    #SMKs BAHARI TEGAL
    response('SMKS YPT TEGAL adalah salah satu satuan pendidikan dengan jenjang SMK di Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah. Dalam menjalankan kegiatannya, SMKS YPT TEGAL berada di bawah naungan Kementerian Pendidikan dan Kebudayaan.', ['smk','smks','ypt','tegal'], single_response=True)
    response('SMKS YPT TEGAL beralamat di JL. DR. SETIABUDI NO. 163, Panggung, Kec. Tegal Timur, Kota Tegal, Jawa Tengah, dengan kode pos 52122.', ['alamat','smk','smks','ypt','tegal'], single_response=True)
    response('Website sekolah dapat dibuka melalui url http://smkypttegal.sch.id. Apabila ingin mengirimkan surat elektronik (email), dapat dikirimkan ke YPT_163@yahoo.com. Nomor Fax sekolah adalah 0283358803.', ['kontak','smk','smks','ypt','tegal'], single_response=True)
    response('SMKS YPT TEGAL menyediakan listrik untuk membantu kegiatan belajar mengajar. Sumber listrik yang digunakan oleh SMKS YPT TEGAL berasal dari PLN.', ['fasilitas','smk','smks','ypt','tegal'], single_response=True)
    response('SMKS YPT TEGAL memiliki akreditasi A, berdasarkan sertifikat 1214/BAN-SM/SK/2018.', ['akreditasi','smk','smks','ypt','tegal'], single_response=True)


    # Longer responses
    response(R_ABOUT, ['apa', 'itu', 'virasschool'], required_words=['apa', 'virasschool'])
    response(R_D4,['tujuan','manfaat','virasschool','viraschool'], required_words=['tujuan','manfaat','virasschool'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/bot')
def bot():
    return render_template('bot.html')

@app.route("/get")
def bot_answer():
    userText = request.args.get('msg')
    return get_response(userText)
