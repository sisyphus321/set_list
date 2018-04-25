import ggml

ggml_f = 'ggml_test.html'
ggml_fh = open(ggml_f,'w')
ggml.open_html( ggml_fh )
ggml.open_body( ggml_fh )
ggml.open_table( ggml_fh )
ggml.close_table( ggml_fh )
ggml.close_body( ggml_fh )
ggml.close_html( ggml_fh )

ggml_fh.close()    