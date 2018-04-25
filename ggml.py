
def open_html( fh ):
    fh.write('<!DOCTYPE HTML>\n')
    fh.write('<html>\n')
    
def close_html( fh ):
    fh.write('</html>\n')
    
#def write_head( fh ):

def open_body( fh ):
    fh.write('  <body>\n')
    fh.write('    <script>\n')
    fh.write('      let last_bg_color = "Chartreuse";\n')
    fh.write('      window.onload = setbg;\n')
    fh.write('      setInterval( setbg, 7000 )\n')
      
    fh.write('      function setbg(){\n')
    fh.write('        if( last_bg_color == "Chartreuse"){\n')
    fh.write('          last_bg_color = "DeepSkyBlue";\n')
    fh.write('        }\n')
    fh.write('        else{\n')
    fh.write('          last_bg_color = "Chartreuse";\n')
    fh.write('        }\n')
    fh.write('        document.body.style.backgroundColor = last_bg_color;\n')
    fh.write('      }\n')
    fh.write('    </script>\n')

def close_body( fh ):
    fh.write('  </body>\n')
    
def open_table( fh ):
    fh.write('    <table>\n')

def close_table( fh ):
    fh.write('    </table>\n')


if __name__ == "__main__":
    f = 'test.html'
    fh = open(f,'w')
    open_html( fh )
    open_body( fh )
    open_table( fh )
    close_table( fh )
    close_body( fh )
    close_html( fh )

    fh.close()    