import os
import sqlite3
import logging
 
gig_name = 'Mooseheart Lodge, June 8, 2019'
song_list = ["Can't Win for Losing You",
"Messin With the Kid",
"Hey Hey What Can I Do",
"Going Up the Country",
"Let It Ride",
"Dawned On Me",
"Tiny House Guru",
"High Minded",
"Green River",
"Friend of the Devil",
"Cant Hardly Wait",
"Gravel",
"Bad News",
"Whiskey B4 Breakfast",
"Galway Girl",
"Somebody Else",
"Mystery Train",
"Feels So Bad",
"9-1-1",
"Dead Flowers",
"Deal",
"Monkey / Engineer",
"Thrill is Gone",
"Feels so Bad",
"John Barley Corn",
"Whiskey in a Jar",
"Alabama Song",
"Call me a Liar",
"I'll Fight",
"Tonight I'm staying",
"Pastor's Wife",
"Sunny Afternoon",
"Dear Mr. Fantasy",
"The Weight",
"Lodi",
"Pyramid of Cans",
"Down by the Water",
"East Lombard Girl"
 ]

def print_head(file_obj, headstring):
    file_obj.write('{}<head>\n'.format(' '*2))
    file_obj.write('{}<h2>{}</h2>\n'.format(' '*4, headstring))
    file_obj.write('{}</head>\n'.format(' '*2))
    
def body_color_script(file_obj):
    file_obj.write("""        <script>
            let last_bg_color = "Chartreuse";
            window.onload = setbg;
            setInterval( setbg, 7000 )
      
            function setbg(){
                if( last_bg_color == "Chartreuse"){
                    last_bg_color = "DeepSkyBlue";
            }
            else{
                last_bg_color = "Chartreuse";
            }
            document.body.style.backgroundColor = last_bg_color;        
        }
        </script>
        """)
    

def song_idx(dbh, t_song):
    alias_query = 'SELECT song_idx FROM title_aliases WHERE alias_title = ? COLLATE NOCASE'
    tt_song = t_song.lstrip()
    logging.debug('alias_query = %s', alias_query)
    dbh.execute(alias_query, (tt_song,))
    song_idx = dbh.fetchone()
    # print('**** get_song_idx: t_song = |', t_song, '|, song_idx = ', song_idx )
    logging.debug('t_song: %s, get_song_idx: %s', t_song, song_idx)
    if song_idx:
        return song_idx[0]
    else:
        return None

def arr_idx(dbh, song_idx):
    arr_query = 'SELECT argmnt_idx FROM arrangements WHERE song_idx = ?'
    # print('***** song_idx = ', song_idx )
    dbh.execute(arr_query, (song_idx,))
    arr_index = dbh.fetchone()
    if arr_index:
        return arr_index[0]
    else:
        return None

def arr_path(dbh, song_idx):
    arr_query = 'SELECT argmnt_idx, filepath FROM arrangements WHERE song_idx = ?'
    dbh.execute(arr_query, (song_idx,))
    arr_data = dbh.fetchall()
    if arr_data:
        return arr_data[0]
    else:
        return None
    
#logging.basicConfig(level=logging.DEBUG)    
logging.basicConfig(level=logging.INFO)

music_db = '/Users/sisyp/Documents/SONA/scripts/set_list/music_db.db'
if os.path.isfile(music_db):
    logging.info('found db file')
else:
    logging.error('failed to find db file. Exitting')
    exit()

mdbh = sqlite3.connect(music_db)
mc = mdbh.cursor()
    
#res = mc.execute("SELECT name FROM sqlite_master WHERE type='table';")
#for name in res:
#    print('NAME: ',name[0])

html_file = open('test.html', 'w')
html_file.write('<!DOCTYPE HTML>\n')
html_file.write('<html>\n')
html_file.write('{}<font size="6">\n'.format(' '*2))
print_head(html_file, gig_name)
html_file.write('{}<body>\n'.format(' '*2))
body_color_script(html_file)
html_file.write('{}<table>\n'.format(' '*2))

for song in song_list:
    song_index = song_idx(mc, song)
    if song_index:
        songdata = arr_path(mc, song_index)
        if songdata:
            songpath = 'file://c:/Users/sisyp/Documents/SONA/' + songdata[1]
        else:
            songpath = ''
            print('no path for {} (song_index = {})'.format(song, song_index))
        
    else:
        print('no info for {}'.format(song))
        songpath = ''

    html_file.write('{}<tr>\n'.format(' '*4))
    html_file.write('{}<td><a href="{}">{}</a></td>\n'.format(' '*6, songpath, song))
    html_file.write('{}</tr>\n'.format(' '*4))
    logging.info('%s: index = %s', song, song_index)
    
html_file.write('{}</table>\n'.format(' '*2))
html_file.write('{}</body>\n'.format(' '*2))
html_file.write('</html>\n')
html_file.close()

mdbh.close()
