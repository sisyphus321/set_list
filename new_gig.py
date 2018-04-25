import sqlite3
import platform

def new_gig_read_gig_file( gig_file ):
    gig_fh = open( gig_file, 'r' )
    gig_venue = gig_fh.readline().rstrip()
    gig_date  = gig_fh.readline().rstrip()
    set_lists = gig_fh.readline().split(',')
    gig_fh.close()
    return (gig_venue, gig_date, set_lists )
    
def new_gig_idx( dbh, gig_venue, gig_date ):
    gig_query = 'SELECT gig_idx FROM gigs WHERE venue=? AND gig_date=?'
    dbh.execute( gig_query, (gig_venue, gig_date))
    gig_idx = dbh.fetchone()
    print( 'gig_idx = ',gig_idx)
    return gig_idx
    
def new_gig_create( dbh, gig_venue, gig_date ):
    new_gig_cmd = 'INSERT INTO gigs (venue, gig_date) VALUES (?,?)'
    dbh.execute( new_gig_cmd, (gig_venue, gig_date))
    gig_idx = new_gig_idx( dbh, gig_venue, gig_date )
    #print('%%%%%% gig_idx = ', gig_idx[0] )
    return gig_idx[0]
    
def get_song_idx(dbh,t_song):
    alias_query = 'SELECT song_idx FROM title_aliases WHERE alias_title = ?'
    tt_song = t_song.lstrip()
    dbh.execute( alias_query, (tt_song,) )
    song_idx = dbh.fetchone()
    # print('**** get_song_idx: t_song = |', t_song, '|, song_idx = ', song_idx )
    return song_idx

def get_arr_index( dbh, song_idx ):
    arr_query = 'SELECT argmnt_idx FROM arrangements WHERE song_idx = ?'
    # print('***** song_idx = ', song_idx )
    dbh.execute( arr_query, (song_idx,) )
    arr_index = dbh.fetchone()
    return arr_index

def push_song_setlist(dbh, set_num, gig_idx, place_in_list, arr_index):
    # print('++++ push_song_setlist:', set_num, gig_idx, place_in_list, arr_index )
    push_song_cmd = 'INSERT into set_lists (set_num,gig_idx,place_in_set,argmnt_idx) VALUES(?,?,?,?)'
    dbh.execute( push_song_cmd, (set_num, gig_idx, place_in_list, arr_index) )
    
def new_gig_setlist_create(dbh, setlist_file, gig_idx, set_num ):
    slfh = open( setlist_file, 'r' )
    song_list = slfh.readlines()
    slfh.close()
    place_in_list = 1
    for song_name in song_list:
        t_song = song_name.rstrip()
        t_song_cindex = get_song_idx(dbh,t_song)
        #print('::::::: t_song_cindex = ', t_song_cindex )
        if t_song_cindex != None:
            arr_index = get_arr_index(dbh, t_song_cindex[0] )
            if arr_index != None:
                push_song_setlist(dbh, set_num, gig_idx, place_in_list, arr_index[0])
        else:
            print( t_song, ' not in database')
        place_in_list += 1

if __name__ == "__main__":
    if platform.node() == "5CB345145G":  # work PC
        music_db = '/scratch/setlist/music_db.sqlite'
    else:
        music_db = '/Users/sisyp/Documents/SONA/scripts/music_db.sqlite'
    mdbh = sqlite3.connect( music_db )
    mc = mdbh.cursor()
    
    gig_file = input('Name of gig file> ')
    the_gig = new_gig_read_gig_file( gig_file )
    gig_idx = new_gig_idx( mc, the_gig[0], the_gig[1] )
    if gig_idx == None:
        gig_idx = new_gig_create( mc, the_gig[0], the_gig[1] )
        print('index for the gig is ', gig_idx )
    else:
        print(the_gig[0], ' on ', the_gig[1], ' is already in the database')
    
    print( the_gig )
    set_number = 1
    sets = the_gig[2]
    sets.sort()
    for setlist_file in sets:
        print(setlist_file)
        new_gig_setlist_create(mc,setlist_file,gig_idx,set_number)
        
    mdbh.commit()
    mdbh.close()