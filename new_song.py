import sqlite3
import platform

def new_song_import(ns):
    insert_song_cmd  = 'INSERT INTO song_table (song_title) VALUES (?)'
    insert_alias_cmd = 'INSERT INTO title_aliases (song_idx, alias_title) VALUES (?,?)'
    query_song_cmd  = 'SELECT song_idx FROM song_table WHERE song_title=?'

    if platform.node() == "5CB345145G":  # work PC
        music_db = '/scratch/setlist/music_db.sqlite'
    else:
        music_db = '/Users/sisyp/Documents/SONA/scripts/set_list/music_db.db'
        
    mdbh = sqlite3.connect( music_db )
    mc = mdbh.cursor()

    mc.execute( insert_song_cmd, (ns,) )

    mc.execute( query_song_cmd, (ns,) )
    song_tbl_idx, = mc.fetchone()
    print( song_tbl_idx )

    mc.execute( insert_alias_cmd, (song_tbl_idx,ns) )
    
    mdbh.commit()
    mdbh.close()

if __name__ == "__main__":
    new_song = input('new song cannonical name> ')
    new_song_import( new_song )