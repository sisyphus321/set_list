import sqlite3

music_db = '/scratch/setlist/music_db.sqlite'
mdbh = sqlite3.connect( music_db )
mc = mdbh.cursor()

mc.execute('CREATE TABLE song_table (song_idx integer primary key, song_title char(64))')
mc.execute('CREATE TABLE title_aliases (alias_idx integer primary key, song_idx int(4), alias_title char(64))' )
mc.execute('CREATE TABLE arrangements (argmnt_idx integer primary key, song_idx int(4), filepath char(128), argmnt_notes char(128))' )
mc.execute('CREATE TABLE gigs (gig_idx integer primary key, venue char(64), gig_date)')
mc.execute('CREATE TABLE set_lists (set_idx integer primary key, set_num int(2), gig_idx int(4), place_in_set, argmnt_idx int(4))')
    
mdbh.commit()
mdbh.close()